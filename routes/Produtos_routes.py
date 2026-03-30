from flask import Blueprint, render_template

produtossite = Blueprint('produtossite', __name__)

@produtossite.route('/')
def home_produtos():
    return render_template('produto/produtos.html')


@produtossite.route('/lista')
def lista_produtos():
    return render_template('produto/listproduto.html')

@produtossite.route('/cadastro')
def cadastro_produtos():
    return render_template('produto/cadproduto.html')

@produtossite.route("/editar/<int:id_produto>")
def editar_produto(id_produto):
    return render_template("produto/editproduto.html")


# @produtossite.route("/deletar/<int:id_produto>", methods=["POST"])
# def deletar_produto(id_produto):
#     produto = Produto.query.get_or_404(id_produto)
#     db.session.delete(produto)
#     db.session.commit()

#     return redirect(url_for("produtossite.lista_produtos"))
