from flask import Flask, render_template, request, redirect, url_for

usuarios = {}

app=Flask(__name__)

@app.route("/")
def inicio():
    return render_template("inicio.html")








@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]

        if usuario in usuarios and usuarios[usuario] == contraseña:
            return f"bienvenido {usuario}"
        else:
            return "vuelve a intentar"
        
    return render_template("login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]

        if usuario in usuarios:
            return "este usuario ya existe"
        else:
            usuarios[usuario] = contraseña
            return redirect(url_for('login'))
    return render_template("registro.html")



if __name__ == "__main__":
    app.run(debug=True)
