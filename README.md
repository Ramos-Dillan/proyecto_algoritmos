# API Vademécum – Proyecto Algoritmos

API REST desarrollada en **Python + Flask** para la gestión de medicamentos, laboratorios y grupos terapéuticos.

## 🧠 Descripción

Esta API permite:
- ✅ Crear y consultar **laboratorios**
- ✅ Crear y consultar **grupos terapéuticos**
- ✅ Crear y consultar **productos (medicamentos)**
- ✅ Gestionar relaciones entre las tablas

**Base de datos:** PostgreSQL  
**Nombre DB:** `vademecumDB`

## 🗄 Estructura de la Base de Datos

| Tabla | Campos |
|-------|--------|
| **🏭 laboratory** | `id`, `name`, `country` |
| **🏥 therapeutic_groups** | `id`, `name`, `description` |
| **💊 products** | `id`, `name`, `price`, `laboratory_id (FK)`, `therapeutic_group_id (FK)` |

## 📂 Estructura del Proyecto
vademecum_project/
├─ app.py                # Archivo principal de la aplicación
├─ database.py           # Configuración y conexión a la base de datos
├─ config.py             # Configuraciones generales de la app
├─ .env                  # Variables de entorno
├─ .gitignore            # Archivos y carpetas ignoradas por Git
├─ requirements.txt      # Dependencias del proyecto
├─ README.md             # Documentación del proyecto
├─ models/               # Modelos de datos
├─ routes/               # Rutas de la aplicación
├─ services/             # Lógica de negocio y servicios
└─ utils/                # Funciones y utilidades auxiliares

