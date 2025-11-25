# Solución de Problemas - "Registration failed"

## Problema: "Registration failed" desde cliente en otra PC

### Verificaciones Rápidas

1. **¿El servidor está corriendo?**
   - En el servidor, verifica que veas: `Running on http://0.0.0.0:5000`
   - Si no, ejecuta: `cd backend && python run.py`

2. **¿La IP es correcta?**
   - En el servidor, ejecuta `ipconfig` (Windows) o `ifconfig` (Linux/Mac)
   - Verifica que el cliente tenga la IP correcta en su archivo `.env`

3. **¿Pueden conectarse?**
   - Desde el cliente, abre el navegador y ve a: `http://IP_DEL_SERVIDOR:5000/api/register`
   - Deberías ver un error JSON (eso significa que la conexión funciona)

### Soluciones Comunes

#### 1. Error de Conexión (Network Error)

**Síntoma:** En la consola del navegador (F12) ves "Network Error" o "ECONNREFUSED"

**Solución:**
- Verifica que el firewall permita conexiones en el puerto 5000
- Verifica que la IP en `.env` sea correcta
- Asegúrate de que todos estén en la misma red

#### 2. Error CORS

**Síntoma:** En la consola ves "CORS policy" o "Access-Control-Allow-Origin"

**Solución:**
- El backend ya está configurado para permitir CORS desde cualquier origen
- Si persiste, reinicia el servidor backend

#### 3. Error de Base de Datos

**Síntoma:** En el servidor ves errores de MySQL

**Solución:**
- Verifica que MySQL esté corriendo
- Verifica las credenciales en `backend/.env`
- Verifica que la base de datos exista

#### 4. Error de Validación

**Síntoma:** El mensaje dice "Username already exists" o "Email already exists"

**Solución:**
- Usa un username/email diferente
- O elimina el usuario existente de la base de datos

### Debugging Paso a Paso

1. **Abre la consola del navegador (F12) en el cliente**
   - Ve a la pestaña "Console"
   - Intenta registrar de nuevo
   - Copia cualquier error que aparezca

2. **Revisa la pestaña "Network"**
   - Filtra por "register"
   - Click en la petición
   - Revisa:
     - Status code (debería ser 201 o 400/500)
     - Response (el mensaje de error del servidor)
     - Request URL (debería ser `http://IP:5000/api/register`)

3. **Revisa los logs del servidor**
   - En la terminal donde corre el backend
   - Deberías ver las peticiones entrantes
   - Si hay errores, aparecerán ahí

### Verificación de Configuración

**En el cliente, verifica `frontend/.env`:**
```env
VITE_API_URL=http://192.168.1.100:5000
VITE_SOCKET_URL=http://192.168.1.100:5000
```
*(Reemplaza con la IP real del servidor)*

**En el servidor, verifica `backend/.env`:**
```env
DATABASE_URL=mysql+pymysql://usuario:password@localhost/chat_db
```
*(Verifica que las credenciales sean correctas)*

### Comandos de Prueba

**Desde el cliente (en PowerShell/CMD):**
```bash
# Prueba si puedes alcanzar el servidor
curl http://IP_DEL_SERVIDOR:5000/api/register
```

**Desde el servidor:**
```bash
# Verifica que el servidor esté escuchando
netstat -an | findstr :5000
```

### Si Nada Funciona

1. Verifica que ambos estén en la misma red WiFi/Ethernet
2. Prueba hacer ping desde el cliente al servidor:
   ```bash
   ping IP_DEL_SERVIDOR
   ```
3. Verifica que no haya un antivirus bloqueando las conexiones
4. Intenta desactivar temporalmente el firewall para probar

