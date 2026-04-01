from flask import Blueprint, request, jsonify, session
from model import db, Venda, ItemVenda, Produto, Cliente
from routes.api.login_api import login_required, admin_required

vendasapi = Blueprint("vendasapi", __name__)


# LISTAR
@vendasapi.route("/vendas", methods=["GET"])
@login_required
def get_vendas():
    vendas = Venda.query.all()
    
    return jsonify([
        {"id": v.id_venda,
        "id_cliente": v.id_cliente,
        "cliente": v.cliente.nome,
        "preco_total": v.preco_total,
        "data_venda": v.data_venda.strftime("%d/%m/%Y %H:%M")}
        for v in vendas
    ])


# CRIAR
@vendasapi.route("/vendas", methods=["POST"])
@login_required
def efetuar_venda():
    data = request.get_json()
    id_cliente = data.get("id_cliente")
    id_user = session.get("user_id")
    itens = data.get("itens", [])

    if not id_cliente or not itens:
        return jsonify({"error": "Dados incompletos"}), 400

    # ITENS DUPLICADOS
    itens_dict = {}
    for item in itens:
        id_p = int(item["id_produto"])
        qtd = int(item["quantidade"])
        itens_dict[id_p] = itens_dict.get(id_p, 0) + qtd

    # VALIDA ESTOQUE
    total = 0
    for id_p, qtd in itens_dict.items():
        produto = Produto.query.get(id_p)
        if not produto:
            return jsonify({"error": f"Produto {id_p} não encontrado"}), 404
        if produto.quantidade < qtd:
            return jsonify({"error": f"Estoque insuficiente para {produto.nome_produto}"}), 400
        total += produto.preco * qtd

    venda = Venda(id_cliente=id_cliente, id_user=id_user, preco_total=total)
    
    db.session.add(venda)
    db.session.commit()

    for id_p, qtd in itens_dict.items():
        produto = Produto.query.get(id_p)
        produto.quantidade -= qtd
        item = ItemVenda(
            id_venda=venda.id_venda,
            id_produto=produto.id_produto,
            quantidade=qtd,
            preco_unitario=produto.preco,
            id_user=id_user
        )
        db.session.add(item)

    db.session.commit()
    return jsonify({"message": "Venda realizada", "id": venda.id_venda, "total": total}), 201


# DELETAR
@vendasapi.route("/vendas/<int:id>", methods=["DELETE"])
@admin_required
def delete_venda(id):
    venda = Venda.query.get_or_404(id)
    
    # VALIDA ESTOQUE
    for item in venda.itens:
        item.produto.quantidade += item.quantidade
        
    db.session.delete(venda)
    db.session.commit()
    
    return jsonify({"message": "Venda deletada"})


# BUSCAR
@vendasapi.route("/vendas/<int:id>", methods=["GET"])
@login_required
def get_venda(id):
    venda = Venda.query.get_or_404(id)
    
    return jsonify({
        "id": venda.id_venda,
        "id_cliente": venda.id_cliente,
        "cliente": venda.cliente.nome,
        "preco_total": venda.preco_total,
        "data_venda": venda.data_venda.strftime("%d/%m/%Y %H:%M"),
        "itens": [
            {
                "id_produto": item.id_produto,
                "nome_produto": item.produto.nome_produto,
                "quantidade": item.quantidade,
                "preco_unitario": item.preco_unitario
            }
            for item in venda.itens
        ]
    })
