from flask import Flask, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "admin-secret-key"  # só você sabe

# Conecta no mesmo banco do app principal
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo do usuário (mesmo que o app principal)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    balance = db.Column(db.Float)

# Login admin
ADMIN_PASSWORD = "123456"  # você pode mudar depois

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/")
        else:
            return "Senha errada"
    return """
        <h2>Admin Login</h2>
        <form method="POST">
            <input type="password" name="password" placeholder="Senha admin">
            <button>Entrar</button>
        </form>
    """

# Dashboard admin
@app.route("/")
def dashboard():
    if "admin" not in session:
        return redirect("/login")

    users = User.query.all()

    html = "<h2>Painel Admin</h2>"
    for user in users:
        html += f"""
        <p>
        ID: {user.id} | Usuário: {user.username} | Saldo: {user.balance}
        <a href='/add/{user.id}/100'>+100</a>
        </p>
        """
    return html

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
