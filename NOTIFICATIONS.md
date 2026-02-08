# Sistema de Notificaciones Multi-Canal para Calibre-Web

## Descripción General

Este sistema permite enviar notificaciones automáticas a los usuarios cuando se añaden nuevos libros a la biblioteca. Soporta múltiples canales de notificación:

- **Email**: Utilizando la configuración de correo existente
- **WhatsApp**: A través de Evolution API (auto-hospedado)
- **Telegram**: Usando Telegram Bot API
- **Web Push**: Notificaciones push en el navegador (funcionalidad básica)

## Características

- ✅ Campo opcional de número de teléfono para usuarios
- ✅ Campo opcional de Telegram Chat ID
- ✅ Preferencias de notificación configurables por usuario
- ✅ Notificaciones automáticas al subir nuevos libros
- ✅ Sistema modular y extensible
- ✅ Soporte para múltiples canales simultáneos

## Instalación

### Requisitos

Instala las dependencias opcionales según los canales que quieras usar:

```bash
# Para Web Push (opcional y experimental)
pip install pywebpush

# Para peticiones HTTP (WhatsApp/Telegram)
pip install requests
```

### Configuración de Base de Datos

**¡IMPORTANTE!** La migración de base de datos es ahora automática.

Al iniciar Calibre-Web, el sistema detecta automáticamente si faltan campos de notificación y los añade. **No necesitas ejecutar ningún script manualmente**.

Si prefieres hacerlo manualmente, puedes usar:
```bash
python migrate_notifications.py
```

## Configuración

### 1. Configuración de Email

El sistema de notificaciones por email utiliza la configuración de correo existente en Calibre-Web.

1. Ve a **Admin** → **Configuration** → **E-Mail Server Settings**
2. Configura tu servidor SMTP
3. Las notificaciones de email estarán disponibles automáticamente

### 2. Configuración de WhatsApp (Evolution API)

**📌 ¿YA TIENES EVOLUTION API INSTALADO?**  
**👉 Ve a: [CONFIGURAR_EVOLUTION_API.md](CONFIGURAR_EVOLUTION_API.md)** para la guía paso a paso.

Para habilitar notificaciones por WhatsApp usando Evolution API:

1. **Instala Evolution API** (servidor auto-hospedado):
   - Documentación: https://evolution-api.com/
   - Docker: `docker run -d -p 8080:8080 atendai/evolution-api`
   
2. **Conecta una instancia de WhatsApp**:
   - Accede a la API en `http://localhost:8080`
   - Crea una nueva instancia (ej: `calibre-web`)
   - Escanea el código QR con tu WhatsApp

3. **Obtén tu API Key**:
   - Se genera automáticamente al crear la instancia
   - O configúrala en las variables de entorno de Evolution API

4. **Añade la configuración en Calibre-Web**:
   ```python
   config_use_evolution_api = True
   config_evolution_api_url = 'http://localhost:8080'  # URL de tu servidor Evolution API
   config_evolution_api_key = 'tu_api_key_aqui'
   config_evolution_api_instance = 'calibre-web'  # Nombre de tu instancia
   ```

**Ventajas de Evolution API**:
- ✅ Auto-hospedado (no dependes de servicios externos)
- ✅ Sin costos (no necesitas cuenta de Twilio)
- ✅ Conexión directa a WhatsApp Web
- ✅ Más control sobre tus datos

### 3. Configuración de Telegram

Para habilitar notificaciones por Telegram:

