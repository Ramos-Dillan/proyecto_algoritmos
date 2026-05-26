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
- ✅ **Asistente IA Oftalmológico** integrado al vademécum

**Base de datos:** PostgreSQL  
**Nombre DB:** `vademecumDB`  
**Puerto por defecto:** `http://localhost:5000`

---

## 🗂️ Estructura del Proyecto — Backend

```
proyecto_algoritmos/
├── common/
│   └── http.py                  # Helpers de respuesta HTTP
├── db/
│   ├── db.py                    # Conexión SQLAlchemy
│   └── models.py                # Modelos ORM
├── routes/
│   ├── assistant/               # Asistente IA oftalmológico
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

### 🤖 Asistente IA Oftalmológico — `/assistant`

> Requiere JWT. Powered by **Google Gemini**.

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/assistant/chat` | Enviar consulta al asistente IA |

#### ¿Qué puede hacer el asistente?

El asistente clínico oftalmológico responde tres tipos de consultas, usando exclusivamente los medicamentos registrados en el vademécum de la plataforma:

| Tipo de consulta | Ejemplo | Respuesta |
|---|---|---|
| **Por síntomas** | "Tengo ojo rojo y secreción amarilla" | Posible diagnóstico + medicamentos del vademécum con dosis |
| **Por medicamento** | "¿Para qué sirve la Ofloxacina?" | Descripción, usos, dosis y notas del medicamento |
| **Por diagnóstico** | "¿Qué se usa para conjuntivitis bacteriana?" | Lista de medicamentos disponibles con dosificación |

> ⚠️ El asistente siempre incluye el aviso: *"Esto es orientativo, consulta con tu oftalmólogo"*. No inventa medicamentos — solo recomienda los que existen en la base de datos.

#### POST `/assistant/chat`

**Request:**
```json
{
  "message": "Tengo ojo rojo y secreción amarilla, ¿qué medicamento uso?"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "response": "Basado en tus síntomas, podría tratarse de una conjuntivitis bacteriana. Los medicamentos disponibles en el vademécum son:\n\n- Oflox (Ofloxacina 0.3%): 1 gota cada 6 horas por 7 días.\n- Ophthabracin (Tobramicina 0.3%): 1 gota cada 6 horas por 7 días.\n\nEsto es orientativo, consulta con tu oftalmólogo.",
    "user_message": "Tengo ojo rojo y secreción amarilla, ¿qué medicamento uso?"
  }
}
```

#### Configuración del asistente

El asistente requiere una API key de Google Gemini. Agrégala al `.env`:

```env
GEMINI_API_KEY=AIzaSy_tu_api_key_aqui
```

