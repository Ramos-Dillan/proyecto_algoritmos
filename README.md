# API Vademécum – Proyecto Algoritmos

API REST desarrollada en **Python + Flask** para la gestión de medicamentos, laboratorios y grupos terapéuticos.

### 📄 Normalización del archivo Vademécum Optometría

Para normalizar el archivo se realizó el siguiente procedimiento:

Identificación de entidades principales:

Laboratory: Nombre del laboratorio que produce el medicamento.

TherapeuticGroup: Familia o mecanismo de acción de los medicamentos. Cada sheet del Excel corresponde a un grupo terapéutico.

Product: Medicamentos específicos, con atributos de nombre genérico, nombre comercial, concentración, forma farmacéutica, posología, notas, estado activo (is_active) y relación con laboratorio y grupo terapéutico.

Atributos adicionales:

description o potential_illness en TherapeuticGroup: corresponde a la descripción de uso o indicaciones del grupo de medicamentos (ej: "Este tipo de medicamentos se utilizan en infecciones oculares bacterianas externas como conjuntivitis, blefaritis o queratitis").

is_active en Product: indica si el medicamento está actualmente disponible o activo.

Relaciones establecidas:

Un Laboratory puede producir muchos Products → relación 1:N.

Un TherapeuticGroup puede tener muchos Products → relación 1:N.

Cada Product pertenece a un Laboratory y a un TherapeuticGroup → llaves foráneas (laboratory_id, therapeutic_group_id).

Normalización lograda:

Separación de datos repetidos (laboratorios y grupos terapéuticos) en tablas independientes.

Eliminación de redundancias en productos, concentraciones y notas.

Cada tabla tiene su llave primaria y relaciones establecidas, lo que permite integridad referencial y facilita consultas CRUD desde Python.

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
| **🏭 laboratory** | `id`, `name`,`products` |
| **🏥 therapeutic_groups** | `id`, `name`, `mechanism`,`description`,`products` |
| **💊 products** | `id`, `generic_name`, `commercial_name`, `concentration`, `pharmaceutical_form`,`dosage`,`notes`,`is_active`,`laboratory_id(FK)`, `therapeutic_group_id(FK) `|

## 📂 Estructura del Proyecto
```
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
```
### ⚙️ Instalación y Ejecución
## 1️⃣ Clonar el repositorio
```
git clone https://github.com/Ramos-Dillan/proyecto_algoritmos.git
cd proyecto_algoritmos
```
## 2️⃣ Crear entorno virtual
# Windows:
```
python -m venv venv
venv\Scripts\activate
```
# Mac / Linux:
```
python3 -m venv venv
source venv/bin/activate
```
###3️⃣ Instalar dependencias
```
pip install -r requirements.txt
```
### 4️⃣ Configurar variables de entorno
## Crear archivo .env:
```
DATABASE_URL=postgresql://usuario:password@localhost:5432/vademecumDB
SECRET_KEY=clave_secreta
```
## ⚙️ Creación de tablas desde Python
las tablas se crean automáticamente con SQLAlchemy ejecutando:
```
from database import db
from models.laboratory import Laboratory
from models.products import Product
from models.therapeutic_groups import TherapeuticGroup

# Crear todas las tablas en la DB
db.create_all()
print("Tablas creadas correctamente")
```
### 5️⃣ Ejecutar el servidor
```
python app.py
```
### Servidor: http://127.0.0.1:5000

### 🚀 Uso de la API (Postman)
## 🔹 Crear Laboratorio
```
POST http://127.0.0.1:5000/laboratories
```
#Body(Json)
```
{
  "name": "Pfizer",
  
}

```
#Respuesta 
```
{
  "message": "Laboratory created successfully"
}

```
#Actualizacion 
```
PUT http://127.0.0.1:5000/laboratories/<id>
```
#Body (JSON)
```
{
  "name": "Bayer Updated"
}
```
#Respuesta 
```
{
  "message": "Laboratory updated successfully"
}
```
#Eliminar laboratorio
```
DELETE http://127.0.0.1:5000/laboratories/<id>
```
#Respuesta esperada
```
{
  "message": "Laboratory deleted successfully"
}
```
# Crear grupo terapeutico
```
POST http://127.0.0.1:5000/therapeutic-groups

```

