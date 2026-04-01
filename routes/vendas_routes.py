from flask import Blueprint, redirect, render_template, session, flash
from model import Venda
from routes.api.login_api import login_required, admin_required

vendassite = Blueprint('vendassite', __name__)

@vendassite.route('/')
@login_required
def home_vendas():
    return render_template('vendas/vendas.html')


@vendassite.route('/efetuar')
@login_required
def efetuar_vendas():
        return render_template("vendas/efetvenda.html")


@vendassite.route("/lista")
@login_required
def listar_vendas():
    print(session)
    return render_template("vendas/listvenda.html")


@vendassite.route("/acessar/<int:id_venda>")
@login_required
def acessar_venda(id_venda):
    return render_template("vendas/acessvenda.html")


@vendassite.route('/fim/<int:id_venda>')
@login_required
def fim_venda(id_venda):
    venda = Venda.query.get_or_404(id_venda)
    return render_template('vendas/fimvenda.html', venda=venda)


# @vendassite.route("/deletar/<int:id_venda>", methods=["POST"])
# def deletar_venda(id_venda):
#     venda = Venda.query.filter_by(id_venda=id_venda).first()
    
#     for item in venda.itens:
#         produto = item.produto
#         produto.quantidade += item.quantidade
        
#     db.session.delete(venda)
#     db.session.commit()

#     return redirect(url_for("vendassite.listar_vendas"))