Para obtener una key gratuita: [aistudio.google.com](https://aistudio.google.com)

Instalar la librería de Gemini:

```bash
pip install google-genai
```

El modelo utilizado es `gemini-2.5-flash`, con un límite de 250 requests/día en el free tier.

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
google-genai                # Asistente IA con Google Gemini
```

---

---

# 🖥️ Frontend — Vademécum CES

Interfaz web desarrollada en **Angular 21** para consumir la API REST del vademécum institucional. Permite autenticación, navegación por roles, gestión de productos, laboratorios, categorías, grupos terapéuticos, usuarios y visualización del dashboard.

**Framework:** Angular 21  
**Puerto por defecto:** `http://localhost:4200`  
**API base:** `http://localhost:5000`

---

## 🎨 Descripción de la Interfaz

La aplicación cuenta con un diseño oscuro moderno, orientado a entornos clínicos y académicos. Todas las vistas siguen una paleta de colores consistente basada en tonos azules y grises oscuros, con acentos en cyan y gradientes tipo neón que refuerzan la identidad visual del sistema.

### 🔐 Pantalla de Login

Pantalla de acceso dividida en dos secciones: el lado izquierdo presenta la identidad de la plataforma con el logo de **Universidad CES** y un botón de registro; el lado derecho contiene el formulario de inicio de sesión con campos de email y contraseña, un enlace de recuperación de contraseña, el botón principal de **Login** y accesos rápidos mediante íconos de Google, Facebook, GitHub y LinkedIn. El fondo usa una imagen ambiental de laboratorio con cápsulas flotantes que refuerza la temática farmacéutica.

### 🏠 Vista Home (Panel principal)

Página de bienvenida tras el login, organizada en tarjetas informativas. Muestra la arquitectura del sistema con los módulos disponibles (Productos, Laboratorios, Categorías, Grupos Terapéuticos, Usuarios & Roles), una descripción de las capacidades de la plataforma y botones de acceso rápido a **Explorar productos** y **Ver dashboard**. En la parte inferior se presentan tarjetas destacando los cuatro pilares del sistema: Gestión de Productos, Control de Usuarios, Dashboard Inteligente, Seguridad y Trazabilidad, y el nuevo **Asistente IA Oftalmológico**.

### 🤖 Asistente IA (Chat flotante)

Botón flotante permanente en la esquina inferior derecha de la interfaz, visible en todas las vistas protegidas. Al hacer clic, abre un panel de chat con diseño oscuro integrado al estilo de la plataforma. El asistente responde consultas sobre síntomas oculares, medicamentos específicos y diagnósticos, usando únicamente los productos registrados en el vademécum. La tarjeta de inicio también actúa como acceso directo al chat.

### 📊 Vista Dashboard

Panel de estadísticas en tiempo real compuesto por:
- **Tarjetas de resumen** en la parte superior con conteo de Usuarios, Productos, Grupos terapéuticos y Productos activos.
- **Gráfica de actividad del sistema** (línea) que muestra la distribución entre Usuarios, Productos, Labs y Grupos.
- **Gráfica de estado de productos** (dona) que diferencia entre productos activos e inactivos.
- **Gráfica de productos por categorías** (barras) con el desglose por cada categoría registrada.

### 🧭 Navegación y Layout

La aplicación usa dos layouts diferenciados:
- **`auth-shell`**: layout minimalista para rutas públicas (login, registro, recuperación de contraseña), sin barra lateral ni encabezado de sesión.
- **`shell`**: layout principal para rutas protegidas, con barra lateral izquierda de navegación (Home, Productos, Usuarios, Dashboard) y barra superior con el nombre y rol del usuario autenticado. El sidebar es colapsable mediante un botón de menú.

---

## 🗂️ Estructura del Proyecto — Frontend

```
fronted-test/src/app/
├── app.config.ts                    # Configuración principal de la app
├── app.html                         # Shell HTML raíz (incluye chat flotante IA)
├── app.routes.ts                    # Definición de rutas
├── app.scss                         # Estilos globales (incluye estilos del chat)
├── app.spec.ts                      # Pruebas del componente raíz
├── app.ts                           # Componente raíz (lógica del asistente IA)
│
├── features/
│   ├── categories/                  # Gestión de categorías
│   │   ├── categories.html
│   │   ├── categories.scss
│   │   └── categories.ts
│   │
│   ├── dashboard/                   # Dashboard con estadísticas
│   │   ├── dashboard.html
│   │   ├── dashboard.scss
│   │   └── dashboard.ts
│   │
│   ├── forgot-password/             # Solicitud de reset de contraseña
│   │   ├── forgot-password.html
│   │   ├── forgot-password.scss
│   │   └── forgot-password.ts
│   │
│   ├── guards/                      # Guards de rutas
│   │   ├── auth.guards.ts           # Verifica sesión activa (JWT)
│   │   └── role.guard.ts            # Verifica rol del usuario
│   │
│   ├── home/                        # Página de inicio
│   │   ├── home.html
│   │   ├── home.scss
│   │   └── home.ts
│   │
│   ├── layout/
│   │   ├── auth-shell/              # Layout para rutas públicas (login, register)
│   │   │   ├── auth-shell.html
│   │   │   ├── auth-shell.scss
│   │   │   └── auth-shell.ts
│   │   └── shell/                   # Layout para rutas protegidas (sidebar, navbar)
│   │       ├── shell.html
│   │       ├── shell.scss
│   │       └── shell.ts
│   │
│   ├── login/                       # Inicio de sesión
│   │   ├── login.html
│   │   ├── login.scss
│   │   └── login.ts
│   │
│   ├── products/                    # Listado y detalle de productos
│   │   ├── product-detail.html
│   │   ├── product-detail.scss
│   │   ├── product-detail.ts
│   │   ├── products.html
│   │   ├── products.scss
│   │   └── products.ts
│   │
│   ├── register/                    # Registro de nuevos usuarios
│   │   ├── register.html
│   │   ├── register.scss
│   │   └── register.ts
│   │
│   ├── reset-password/              # Restablecimiento de contraseña
│   │   ├── reset-password.html
│   │   ├── reset-password.scss
│   │   └── reset-password.ts
│   │
│   ├── roles/                       # Gestión de roles
│   │   ├── roles.html
│   │   ├── roles.scss
│   │   └── roles.ts
│   │
│   ├── therapeutic-groups/          # Gestión de grupos terapéuticos
│   │   ├── therapeutic-groups.html
│   │   ├── therapeutic-groups.scss
│   │   └── therapeutic-groups.ts
│   │
│   └── users/                       # Gestión de usuarios
│       ├── users.html
│       ├── users.scss
│       └── users.ts
│
├── interceptors/
│   └── auth.interceptor.ts          # Adjunta JWT a cada petición HTTP
│
└── service/
    ├── loginservice/
    │   └── login_service.ts         # Autenticación y manejo de sesión
    ├── productService/
    │   └── productService.ts        # CRUD de productos y filtros
    └── userService/
        └── userService.ts           # CRUD de usuarios
```

---

## 🔐 Guards de Rutas

| Guard | Archivo | Descripción |
|---|---|---|
| `AuthGuard` | `auth.guards.ts` | Redirige al login si no hay sesión activa |
| `RoleGuard` | `role.guard.ts` | Restringe acceso a rutas según el rol del usuario |

Las rutas protegidas verifican el JWT almacenado localmente. Si el token es inválido o expiró, el usuario es redirigido automáticamente al login.

---

## 🌐 Interceptor HTTP

`auth.interceptor.ts` intercepta todas las peticiones salientes y adjunta automáticamente el token JWT en el header:

```
Authorization: Bearer <access_token>
```

Esto evita tener que configurar el header manualmente en cada servicio.

---

## 🛠️ Servicios

| Servicio | Archivo | Responsabilidad |
|---|---|---|
| `LoginService` | `login_service.ts` | Login, logout, almacenamiento y lectura del token y datos del usuario |
| `ProductService` | `productService.ts` | Obtener, crear, actualizar, eliminar y filtrar productos |
| `UserService` | `userService.ts` | Obtener, actualizar y eliminar usuarios |

---

## 🗺️ Vistas y Rutas

| Vista | Ruta | Acceso | Descripción |
|---|---|---|---|
| Login | `/login` | Público | Inicio de sesión |
| Register | `/register` | Público | Registro de nuevo usuario |
| Forgot Password | `/forgot-password` | Público | Solicitar reset por correo |
| Reset Password | `/reset-password` | Público | Restablecer contraseña con token |
| Home | `/home` | Autenticado | Página principal con acceso directo al asistente IA |
| Dashboard | `/dashboard` | Autenticado | Estadísticas y gráficas |
| Products | `/products` | Autenticado | Listado de medicamentos con filtros |
| Product Detail | `/products/:id` | Autenticado | Detalle de un medicamento |
| Categories | `/categories` | Autenticado | Gestión de categorías |
| Therapeutic Groups | `/therapeutic-groups` | Autenticado | Gestión de grupos terapéuticos |
| Roles | `/roles` | admin | Gestión de roles |
| Users | `/users` | admin | Gestión de usuarios |

---

## ⚙️ Instalación y Ejecución — Frontend

### 1️⃣ Acceder al directorio del frontend

```bash
cd fronted-test
```

### 2️⃣ Instalar dependencias

```bash
npm install
```

### 3️⃣ Configurar la URL de la API

En `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiBaseURL: 'http://localhost:5000'
};
```

### 4️⃣ Ejecutar el servidor de desarrollo

```bash
npm start
# o
ng serve
```

Aplicación disponible en: `http://localhost:4200`

### 5️⃣ Build de producción

```bash
npm run build
```

Los archivos compilados quedan en `dist/`.

---

## 📦 Dependencias principales — Frontend

```
@angular/core             ^21.2.0    Framework principal
@angular/router           ^21.2.0    Navegación y rutas
@angular/forms            ^21.2.0    Formularios reactivos y de plantilla
@angular/common           ^21.2.0    HTTP client y utilidades
chart.js                  ^4.5.1     Librería de gráficas
ng2-charts                ^10.0.0    Wrapper Angular para Chart.js
@fortawesome/fontawesome-free  ^7.2.0    Íconos
rxjs                      ~7.8.0     Programación reactiva
```

**Herramientas de desarrollo:**
```
@angular/cli              ^21.2.9
typescript                ~5.9.2
prettier                  ^3.8.1
vitest                    ^4.0.8
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
