# app/routes/usuarios.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Usuario, Rol

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
@jwt_required()
def listar():
    usuarios = Usuario.query.filter_by(activo=True).all()
    return jsonify([u.to_dict() for u in usuarios]), 200

@usuarios_bp.route('/', methods=['POST'])
@jwt_required()
def crear():
    data = request.get_json()
    required = ['usuario', 'contrasena', 'nombre_completo', 'rol_id']
    for f in required:
        if not data.get(f):
            return jsonify({'error': f'{f} es requerido'}), 400
    if Usuario.query.filter_by(usuario=data['usuario']).first():
        return jsonify({'error': 'El usuario ya existe'}), 409
    u = Usuario(
        usuario=data['usuario'],
        nombre_completo=data['nombre_completo'],
        email=data.get('email'),
        rol_id=data['rol_id']
    )
    u.set_password(data['contrasena'])
    db.session.add(u)
    db.session.commit()
    return jsonify(u.to_dict()), 201

@usuarios_bp.route('/<int:uid>', methods=['PUT'])
@jwt_required()
def actualizar(uid):
    u = Usuario.query.get_or_404(uid)
    data = request.get_json()
    for k in ['nombre_completo', 'email', 'rol_id', 'activo']:
        if k in data:
            setattr(u, k, data[k])
    if 'contrasena' in data:
        u.set_password(data['contrasena'])
    db.session.commit()
    return jsonify(u.to_dict()), 200
