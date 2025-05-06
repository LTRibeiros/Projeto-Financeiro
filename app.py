from datetime import datetime
from flask import Flask
from flask import render_template, request
from sqlalchemy.exc import IntegrityError

from database.database import db, Usuario, Session, Lancamento, Relatorio

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


@app.route('/pesquisa', methods=['post'])
def pesquisa():
    data_inicial = request.form["data_inicio"]
    data_inicio_ = datetime.strptime(data_inicial, '%Y-%m-%d').date()
    data_final = request.form["data_fim"]
    data_fim_ = datetime.strptime(data_final, '%Y-%m-%d').date()
    valor_minimo = request.form["valor_minimo"]
    valor_maximo = request.form["valor_maximo"]
    pesquisa_categoria = request.form["pesquisa_categoria"]
    novo_lancamento = Relatorio(data_inicial=data_inicio_, data_final=data_fim_, valor_minimo=valor_minimo,
                                valor_maximo=valor_maximo, pesquisa_categoria=pesquisa_categoria)

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
