from flask import Flask
from routes.api.cliente_api import clienteapi
from routes.api.produtos_api import produtosapi
from routes.api.vendas_api import vendasapi
from routes.cliente_routes import clientesite 
from routes.vendas_routes import vendassite 
from routes.Produtos_routes import produtossite
from routes.home_routes import homesite
from model import db

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///siteapp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '123456789' 
    
    db.init_app(app)

    # HTML
    app.register_blueprint(homesite)
    app.register_blueprint(clientesite, url_prefix="/cliente")
    app.register_blueprint(vendassite, url_prefix="/vendas")
    app.register_blueprint(produtossite, url_prefix="/produtos")
    
    # API
    app.register_blueprint(clienteapi, url_prefix="/api")
    app.register_blueprint(produtosapi, url_prefix="/api")
    app.register_blueprint(vendasapi, url_prefix="/api")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)