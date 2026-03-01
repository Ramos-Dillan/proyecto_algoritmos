API Vademécum – Proyecto Algoritmos
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

Tabla	Campos
🏭 laboratory	id, name, country
🏥 therapeutic_groups	id, name, description
💊 products	id, name, price, laboratory_id (FK), therapeutic_group_id (FK)
📂 Estructura del Proyecto
text
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
bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
2️⃣ Crear entorno virtual
Windows:

bash
python -m venv venv
venv\Scripts\activate
Mac/Linux:

bash
python3 -m venv venv
source venv/bin/activate
3️⃣ Instalar dependencias
bash
pip install -r requirements.txt
4️⃣ Configurar variables de entorno
Crear archivo .env en la raíz del proyecto:

text
DATABASE_URL=postgresql://usuario:password@localhost:5432/vademecumDB
SECRET_KEY=clave_secreta
5️⃣ Ejecutar el servidor
bash
python app.py
El servidor se ejecutará en: http://127.0.0.1:5000

🚀 Uso de la API
🔹 Crear Laboratorio
text
POST http://127.0.0.1:5000/laboratories
Body (JSON):

json
{
  "name": "Pfizer",
  "country": "USA"
}
Respuesta:

json
{
  "message": "Laboratory created successfully"
}
🔹 Crear Grupo Terapéutico
text
POST http://127.0.0.1:5000/therapeutic-groups
Body (JSON):

json
{
  "name": "Analgesicos",
  "description": "Medicamentos para el dolor"
}
🔹 Crear Producto
text
POST http://127.0.0.1:5000/products
Body (JSON):

json
{
  "name": "Ibuprofeno",
  "price": 15000,
  "laboratory_id": 1,
  "therapeutic_group_id": 1
}
Respuesta:

json
{
  "message": "Product created successfully"
}
🔹 Obtener todos los productos
text
GET http://127.0.0.1:5000/products
Respuesta esperada:

json
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
La carpeta docs/ contiene los siguientes pantallazos requeridos:

<img width="1105" height="205" alt="image" src="https://github.com/user-attachments/assets/5834ac64-5002-46fd-9959-cae753fc002f" />


postman_create_laboratory.png

postman_create_group.png

postman_create_product.png

postman_get_products.png

database_tables.png

📌 Archivo .gitignore
El proyecto incluye .gitignore para evitar subir:

venv/

.env

__pycache__/

Archivos temporales

👨‍💻 Autor
Santiago Barrera
Proyecto – Algoritmos
Ingeniería Biomédica



