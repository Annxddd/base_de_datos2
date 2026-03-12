from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    usuarios = db.relationship('Usuario', backref='rol', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'nombre': self.nombre, 'descripcion': self.descripcion}


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    nombre_completo = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'usuario': self.usuario,
            'nombre_completo': self.nombre_completo,
            'email': self.email,
            'rol': self.rol.nombre if self.rol else None,
            'activo': self.activo
        }


class Aseguradora(db.Model):
    __tablename__ = 'aseguradoras'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(30), nullable=False, unique=True)
    nombre = db.Column(db.String(150), nullable=False)
    ruc = db.Column(db.String(50))
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(120))
    activa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expedientes = db.relationship('Expediente', backref='aseguradora', lazy=True)

    def to_dict(self):
        return {
            'id': self.id, 'codigo': self.codigo, 'nombre': self.nombre,
            'ruc': self.ruc, 'telefono': self.telefono,
            'email': self.email, 'activa': self.activa
        }


class Juzgado(db.Model):
    __tablename__ = 'juzgados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False, unique=True)
    ubicacion = db.Column(db.String(150))
    ciudad = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'nombre': self.nombre,
            'ubicacion': self.ubicacion, 'ciudad': self.ciudad, 'activo': self.activo
        }


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    cedula = db.Column(db.String(30), unique=True)
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(120))
    direccion = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expedientes = db.relationship('Expediente', backref='cliente', lazy=True)

    def to_dict(self):
        return {
            'id': self.id, 'nombre': self.nombre, 'cedula': self.cedula,
            'telefono': self.telefono, 'email': self.email, 'direccion': self.direccion
        }


class EstadoExpediente(db.Model):
    __tablename__ = 'estados_expediente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(20))
    icono = db.Column(db.String(50))
    expedientes = db.relationship('Expediente', backref='estado', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'nombre': self.nombre, 'color': self.color, 'icono': self.icono}


class Expediente(db.Model):
    __tablename__ = 'expedientes'
    id = db.Column(db.Integer, primary_key=True)
    numero_expediente = db.Column(db.String(50), nullable=False, unique=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    aseguradora_id = db.Column(db.Integer, db.ForeignKey('aseguradoras.id'), nullable=False)
    juzgado_id = db.Column(db.Integer, db.ForeignKey('juzgados.id'))
    usuario_asignado_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    estado_id = db.Column(db.Integer, db.ForeignKey('estados_expediente.id'), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_cierre = db.Column(db.Date)
    monto_reclamado = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    agenda = db.relationship('Agenda', backref='expediente', lazy=True)
    usuario_asignado = db.relationship('Usuario', foreign_keys=[usuario_asignado_id])

    def to_dict(self):
        return {
            'id': self.id,
            'numero_expediente': self.numero_expediente,
            'cliente': self.cliente.to_dict() if self.cliente else None,
            'aseguradora': self.aseguradora.to_dict() if self.aseguradora else None,
            'juzgado': self.juzgado.to_dict() if self.juzgado else None,
            'estado': self.estado.to_dict() if self.estado else None,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_cierre': self.fecha_cierre.isoformat() if self.fecha_cierre else None,
            'monto_reclamado': self.monto_reclamado,
            'usuario_asignado': self.usuario_asignado.nombre_completo if self.usuario_asignado else None
        }


class Agenda(db.Model):
    __tablename__ = 'agenda'
    id = db.Column(db.Integer, primary_key=True)
    expediente_id = db.Column(db.Integer, db.ForeignKey('expedientes.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time)
    descripcion = db.Column(db.Text)
    juzgado_id = db.Column(db.Integer, db.ForeignKey('juzgados.id'))
    usuario_responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    completada = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    juzgado = db.relationship('Juzgado', foreign_keys=[juzgado_id])
    usuario_responsable = db.relationship('Usuario', foreign_keys=[usuario_responsable_id])

    def to_dict(self):
        return {
            'id': self.id,
            'expediente_id': self.expediente_id,
            'aseguradora': self.expediente.aseguradora.codigo if self.expediente else None,
            'cliente': self.expediente.cliente.nombre if self.expediente else None,
            'juzgado': self.juzgado.nombre if self.juzgado else None,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'hora': self.hora.strftime('%H:%M') if self.hora else None,
            'descripcion': self.descripcion,
            'completada': self.completada
        }
