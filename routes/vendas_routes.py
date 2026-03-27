from flask import Blueprint, redirect, render_template, url_for, request, flash
from model import ItemVenda, db, Venda, Produto, Cliente

vendassite = Blueprint('vendassite', __name__)

@vendassite.route('/')
def home_vendas():
    return render_template('vendas/vendas.html')

@vendassite.route('/efetuar', methods=["GET","POST"])
def efetuar_vendas():
    if request.method == "POST":
        id_cliente = request.form.get("id_cliente")
        ids_produtos = request.form.getlist("id_produto[]")
        quantidades = request.form.getlist("quantidade[]")

        itens_dict = {}

        for id_p, qtd in zip(ids_produtos, quantidades):
            id_p = int(id_p)  # 🔥 IMPORTANTE
            qtd = int(qtd)

            if id_p in itens_dict:
                itens_dict[id_p] += qtd
            else:
                itens_dict[id_p] = qtd

        total = 0
        #  Validar estoque
        for id_p, qtd in itens_dict.items():
            produto = Produto.query.get(int(id_p))
            if produto.quantidade < qtd:
                flash(f"Estoque insuficiente para {produto.nome_produto}")
                return redirect(url_for("vendassite.efetuar_vendas"))

            total += produto.preco * qtd

        venda = Venda(
            id_cliente=id_cliente,
            preco_total=total
        )
        db.session.add(venda)
        db.session.commit()

        for id_p, qtd in itens_dict.items():
            produto = Produto.query.get(id_p)
            produto.quantidade -= qtd

            item = ItemVenda(
                id_venda=venda.id_venda,
                id_produto=produto.id_produto,
                quantidade=qtd,
                preco_unitario=produto.preco
            )
            db.session.add(item)

        db.session.commit()
        
        print(request.form)
        print("ID CLIENTE:", request.form.get("id_cliente"))

        return render_template("vendas/fimvenda.html", venda=venda)
    clientes = Cliente.query.all()
    produtos = Produto.query.all()

    produtos_json = [{"id_produto": p.id_produto,"nome_produto": p.nome_produto,"preco": p.preco}for p in produtos]

    return render_template("vendas/efetvenda.html", clientes=clientes, produtos=produtos, produtos_json=produtos_json)


@vendassite.route("/lista")
def listar_vendas():
    vendas = Venda.query.all()
    return render_template("vendas/listvenda.html", vendas=vendas)

@vendassite.route("/acessar/<int:id_venda>")
def acessar_venda(id_venda):
    venda = Venda.query.filter_by(id_venda=id_venda).first()
    print(len(venda.itens))
    return render_template("vendas/acessvenda.html", venda=venda)

@vendassite.route("/deletar/<int:id_venda>", methods=["POST"])
def deletar_venda(id_venda):
    venda = Venda.query.filter_by(id_venda=id_venda).first()
    
    for item in venda.itens:
        produto = item.produto
        produto.quantidade += item.quantidade
        
    db.session.delete(venda)
    db.session.commit()

    return redirect(url_for("vendassite.listar_vendas"))