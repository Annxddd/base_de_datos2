from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from app import db
from app.models import Expediente, EstadoExpediente

expedientes_bp = Blueprint('expedientes', __name__)


@expedientes_bp.route('/', methods=['GET'])
@jwt_required()
def listar_expedientes():
    """
    Lista expedientes con filtros opcionales.
    Query params: estado, aseguradora_id, cliente_id, page, per_page
    """
    estado = request.args.get('estado')
    aseguradora_id = request.args.get('aseguradora_id')
    cliente_id = request.args.get('cliente_id')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    q = Expediente.query
    if estado:
        q = q.join(EstadoExpediente).filter(EstadoExpediente.nombre == estado)
    if aseguradora_id:
        q = q.filter(Expediente.aseguradora_id == int(aseguradora_id))
    if cliente_id:
        q = q.filter(Expediente.cliente_id == int(cliente_id))

    paginado = q.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'expedientes': [e.to_dict() for e in paginado.items],
        'total': paginado.total,
        'paginas': paginado.pages,
        'pagina_actual': page
    }), 200


@expedientes_bp.route('/<int:exp_id>', methods=['GET'])
@jwt_required()
def obtener_expediente(exp_id):
    """Obtiene un expediente por ID."""
    exp = Expediente.query.get_or_404(exp_id)
    return jsonify(exp.to_dict()), 200


@expedientes_bp.route('/', methods=['POST'])
@jwt_required()
def crear_expediente():
    """
    Crea un nuevo expediente.
    Body: { numero_expediente, cliente_id, aseguradora_id, estado_id,
            juzgado_id, descripcion, fecha_inicio, monto_reclamado }
    """
    data = request.get_json()
    required = ['numero_expediente', 'cliente_id', 'aseguradora_id', 'estado_id', 'fecha_inicio']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} es requerido'}), 400

    try:
        fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400

    exp = Expediente(
        numero_expediente=data['numero_expediente'],
        cliente_id=data['cliente_id'],
        aseguradora_id=data['aseguradora_id'],
        juzgado_id=data.get('juzgado_id'),
        usuario_asignado_id=data.get('usuario_asignado_id'),
        estado_id=data['estado_id'],
        descripcion=data.get('descripcion'),
        fecha_inicio=fecha_inicio,
        monto_reclamado=data.get('monto_reclamado')
    )
    db.session.add(exp)
    db.session.commit()
    return jsonify(exp.to_dict()), 201


@expedientes_bp.route('/<int:exp_id>', methods=['PUT'])
@jwt_required()
def actualizar_expediente(exp_id):
    """Actualiza un expediente existente."""
    exp = Expediente.query.get_or_404(exp_id)
    data = request.get_json()

    campos = ['aseguradora_id', 'juzgado_id', 'estado_id',
              'descripcion', 'monto_reclamado', 'usuario_asignado_id']
    for campo in campos:
        if campo in data:
            setattr(exp, campo, data[campo])

    if 'fecha_cierre' in data and data['fecha_cierre']:
        exp.fecha_cierre = datetime.strptime(data['fecha_cierre'], '%Y-%m-%d').date()

    db.session.commit()
    return jsonify(exp.to_dict()), 200


@expedientes_bp.route('/<int:exp_id>', methods=['DELETE'])
@jwt_required()
def eliminar_expediente(exp_id):
    """Elimina un expediente."""
    exp = Expediente.query.get_or_404(exp_id)
    db.session.delete(exp)
    db.session.commit()
    return jsonify({'mensaje': 'Expediente eliminado'}), 200


@expedientes_bp.route('/resumen', methods=['GET'])
@jwt_required()
def resumen_expedientes():
    """Retorna conteo de expedientes por estado (para los badges del dashboard)."""
    estados = EstadoExpediente.query.all()
    resumen = {}
    for e in estados:
        resumen[e.nombre] = Expediente.query.filter_by(estado_id=e.id).count()
    return jsonify(resumen), 200
