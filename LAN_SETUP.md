# Configuración para Red LAN (Cliente-Servidor)

Esta guía te ayudará a configurar el sistema para que funcione en una red local (LAN), permitiendo que múltiples usuarios se conecten al mismo servidor.

## Configuración del Servidor

### 1. Encontrar tu IP Local

**Windows:**
```bash
ipconfig
```
Busca "Dirección IPv4" (ejemplo: `192.168.1.100`)

**Linux/Mac:**
```bash
ifconfig
# o
ip addr show
```
Busca la IP de tu interfaz de red (ejemplo: `192.168.1.100`)

### 2. Configurar el Backend

El backend ya está configurado para escuchar en todas las interfaces (`0.0.0.0`), así que solo necesitas ejecutarlo:

```bash
cd backend
python run.py
```

El servidor estará disponible en: `http://TU_IP:5000` (ejemplo: `http://192.168.1.100:5000`)

### 3. Configurar el Firewall

**Windows:**
1. Abre "Firewall de Windows Defender"
2. Click en "Configuración avanzada"
3. Click en "Reglas de entrada" → "Nueva regla"
4. Selecciona "Puerto" → Siguiente
5. TCP → Puertos específicos: `5000, 3000` → Siguiente
6. Permitir la conexión → Siguiente
7. Marca todos los perfiles → Siguiente
8. Nombre: "Chat App" → Finalizar

**Linux (ufw):**
```bash
sudo ufw allow 5000/tcp
sudo ufw allow 3000/tcp
```

## Configuración de los Clientes

### Opción 1: Usando Variables de Entorno (Recomendado)

1. **Copia el archivo de ejemplo:**
```bash
cd frontend
cp .env.example .env
```

2. **Edita el archivo `.env` y cambia la IP:**
```env
VITE_API_URL=http://192.168.1.100:5000
VITE_SOCKET_URL=http://192.168.1.100:5000
```
*(Reemplaza `192.168.1.100` con la IP del servidor)*

3. **Reinicia el servidor de desarrollo:**
```bash
npm run dev
```

### Opción 2: Modificar el archivo de configuración directamente

Edita `frontend/src/config.js`:

```javascript
export const API_BASE_URL = 'http://192.168.1.100:5000'
export const SOCKET_URL = 'http://192.168.1.100:5000'
```
*(Reemplaza `192.168.1.100` con la IP del servidor)*

## Pasos para Compartir

### En el Servidor (PC que ejecuta el backend):

1. Encuentra tu IP local (ver arriba)
2. Ejecuta el backend: `python run.py`
3. Comparte tu IP con tus compañeros (ejemplo: `192.168.1.100`)

### En los Clientes (PCs de tus compañeros):

1. Clonan/descargan el proyecto
2. Configuran el frontend con la IP del servidor (ver arriba)
3. Ejecutan solo el frontend: `npm run dev`
4. Acceden a: `http://localhost:3000` en su navegador

**Nota:** Los clientes NO necesitan ejecutar el backend, solo el frontend.

## Verificación

1. **En el servidor:** Abre `http://localhost:3000` (debería funcionar)
2. **En un cliente:** Abre `http://localhost:3000` (debería conectarse al servidor)
3. **Prueba:** Crea una cuenta en el servidor y otra en un cliente, luego intenta chatear

## Solución de Problemas

### "No se puede conectar al servidor"
- Verifica que el servidor esté ejecutándose
- Verifica que la IP sea correcta
- Verifica que el firewall permita las conexiones
- Asegúrate de que todos estén en la misma red

### "CORS Error"
- El backend ya está configurado para permitir CORS desde cualquier origen
- Si persiste, verifica que `Flask-CORS` esté instalado

### "Socket connection error"
- Verifica que la IP en `.env` sea correcta
- Verifica que el puerto 5000 esté abierto en el firewall
- Asegúrate de usar `http://` (no `https://`) en la IP local

## Estructura Cliente-Servidor

```
┌─────────────────┐
│   SERVIDOR      │
│  (Backend +     │
│   Frontend)     │
│  IP: 192.168... │
└────────┬────────┘
         │
         │ Red LAN
         │
    ┌────┴────┬──────────┬──────────┐
    │        │          │          │
┌───▼───┐ ┌──▼───┐  ┌───▼───┐  ┌───▼───┐
│Cliente│ │Cliente│ │Cliente│ │Cliente│
│  1    │ │  2   │ │  3   │ │  N    │
│(Solo  │ │(Solo │ │(Solo │ │(Solo │
│Frontend)│ │Frontend)│ │Frontend)│ │Frontend)│
└───────┘ └──────┘ └──────┘ └──────┘
```

## Notas Importantes

- Todos los usuarios deben estar en la **misma red WiFi/Ethernet**
- El servidor debe estar **siempre encendido** para que los clientes se conecten
- La IP del servidor puede cambiar si se desconecta/reconecta a la red
- Para una IP fija, configura una IP estática en el router o en el sistema operativo

