import sqlite3
from datetime import datetime
from flask import Flask, redirect, url_for, session, flash
from flask import render_template, request
from matplotlib import pyplot as plt
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import Usuario, Session, Lancamento, Relatorio
import os

app = Flask(__name__, static_url_path='/static')

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
    return render_template("index.html")


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
    import pandas as pd

    connectdb = sqlite3.connect("banco.db")
    session_id = session['usuario_id']
    data_inicial = request.form["data_inicio"]
    inicio = datetime.strptime(data_inicial, '%Y-%m-%d').date()
    data_final = request.form["data_fim"]
    final = datetime.strptime(data_final, '%Y-%m-%d').date()
    minimo = request.form["valor_minimo"]
    maximo = request.form["valor_maximo"]
    categoria = request.form["pesquisa_categoria"]

    query = ("""
        SELECT descricao, valor, categoria, data
        FROM lancamentos
        WHERE 
            data >= :data_inicial
            AND data <= :data_final
            AND valor >= :valor_minimo
            AND valor <= :valor_maximo
            
            AND usuario_id = :id
    """)

    # passagem de parâmetros de variaveis (evita sqlinjection
    params={
        'data_inicial': inicio,
        'data_final': final,
        'valor_minimo': minimo,
        'valor_maximo': maximo,

        'id': session_id
    }

    if categoria and categoria != 'todas':
        query += " AND categoria = :categoria"
        params['categoria'] = categoria

    lf = pd.read_sql_query(
        query,
        connectdb,
        params=params)

    altura = max(1.5, 0.5 * len(lf))
    fig, ax = plt.subplots(figsize=(8,altura))
    ax.axis('off')
    tabela = ax.table(cellText=lf.values, colLabels=lf.columns, cellLoc='center', loc='center')
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1, 1.5)
    plt.tight_layout()

    # Salva na pasta static
    caminho = 'static/gastofiltrado.png'
    plt.savefig(caminho, bbox_inches='tight')
    plt.close()

    return render_template("index.html", pesquisa_gerada=True)


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

    plt.title('Porcentagem de Gastos por Categoria', fontweight='bold')
    plt.legend(df['categoria'], loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(right=0.75)
    plt.savefig('static/relatorio.png')
    plt.tight_layout()

    return render_template("index.html", relatorio_gerado=True)


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
