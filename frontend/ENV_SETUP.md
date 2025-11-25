# Configuración de Variables de Entorno

Para conectar el frontend al servidor en una red LAN, necesitas configurar las variables de entorno.

## Pasos

1. **Crea un archivo `.env` en la carpeta `frontend/`:**

```env
VITE_API_URL=http://192.168.1.100:5000
VITE_SOCKET_URL=http://192.168.1.100:5000
```

2. **Reemplaza `192.168.1.100` con la IP del servidor**

   - En Windows: Ejecuta `ipconfig` y busca "Dirección IPv4"
   - En Linux/Mac: Ejecuta `ifconfig` o `ip addr show`

3. **Reinicia el servidor de desarrollo:**

```bash
npm run dev
```

## Notas

- El archivo `.env` debe estar en la carpeta `frontend/`
- Si cambias la IP, reinicia el servidor de desarrollo
- Para desarrollo local, puedes usar `http://localhost:5000`
- Para LAN, usa la IP del servidor (ejemplo: `http://192.168.1.100:5000`)

