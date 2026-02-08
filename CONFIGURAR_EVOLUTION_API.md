# 🚀 Configurar Evolution API en Calibre-Web
## Guía Rápida (Ya tienes Evolution API instalado)

Esta guía es para cuando **ya tienes un servidor Evolution API corriendo**.

---

## 📋 Paso 1: Preparar Evolution API

### 1.1. Accede al Manager de Evolution API
Abre tu navegador: `http://tu-servidor:8080/manager`

### 1.2. Obtén tu API Key
La API Key es la que configuraste en tu servidor Evolution API. La puedes encontrar:
- En las variables de entorno: `AUTHENTICATION_API_KEY`
- O en el archivo de configuración de Evolution API

**Ejemplo**: `mi_clave_secreta_123`

### 1.3. Crea o identifica tu instancia

**Opción A: Crear nueva instancia**
1. En el manager, clic en "Crear instancia"
2. Nombre sugerido: `calibre-web`
3. Escanea el código QR con tu WhatsApp
4. ¡Tu WhatsApp está conectado!

**Opción B: Usar instancia existente**
Si ya tienes una instancia conectada, puedes usarla.
Solo necesitas el nombre de la instancia.

---

## 🔧 Paso 2: Configurar Calibre-Web

### 🚀 MÉTODO RECOMENDADO: Script Automático

El método más fácil y seguro es usar el script de configuración:

```bash
cd /ruta/a/calibre-web
python configure_evolution_api.py
```

**El script:**
- ✅ Busca automáticamente la base de datos
- ✅ Te pide los datos (URL, API Key, Instancia)
- ✅ Verifica la configuración actual
- ✅ Actualiza la base de datos
- ✅ Muestra los próximos pasos

**Ejemplo de uso**:
```
🔧 Configuración de Evolution API para Calibre-Web

📂 Base de datos encontrada: /path/to/app.db
✅ Base de datos verificada

📝 Introduce los datos de tu servidor Evolution API:

   URL del servidor: http://192.168.1.100:8080
   API Key: abc123xyz789
   Nombre de instancia [calibre-web]: mi-calibre

Resumen:
  URL:        http://192.168.1.100:8080
  API Key:    ********x789
  Instancia:  mi-calibre

¿Guardar? (sí/no): sí

✅ ¡Configuración guardada exitosamente!
```

---

### 2.1. Método Manual A: Base de datos SQL

1. **Inicia sesión** como admin en Calibre-Web
2. Ve a **Admin** → **Configuration**
3. Busca la sección de **Notificaciones** (si está disponible en UI)
4. Añade:
   - **Evolution API URL**: `http://tu-servidor:8080`
   - **Evolution API Key**: `mi_clave_secreta_123`
   - **Evolution API Instance**: `calibre-web`
   - **Activar Evolution API**: ☑️

### 2.2. Método 2: Directamente en la base de datos

Si no hay interfaz de admin disponible, puedes configurarlo en la base de datos:

```bash
# Accede a la base de datos de Calibre-Web
sqlite3 /ruta/a/app.db

# Ejecuta estos comandos:
UPDATE settings SET 
  config_use_evolution_api = 1,
  config_evolution_api_url = 'http://tu-servidor:8080',
  config_evolution_api_key = 'mi_clave_secreta_123',
  config_evolution_api_instance = 'calibre-web';

.exit
```

### 2.3. Método 3: Editar config_sql.py (Desarrollo)

Si estás en desarrollo, puedes editar directamente:

**Archivo**: `cps/config_sql.py`

Asegúrate de que estas líneas estén configuradas:
```python
config_use_evolution_api = True
config_evolution_api_url = "http://tu-servidor:8080"
config_evolution_api_key = "mi_clave_secreta_123"
config_evolution_api_instance = "calibre-web"
```

---

## 👤 Paso 3: Configurar Usuarios

### 3.1. Como Admin (configurar otros usuarios)
1. Ve a **Admin** → **Edit User**
2. Selecciona el usuario
3. Desplázate a la sección **Notification Settings**
4. Añade:
   - **Phone Number**: `+34612345678` (con código de país)
   - **Notify via WhatsApp**: ☑️
5. Guarda cambios

### 3.2. Como Usuario (configurarte a ti mismo)
1. Ve a tu **Perfil** (icono de usuario arriba derecha)
2. Desplázate a **Notification Settings**
3. Añade:
   - **Phone Number**: `+34612345678` (incluye +código_país)
   - **Notify via WhatsApp**: ☑️
4. Guarda cambios

**⚠️ IMPORTANTE sobre el número de teléfono:**
- DEBE incluir el código de país: `+34612345678` ✅
- Sin espacios, guiones u otros caracteres
- Formato correcto: `+[código_país][número]`
- Ejemplos:
  - España: `+34612345678`
  - México: `+5215512345678`
  - Argentina: `+5491112345678`

---

## 🧪 Paso 4: Probar que Funciona

