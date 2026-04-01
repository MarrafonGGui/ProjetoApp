from flask import Blueprint, flash, render_template, session, redirect
from routes.api.login_api import login_required, admin_required

produtossite = Blueprint('produtossite', __name__)

@produtossite.route('/')
@login_required
def home_produtos():
    return render_template('produto/produtos.html')


@produtossite.route('/lista')
@login_required
def lista_produtos():
    return render_template('produto/listproduto.html')

@produtossite.route('/cadastro')
def cadastro_produtos():
    if not session.get("is_admin"):
        flash("Acesso Restrito!!")
        return redirect("/produtos")
    return render_template('produto/cadproduto.html')

@produtossite.route("/editar/<int:id_produto>")
def editar_produto(id_produto):
    if not session.get("is_admin"):
        flash("Acesso Restrito!!")
        return redirect("/produtos/lista")
    return render_template("produto/editproduto.html")


# @produtossite.route("/deletar/<int:id_produto>", methods=["POST"])
# def deletar_produto(id_produto):
#     produto = Produto.query.get_or_404(id_produto)
#     db.session.delete(produto)
#     db.session.commit()

#     return redirect(url_for("produtossite.lista_produtos"))
