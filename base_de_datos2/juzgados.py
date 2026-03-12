# app/routes/juzgados.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Juzgado

juzgados_bp = Blueprint('juzgados', __name__)

@juzgados_bp.route('/', methods=['GET'])
@jwt_required()
def listar():
    items = Juzgado.query.filter_by(activo=True).all()
    return jsonify([i.to_dict() for i in items]), 200

@juzgados_bp.route('/', methods=['POST'])
@jwt_required()
def crear():
    data = request.get_json()
    if not data.get('nombre'):
        return jsonify({'error': 'nombre es requerido'}), 400
    item = Juzgado(nombre=data['nombre'], ubicacion=data.get('ubicacion'), ciudad=data.get('ciudad'))
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@juzgados_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def actualizar(item_id):
    item = Juzgado.query.get_or_404(item_id)
    data = request.get_json()
    for k, v in data.items():
        if hasattr(item, k):
            setattr(item, k, v)
    db.session.commit()
    return jsonify(item.to_dict()), 200
