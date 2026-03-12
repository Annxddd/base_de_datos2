from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import date, datetime
from app import db
from app.models import Agenda, Expediente, EstadoExpediente

agenda_bp = Blueprint('agenda', __name__)


@agenda_bp.route('/dia', methods=['GET'])
@jwt_required()
def agenda_del_dia():
    """
    Agenda del día (vista principal del prototipo).
    Query param: fecha (YYYY-MM-DD), por defecto hoy.
    Returns: lista de audiencias + contadores de expedientes.
    """
    fecha_str = request.args.get('fecha')
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else date.today()
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400

    citas = Agenda.query.filter_by(fecha=fecha).order_by(Agenda.hora).all()

    # Contadores de expedientes por estado
    pendientes = Expediente.query.join(EstadoExpediente).filter(
        EstadoExpediente.nombre == 'Pendiente').count()
    en_curso = Expediente.query.join(EstadoExpediente).filter(
        EstadoExpediente.nombre == 'En curso').count()
    cerrados = Expediente.query.join(EstadoExpediente).filter(
        EstadoExpediente.nombre == 'Cerrado').count()

    return jsonify({
        'fecha': fecha.isoformat(),
        'dia_semana': fecha.strftime('%A'),
        'agenda': [c.to_dict() for c in citas],
        'resumen': {
            'pendientes': pendientes,
            'en_curso': en_curso,
            'cerrados': cerrados
        }
    }), 200


@agenda_bp.route('/', methods=['GET'])
@jwt_required()
def listar_agenda():
    """Lista agenda con filtros opcionales: fecha_inicio, fecha_fin, expediente_id."""
    fi = request.args.get('fecha_inicio')
    ff = request.args.get('fecha_fin')
    exp_id = request.args.get('expediente_id')

    q = Agenda.query
    if fi:
        q = q.filter(Agenda.fecha >= fi)
    if ff:
        q = q.filter(Agenda.fecha <= ff)
    if exp_id:
        q = q.filter(Agenda.expediente_id == int(exp_id))

    citas = q.order_by(Agenda.fecha, Agenda.hora).all()
    return jsonify([c.to_dict() for c in citas]), 200


@agenda_bp.route('/', methods=['POST'])
@jwt_required()
def crear_cita():
    """
    Crea una nueva cita en la agenda.
    Body: { expediente_id, fecha, hora, descripcion, juzgado_id, usuario_responsable_id }
    """
    data = request.get_json()
    if not data or not data.get('expediente_id') or not data.get('fecha'):
        return jsonify({'error': 'expediente_id y fecha son requeridos'}), 400

    try:
        fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        hora = datetime.strptime(data['hora'], '%H:%M').time() if data.get('hora') else None
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    cita = Agenda(
        expediente_id=data['expediente_id'],
        fecha=fecha,
        hora=hora,
        descripcion=data.get('descripcion'),
        juzgado_id=data.get('juzgado_id'),
        usuario_responsable_id=data.get('usuario_responsable_id')
    )
    db.session.add(cita)
    db.session.commit()
    return jsonify(cita.to_dict()), 201


@agenda_bp.route('/<int:cita_id>', methods=['PUT'])
@jwt_required()
def actualizar_cita(cita_id):
    """Actualiza una cita existente."""
    cita = Agenda.query.get_or_404(cita_id)
    data = request.get_json()

    if 'fecha' in data:
        cita.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
    if 'hora' in data:
        cita.hora = datetime.strptime(data['hora'], '%H:%M').time() if data['hora'] else None
    if 'descripcion' in data:
        cita.descripcion = data['descripcion']
    if 'juzgado_id' in data:
        cita.juzgado_id = data['juzgado_id']
    if 'completada' in data:
        cita.completada = data['completada']

    db.session.commit()
    return jsonify(cita.to_dict()), 200


@agenda_bp.route('/<int:cita_id>', methods=['DELETE'])
@jwt_required()
def eliminar_cita(cita_id):
    """Elimina una cita de la agenda."""
    cita = Agenda.query.get_or_404(cita_id)
    db.session.delete(cita)
    db.session.commit()
    return jsonify({'mensaje': 'Cita eliminada'}), 200
