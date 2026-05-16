from flask import Flask, render_template, request, redirect, url_for
import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gimnasio_app"
)

cursor = db.cursor()
cursor.execute("SELECT * FROM planes")

for fila in cursor:
    print(fila)


app=Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["usuario"]
        correo = request.form["correo"]
        password = request.form["contraseña"]

        cursor = db.cursor()

        # Verificar si ya existe
        cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (correo,))
        existe = cursor.fetchone()

        if existe:
            return "este correo ya existe"
        else:
            cursor.execute(
                "INSERT INTO usuarios (nombre, correo, password) VALUES (%s, %s, %s)",
                (nombre, correo, password)
            )
            db.commit()

            return redirect(url_for('login'))

    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["contraseña"]

        cursor = db.cursor(dictionary=True)

        # Buscar usuario en DB
        cursor.execute(
            "SELECT * FROM usuarios WHERE correo=%s AND password=%s",
            (correo, password)
        )
        usuario = cursor.fetchone()

        if usuario:
            user_id = usuario["id"]

            # Verificar membresía
            cursor.execute(
                "SELECT * FROM membresias WHERE usuario_id=%s AND estado='activa'",
                (user_id,)
            )
            membresia = cursor.fetchone()

            if membresia:
                return redirect(url_for("dashboard"))
            else:
                return redirect(url_for("planes"))

        return "Usuario o contraseña incorrectos"

    return render_template("login.html")

@app.route("/planes")
def planes():
    return render_template("planes.html")



if __name__ == "__main__":
    app.run(debug=True)