1. Crea un bot con [@BotFather](https://t.me/botfather) en Telegram
2. Obtén el **Bot Token**
3. Los usuarios deben obtener su **Chat ID** usando [@userinfobot](https://t.me/userinfobot)
4. Añade la configuración:
   - `config_use_telegram`: true
   - `config_telegram_bot_token`: Tu bot token

### 4. Configuración de Web Push

Para habilitar notificaciones Web Push:

**Nota**: Esta funcionalidad está en desarrollo básico. Requiere configuración manual adicional.

1. Activa la opción en la configuración:
   ```python
   config_use_webpush = True
   ```

2. La implementación completa de Web Push requiere:
   - Claves VAPID
   - Service Worker en el frontend
   - Suscripción de usuarios
   
3. Por ahora, esta opción está disponible para desarrollo futuro.

## Uso para Usuarios

### Configurar Preferencias de Notificación

1. Ve a tu perfil de usuario (o el administrador puede editarlo)
2. Desplázate hasta la sección **Notification Settings**
3. Configura tus datos de contacto:
   - **Phone Number**: Tu número con código de país (ej: +34612345678)
   - **Telegram Chat ID**: Tu ID de chat de Telegram
4. Activa los canales de notificación que prefieras:
   - ☑️ Email
   - ☑️ WhatsApp
   - ☑️ Telegram
   - ☑️ Web Push Notifications
5. Guarda los cambios

### Recibir Notificaciones

Una vez configurado, recibirás notificaciones automáticamente cuando:
- Se suba un nuevo libro a la biblioteca
- El libro esté disponible para descarga

Las notificaciones incluyen:
- Título del libro
- Autor(es)
- Enlace directo al libro (si está configurado el puerto externo)

## Estructura del Código

### Archivos Modificados/Creados

1. **`cps/ub.py`**: Modelo de usuario extendido con campos de notificación
2. **`cps/notifications.py`**: Nuevo módulo con servicios de notificación
3. **`cps/config_sql.py`**: Configuración para servicios externos
4. **`cps/editbooks.py`**: Integración de notificaciones en subida de libros
5. **`cps/admin.py`**: Manejo de preferencias en edición de usuarios
6. **`cps/templates/user_edit.html`**: Interfaz de configuración

### Modelo de Datos

Nuevos campos en el modelo `User`:

```python
phone_number = Column(String(20), default="")
telegram_id = Column(String(120), default="")
notification_preferences = Column(JSON, default={
    "new_books": {
        "email": True,
        "whatsapp": False,
        "telegram": False,
        "push": False
    }
})
```

## API de Notificaciones

### Enviar Notificación Programática

```python
from cps import notifications

# Enviar notificación de nuevo libro
notifications.send_new_book_notifications(
    book_title="El Quijote",
    authors=[author_obj1, author_obj2],
    book_id=123
)
```

### Servicios Individuales

```python
# Email
from cps.notifications import EmailNotificationService
EmailNotificationService.send_new_book_notification(user, title, authors, book_id)

# WhatsApp
from cps.notifications import WhatsAppNotificationService
WhatsAppNotificationService.send_new_book_notification(user, title, authors, book_id)

# Telegram
from cps.notifications import TelegramNotificationService
TelegramNotificationService.send_new_book_notification(user, title, authors, book_id)

# Web Push
from cps.notifications import WebPushNotificationService
WebPushNotificationService.send_new_book_notification(user, title, authors, book_id)
```

## Solución de Problemas

### Las notificaciones no se envían

1. **Verifica los logs**: Revisa `calibre-web.log` para errores
2. **Comprueba la configuración**: Asegúrate de que las credenciales sean correctas
3. **Verifica las preferencias del usuario**: Confirma que el usuario tiene notificaciones activadas
4. **Prueba la conexión**: 
   - WhatsApp/Telegram: Verifica que la API responda
   - Email: Usa la función de test de email en el admin

### Errores comunes

**"Twilio credentials not configured"**
- Solución: Configura `config_twilio_sid`, `config_twilio_token` y `config_twilio_whatsapp_from`

**"Telegram bot token not configured"**
- Solución: Configura `config_telegram_bot_token`

**"User has no phone number configured"**
- Solución: El usuario debe añadir su número de teléfono en su perfil

**"User has no Telegram ID configured"**
- Solución: El usuario debe obtener su Chat ID y añadirlo en su perfil

## Seguridad

### Mejores Prácticas

1. **Protege las credenciales**: Nunca expongas tokens o claves en código público
2. **Usa HTTPS**: Especialmente importante para Web Push
3. **Valida números de teléfono**: Asegúrate de que incluyan código de país
4. **Limita rate limits**: Implementa límites para evitar spam
5. **Encripta datos sensibles**: Considera encriptar tokens en la BD

## Futuras Mejoras

Posibles extensiones del sistema:

- [ ] Notificaciones para eventos adicionales (libros editados, series completadas, etc.)
- [ ] Plantillas de mensajes personalizables
- [ ] Programación de notificaciones (digest diario/semanal)
- [ ] Filtros de notificación (solo ciertos géneros, autores, etc.)
- [ ] Dashboard de notificaciones enviadas
- [ ] Soporte para Discord, Slack, etc.
- [ ] Sistema de cola para manejo masivo de notificaciones
- [ ] Notificaciones para libro próximo a vencer (en caso de préstamos)

## Soporte

Para problemas o preguntas:
1. Revisa los logs de Calibre-Web
2. Consulta este documento
3. Verifica la configuración de servicios externos
4. Reporta issues con información detallada

## Licencia

Este código sigue la misma licencia que Calibre-Web (GPL v3).
