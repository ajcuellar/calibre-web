# Configuración de Ejemplo para Notificaciones
# Este archivo muestra cómo configurar cada servicio de notificación

## 1. EMAIL (Ya configurado en Calibre-Web)
# Las notificaciones por email usan la configuración SMTP existente.
# Ve a: Admin → Configuration → E-Mail Server Settings

## 2. WHATSAPP (vía Evolution API)
# Evolution API es un servidor auto-hospedado que se conecta a WhatsApp Web
# Es GRATIS y no necesitas cuenta de Twilio

# Paso 1: Instalar Evolution API
# Opción A - Docker (recomendado):
"""
docker run -d \
  --name evolution-api \
  -p 8080:8080 \
  -e AUTHENTICATION_API_KEY=tu_clave_secreta_aqui \
  atendai/evolution-api
"""

# Opción B - Manual:
# Clona el repositorio: https://github.com/EvolutionAPI/evolution-api
# Sigue las instrucciones de instalación

# Paso 2: Conectar WhatsApp
# 1. Accede a http://localhost:8080/manager
# 2. Crea una nueva instancia (nombre: calibre-web)
# 3. Escanea el código QR con tu WhatsApp
# 4. ¡Listo! Tu WhatsApp está conectado

# Configuración en Calibre-Web:
config_use_evolution_api = True
config_evolution_api_url = "http://localhost:8080"
config_evolution_api_key = "tu_clave_secreta_aqui"  # La que configuraste en AUTHENTICATION_API_KEY
config_evolution_api_instance = "calibre-web"  # Nombre de tu instancia

# Configuración de usuario:
# - Phone Number: +34612345678 (incluir código de país, sin espacios)
# - Activar checkbox "WhatsApp" en notificaciones

# IMPORTANTE: 
# - El número debe estar en formato internacional (+34612345678)
# - El número debe tener WhatsApp instalado y activo
# - Evolution API debe estar corriendo y conectado

## 3. TELEGRAM
# Necesitas crear un bot de Telegram

# Paso 1: Crear bot
# - Habla con @BotFather en Telegram
# - Envía /newbot
# - Sigue las instrucciones
# - Guarda el token que te da

# Configuración en Calibre-Web:
config_use_telegram = True
config_telegram_bot_token = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"

# Configuración de usuario:
# - Obtén tu Chat ID: habla con @userinfobot en Telegram
# - Telegram ID: 123456789
# - Activar checkbox "Telegram" en notificaciones

# Paso 2: Usuario debe iniciar conversación con el bot
# - Buscar el bot en Telegram (nombre que le pusiste)
# - Enviar /start al bot

## 4. WEB PUSH (Notificaciones en navegador)
# Funcionalidad básica - En desarrollo

# Configuración en Calibre-Web:
config_use_webpush = True

# Nota: La implementación completa de Web Push requiere:
# - Service Worker en el frontend
# - Sistema de suscripciones
# - Claves VAPID (para producción)
# Esta funcionalidad está disponible para desarrollo futuro

## EJEMPLO COMPLETO DE CONFIGURACIÓN

**⚠️ IMPORTANTE: Nunca subas credenciales reales a Git**

### Opción 1: Variables de Entorno (RECOMENDADO)

Crea un archivo `.env` en la raíz del proyecto (añadido a `.gitignore`):

```bash
# .env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_SSL=1
MAIL_LOGIN=your-email@example.com
MAIL_PASSWORD=your-app-password-here
MAIL_FROM="Calibre-Web <your-email@example.com>"

# Evolution API (WhatsApp)
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=your-secret-key-here
EVOLUTION_API_INSTANCE=calibre-web

# Telegram
TELEGRAM_BOT_TOKEN=1234567890:REPLACE-WITH-YOUR-BOT-TOKEN
```

Luego en tu código Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Carga variables de .env

