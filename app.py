from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "admin-secret-key"

# Conecta no mesmo banco do app principal
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    balance = db.Column(db.Float, default=10000.0)  # saldo inicial

# Cria a tabela automaticamente se não existir
with app.app_context():
    db.create_all()

# Senha do admin (pode mudar via variável de ambiente)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "123456")

# Página de login admin
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/")
        else:
            return "Senha incorreta"
    return render_template("login.html")

# Dashboard admin
@app.route("/")
def dashboard():
    if "admin" not in session:
        return redirect("/login")

    users = User.query.all()
    return render_template("admin.html", users=users)

# Adicionar saldo
@app.route("/add/<int:user_id>/<float:amount>")
def add(user_id, amount):
    if "admin" not in session:
        return redirect("/login")

    user = User.query.get(user_id)
    if not user:
        return "Usuário não encontrado"

    user.balance += amount
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run()
