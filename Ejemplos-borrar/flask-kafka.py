from flask import Flask, request, jsonify
from confluent_kafka import Producer, Consumer, KafkaError
from cryptography.fernet import Fernet

app = Flask(__name__)
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'mi_tema'
SECRET_KEY = b'secret_key_for_encryption'  # Genera una clave secreta segura para tu aplicación

# Configuración del productor de Kafka
producer_config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'client.id': 'flask-producer'
}
kafka_producer = Producer(producer_config)

# Configuración del consumidor de Kafka
consumer_config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'flask-consumer-group',
    'auto.offset.reset': 'earliest'
}
kafka_consumer = Consumer(consumer_config)
kafka_consumer.subscribe([KAFKA_TOPIC])

# Configuración del cifrado y descifrado
cipher_suite = Fernet(SECRET_KEY)

# Función para cifrar un mensaje
def encrypt_message(message):
    return cipher_suite.encrypt(message.encode('utf-8'))

# Función para descifrar un mensaje
def decrypt_message(encrypted_message):
    return cipher_suite.decrypt(encrypted_message).decode('utf-8')

# Función para consumir mensajes en segundo plano
def consume_messages():
    while True:
        msg = kafka_consumer.poll(1.0)  # Espera 1 segundo por nuevos mensajes

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Descifra y procesa el mensaje (aquí puedes realizar análisis de sentimientos u otras operaciones)
        decrypted_message = decrypt_message(msg.value())
        print('Mensaje recibido: {}'.format(decrypted_message))

# Inicia el consumidor en segundo plano
from threading import Thread
consumer_thread = Thread(target=consume_messages)
consumer_thread.start()

@app.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    try:
        mensaje = request.json['mensaje']
        
        # Cifra el mensaje antes de enviarlo al tópico de Kafka
        encrypted_message = encrypt_message(mensaje)
        kafka_producer.produce(KAFKA_TOPIC, value=encrypted_message)
        kafka_producer.flush()

        return jsonify({'status': 'Mensaje enviado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
