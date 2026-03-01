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

proyecto_algoritmos/
├── app.py
├── database.py
├── config.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── models/
├── routes/
├── services/
└── utils/
