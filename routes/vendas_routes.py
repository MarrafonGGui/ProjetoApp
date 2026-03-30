from flask import Blueprint, redirect, render_template
from model import Venda

vendassite = Blueprint('vendassite', __name__)

@vendassite.route('/')
def home_vendas():
    return render_template('vendas/vendas.html')


@vendassite.route('/efetuar')
def efetuar_vendas():
        return render_template("vendas/efetvenda.html")


@vendassite.route("/lista")
def listar_vendas():
    return render_template("vendas/listvenda.html")


@vendassite.route("/acessar/<int:id_venda>")
def acessar_venda(id_venda):
    return render_template("vendas/acessvenda.html")


@vendassite.route('/fim/<int:id_venda>')
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