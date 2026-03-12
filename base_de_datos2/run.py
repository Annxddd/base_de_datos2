from app import create_app, db
from app.models import (Rol, Usuario, Aseguradora, Juzgado,
                         EstadoExpediente, Cliente, Expediente, Agenda)
from datetime import date, time

app = create_app()


def seed_database():
    """Poblar la base de datos con datos de ejemplo del prototipo."""
    # Roles
    roles_data = [
        ('admin', 'Administrador del sistema'),
        ('abogado', 'Abogado con acceso a expedientes'),
        ('asistente', 'Asistente con acceso limitado')
    ]
    for nombre, desc in roles_data:
        if not Rol.query.filter_by(nombre=nombre).first():
            db.session.add(Rol(nombre=nombre, descripcion=desc))

    # Estados
    estados_data = [
        ('Pendiente', '#8B6914', 'clipboard'),
        ('En curso', '#D4A017', 'file-arrow'),
        ('Cerrado', '#333333', 'file-zip')
    ]
    for nombre, color, icono in estados_data:
        if not EstadoExpediente.query.filter_by(nombre=nombre).first():
            db.session.add(EstadoExpediente(nombre=nombre, color=color, icono=icono))

    # Aseguradoras
    aseguradoras_data = [
        ('ASSA', 'ASSA Compañía de Seguros'),
        ('ANCON', 'ANCON Seguros'),
        ('CONANCE', 'CONANCE'),
        ('PARTICULAR', 'Cliente Particular'),
        ('INTEROCEANICA', 'Interoceanica de Seguros')
    ]
    for codigo, nombre in aseguradoras_data:
        if not Aseguradora.query.filter_by(codigo=codigo).first():
            db.session.add(Aseguradora(codigo=codigo, nombre=nombre))

    # Juzgados
    juzgados_data = [
        ('JUZGADO 1RO (PEDREGAL)', 'Pedregal', 'Panamá'),
        ('JUZGADO 3RO (PEDREGAL)', 'Pedregal', 'Panamá'),
        ('JUZGADO 4TO (PEDREGAL)', 'Pedregal', 'Panamá'),
        ('JUZGADO 5TO (PEDREGAL)', 'Pedregal', 'Panamá'),
        ('ALCALDIA DE PANAMA', 'Ciudad de Panamá', 'Panamá'),
        ('CHITRE', 'Chitré', 'Herrera')
    ]
    for nombre, ubicacion, ciudad in juzgados_data:
        if not Juzgado.query.filter_by(nombre=nombre).first():
            db.session.add(Juzgado(nombre=nombre, ubicacion=ubicacion, ciudad=ciudad))

    db.session.commit()

    # Usuario admin
    if not Usuario.query.filter_by(usuario='admin').first():
        rol_admin = Rol.query.filter_by(nombre='admin').first()
        u = Usuario(
            usuario='admin',
            nombre_completo='Lic. Juan Pérez',
            email='admin@legal.com',
            rol_id=rol_admin.id
        )
        u.set_password('admin123')
        db.session.add(u)
        db.session.commit()

    # Clientes de ejemplo
    clientes_data = [
        ('Anthony Trejos', '8-123-456'),
        ('Luis Molina', '4-234-567'),
        ('Katherine Kent', '2-345-678'),
        ('Martin Alvarado', '6-456-789'),
        ('Joel Arauz Rodriguez', '1-567-890'),
        ('Michelle Vega', '8-678-901'),
        ('Candice Henry', '3-789-012')
    ]
    clientes_creados = []
    for nombre, cedula in clientes_data:
        c = Cliente.query.filter_by(cedula=cedula).first()
        if not c:
            c = Cliente(nombre=nombre, cedula=cedula)
            db.session.add(c)
        clientes_creados.append(c)
    db.session.commit()

    # Expedientes y agenda de ejemplo
    if Expediente.query.count() == 0:
        aseguradoras = {a.codigo: a for a in Aseguradora.query.all()}
        juzgados = {j.nombre: j for j in Juzgado.query.all()}
        estado_pendiente = EstadoExpediente.query.filter_by(nombre='Pendiente').first()
        clientes = Cliente.query.all()

        exp_data = [
            ('EXP-001', clientes[0], aseguradoras['ASSA'], juzgados['JUZGADO 5TO (PEDREGAL)']),
            ('EXP-002', clientes[1], aseguradoras['ANCON'], juzgados['JUZGADO 4TO (PEDREGAL)']),
            ('EXP-003', clientes[2], aseguradoras['ASSA'], juzgados['JUZGADO 5TO (PEDREGAL)']),
            ('EXP-004', clientes[3], aseguradoras['CONANCE'], juzgados['JUZGADO 1RO (PEDREGAL)']),
            ('EXP-005', clientes[4], aseguradoras['PARTICULAR'], juzgados['JUZGADO 3RO (PEDREGAL)']),
            ('EXP-006', clientes[5], aseguradoras['INTEROCEANICA'], juzgados['ALCALDIA DE PANAMA']),
            ('EXP-007', clientes[6], aseguradoras['ANCON'], juzgados['CHITRE']),
        ]

        expedientes_creados = []
        for num, cliente, aseg, juz in exp_data:
            exp = Expediente(
                numero_expediente=num,
                cliente_id=cliente.id,
                aseguradora_id=aseg.id,
                juzgado_id=juz.id,
                estado_id=estado_pendiente.id,
                fecha_inicio=date(2019, 1, 1)
            )
            db.session.add(exp)
            expedientes_creados.append((exp, juz))

        db.session.commit()

        # Agenda del 7 de enero 2019 (como en el prototipo)
        horas = [time(9, 0), time(9, 30), time(10, 0), time(10, 30),
                 time(11, 0), time(11, 30), time(14, 0)]
        for i, ((exp, juz), hora) in enumerate(zip(expedientes_creados, horas)):
            cita = Agenda(
                expediente_id=exp.id,
                fecha=date(2019, 1, 7),
                hora=hora,
                juzgado_id=juz.id,
                descripcion='Audiencia programada'
            )
            db.session.add(cita)

        db.session.commit()
        print("✅ Base de datos poblada con datos de ejemplo.")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
        print("✅ Tablas creadas exitosamente.")
        print("🚀 Iniciando servidor en http://localhost:5000")
    app.run(debug=True, port=5000)
