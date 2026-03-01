📌 API Vademécum – Proyecto Algoritmos

API REST desarrollada en Python + Flask para la gestión de medicamentos, laboratorios y grupos terapéuticos.

🧠 Descripción

Esta API permite:

Crear y consultar laboratorios

Crear y consultar grupos terapéuticos

Crear y consultar productos (medicamentos)

Gestionar relaciones entre las tablas

Base de datos utilizada: PostgreSQL
Nombre de la base de datos: vademecumDB

🗄 Estructura de la Base de Datos

La base de datos contiene 3 tablas:

🏭 laboratory

id

name

country

🏥 therapeutic_groups

id

name

description

💊 products

id

name

price

laboratory_id (FK)

therapeutic_group_id (FK)

📂 Estructura del Proyecto
vademecum_project/
├─ app.py
├─ database.py
├─ config.py
├─ .env
├─ .gitignore
├─ requirements.txt
├─ README.md
├─ models/
├─ routes/
├─ services/
└─ utils/
⚙️ Instalación y Ejecución
1️⃣ Clonar el repositorio
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
2️⃣ Crear entorno virtual
Windows
python -m venv venv
venv\Scripts\activate
Mac/Linux
python3 -m venv venv
source venv/bin/activate
3️⃣ Instalar dependencias
pip install -r requirements.txt
4️⃣ Configurar variables de entorno

Crear archivo .env en la raíz del proyecto:

DATABASE_URL=postgresql://usuario:password@localhost:5432/vademecumDB
SECRET_KEY=clave_secreta
5️⃣ Ejecutar el servidor
python app.py

El servidor se ejecutará en:

http://127.0.0.1:5000
🚀 Uso de la API con Postman
🔹 Crear Laboratorio

POST

http://127.0.0.1:5000/laboratories

Body → raw → JSON:

{
  "name": "Pfizer",
  "country": "USA"
}

Respuesta esperada:

{
  "message": "Laboratory created successfully"
}
🔹 Crear Grupo Terapéutico

POST

http://127.0.0.1:5000/therapeutic-groups
{
  "name": "Analgesicos",
  "description": "Medicamentos para el dolor"
}
🔹 Crear Producto

POST

http://127.0.0.1:5000/products
{
  "name": "Ibuprofeno",
  "price": 15000,
  "laboratory_id": 1,
  "therapeutic_group_id": 1
}

Respuesta esperada:

{
  "message": "Product created successfully"
}
🔹 Obtener todos los productos

GET

http://127.0.0.1:5000/products

Respuesta esperada:

[
  {
    "id": 1,
    "name": "Ibuprofeno",
    "price": 15000,
    "laboratory": "Pfizer",
    "therapeutic_group": "Analgesicos"
  }
]
📸 Evidencias Requeridas

Agregar una carpeta docs/ con los siguientes pantallazos:

docs/
├─ server_running.png
├─ postman_create_laboratory.png
├─ postman_create_group.png
├─ postman_create_product.png
├─ postman_get_products.png
├─ database_tables.png

Luego agregarlos en el README así:

![Servidor corriendo](docs/server_running.png)
![Crear laboratorio](docs/postman_create_laboratory.png)
📌 Archivo .gitignore

El proyecto incluye .gitignore para evitar subir:

venv/

.env

pycache/

archivos temporales

👨‍💻 Autor

Santiago Barrera
Proyecto – Algoritmos
Ingeniería Biomédica
