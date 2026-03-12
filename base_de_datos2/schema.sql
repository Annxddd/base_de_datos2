-- ============================================================
-- SISTEMA DE GESTIÓN LEGAL - ESQUEMA DE BASE DE DATOS
-- Basado en prototipo: Login + Agenda del día
-- ============================================================

-- Tabla: roles de usuario
CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: usuarios del sistema
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    nombre_completo TEXT NOT NULL,
    email TEXT UNIQUE,
    rol_id INTEGER NOT NULL,
    activo INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

-- Tabla: aseguradoras
CREATE TABLE aseguradoras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,   -- ej: ASSA, ANCON, CONANCE
    nombre TEXT NOT NULL,
    ruc TEXT,
    telefono TEXT,
    email TEXT,
    activa INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: juzgados
CREATE TABLE juzgados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,   -- ej: JUZGADO 5TO (PEDREGAL)
    ubicacion TEXT,
    ciudad TEXT,
    activo INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: clientes / demandantes
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cedula TEXT UNIQUE,
    telefono TEXT,
    email TEXT,
    direccion TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: estados de expediente
CREATE TABLE estados_expediente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,   -- Pendiente, En curso, Cerrado
    color TEXT,                    -- para UI: gold, orange, dark
    icono TEXT
);

-- Tabla: expedientes (casos legales)
CREATE TABLE expedientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_expediente TEXT NOT NULL UNIQUE,
    cliente_id INTEGER NOT NULL,
    aseguradora_id INTEGER NOT NULL,
    juzgado_id INTEGER,
    usuario_asignado_id INTEGER,
    estado_id INTEGER NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_cierre DATE,
    monto_reclamado REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (aseguradora_id) REFERENCES aseguradoras(id),
    FOREIGN KEY (juzgado_id) REFERENCES juzgados(id),
    FOREIGN KEY (usuario_asignado_id) REFERENCES usuarios(id),
    FOREIGN KEY (estado_id) REFERENCES estados_expediente(id)
);

-- Tabla: agenda (citas / audiencias)
CREATE TABLE agenda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expediente_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora TIME,
    descripcion TEXT,
    juzgado_id INTEGER,
    usuario_responsable_id INTEGER,
    completada INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expediente_id) REFERENCES expedientes(id),
    FOREIGN KEY (juzgado_id) REFERENCES juzgados(id),
    FOREIGN KEY (usuario_responsable_id) REFERENCES usuarios(id)
);

-- ============================================================
-- DATOS INICIALES
-- ============================================================

INSERT INTO roles (nombre, descripcion) VALUES
    ('admin', 'Administrador del sistema'),
    ('abogado', 'Abogado con acceso a expedientes'),
    ('asistente', 'Asistente con acceso limitado');

INSERT INTO estados_expediente (nombre, color, icono) VALUES
    ('Pendiente', '#8B6914', 'clipboard'),
    ('En curso', '#D4A017', 'file-arrow'),
    ('Cerrado', '#333333', 'file-zip');

INSERT INTO aseguradoras (codigo, nombre) VALUES
    ('ASSA', 'ASSA Compañía de Seguros'),
    ('ANCON', 'ANCON Seguros'),
    ('CONANCE', 'CONANCE'),
    ('PARTICULAR', 'Cliente Particular'),
    ('INTEROCEANICA', 'Interoceanica de Seguros');

INSERT INTO juzgados (nombre, ubicacion, ciudad) VALUES
    ('JUZGADO 1RO (PEDREGAL)', 'Pedregal', 'Panamá'),
    ('JUZGADO 3RO (PEDREGAL)', 'Pedregal', 'Panamá'),
    ('JUZGADO 4TO (PEDREGAL)', 'Pedregal', 'Panamá'),
    ('JUZGADO 5TO (PEDREGAL)', 'Pedregal', 'Panamá'),
    ('ALCALDIA DE PANAMA', 'Ciudad de Panamá', 'Panamá'),
    ('CHITRE', 'Chitré', 'Herrera');

-- Usuario administrador por defecto (password: admin123)
INSERT INTO usuarios (usuario, password_hash, nombre_completo, email, rol_id) VALUES
    ('admin', 'pbkdf2:sha256:260000$placeholder', 'Lic. Juan Pérez', 'admin@legal.com', 1);
