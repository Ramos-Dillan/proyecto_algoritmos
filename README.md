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
- ✅ **Asistente IA Oftalmológico** integrado al vademécum (Google Gemini)

**Base de datos:** PostgreSQL  
**Nombre DB:** `vademecumDB`  
**Puerto por defecto:** `http://localhost:5000`

---

## 🗂️ Estructura del Proyecto — Backend

```
proyecto_algoritmos/
├── common/
│   └── http.py                          # Helpers de respuesta HTTP
├── db/
│   ├── db.py                            # Conexión SQLAlchemy
│   └── models.py                        # Modelos ORM
├── routes/
│   ├── assistant/                       # Asistente IA oftalmológico
│   │   ├── assistant_routes.py          # Blueprint y rutas del asistente
│   │   ├── assistant_controller.py      # Controlador (valida input)
│   │   ├── assistant_service.py         # Lógica: consulta BD + llama a Gemini
│   │   └── __init__.py
│   ├── auth/                            # Autenticación y usuarios
│   ├── categories/                      # Categorías
│   ├── dashboard/                       # Dashboard y estadísticas
│   ├── laboratories/                    # Laboratorios
│   ├── products/                        # Productos
│   ├── roles/                           # Roles
│   └── therapeutic_groups/              # Grupos terapéuticos
├── security/
│   └── roles.py                         # Decorador role_required
├── app.py                               # Entry point Flask
├── config.py                            # Configuración (claves, JWT, Gemini)
├── db_init.py                           # Inicialización de tablas
├── .env                                 # Variables de entorno
├── .gitignore
├── requirements.txt
└── README.md
```

### 🤖 Detalle del módulo `assistant`

El asistente NO usa un repositorio separado — la consulta a la base de datos está fusionada directamente en `assistant_service.py`:

| Archivo | Responsabilidad |
|---|---|
| `assistant_routes.py` | Define el endpoint `POST /assistant/chat`, protegido con JWT |
| `assistant_controller.py` | Valida que el mensaje no esté vacío y delega al service |
| `assistant_service.py` | Consulta el vademécum completo desde PostgreSQL y genera la respuesta con Gemini 2.5 Flash |

**Flujo:**
```
POST /assistant/chat
  → assistant_controller.py  (valida input)
  → assistant_service.py     (consulta BD completa + construye prompt)
  → Google Gemini API        (genera respuesta clínica)
  → retorna JSON al cliente
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
Laboratory       (1) ──── (N) Product
TherapeuticGroup (1) ──── (N) Product
Category         (1) ──── (N) Product
Role             (1) ──── (N) User
```

---

## ⚙️ Instalación y Ejecución — Backend

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

# Asistente IA (Gemini)
GEMINI_API_KEY=tu_api_key_de_gemini

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

### 👤 Roles — `/role`

| Método | Endpoint | Rol requerido | Descripción |
|---|---|---|---|
| POST | `/role/create` | admin | Crear rol |
| GET | `/role/roles` | admin, medico | Obtener todos los roles |
| GET | `/role/users` | admin | Obtener todos los usuarios |

### 🏭 Laboratorios — `/laboratory`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/laboratory/getAll` | Obtener todos los laboratorios |
| POST | `/laboratory/createLaboratory` | Crear laboratorio |
| PUT | `/laboratory/updateLaboratory/<id>` | Actualizar laboratorio |
| DELETE | `/laboratory/deleteLaboratory/<id>` | Eliminar laboratorio |

### 🗂️ Categorías — `/categories`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/categories/getAll` | Obtener todas las categorías |
| POST | `/categories/createCategory` | Crear categoría |
| PUT | `/categories/updateCategory/<id>` | Actualizar categoría |
| DELETE | `/categories/deleteCategory/<id>` | Eliminar categoría |

### 💉 Grupos Terapéuticos — `/therapeutic_group`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/therapeutic_group/getAll` | Obtener todos los grupos |
| POST | `/therapeutic_group/createTherapeuticGroup` | Crear grupo |
| PUT | `/therapeutic_group/updateTherapeuticGroup/<id>` | Actualizar grupo |
| DELETE | `/therapeutic_group/deleteTherapeuticGroup/<id>` | Eliminar grupo |

