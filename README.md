# Sistema de Chat Completo

Sistema de chat en tiempo real con videollamadas, similar a Discord, desarrollado con Flask (backend) y Vue 3 + Vite (frontend).

## Características

- ✅ Chat persistente (mensajes guardados en MySQL)
- ✅ Chats directos y grupos
- ✅ Videollamadas con WebRTC
- ✅ Compartir pantalla
- ✅ Control de audio/video (mute, encender/apagar cámara)
- ✅ Envío de archivos y audios
- ✅ Ver usuarios conectados
- ✅ Autenticación con JWT
- ✅ WebSockets para comunicación en tiempo real

## Requisitos

- Python 3.8+
- Node.js 16+
- MySQL 5.7+

## Instalación

### Backend

1. Navega a la carpeta `backend`:
```bash
cd backend
```

2. Crea un entorno virtual:
```bash
python -m venv venv
```

3. Activa el entorno virtual:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

5. Crea un archivo `.env` basado en `.env.example`:
```bash
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu-secret-key-aqui
JWT_SECRET_KEY=tu-jwt-secret-key-aqui
DATABASE_URL=mysql+pymysql://usuario:password@localhost/nombre_db
UPLOAD_FOLDER=uploads
MAX_UPLOAD_SIZE=10485760
```

6. Crea la base de datos en MySQL:
```sql
CREATE DATABASE nombre_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

7. Ejecuta el servidor:
```bash
python run.py
```

El backend estará disponible en `http://localhost:5000`

### Frontend

1. Navega a la carpeta `frontend`:
```bash
cd frontend
```

2. Instala las dependencias:
```bash
npm install
```

3. Ejecuta el servidor de desarrollo:
```bash
npm run dev
```

El frontend estará disponible en `http://localhost:3000`

## Uso

1. **Registro/Login**: Crea una cuenta o inicia sesión
2. **Crear Chat**: Haz clic en "+ Nuevo" para crear un chat directo o grupo
3. **Enviar Mensajes**: Escribe mensajes, envía archivos o graba audios
4. **Videollamadas**: Haz clic en el botón de llamada en el header del chat
5. **Controles de Llamada**: 
   - 🔊/🔇: Activar/desactivar audio
   - 📹/📵: Activar/desactivar video
   - 🖥️: Compartir pantalla
   - 📞: Finalizar llamada

## Estructura del Proyecto

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── websocket_handlers.py
│   │   └── utils.py
│   ├── uploads/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── stores/
│   │   ├── services/
│   │   ├── views/
│   │   └── router/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Tecnologías Utilizadas

### Backend
- Flask
- Flask-SocketIO
- Flask-JWT-Extended
- SQLAlchemy
- PyMySQL
- bcrypt

### Frontend
- Vue 3
- Vite
- Pinia
- Vue Router
- Socket.IO Client
- Axios

## Notas

- Los archivos se almacenan localmente en la carpeta `backend/uploads/`
- Las videollamadas usan servidores STUN públicos de Google
- El sistema está diseñado para desarrollo/educación, no para producción sin mejoras de seguridad adicionales

## Configuración para Red LAN (Cliente-Servidor)

Para que múltiples usuarios se conecten en la misma red local, consulta el archivo **[LAN_SETUP.md](LAN_SETUP.md)** con instrucciones detalladas.

**Resumen rápido:**
1. Servidor: Encuentra tu IP local (`ipconfig` en Windows) y ejecuta el backend
2. Clientes: Configuran el frontend con la IP del servidor en `.env`
3. Todos acceden a `http://localhost:3000` en sus navegadores

## Compartir el Proyecto

### Opción 1: Usar Git (Recomendado)

1. **Inicializar repositorio Git:**
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Crear un repositorio en GitHub/GitLab:**
   - Ve a GitHub.com o GitLab.com
   - Crea un nuevo repositorio
   - No inicialices con README (ya tenemos uno)

3. **Conectar y subir:**
```bash
git remote add origin https://github.com/tu-usuario/tu-repo.git
git branch -M main
git push -u origin main
```

4. **Para que tus compañeros lo clonen:**
```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

### Opción 2: Compartir por archivo comprimido

1. **Comprimir el proyecto** (excluyendo venv, node_modules, etc.):
   - En Windows: Selecciona las carpetas `backend` y `frontend` y el archivo `README.md`
   - Comprime en ZIP
   - **NO incluyas**: `venv/`, `node_modules/`, `.env`, `uploads/`

2. **Compartir el ZIP** por:
   - Google Drive
   - OneDrive
   - WeTransfer
   - Email (si el archivo no es muy grande)

### Configuración inicial para nuevos usuarios

Después de clonar/descomprimir, cada compañero debe:

1. **Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# o: source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

2. **Crear archivo `.env` en `backend/`:**
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu-secret-key-aqui
JWT_SECRET_KEY=tu-jwt-secret-key-aqui
DATABASE_URL=mysql+pymysql://usuario:password@localhost/nombre_db
UPLOAD_FOLDER=uploads
MAX_UPLOAD_SIZE=10485760
```

3. **Crear la base de datos en MySQL:**
```sql
CREATE DATABASE nombre_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. **Frontend:**
```bash
cd frontend
npm install
```

5. **Ejecutar:**
   - Backend: `python run.py` (en carpeta backend)
   - Frontend: `npm run dev` (en carpeta frontend)

