from flask import Blueprint, flash, render_template, request, redirect, url_for, flash
from model import db, Cliente

clientesite = Blueprint('clientesite', __name__)

@clientesite.route("/")
def home_cliente():
    return render_template('cliente/cliente.html')


@clientesite.route("/cadastro", methods=["GET", "POST"])
def cadastro_cliente():
    if request.method == "POST":
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        email = request.form.get("email")

        cpf = ''.join(filter(str.isdigit, cpf))

        if not validar_cpf(cpf):
            flash("CPF inválido")
            return redirect(url_for("clientesite.cadastro_cliente"))

        existe = Cliente.query.filter_by(cpf=cpf).first()
        if existe:
            flash("CPF já cadastrado")
            return redirect(url_for("clientesite.cadastro_cliente"))

        cliente = Cliente(cpf=cpf, nome=nome, email=email)
        db.session.add(cliente)
        db.session.commit()

        return redirect(url_for("clientesite.cadastro_cliente"))
    return render_template('cliente/cadcliente.html')


@clientesite.route("/lista")
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('cliente/listcliente.html', clientes=clientes)

    
@clientesite.route("/editar/<int:id_cliente>", methods=["GET", "POST"])
def editar_cliente(id_cliente):
    cliente = Cliente.query.get(id_cliente)

    if not cliente:
        return "Cliente não encontrado"

    if request.method == "POST":
        cliente.nome = request.form.get("nome")
        cliente.email = request.form.get("email")

        db.session.commit()

        return redirect(url_for("clientesite.listar_clientes"))

    return render_template("cliente/editcliente.html", cliente=cliente)


@clientesite.route("/deletar/<int:id_cliente>", methods=["POST"])
def deletar_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for("clientesite.listar_clientes"))    





def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Primeiro dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10

    # Segundo dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{d1}{d2}"
