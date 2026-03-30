from flask import Blueprint, request, jsonify
from model import db, Cliente

clienteapi = Blueprint("clienteapi", __name__)

# Validação de CPF
def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (soma * 10 % 11) % 10
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{d1}{d2}"

# LISTAR
@clienteapi.route("/clientes", methods=["GET"])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([
        {"id": c.id_cliente, 
        "cpf": c.cpf, 
        "nome": c.nome, 
        "email": c.email}
        for c in clientes
    ])
    
# CRIAR
@clienteapi.route("/clientes", methods=["POST"])
def create_cliente():
    data = request.get_json()
    cpf = ''.join(filter(str.isdigit, data.get("cpf", "")))
 
    if not validar_cpf(cpf):
        return jsonify({"error": "CPF inválido"}), 400
 
    if Cliente.query.filter_by(cpf=cpf).first():
        return jsonify({"error": "CPF já cadastrado"}), 409
 
    cliente = Cliente(cpf=cpf, nome=data["nome"], email=data["email"])
    db.session.add(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente criado", "id": cliente.id_cliente}), 201
 
# ATUALIZAR
@clienteapi.route("/clientes/<int:id>", methods=["PUT"])
def update_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.get_json()

    cliente.nome = data.get("nome", cliente.nome)
    cliente.email = data.get("email", cliente.email)

    db.session.commit()

    return jsonify({"message": "Atualizado"})

# DELETAR
@clienteapi.route("/clientes/<int:id>", methods=["DELETE"])
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    db.session.delete(cliente)
    db.session.commit()

    return jsonify({"message": "Deletado"})

# BUSCAR
@clienteapi.route("/clientes/<int:id>", methods=["GET"])
def get_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    return jsonify({"id": cliente.id_cliente,
                    "cpf": cliente.cpf,
                    "nome": cliente.nome,
                    "email": cliente.email
                    })