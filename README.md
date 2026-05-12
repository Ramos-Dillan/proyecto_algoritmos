# 💊 API Vademécum CES — Proyecto Algoritmos

API REST desarrollada en **Python + Flask** para la gestión farmacéutica institucional: medicamentos, laboratorios, grupos terapéuticos, categorías, usuarios y roles.

---

## 🧠 Descripción

Sistema de gestión farmacéutica que permite:

- ✅ Autenticación con JWT y control de acceso por roles
- ✅ Gestión completa de **productos (medicamentos)**
- ✅ Gestión de **laboratorios**, **categorías** y **grupos terapéuticos**
- ✅ Administración de **usuarios** y **roles**
- ✅ **Dashboard** con estadísticas en tiempo real
- ✅ Recuperación de contraseña por correo electrónico
- ✅ Filtros y paginación en productos

**Base de datos:** PostgreSQL  
**Nombre DB:** `vademecumDB`  
**Puerto por defecto:** `http://localhost:5000`

---

## 🗂️ Estructura del Proyecto

```
proyecto_algoritmos/
├── common/
│   └── http.py                  # Helpers de respuesta HTTP
├── db/
│   ├── db.py                    # Conexión SQLAlchemy
│   └── models.py                # Modelos ORM
├── routes/
│   ├── auth/                    # Autenticación y usuarios
│   ├── categories/              # Categorías
│   ├── dashboard/               # Dashboard y estadísticas
│   ├── laboratories/            # Laboratorios
│   ├── products/                # Productos
│   ├── roles/                   # Roles
│   └── therapeutic_groups/      # Grupos terapéuticos
├── security/
│   └── roles.py                 # Decorador role_required
├── app.py                       # Entry point Flask
├── config.py                    # Configuración
├── db_init.py                   # Inicialización de tablas
├── .env                         # Variables de entorno
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🗄️ Modelo de Base de Datos

| Tabla | Campos principales |
|---|---|
| **users** | `id`, `username`, `email`, `identification`, `password`, `role_id (FK)`, `is_active`, `reset_token`, `reset_token_expires` |
| **roles** | `id`, `name` |
| **products** | `id`, `generic_name`, `commercial_name`, `concentration`, `pharmaceutical_form`, `dosage`, `notes`, `is_active`, `image_url`, `therapeutic_group_id (FK)`, `laboratory_id (FK)`, `category_id (FK)` |
| **laboratories** | `id`, `name` |
| **therapeutic_groups** | `id`, `name`, `mechanism`, `description` |
| **categories** | `id`, `name` |

### Relaciones

```
Laboratory      (1) ──── (N) Product
TherapeuticGroup (1) ──── (N) Product
Category        (1) ──── (N) Product
Role            (1) ──── (N) User
```

---

## ⚙️ Instalación y Ejecución

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Ramos-Dillan/proyecto_algoritmos.git
cd proyecto_algoritmos
```

### 2️⃣ Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno

Crear archivo `.env` en la raíz:

```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/vademecumDB
SECRET_KEY=clave_secreta_jwt

# Correo para recuperación de contraseña (opcional en dev)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tucorreo@gmail.com
SMTP_PASS=tu_app_password
SMTP_FROM=tucorreo@gmail.com
APP_NAME=Vademecum

# URL del frontend para el link de reset
FRONTEND_URL=http://localhost:4200
```

### 5️⃣ Crear tablas en la base de datos

```bash
python db_init.py
```

### 6️⃣ Ejecutar el servidor

```bash
python app.py
```

Servidor disponible en: `http://127.0.0.1:5000`

---

## 🔐 Autenticación

Todos los endpoints protegidos requieren un token JWT en el header:

```
Authorization: Bearer <access_token>
```

El token se obtiene en el endpoint de login.

### Asignación automática de roles por correo

| Dominio del correo | Rol asignado |
|---|---|
| `@admin.com` | `admin` |
| `@medico.com` | `medico` |
| Cualquier otro | `estudiante` |

---

## 📌 Endpoints

### 🔑 Auth — `/auth`

| Método | Endpoint | Auth | Descripción |
|---|---|---|---|
| POST | `/auth/create` | ❌ | Registrar nuevo usuario |
| POST | `/auth/login` | ❌ | Iniciar sesión |
| POST | `/auth/forgot-password` | ❌ | Solicitar reset de contraseña |
| POST | `/auth/reset-password` | ❌ | Restablecer contraseña con token |
| GET | `/auth/users` | ✅ | Obtener todos los usuarios |
| PATCH | `/auth/users/<id>` | ✅ | Actualizar usuario |
| DELETE | `/auth/users/<id>` | ✅ | Eliminar usuario |

#### POST `/auth/create`
```json
{
  "username": "juanperez",
  "email": "juan@estudiante.com",
  "identification": "1234567890",
  "password": "123456"
}
```
```json
{
  "status": "success",
  "message": "Usuario creado correctamente",
  "data": {
    "id": 1,
    "username": "juanperez",
    "email": "juan@estudiante.com",
    "identification": "1234567890",
    "role": "estudiante"
  }
}
```

#### POST `/auth/login`
```json
{
  "email": "admin@admin.com",
  "password": "123456"
}
```
```json
{
  "status": "success",
  "message": "Login exitoso",
  "data": {
    "access_token": "eyJ...",
    "user": {
      "id": 1,
      "username": "Admin",
      "email": "admin@admin.com",
      "role": "admin"
    }
  }
}
```

#### POST `/auth/forgot-password`
```json
{ "email": "usuario@correo.com" }
```

#### POST `/auth/reset-password`
```json
{
  "token": "token_recibido_por_correo",
  "password": "nueva_contraseña"
}
```

