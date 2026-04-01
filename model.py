from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
    
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)

    preco_total = db.Column(db.Float, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    
    itens = db.relationship("ItemVenda", backref="venda", cascade="all, delete-orphan")
    user = db.relationship("User", backref="vendas")
    
    
class ItemVenda(db.Model):
    __tablename__ = "itens_venda"
    
    id = db.Column(db.Integer, primary_key=True)

    id_venda = db.Column(db.Integer, db.ForeignKey('vendas.id_venda'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id_produto'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)

    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    
    
class User(db.Model):
    __tablename__ = "users"

    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    itens = db.relationship("ItemVenda", backref="user")
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
