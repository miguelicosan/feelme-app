//Insertar un usuario nuevo
db.usuarios.insertOne({
    nombre: "Usuario",
    apellidos: "Ejemplo",
    email: "usuario@example.com",
    contrasena: "hash_de_contraseña",
    edad: 25,
    sexo: "masculino",
    peso: 70.5,
    altura: 175,
    confirmado: false,
});
