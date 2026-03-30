from flask import Blueprint, flash, render_template

clientesite = Blueprint('clientesite', __name__)

@clientesite.route("/")
def home_cliente():
    return render_template('cliente/cliente.html')


@clientesite.route("/cadastro")
def cadastro_cliente():
    return render_template('cliente/cadcliente.html')


@clientesite.route("/lista")
def listar_clientes():
    return render_template('cliente/listcliente.html')

    
@clientesite.route("/editar/<int:id_cliente>")
def editar_cliente(id_cliente):
    return render_template("cliente/editcliente.html")


# @clientesite.route("/deletar/<int:id_cliente>", methods=["POST"])
# def deletar_cliente(id_cliente):
#     cliente = Cliente.query.get_or_404(id_cliente)
#     db.session.delete(cliente)
#     db.session.commit()

#     return redirect(url_for("clientesite.listar_clientes"))