### 📦 Productos — `/product`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/product/getAll` | Obtener todos los productos |
| GET | `/product/get/<id>` | Obtener producto por ID |
| GET | `/product/filter` | Filtrar y paginar productos |
| POST | `/product/createProduct` | Crear producto |
| PUT | `/product/updateProduct/<id>` | Actualizar producto |
| PATCH | `/product/toggleActive/<id>` | Activar / desactivar producto |
| DELETE | `/product/deleteProduct/<id>` | Eliminar producto |

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

### 🤖 Asistente IA Oftalmológico — `/assistant`

> Requiere JWT. Powered by **Google Gemini 2.5 Flash**.

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/assistant/chat` | Enviar consulta al asistente IA |

#### ¿Qué puede hacer el asistente?

| Tipo de consulta | Ejemplo | Respuesta |
|---|---|---|
| **Por síntomas** | "Tengo ojo rojo y secreción amarilla" | Posible diagnóstico + medicamentos del vademécum con dosis |
| **Por medicamento** | "¿Para qué sirve la Ofloxacina?" | Descripción, usos, dosis y notas |
| **Por diagnóstico** | "¿Qué se usa para conjuntivitis bacteriana?" | Lista de medicamentos disponibles |
| **Por grupo terapéutico** | "¿Qué inhibidores de membrana hay?" | Medicamentos del grupo con dosis |

> ⚠️ El asistente siempre incluye el aviso: *"Esto es orientativo, consulta con tu oftalmólogo"*. Solo recomienda medicamentos existentes en la base de datos.

#### POST `/assistant/chat`

**Request:**
```json
{ "message": "Tengo ojo rojo y secreción amarilla, ¿qué medicamento uso?" }
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "response": "Basado en tus síntomas, podría tratarse de una conjuntivitis bacteriana...\n\n⚠️ Esto es orientativo, consulta con tu oftalmólogo",
    "user_message": "Tengo ojo rojo y secreción amarilla, ¿qué medicamento uso?"
  }
}
```

#### Configuración

```env
GEMINI_API_KEY=AIzaSy_tu_api_key_aqui
```

```bash
pip install google-genai
```

### 📊 Dashboard — `/dashboard`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/dashboard/summary` | Obtener resumen estadístico |

---

## 📦 Dependencias principales — Backend

```
Flask==3.1.3
Flask-CORS==4.0.1
Flask-JWT-Extended==4.6.0
Flask-SQLAlchemy==3.1.1
psycopg2-binary==2.9.11
python-dotenv==1.2.2
SQLAlchemy==2.0.47
Werkzeug==3.1.6
google-genai
```

---

---

# 🖥️ Frontend — Vademécum CES

Interfaz web desarrollada en **Angular 21** para consumir la API REST del vademécum institucional.

**Framework:** Angular 21  
**Puerto por defecto:** `http://localhost:4200`  
**API base:** `http://localhost:5000`

---

## 🗂️ Estructura del Proyecto — Frontend

```
fronted-test/src/app/
├── app.config.ts                          # Configuración principal de la app
├── app.html                               # Shell raíz (solo <router-outlet> + <app-assistant>)
├── app.routes.ts                          # Definición de rutas con guards
├── app.scss                               # Estilos globales
├── app.ts                                 # Componente raíz (importa AssistantComponent)
│
├── features/
│   ├── assistant/                         # 🤖 Asistente IA (componente standalone)
│   │   ├── assistant.html                 # Chat flotante (burbuja + ventana)
│   │   ├── assistant.scss                 # Estilos del chat
│   │   └── assistant.ts                   # Lógica del chat (usa AssistantService)
│   │
│   ├── categories/
│   ├── dashboard/
│   ├── forgot-password/
│   ├── guards/
│   │   ├── auth.guards.ts                 # Verifica sesión activa (JWT)
│   │   └── role.guard.ts                  # Verifica rol del usuario
│   ├── home/
│   ├── layout/
│   │   ├── auth-shell/                    # Layout rutas públicas
│   │   └── shell/                         # Layout rutas protegidas (sidebar + navbar)
│   ├── login/
│   ├── products/
│   ├── register/
│   ├── reset-password/
│   ├── roles/
│   ├── therapeutic-groups/
│   └── users/
│
├── interceptors/
│   └── auth.interceptor.ts                # Adjunta JWT automáticamente a cada petición
│
└── service/
    ├── AssistantService/
    │   └── assistant.service.ts           # Llama a POST /assistant/chat con JWT
    ├── loginservice/
    │   └── login_service.ts               # Autenticación y manejo de sesión
    ├── productService/
    │   └── productService.ts              # CRUD de productos y filtros
    └── userService/
        └── userService.ts                 # CRUD de usuarios
```