#Body(Json)
```
{
  "name": "Analgestics",
  "mechanism: "Pain relief",
  "description" : "Diugs used to reduce pain"
  
}

```
#Crear producto
```
POST http://127.0.0.1:5000/products

```
# Body (JSON):
```
{
  "generic_name": "Paracetamol",
  "commercial_name": Tylenol,
  "concentration": "500 mg",
  "pharmaceutical_form": "Tablet",
  "dosage": "I tablet every 8h",
  "hotes": "Take after meals",
  "is_active" : true,
  "laboratory_id": 1
}

```

#Respuesta
```
{
  "message": "Product created successfully"
}

```

#Obtener productos
```
GET http://127.0.0.1:5000/products

```

#Respuesta
```
 {
            "commercial_name": "Tylenol",
            "concentration": "500mg",
            "dosage": "1 tablet every 8h",
            "generic_name": "Paracetamol",
            "id": 2,
            "is_active": true,
            "laboratory_id": 1,
            "notes": "Take after meals",
            "pharmaceutical_form": "Tablet",
            "therapeutic_group_id": 1
        }


```

#Actualizar producto
```
PUT http://127.0.0.1:5000/products/<id>
```

#Body(JSON)
```
{
  "generic_name": "Paracetamol Extra",
  "commercial_name": "Tylenol Extra",
  "concentration": "650mg",
  "pharmaceutical_form": "Tablet",
  "dosage": "1 tablet every 6h",
  "notes": "Updated notes",
  "is_active": false,
  "therapeutic_group_id": 1,
  "laboratory_id": 1
}
```
#Respuesta
```
{
    "message": "Product updated successfully",
}
```
#Eliminar producto
```
DELETE http://127.0.0.1:5000/products/<id>
```
#Respuesta
```
{
  "message": "Product deleted successfully"
}
```
##Therapeutic_groups
#Crear grupo terapéutico
```
 POST http://127.0.0.1:5000/therapeutic-groups
```

#Body(JSON)
```
{
  "name": "Antibiotics",
  "mechanism": "Bacterial inhibition",
  "description": "Drugs used to fight infections"
}
```
#Respuesta
```
{
    "data": {
        "id": 2,
        "name": "Antibiotics"
    },
    "message": "Grupo terapéutico creado",
    "success": true
}
```

#Obtener grupos terapeuticos
```
GET http://127.0.0.1:5000/therapeutic-groups
```
#Respuesta
```
{
            "description": "Updated description for antibiotics",
            "id": 2,
            "mechanism": "Bacterial inhibition improved",
            "name": "Antibiotics Updated"
        },
        {
            "description": "Drugs used to fight infections",
            "id": 3,
            "mechanism": "Bacterial inhibition",
            "name": "Antibiotics"
        }
    ],
    "message": "Lista de grupos",
   
}
```

#Actualizar grupo terapeutico
```
PUT http://127.0.0.1:5000/therapeutic-groups/<id>
```
#Body(JSON)
```
{
  "name": "Antibiotics Updated",
  "mechanism": "Bacterial inhibition improved",
  "description": "Updated description for antibiotics"
}
```
#Respuesta
```
{
    "data": {
        "description": "Updated description for antibiotics",
        "id": 1,
        "mechanism": "Bacterial inhibition improved",
        "name": "Antibiotics Updated"
    },
    "message": "Grupo terapéutico actualizado",
    "success": true
}
```
#Eliminar grupo terapeutico
```
DELETE http://127.0.0.1:5000/therapeutic-groups/<id>
```
#Respuesta 
```
{
  "message": "Therapeutic group deleted successfully"
}
```
### 📸Documento evidencias 
[Evidencias.proyecto.pdf](https://github.com/user-attachments/files/25667088/Evidencias.proyecto.pdf)

### 📌 .gitignore

El proyecto incluye .gitignore para evitar subir:
-venv/
-.env
-__pycache__/
-Archivos temporales

### 👨‍💻 Autor
Dillan Ramos Barrera
Proyecto – Algoritmos
Ingeniería Biomédica






