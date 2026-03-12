from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.agenda import agenda_bp
    from app.routes.expedientes import expedientes_bp
    from app.routes.aseguradoras import aseguradoras_bp
    from app.routes.juzgados import juzgados_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.clientes import clientes_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(agenda_bp, url_prefix='/api/agenda')
    app.register_blueprint(expedientes_bp, url_prefix='/api/expedientes')
    app.register_blueprint(aseguradoras_bp, url_prefix='/api/aseguradoras')
    app.register_blueprint(juzgados_bp, url_prefix='/api/juzgados')
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
    app.register_blueprint(clientes_bp, url_prefix='/api/clientes')

    return app
