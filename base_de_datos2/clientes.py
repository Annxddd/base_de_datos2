# app/routes/clientes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Cliente

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['GET'])
@jwt_required()
def listar():
    buscar = request.args.get('q', '')
    q = Cliente.query
    if buscar:
        q = q.filter(Cliente.nombre.ilike(f'%{buscar}%') | Cliente.cedula.ilike(f'%{buscar}%'))
    clientes = q.order_by(Cliente.nombre).all()
    return jsonify([c.to_dict() for c in clientes]), 200

@clientes_bp.route('/<int:cid>', methods=['GET'])
@jwt_required()
def obtener(cid):
    c = Cliente.query.get_or_404(cid)
    return jsonify(c.to_dict()), 200

@clientes_bp.route('/', methods=['POST'])
@jwt_required()
def crear():
    data = request.get_json()
    if not data.get('nombre'):
        return jsonify({'error': 'nombre es requerido'}), 400
    c = Cliente(
        nombre=data['nombre'],
        cedula=data.get('cedula'),
        telefono=data.get('telefono'),
        email=data.get('email'),
        direccion=data.get('direccion')
    )
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201

@clientes_bp.route('/<int:cid>', methods=['PUT'])
@jwt_required()
def actualizar(cid):
    c = Cliente.query.get_or_404(cid)
    data = request.get_json()
    for k in ['nombre', 'cedula', 'telefono', 'email', 'direccion']:
        if k in data:
            setattr(c, k, data[k])
    db.session.commit()
    return jsonify(c.to_dict()), 200
