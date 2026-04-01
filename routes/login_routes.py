from flask import Blueprint, render_template, session, redirect, flash

loginsite = Blueprint('loginsite', __name__)

@loginsite.route('/login')
def login():
    if "user_id" in session:
        return redirect("/")
    return render_template('login.html')

@loginsite.route("/admin/criar")
def registrar_user():
    if not session.get("is_admin"):
        flash("Acesso Restrito!!")
        return redirect("/")
    return render_template('admin/criausuario.html')

@loginsite.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@loginsite.route("/admin/gestao")
def gestao():
    if not session.get("is_admin"):
        flash("Acesso Restrito!!")
        return redirect("/")
    return render_template('admin/gestao.html')
