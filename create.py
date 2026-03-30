from app import create_app
from model import db, Cliente, Produto

app = create_app()

with app.app_context():
    try:
        print(db.metadata.tables.keys())
        db.create_all()
        print("Banco e tabelas criados!")
    except Exception as e:
        print(f"Erro ao criar o banco: {e}")