config = {
    # Email
    'mail_server': os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    'mail_port': int(os.getenv('MAIL_PORT', 587)),
    'mail_use_ssl': int(os.getenv('MAIL_USE_SSL', 1)),
    'mail_login': os.getenv('MAIL_LOGIN'),
    'mail_password': os.getenv('MAIL_PASSWORD'),
    'mail_from': os.getenv('MAIL_FROM'),
    
    # Evolution API
    'config_use_evolution_api': os.getenv('EVOLUTION_API_URL') is not None,
    'config_evolution_api_url': os.getenv('EVOLUTION_API_URL'),
    'config_evolution_api_key': os.getenv('EVOLUTION_API_KEY'),
    'config_evolution_api_instance': os.getenv('EVOLUTION_API_INSTANCE', 'calibre-web'),
    
    # Telegram
    'config_use_telegram': os.getenv('TELEGRAM_BOT_TOKEN') is not None,
    'config_telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
}
```

### Opción 2: Configuración desde Base de Datos

Calibre-Web ya usa una base de datos para la configuración. Usa el panel de administración:

```python
# Ya está implementado en Calibre-Web
# Admin → Edit Basic Configuration
# No necesitas código adicional
```

### Opción 3: Docker Compose (solo para Docker)

```yaml
# docker-compose.yml
□ WhatsApp
□ Web Push
"""

## TESTING

# Para probar cada servicio, usa estos comandos en la consola de Python de Calibre-Web:

"""
from cps import ub, notifications

# Obtener un usuario de prueba
user = ub.session.query(ub.User).filter(ub.User.name == "tu_usuario").first()

# Probar Email
notifications.EmailNotificationService.send_new_book_notification(
    user, "Libro de Prueba", [], None
)

# Probar WhatsApp
notifications.WhatsAppNotificationService.send_new_book_notification(
    user, "Libro de Prueba", [], None
)

# Probar Telegram
notifications.TelegramNotificationService.send_new_book_notification(
    user, "Libro de Prueba", [], None
)

# Probar Web Push
notifications.WebPushNotificationService.send_new_book_notification(
    user, "Libro de Prueba", [], None
)
"""

## COSTOS APROXIMADOS

# Email: Gratis (usando tu servidor SMTP) o muy barato con servicios como SendGrid
# WhatsApp (Twilio): ~$0.005 por mensaje enviado (después de créditos gratis)
# Telegram: Completamente gratis
# Web Push: Gratis
Evolution API): ¡Completamente gratis! (auto-hospedado)
# Telegram: Completamente gratis
# Web Push: Gratis

## LÍMITES Y MEJORES PRÁCTICAS

# Evolution API (WhatsApp):
# - Límite: Sin límite específico (depende de tu servidor)
# - DEBE estar corriendo y conectado a WhatsApp Web
# - El número del usuario debe tener WhatsApp activo
# - Formato internacional: +34612345678 (sin espacios)
# - Usuario debe haber iniciado conversación con el bot (/start)
# - Gratis y sin límites prácticos para uso personal

# Email:
# - Límite: Depende de tu servidor SMTP
# - Gmail: 500 emails/día con cuenta gratuita
# - Puede ir a spam si no tienes SPF/DKIM configurado

# Web Push:
# - Límite: Sin límite específico
# - Requiere HTTPS en producción
# - Usuario debe dar permiso en el navegador

## ENLACES ÚTILES

# Twilio:
# - Console: https://console.twilio.com/
# Evolution API (WhatsApp):
# - Sitio oficial: https://evolution-api.com/
# - GitHub: https://github.com/EvolutionAPI/evolution-api
# - Documentación: https://doc.evolution-api.com/
# - BotFather: https://t.me/botfather
# - Docs: https://core.telegram.org/bots

# Web Push:
# - Docs: https://developers.google.com/web/fundamentals/push-notifications
# - pywebpush: https://github.com/web-push-libs/pywebpush

## SOPORTE

# Si tienes problemas:
# 1. Revisa los logs de Calibre-Web
# 2. Verifica que las credenciales sean correctas
# 3. Comprueba que el usuario tiene los datos necesarios
# 4. Prueba cada servicio individualmente
# 5. Consulta NOTIFICATIONS.md para más detalles
