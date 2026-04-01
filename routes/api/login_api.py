from flask import Blueprint, request, jsonify, session
from functools import wraps
from model import db, User

loginapi = Blueprint("loginapi", __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Não autorizado"}), 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return jsonify({"error": "Acesso restrito"}), 403
        return f(*args, **kwargs)
    return decorated



@loginapi.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not user.check_password(data.get("password")):
        return jsonify({"error": "Credenciais inválidas"}), 401

    session["user_id"] = user.id_user
    session["is_admin"] = user.is_admin

    return jsonify({
        "message": "Login realizado",
        "is_admin": user.is_admin
    })


@loginapi.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logout realizado"})


@loginapi.route("/admin/criar", methods=["POST"])
@admin_required
def registrar():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    is_admin = data.get("is_admin", False)

    if not username or not password:
        return jsonify({"error": "Dados incompletos"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Usuário já existe"}), 409

    user = User(username=username, is_admin=is_admin)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuário criado com sucesso"}), 201


@loginapi.route("/user", methods=["GET"])
def user():
    from flask import session

    if "user_id" not in session:
        return jsonify({"error": "Não logado"}), 401

    user = User.query.get(session["user_id"])

    return jsonify({
        "id": user.id_user,
        "username": user.username,
        "is_admin": user.is_admin
    })
    
@loginapi.route("/admin/gestao", methods=["GET"])
@admin_required
def gestao():
    return jsonify({"message": "Acesso à gestão concedido"})