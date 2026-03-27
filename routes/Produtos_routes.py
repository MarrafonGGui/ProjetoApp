from flask import Blueprint, render_template, url_for, request, redirect, flash
from model import db, Produto

produtossite = Blueprint('produtossite', __name__)

@produtossite.route('/', methods=["GET", "POST"])
def home_produtos():
    return render_template('produto/produtos.html')


@produtossite.route('/lista')
def lista_produtos():
    produtos = Produto.query.all()
    return render_template('produto/listproduto.html', produtos=produtos)

@produtossite.route('/cadastro', methods=["GET", "POST"])
def cadastro_produtos():
    if request.method == "POST":
        nome = request.form.get("nome")
        preco = request.form.get("preco")
        quantidade = int(request.form.get("quantidade"))

        # verifica se já existe
        produto_existente = Produto.query.filter_by(nome_produto=nome).first()
        if produto_existente:
            flash("Produto já cadastrado")
            return redirect(url_for("produtossite.cadastro_produtos"))
        
        if float(preco) <= 0:
            flash("Preço deve ser maior que zero")
            return redirect(url_for("produtossite.cadastro_produtos"))

        else:
            # cria novo produto
            produto = Produto(
                nome_produto=nome,
                preco=float(preco),
                quantidade=quantidade
            )
            db.session.add(produto)
        db.session.commit()

        return redirect(url_for("produtossite.cadastro_produtos"))
    lista_produtos = Produto.query.all()

    return render_template('produto/cadproduto.html', produtos=lista_produtos)



@produtossite.route("/editar/<int:id_produto>", methods=["GET", "POST"])
def editar_produto(id_produto):
    produto = Produto.query.get(id_produto)

    if not produto:
        return "Produto não encontrado"

    if request.method == "POST":
        produto.nome_produto = request.form.get("nome")
        produto.preco = float(request.form.get("preco"))
        produto.quantidade = int(request.form.get("quantidade"))

        db.session.commit()

        return redirect(url_for("produtossite.lista_produtos"))

    return render_template("produto/editproduto.html", produto=produto)


@produtossite.route("/deletar/<int:id_produto>", methods=["POST"])
def deletar_produto(id_produto):
    produto = Produto.query.get_or_404(id_produto)
    db.session.delete(produto)
    db.session.commit()

    return redirect(url_for("produtossite.lista_produtos"))
