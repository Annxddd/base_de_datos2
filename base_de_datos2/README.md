# Sistema de Gestión Legal — API REST

Proyecto desarrollado desde prototipo de interfaz visual hasta API REST con Flask y Python.

## Estructura del Proyecto

```
legal_app/
├── run.py                  # Punto de entrada + seed de datos
├── config.py               # Configuración (DB, JWT, CORS)
├── requirements.txt        # Dependencias Python
├── schema.sql              # Esquema SQL completo
└── app/
    ├── __init__.py         # Factory de la app Flask
    ├── models.py           # Modelos SQLAlchemy (7 entidades)
    └── routes/
        ├── auth.py         # POST /api/auth/login, GET /api/auth/me
        ├── agenda.py       # CRUD agenda + GET /api/agenda/dia
        ├── expedientes.py  # CRUD expedientes + resumen
        ├── aseguradoras.py # CRUD aseguradoras
        ├── juzgados.py     # CRUD juzgados
        ├── usuarios.py     # CRUD usuarios
        └── clientes.py     # CRUD clientes con búsqueda
```

## Instalación y Ejecución

```bash
pip install -r requirements.txt
python run.py
```

El servidor inicia en `http://localhost:5000`.  
Credenciales por defecto: `admin` / `admin123`

## Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | /api/auth/login | Login → JWT token |
| GET | /api/agenda/dia?fecha=2019-01-07 | Agenda del día |
| GET | /api/expedientes/resumen | Contadores (102 pendientes, 72 en curso, 204 cerrados) |
| GET | /api/expedientes/ | Lista con paginación |
| POST | /api/expedientes/ | Crear expediente |

## Entidades

- **Roles** → **Usuarios** (1:N)
- **Clientes** → **Expedientes** (1:N)
- **Aseguradoras** → **Expedientes** (1:N)
- **Juzgados** → **Expedientes** (1:N)
- **Estados** → **Expedientes** (1:N)
- **Expedientes** → **Agenda** (1:N)