### 4.1. Verificar conexión Evolution API

**Prueba manual con curl**:
```bash
curl -X POST "http://tu-servidor:8080/message/sendText/calibre-web" \
  -H "Content-Type: application/json" \
  -H "apikey: mi_clave_secreta_123" \
  -d '{
    "number": "34612345678",
    "textMessage": {
      "text": "Prueba de Calibre-Web"
    }
  }'
```

Si recibes un mensaje en WhatsApp, **¡funciona!** ✅

### 4.2. Probar desde Calibre-Web

1. Sube un nuevo libro a la biblioteca
2. El sistema enviará automáticamente notificaciones WhatsApp
3. Verifica que llegas a recibir el mensaje

**Formato del mensaje**:
```
📚 New book available!

Title: El Quijote
Author(s): Miguel de Cervantes

🔗 https://tu-calibre-web.com/book/123
```

---

## 🔍 Verificar Configuración

### Revisar logs de Calibre-Web
```bash
# Ver logs en tiempo real
tail -f /ruta/a/calibre-web.log

# Buscar mensajes de notificación
grep "WhatsApp notification" /ruta/a/calibre-web.log
```

**Mensajes esperados**:
- ✅ `WhatsApp notification sent to +34612345678 via Evolution API`
- ❌ `Evolution API credentials not configured` → Revisa configuración
- ❌ `No phone number provided` → Usuario sin número configurado

### Verificar que Evolution API está corriendo
```bash
# Comprobar que Evolution API responde
curl http://tu-servidor:8080/

# Debería devolver información del servidor
```

---

## 🐛 Solución de Problemas

### Problema: "Evolution API credentials not configured"
**Solución**:
- Verifica que `config_use_evolution_api = True`
- Verifica que la URL es correcta
- Verifica que la API Key es correcta

### Problema: "Failed to send WhatsApp notification: 401"
**Solución**:
- Tu API Key es incorrecta
- Verifica la clave en tu servidor Evolution API

### Problema: "Failed to send WhatsApp notification: 404"
**Solución**:
- El nombre de la instancia es incorrecto
- Verifica que la instancia existe en Evolution API
- O la instancia no está conectada a WhatsApp

### Problema: El usuario no recibe mensajes
**Causas posibles**:
1. **Número mal formateado**:
   - ❌ `612345678` → Falta código de país
   - ❌ `+34 612 345 678` → Tiene espacios
   - ✅ `+34612345678` → Correcto

2. **Instancia de Evolution API desconectada**:
   - Accede al manager y verifica status
   - Reconecta si es necesario

3. **Notificaciones WhatsApp desactivadas**:
   - Usuario debe activar checkbox "WhatsApp" en su perfil

### Problema: "Connection refused"
**Solución**:
- Evolution API no está corriendo
- URL incorrecta
- Firewall bloqueando la conexión
- Verifica con: `curl http://tu-servidor:8080/`

---

## 📝 Ejemplo Completo de Configuración

### Tu Servidor Evolution API
- **URL**: `http://192.168.1.100:8080`
- **API Key**: `abc123xyz789`
- **Instancia conectada**: `mi-calibre`

### Configuración en Calibre-Web (app.db)
```sql
UPDATE settings SET 
  config_use_evolution_api = 1,
  config_evolution_api_url = 'http://192.168.1.100:8080',
  config_evolution_api_key = 'abc123xyz789',
  config_evolution_api_instance = 'mi-calibre'
WHERE id = 1;
```

### Usuario configurado
- **Email**: juan@ejemplo.com
- **Phone Number**: +34666123456
- **Notifications**:
  - ☑️ Email
  - ☑️ WhatsApp
  - ☐ Telegram
  - ☐ Push

---

## ✅ Checklist Final

- [ ] Evolution API corriendo y accesible
- [ ] Instancia creada y WhatsApp conectado (QR escaneado)
- [ ] API Key obtenida
- [ ] Calibre-Web configurado con URL, Key e Instance
- [ ] Usuario con número de teléfono (formato: +34612345678)
- [ ] Checkbox "WhatsApp" activado en notificaciones
- [ ] Prueba enviando un mensaje manual con curl ✅
- [ ] Subir un libro de prueba y verificar notificación ✅

---

## 🎯 ¡Todo Listo!

Si completaste todos los pasos:
1. Sube un nuevo libro
2. Deberías recibir un WhatsApp automáticamente
3. Si no llega, revisa los logs y la sección de problemas

**¿Necesitas ayuda?** Revisa el archivo `NOTIFICATIONS.md` para más detalles técnicos.

---

## 📚 Enlaces Útiles

- **Evolution API Docs**: https://doc.evolution-api.com/
- **Evolution API GitHub**: https://github.com/EvolutionAPI/evolution-api
- **Calibre-Web**: https://github.com/janeczku/calibre-web

---

**Última actualización**: 8 de febrero de 2026  
**Versión**: 2.0.0
