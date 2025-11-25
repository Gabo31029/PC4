# Guía de Configuración Rápida

## Para nuevos miembros del equipo

### 1. Clonar/Descargar el proyecto

Si usas Git:
```bash
git clone [URL_DEL_REPOSITORIO]
cd Chat-PC4
```

Si recibiste un ZIP:
- Descomprime el archivo
- Abre la carpeta en tu editor

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

1. Asegúrate de tener MySQL instalado y corriendo
2. Crea la base de datos:
```sql
CREATE DATABASE chat_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. Crea el archivo `.env` en la carpeta `backend/`:
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu-secret-key-cambiar-en-produccion
JWT_SECRET_KEY=tu-jwt-secret-key-cambiar-en-produccion
DATABASE_URL=mysql+pymysql://root:tu_password@localhost/chat_db
UPLOAD_FOLDER=uploads
MAX_UPLOAD_SIZE=10485760
```

**⚠️ IMPORTANTE:** Cambia `root` y `tu_password` por tus credenciales de MySQL.

### 4. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install
```

### 5. Ejecutar el proyecto

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Si no está activado
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 6. Acceder a la aplicación

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### Solución de Problemas Comunes

**Error: "ModuleNotFoundError"**
- Asegúrate de tener el entorno virtual activado
- Ejecuta `pip install -r requirements.txt` nuevamente

**Error de conexión a MySQL**
- Verifica que MySQL esté corriendo
- Revisa las credenciales en el archivo `.env`
- Asegúrate de que la base de datos exista

**Error en el frontend**
- Ejecuta `npm install` nuevamente
- Borra `node_modules` y vuelve a instalar si es necesario

**Puerto ya en uso**
- Cambia el puerto en `run.py` (backend) o `vite.config.js` (frontend)
- O cierra la aplicación que está usando ese puerto
