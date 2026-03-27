from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = "clientes"

    id_cliente = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    
    vendas = db.relationship("Venda", backref="cliente")


class Produto(db.Model):
    __tablename__ = "produtos"

    id_produto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(150), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    
    itens = db.relationship("ItemVenda", backref="produto")
        
    
class Venda(db.Model):
    __tablename__ = "vendas"

    id_venda = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)

    preco_total = db.Column(db.Float, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    itens = db.relationship("ItemVenda", backref="venda", cascade="all, delete-orphan")
    
    
class ItemVenda(db.Model):
    __tablename__ = "itens_venda"
    
    id = db.Column(db.Integer, primary_key=True)

    id_venda = db.Column(db.Integer, db.ForeignKey('vendas.id_venda'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id_produto'), nullable=False)

    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)