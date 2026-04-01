from flask import Blueprint, request, jsonify
from model import db, Produto
from routes.api.login_api import login_required, admin_required

produtosapi = Blueprint("produtosapi", __name__)


# LISTAR
@produtosapi.route("/produtos", methods=["GET"])
@login_required
def get_produtos():
    produtos = Produto.query.all()
    
    return jsonify([
        {"id": p.id_produto, 
         "nome": p.nome_produto, 
         "preco": p.preco, 
         "quantidade": p.quantidade}
        for p in produtos
    ])


# CRIAR
@produtosapi.route("/produtos", methods=["POST"])
@admin_required
def create_produto():
    data = request.get_json()
    nome = data.get("nome", "").strip()
    preco = float(data.get("preco", 0))
    quantidade = int(data.get("quantidade", 0))

    if Produto.query.filter_by(nome_produto=nome).first():
        return jsonify({"error": "Produto já cadastrado"}), 409

    if preco <= 0:
        return jsonify({"error": "Preço deve ser maior que zero"}), 400

    produto = Produto(nome_produto=nome, preco=preco, quantidade=quantidade)
    
    db.session.add(produto)
    db.session.commit()
    
    return jsonify({"message": "Produto criado", "id": produto.id_produto}), 201


# ATUALIZAR
@produtosapi.route("/produtos/<int:id>", methods=["PUT"])
@admin_required
def update_produto(id):
    produto = Produto.query.get_or_404(id)
    data = request.get_json()
    
    produto.nome_produto = data.get("nome", produto.nome_produto)
    produto.preco = float(data.get("preco", produto.preco))
    produto.quantidade = int(data.get("quantidade", produto.quantidade))
    
    db.session.commit()
    
    return jsonify({"message": "Produto atualizado"})


# DELETAR
@produtosapi.route("/produtos/<int:id>", methods=["DELETE"])
@admin_required
def delete_produto(id):
    produto = Produto.query.get_or_404(id)
    
    db.session.delete(produto)
    db.session.commit()
    
    return jsonify({"message": "Produto deletado"})


# BUSCAR
@produtosapi.route("/produtos/<int:id>", methods=["GET"])
@login_required
def get_produto(id):
    produto = Produto.query.get_or_404(id)
    
    return jsonify({"id": produto.id_produto, 
                    "nome": produto.nome_produto, 
                    "preco": produto.preco, 
                    "quantidade": produto.quantidade
                    })

