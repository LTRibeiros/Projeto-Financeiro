from datetime import datetime
from flask import Flask
from flask import render_template, request

from database.database import db, Usuario, Session, Lancamento, Categoria

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
    valor = request.form["valor"]
    data = request.form["data"]
    data_obj = datetime.strptime(data, '%Y-%m-%d').date()
    novo_lancamento = Lancamento(descricao=descricao, valor=valor, data=data_obj)

    sessionCommit(novo_lancamento)
    return "Tudo certo"

@app.route('/submitcategoria', methods=['post'])
def submitcategoria():
    nome = request.form["nome"]
    tipo = request.form["tipo"]
    novo_categoria = Categoria(nome=nome, tipo=tipo)
    sessionCommit(novo_categoria)

    return "Tudo certo"



def sessionCommit(novo_commit):
    session = Session()  # Crie uma sessão manualmente
    session.add(novo_commit)
    session.commit()
    session.close()  # Feche a sessão


if __name__ == "__app__":
    app.run(debug=True)