### 🤖 Detalle del módulo `assistant` (Frontend)

El asistente es un **componente standalone** que se renderiza globalmente desde `app.html` y es visible en todas las rutas protegidas.

| Archivo | Responsabilidad |
|---|---|
| `assistant.html` | Burbuja flotante + ventana de chat con historial de mensajes |
| `assistant.scss` | Estilos del chat (diseño oscuro, gradientes, scroll) |
| `assistant.ts` | Controla apertura/cierre, envío de mensajes, scroll automático |
| `assistant.service.ts` | HTTP service — llama al backend con el token JWT |

**Flujo del chat:**
```
Usuario escribe mensaje
  → AssistantComponent.sendMessage()
  → AssistantService.sendMessage(text, token)
  → POST http://localhost:5000/assistant/chat
  → Respuesta de Gemini mostrada en el chat
```

El asistente se **oculta automáticamente** en rutas públicas (`/login`, `/register`, `/forgot-password`, `/reset-password`).

---

## 🔐 Guards de Rutas

| Guard | Archivo | Descripción |
|---|---|---|
| `AuthGuard` | `auth.guards.ts` | Redirige al login si no hay sesión activa |
| `RoleGuard` | `role.guard.ts` | Restringe acceso según el rol del usuario |

---

## 🗺️ Vistas y Rutas

| Vista | Ruta | Acceso | Descripción |
|---|---|---|---|
| Login / Register | `/auth` | Público | Auth shell con login y registro |
| Forgot Password | `/forgot-password` | Público | Solicitar reset por correo |
| Reset Password | `/reset-password` | Público | Restablecer contraseña con token |
| Home | `/home` | Autenticado | Panel principal con acceso al asistente IA |
| Dashboard | `/dashboard` | Autenticado | Estadísticas y gráficas |
| Products | `/products` | Autenticado | Listado de medicamentos con filtros |
| Product Detail | `/products/:id` | Autenticado | Detalle de un medicamento |
| Categories | `/categories` | Autenticado | Gestión de categorías |
| Therapeutic Groups | `/therapeutic-groups` | Autenticado | Gestión de grupos terapéuticos |
| Roles | `/roles` | admin | Gestión de roles |
| Users | `/users` | admin | Gestión de usuarios |

---

## ⚙️ Instalación y Ejecución — Frontend

```bash
cd fronted-test
npm install
npm start
```

Aplicación disponible en: `http://localhost:4200`

### Configurar URL de la API

En `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiBaseURL: 'http://localhost:5000'
};
```

---

## 📦 Dependencias principales — Frontend

```
@angular/core             ^21.2.0
@angular/router           ^21.2.0
@angular/forms            ^21.2.0
@angular/common           ^21.2.0
chart.js                  ^4.5.1
ng2-charts                ^10.0.0
@fortawesome/fontawesome-free  ^7.2.0
rxjs                      ~7.8.0
```

---

## 📸 Evidencias

[Evidencias.proyecto.pdf](https://github.com/user-attachments/files/25667088/Evidencias.proyecto.pdf)

---

## 👨‍💻 Autores

**Dillan Ramos Barrera**  
**Santiago Ramirez**  
**Samith Ramos**  
Proyecto — Algoritmos  
Ingeniería Biomédica