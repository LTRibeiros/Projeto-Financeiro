import database.database
from flask import Flask
from flask import render_template, request
from database.database import db, Usuario, Session

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['post'])
def submit():
    nome = request.form["name"]
    email = request.form["email"]
    senha = request.form["senha"]
    novo_usuario = Usuario(nome_usuario=nome, email=email, senha=senha)

    session = Session()  # Crie uma sessão manualmente
    session.add(novo_usuario)
    session.commit()
    session.close()  # Feche a sessão
    return "Usuário criado!"

if __name__ == "__app__":
    app.run(debug=True)