#### PATCH `/auth/users/<id>`
```json
{
  "username": "nuevo_nombre",
  "email": "nuevo@correo.com",
  "password": "nueva_contraseña"
}
```

---

### 👤 Roles — `/role`

> Requiere JWT. Crear rol requiere rol `admin`. Obtener roles requiere `admin` o `medico`.

| Método | Endpoint | Rol requerido | Descripción |
|---|---|---|---|
| POST | `/role/create` | admin | Crear rol |
| GET | `/role/roles` | admin, medico | Obtener todos los roles |
| GET | `/role/users` | admin | Obtener todos los usuarios |

#### POST `/role/create`
```json
{ "name": "farmaceutico" }
```

---

### 🏭 Laboratorios — `/laboratory`

> Todos requieren JWT.

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/laboratory/getAll` | Obtener todos los laboratorios |
| POST | `/laboratory/createLaboratory` | Crear laboratorio |
| PUT | `/laboratory/updateLaboratory/<id>` | Actualizar laboratorio |
| DELETE | `/laboratory/deleteLaboratory/<id>` | Eliminar laboratorio |

#### POST `/laboratory/createLaboratory`
```json
{ "name": "Pfizer" }
```

#### PUT `/laboratory/updateLaboratory/<id>`
```json
{ "name": "Bayer Updated" }
```

---

### 🗂️ Categorías — `/categories`

> Todos requieren JWT.

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/categories/getAll` | Obtener todas las categorías |
| POST | `/categories/createCategory` | Crear categoría |
| PUT | `/categories/updateCategory/<id>` | Actualizar categoría |
| DELETE | `/categories/deleteCategory/<id>` | Eliminar categoría |

#### POST `/categories/createCategory`
```json
{ "name": "Antibióticos" }
```

---

### 💉 Grupos Terapéuticos — `/therapeutic_group`

> Todos requieren JWT.

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/therapeutic_group/getAll` | Obtener todos los grupos |
| POST | `/therapeutic_group/createTherapeuticGroup` | Crear grupo |
| PUT | `/therapeutic_group/updateTherapeuticGroup/<id>` | Actualizar grupo |
| DELETE | `/therapeutic_group/deleteTherapeuticGroup/<id>` | Eliminar grupo |

#### POST `/therapeutic_group/createTherapeuticGroup`
```json
{
  "name": "Antibióticos",
  "mechanism": "Inhibición bacteriana",
  "description": "Medicamentos usados para tratar infecciones bacterianas"
}
```

#### Respuesta
```json
{
  "status": "success",
  "message": "Grupo terapéutico creado correctamente",
  "data": {
    "id": 1,
    "name": "Antibióticos",
    "mechanism": "Inhibición bacteriana",
    "description": "Medicamentos usados para tratar infecciones bacterianas"
  }
}
```

---

### 📦 Productos — `/product`

> Todos requieren JWT.

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/product/getAll` | Obtener todos los productos |
| GET | `/product/get/<id>` | Obtener producto por ID |
| GET | `/product/filter` | Filtrar y paginar productos |
| POST | `/product/createProduct` | Crear producto |
| PUT | `/product/updateProduct/<id>` | Actualizar producto |
| PATCH | `/product/toggleActive/<id>` | Activar / desactivar producto |
| DELETE | `/product/deleteProduct/<id>` | Eliminar producto |

#### POST `/product/createProduct`
```json
{
  "generic_name": "Paracetamol",
  "commercial_name": "Tylenol",
  "concentration": "500 mg",
  "pharmaceutical_form": "Tableta",
  "dosage": "1 tableta cada 8 horas",
  "notes": "Tomar después de comer",
  "is_active": true,
  "image_url": "https://url-de-imagen.com/img.png",
  "therapeutic_group_id": 1,
  "laboratory_id": 1,
  "category_id": 1
}
```

#### GET `/product/filter` — Parámetros de query

| Parámetro | Tipo | Descripción |
|---|---|---|
| `search` | string | Busca por nombre genérico o comercial |
| `category_id` | int | Filtra por categoría |
| `therapeutic_group_id` | int | Filtra por grupo terapéutico |
| `laboratory_id` | int | Filtra por laboratorio |
| `is_active` | bool | Filtra por estado activo/inactivo |
| `page` | int | Página (default: 1) |
| `per_page` | int | Items por página (default: 20) |

Ejemplo: `GET /product/filter?search=paracetamol&page=1&per_page=10`

#### PATCH `/product/toggleActive/<id>`
```json
{ "is_active": false }
```

---

### 📊 Dashboard — `/dashboard`

> Requiere JWT.

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/dashboard/summary` | Obtener resumen estadístico |

#### Respuesta
```json
{
  "success": true,
  "data": {
    "totalUsers": 10,
    "totalProducts": 245,
    "totalLabs": 18,
    "totalGroups": 12,
    "totalCategories": 8,
    "activeProducts": 230,
    "inactiveProducts": 15,
    "chart": {
      "groups": ["Antibióticos", "Analgésicos"],
      "products": [45, 38]
    },
    "categoriesChart": {
      "categories": ["Oftalmología", "Cardiología"],
      "products": [60, 42]
    }
  }
}
```

---

## 📦 Dependencias principales

```
Flask==3.1.3
Flask-CORS==4.0.1
Flask-JWT-Extended==4.6.0
Flask-SQLAlchemy==3.1.1
psycopg2-binary==2.9.11
python-dotenv==1.2.2
SQLAlchemy==2.0.47
Werkzeug==3.1.6
```

---

## 📸 Evidencias

[Evidencias.proyecto.pdf](https://github.com/user-attachments/files/25667088/Evidencias.proyecto.pdf)

---

## 👨‍💻 Autor

**Dillan Ramos Barrera**  
Proyecto — Algoritmos  
Ingeniería Biomédica
