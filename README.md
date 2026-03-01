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

⚙️ Instalación y Ejecución
1️⃣ Clonar el repositorio
git clone https://github.com/Ramos-Dillan/proyecto_algoritmos.git
cd proyecto_algoritmos
2️⃣ Crear entorno virtual

Windows:

python -m venv venv
venv\Scripts\activate

Mac / Linux:

python3 -m venv venv
source venv/bin/activate
3️⃣ Instalar dependencias
pip install -r requirements.txt
4️⃣ Configurar variables de entorno

Crear archivo .env con el siguiente contenido:

DATABASE_URL=postgresql://usuario:password@localhost:5432/vademecumDB
SECRET_KEY=clave_secreta
5️⃣ Ejecutar el servidor
python app.py

Servidor corriendo en: http://127.0.0.1:5000

🚀 Uso de la API (Postman)
🔹 Crear Laboratorio

POST http://127.0.0.1:5000/laboratories
Body (JSON):

{
  "name": "Pfizer",
  "country": "USA"
}

Respuesta:

{
  "message": "Laboratory created successfully"
}
🔹 Crear Grupo Terapéutico

POST http://127.0.0.1:5000/therapeutic-groups
Body (JSON):

{
  "name": "Analgesicos",
  "description": "Medicamentos para el dolor"
}
🔹 Crear Producto

POST http://127.0.0.1:5000/products
Body (JSON):

{
  "name": "Ibuprofeno",
  "price": 15000,
  "laboratory_id": 1,
  "therapeutic_group_id": 1
}

Respuesta:

{
  "message": "Product created successfully"
}
🔹 Obtener Productos

GET http://127.0.0.1:5000/products
Respuesta:

[
  {
    "id": 1,
    "name": "Ibuprofeno",
    "price": 15000,
    "laboratory": "Pfizer",
    "therapeutic_group": "Analgesicos"
  }
]
📸 Evidencias
[Evidencias.proyecto.pdf](https://github.com/user-attachments/files/25666563/Evidencias.proyecto.pdf)


📌 .gitignore

El proyecto incluye .gitignore para evitar subir archivos innecesarios:

venv/
.env
__pycache__/
archivos temporales
👨‍💻 Autor

Dillan Ramos Barrera
Proyecto – Algoritmos
Ingeniería Biomédica
