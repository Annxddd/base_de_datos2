from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import Usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Iniciar sesión
    ---
    Body: { "usuario": "admin", "contrasena": "admin123" }
    Returns: { "access_token": "...", "usuario": {...} }
    """
    data = request.get_json()
    if not data or not data.get('usuario') or not data.get('contrasena'):
        return jsonify({'error': 'Usuario y contraseña requeridos'}), 400

    user = Usuario.query.filter_by(usuario=data['usuario'], activo=True).first()
    if not user or not user.check_password(data['contrasena']):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': token, 'usuario': user.to_dict()}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """Retorna el usuario autenticado actual."""
    user_id = get_jwt_identity()
    user = Usuario.query.get_or_404(int(user_id))
    return jsonify(user.to_dict()), 200
