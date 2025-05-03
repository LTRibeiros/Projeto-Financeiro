from sqlalchemy import create_engine, Column, String, Integer, Double, Date, ForeignKey, Boolean, Float
# cria o bando de dados
from sqlalchemy.orm import sessionmaker, declarative_base, foreign  # criar sessão e tabelas

db = create_engine("sqlite:///meubanco.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base() #criação da base

#criação das tabelas:
class Usuario(Base):
    __tablename__ = "usuarios"

    nome_Usuario = Column("nome", String)
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String)
    senha = Column("senha", String)

    def __init__(self, nome_usuario, email, senha):
        self.nome_Usuario = nome_usuario
        self.email = email
        self.senha = senha


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome_Categoria = Column("nome_Categoria", String)
    tipo = Column("tipo", String)

    def __init__(self, nome_categoria, tipo):
        self.nome_Categoria = nome_categoria
        self.tipo = tipo


class Lancamento(Base):
    __tablename__ = "lancamentos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    descricao = Column("descrição", String)
    valor = Column("valor", Double)
    data = Column("data", Date)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    relatorio_id = Column(Integer, ForeignKey("relatorios.id"))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    def __init__(self, descricao, valor, data):
        self.descricao = descricao
        self.valor = valor
        self.data = data


class Relatorio(Base):
    __tablename__ = "relatorios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    titulo = Column("titulo", String)
    data = Column("data", Date)
    total = Column("total",Float)


    def __init__(self, titulo, data, total):
        self.titulo = titulo
        self.data = data
        self.total = total

##########################################################
Base.metadata.create_all(bind=db)

# ForeignKey("usuarios.id")) #ForeingKey
