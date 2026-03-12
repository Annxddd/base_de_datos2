# app/routes/aseguradoras.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Aseguradora

aseguradoras_bp = Blueprint('aseguradoras', __name__)

@aseguradoras_bp.route('/', methods=['GET'])
@jwt_required()
def listar():
    items = Aseguradora.query.filter_by(activa=True).all()
    return jsonify([i.to_dict() for i in items]), 200

@aseguradoras_bp.route('/', methods=['POST'])
@jwt_required()
def crear():
    data = request.get_json()
    if not data.get('codigo') or not data.get('nombre'):
        return jsonify({'error': 'codigo y nombre son requeridos'}), 400
    item = Aseguradora(**{k: data[k] for k in data if hasattr(Aseguradora, k)})
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@aseguradoras_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def actualizar(item_id):
    item = Aseguradora.query.get_or_404(item_id)
    data = request.get_json()
    for k, v in data.items():
        if hasattr(item, k):
            setattr(item, k, v)
    db.session.commit()
    return jsonify(item.to_dict()), 200

@aseguradoras_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def eliminar(item_id):
    item = Aseguradora.query.get_or_404(item_id)
    item.activa = False
    db.session.commit()
    return jsonify({'mensaje': 'Aseguradora desactivada'}), 200
