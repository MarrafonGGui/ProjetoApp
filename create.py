from app import create_app
from model import db, User, Cliente, Produto, Venda, ItemVenda

app = create_app()

with app.app_context():
    try:
        print(db.metadata.tables.keys())
        db.create_all()
        print("Banco e tabelas criados!")
        
        if not User.query.filter_by(username="admin").first():
            admin_user = User(username="admin", is_admin=True)
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()
            print("Usuário admin criado!")
    except Exception as e:
        print(f"Erro ao criar o banco: {e}")
