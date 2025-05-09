from sqlalchemy import create_engine, Integer, String, Float, Boolean, Column, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Configuração do banco de dados (exemplo com SQLite)
db = create_engine("sqlite:///banco.db")
Session = sessionmaker(bind=db)
session_db = Session()
Base = declarative_base()  # criação da base


# criação das tabelas:
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome_usuario = Column("nome", String)
    email = Column("email", String, unique=True)
    senha = Column("senha", String)

    def __init__(self, nome_usuario, email, senha):
        self.nome_usuario = nome_usuario
        self.email = email
        self.senha = senha


class Lancamento(Base):
    __tablename__ = "lancamentos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    descricao = Column("descricao", String)
    categoria = Column("categoria", String)
    valor = Column("valor", Float)
    data = Column("data", Date)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    # relatorio_id = Column(Integer, ForeignKey("relatorios.id"))
    # categoria_id = Column(Integer, ForeignKey("categorias.id"))

    def __init__(self, descricao, categoria, valor, data, usuario_id):
        self.descricao = descricao
        self.categoria = categoria
        self.valor = valor
        self.data = data
        self.usuario_id = usuario_id


class Relatorio(Base):
    __tablename__ = "relatorios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    data_inicial = Column("data_inicial", Date)
    data_final = Column("data_final", Date)
    valor_minimo = Column("valor_minimo", Float)
    valor_maximo = Column("valor_maximo", Float)
    pesquisa_categoria = Column("pesquisa_categoria", String)

    def __init__(self, data_inicial, data_final, valor_minimo, valor_maximo, pesquisa_categoria):
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.valor_minimo = valor_minimo
        self.valor_maximo = valor_maximo
        self.pesquisa_categoria = pesquisa_categoria


##########################################################
Base.metadata.create_all(bind=db)

# ForeignKey("usuarios.id")) #ForeingKey
