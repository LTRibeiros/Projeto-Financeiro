from datetime import datetime
from flask import Flask
from flask import render_template, request
from sqlalchemy.exc import IntegrityError

from database.database import db, Usuario, Session, Lancamento

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submitusuario', methods=['post'])
def submitusuario():
    nome = request.form["name"]
    email = request.form["email"]
    senha = request.form["senha"]
    novo_usuario = Usuario(nome_usuario=nome, email=email, senha=senha)

    sessionCommit(novo_usuario)
    return "Tudo certo"

@app.route('/submitlancamento', methods=['post'])
def submitlancamento():
    descricao = request.form["descricao"]
    categoria = request.form["categoria"]
    valor = request.form["valor"]
    data = request.form["data"]
    data_obj = datetime.strptime(data, '%Y-%m-%d').date()
    novo_lancamento = Lancamento(descricao=descricao, categoria=categoria, valor=valor, data=data_obj)

    sessionCommit(novo_lancamento)
    return "Tudo certo"


def sessionCommit(novo_commit):
    try:
        session = Session()
        session.add(novo_commit)
        session.commit()
        session.close()
    except IntegrityError:
        session.rollback()
        print("já cadastrado!")

if __name__ == "__app__":
    app.run(debug=True)