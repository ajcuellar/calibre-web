# 🎛️ Configuración de Evolution API desde el Panel de Administración

Esta es la forma **recomendada y más fácil** de configurar Evolution API en Calibre-Web.

---

## 📋 Requisitos Previos

Antes de empezar, asegúrate de que:
- ✅ Ya tienes Evolution API instalado y funcionando
- ✅ Tienes una instancia conectada a WhatsApp (código QR escaneado)
- ✅ Conoces tu API Key (variable `AUTHENTICATION_API_KEY`)

---

## 🔧 Paso 1: Configurar Evolution API en Calibre-Web

### 1.1. Accede a la Configuración

1. **Inicia sesión** en Calibre-Web como **administrador**

2. Ve a **Admin** (icono de tuerca) en la barra superior

3. Haz clic en **Edit Basic Configuration**

### 1.2. Habilita Evolution API

Busca la sección **"Evolution API"** y:

1. ☑ Marca el checkbox **"Enable WhatsApp Notifications (Evolution API)"**

2. Completa los 3 campos que aparecen:

   - **Evolution API URL**: `http://localhost:8080`
     - Usa `localhost` si Evolution API está en el mismo servidor
     - Si está en otro servidor: `http://192.168.1.x:8080`
   
   - **Evolution API Key**: `tu_clave_secreta`
     - Es el valor de `AUTHENTICATION_API_KEY` de tu servidor Evolution API
   
   - **Evolution API Instance**: `calibre-web`
     - El nombre de tu instancia conectada (la que tiene el QR escaneado)

3. Haz clic en **"Save"** al final de la página

### 1.3. Reinicia Calibre-Web

Para que los cambios tomen efecto:

```bash
# Si usas systemd
sudo systemctl restart calibre-web

# O simplemente reinicia el proceso manualmente
```

---

## 👤 Paso 2: Configurar Usuarios

Los usuarios deben añadir su número de WhatsApp para recibir notificaciones.

### Como Usuario (configurarte tú mismo)

1. Haz clic en tu **icono de usuario** (arriba derecha)

2. Desplázate hasta la sección **"Notification Settings"**

3. Completa:
   - **Phone Number**: `+34612345678`
     - ⚠️ **IMPORTANTE**: Debe incluir el código de país con `+`
   
4. Marca los canales que quieres:
   - ☑ **WhatsApp**
   - ☐ Email (opcional)
   - ☐ Telegram (opcional)
   - ☐ Web Push (opcional)

5. Haz clic en **"Save"**

### Como Administrador (configurar otros usuarios)

1. Ve a **Admin** → **Edit User**

2. Selecciona el usuario que quieres configurar

3. Desplázate hasta **"Notification Settings"**

4. Añade el **Phone Number** y marca **WhatsApp**

5. Guarda los cambios

---

## ✅ Paso 3: Probar las Notificaciones

### Prueba rápida

1. **Sube un libro nuevo** a Calibre-Web
   - Ve a **Upload** (icono de nube con flecha)
   - Selecciona un archivo EPUB, PDF, etc.
   - Sube el libro

2. **Deberías recibir un WhatsApp** automáticamente con:
   ```
   📚 Nuevo libro en Calibre-Web

   📖 El nombre del libro
   ✍️ Autor(es)
   
   👉 Ver en biblioteca: [enlace]
   ```

### Solución de problemas

Si no recibes el mensaje:

1. **Verifica la configuración**:
   - Admin → Edit Basic Configuration
   - Revisa que los datos sean correctos
   - Confirma que el checkbox está marcado

2. **Verifica el usuario**:
   - Perfil del usuario → Notification Settings
   - El número incluye `+` y código de país
   - El checkbox de WhatsApp está marcado

3. **Verifica Evolution API**:
   ```bash
   # Prueba manual con curl
   curl -X POST "http://tu-servidor:8080/message/sendText/calibre-web" \
     -H "apikey: tu_api_key" \
     -H "Content-Type: application/json" \
     -d '{
       "number": "+34612345678",
       "textMessage": {
         "text": "Prueba de notificación"
       }
     }'
   ```

4. **Revisa los logs de Calibre-Web**:
   ```bash
   # Busca errores relacionados con notificaciones
   tail -f /ruta/a/calibre-web.log | grep -i notification
   ```

---

## 🎯 Resumen Rápido

| Paso | Acción | Ubicación |
|------|--------|-----------|
| 1 | Habilitar Evolution API | Admin → Configuration |
| 2 | Configurar URL, Key, Instance | Misma página |
| 3 | Guardar y reiniciar | - |
| 4 | Añadir número de WhatsApp | Usuario → Notification Settings |
| 5 | Marcar checkbox WhatsApp | Misma sección |
| 6 | Probar subiendo un libro | Upload |

---

## 📚 Más Información

- **Documentación completa**: [NOTIFICATIONS.md](NOTIFICATIONS.md)
- **Configuración avanzada**: [CONFIGURAR_EVOLUTION_API.md](CONFIGURAR_EVOLUTION_API.md)
- **Índice general**: [README_NOTIFICACIONES.md](README_NOTIFICACIONES.md)

---

## ❓ Preguntas Frecuentes

### ¿Dónde encuentro mi API Key?
En las variables de entorno de tu Evolution API, busca `AUTHENTICATION_API_KEY`.

### ¿Qué pongo en "Instance"?
El nombre de la instancia que conectaste escaneando el código QR.

### ¿El número de teléfono debe tener espacios?
No. Formato correcto: `+34612345678` (sin espacios, guiones o paréntesis).

### ¿Puedo usar la misma instancia para varios servicios?
Sí, Evolution API permite enviar mensajes desde la misma instancia a múltiples aplicaciones.

### ¿Necesito reiniciar después de cambiar la configuración?
Sí, es recomendable reiniciar Calibre-Web para que los cambios tomen efecto completamente.
