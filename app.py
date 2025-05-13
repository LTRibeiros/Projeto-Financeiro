from datetime import datetime
from flask import Flask, redirect, url_for, session, flash
from flask import render_template, request
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import Usuario, Session, Lancamento, Relatorio
import os

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY')


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/cadastro')
def cadastro():
    return render_template("cadastro.html")


@app.route('/')
def login():
    return render_template("login.html")


@app.route('/cadastrausuario', methods=['POST'])
def cadastrausuario():
    nome = request.form["name"]
    email = request.form["email"]
    senha = generate_password_hash(request.form["senha"])
    novo_usuario = Usuario(nome_usuario=nome, email=email, senha=senha)

    sessionCommit(novo_usuario)
    return redirect(url_for('login'))


@app.route('/submitlancamento', methods=['POST'])
def submitlancamento():
    descricao = request.form["descricao"]
    categoria = request.form["categoria"]
    valor = request.form["valor"]
    data = request.form["data"]
    data_obj = datetime.strptime(data, '%Y-%m-%d').date()
    usuario_id = session['usuario_id']
    novo_lancamento = Lancamento(descricao=descricao, categoria=categoria, valor=valor, data=data_obj,
                                 usuario_id=usuario_id)

    sessionCommit(novo_lancamento)
    return "Tudo certo"


@app.route('/verificausuario', methods=['POST'])
def verificausuario():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        session_db = Session()
        usuario = session_db.query(Usuario).filter_by(email=email).first()
        session_db.close()

        # Verifica se usuário existe e a senha está correta
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id  # Armazena na sessão
            session['usuario_email'] = usuario.email
            return redirect(url_for('index'))  # Redireciona para área logada

        flash('Email ou senha incorretos!', 'error')
        return redirect(url_for('login'))


@app.route('/pesquisa', methods=['POST'])
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


@app.route('/relatorio', methods=['POST'])
def relatorio():
    import pandas as pd
    import matplotlib.pyplot as plt
    import sqlite3

    session_id = session['usuario_id']
    connectdb = sqlite3.connect("banco.db")
    query = """
    SELECT usuario_id, categoria, SUM(valor) as total
    FROM lancamentos
    WHERE usuario_id = :id
    GROUP BY usuario_id, categoria
    """

    df = pd.read_sql_query(query, connectdb, params={'id': session_id})

    plt.figure(figsize=(8, 8))
    plt.pie(
        df['total'],
        labels=df['categoria'],
        autopct='%1.1f%%',
        startangle=90,
    )

    plt.title('Distribuição de Gastos por Categoria', fontweight='bold')
    plt.legend(df['categoria'], loc="best", bbox_to_anchor=(1, 1))
    plt.savefig('static/relatorio.png')
    plt.tight_layout()
    return "relatório gerado"


def sessionCommit(novo_commit):
    try:
        session = Session()
        session.add(novo_commit)
        session.commit()
        session.close()
    except IntegrityError:
        session.rollback()
        print("já cadastrado!")


if __name__ == "__main__":
    app.run()
