# 🔒 Configuración Segura de Credenciales

## ⚠️ Importante: Nunca Subas Credenciales a Git

Este documento explica cómo configurar credenciales de forma segura para el sistema de notificaciones.

---

## 🎯 Métodos de Configuración Seguros

### Método 1: Variables de Entorno (RECOMENDADO)

#### Paso 1: Crear archivo .env

```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Edita con tus credenciales reales
nano .env  # o vim, code, etc.
```

#### Paso 2: El archivo .env debe contener:

```bash
# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_LOGIN=tu-email@gmail.com
MAIL_PASSWORD=tu-password-real-aqui

# Evolution API
EVOLUTION_API_URL=http://tu-servidor:8080
EVOLUTION_API_KEY=tu-api-key-real
EVOLUTION_API_INSTANCE=calibre-web

# Telegram
TELEGRAM_BOT_TOKEN=1234567890:TU-TOKEN-REAL-AQUI
```

#### Paso 3: Verificar que .env está en .gitignore

```bash
# Verifica que .env esté ignorado
cat .gitignore | grep .env

# Debería mostrar:
# .env
# .env.local
# .env.*.local
```

#### Paso 4: Usar en Python (si es necesario)

Calibre-Web ya gestiona la configuración desde la base de datos, pero si necesitas cargar desde .env:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Acceder a las variables
email = os.getenv('MAIL_LOGIN')
password = os.getenv('MAIL_PASSWORD')
```

---

### Método 2: Panel de Administración (MÁS FÁCIL)

**Calibre-Web ya tiene un panel de administración** que guarda las credenciales de forma segura en la base de datos:

1. **Inicia sesión** como administrador
2. Ve a **Admin** → **Edit Basic Configuration**
3. Configura:
   - **Email Settings**: SMTP, usuario, contraseña
   - **Evolution API**: URL, API Key, Instance
   - **Telegram**: Bot Token
4. **Guarda** los cambios

✅ Las credenciales se guardan cifradas en `app.db`  
✅ `app.db` está en `.gitignore` (no se sube a Git)

---

### Método 3: Docker Secrets (Para Docker)

Si usas Docker Compose:

```yaml
# docker-compose.yml
version: '3.8'
services:
  calibre-web:
    image: calibre-web
    environment:
      - MAIL_LOGIN=${MAIL_LOGIN}
      - MAIL_PASSWORD=${MAIL_PASSWORD}
      - EVOLUTION_API_KEY=${EVOLUTION_API_KEY}
    env_file:
      - .env  # Lee desde .env
    secrets:
      - smtp_password
      
secrets:
  smtp_password:
    file: ./secrets/smtp_password.txt
```

---

## 🚨 Qué NO Hacer

### ❌ NO subas credenciales a Git

```python
# ❌ MAL - Credenciales hardcodeadas
config = {
    'mail_password': 'mi_password_real_123',  # NUNCA HAGAS ESTO
    'api_key': 'ABC123XYZ789'  # NUNCA HAGAS ESTO
}
```

### ❌ NO pongas credenciales en archivos de código

```python
# ❌ MAL
SMTP_PASSWORD = "password123"
API_KEY = "clave-secreta-aqui"
```

### ❌ NO compartas .env con nadie

El archivo `.env` contiene credenciales reales y no debe compartirse.

---

## ✅ Qué SÍ Hacer

### ✅ Usa variables de entorno

```python
# ✅ BIEN
import os
password = os.getenv('MAIL_PASSWORD')
api_key = os.getenv('EVOLUTION_API_KEY')
```

### ✅ Usa el panel de administración

Admin → Edit Basic Configuration → Guarda credenciales ahí

### ✅ Usa .env para local, variables de entorno para producción

```bash
# Local (desarrollo)
# .env con credenciales de prueba

# Producción (servidor)
export MAIL_PASSWORD="password_produccion"
export EVOLUTION_API_KEY="key_produccion"
```

---

## 🔍 Verificar Seguridad

### 1. Verifica que .env no está en Git

```bash
git status
# .env NO debe aparecer

git check-ignore .env
# Debería mostrar: .env (está ignorado)
```

### 2. Verifica que no hay credenciales en el código

```bash
# Buscar posibles credenciales hardcodeadas
grep -r "password.*=" --include="*.py" .
grep -r "api.*key.*=" --include="*.py" .
```

### 3. Usa herramientas de escaneo

```bash
# Instala git-secrets
brew install git-secrets  # macOS
# o apt-get install git-secrets  # Linux

# Escanea el repositorio
git secrets --scan
```

---

## 🔐 Generar Contraseñas Seguras

### Para Gmail (App Password)

1. Ve a https://myaccount.google.com/security
2. **Verificación en 2 pasos** → Activar
3. **Contraseñas de aplicaciones** → Generar
4. Usa esa contraseña en `MAIL_PASSWORD`

### Para Evolution API

```bash
# Genera una API key segura
openssl rand -hex 32
```

### Para Telegram Bot

1. Habla con @BotFather en Telegram
2. `/newbot` → Sigue instrucciones
3. Guarda el token que te da

---

## 📚 Recursos Adicionales

- [12-Factor App - Config](https://12factor.net/config)
- [OWASP - Secrets Management](https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password)
- [GitHub - Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

---

## ❓ Preguntas Frecuentes

### ¿Qué hago si ya subí credenciales a Git?

1. **Cambia las credenciales inmediatamente** (nueva contraseña, nueva API key)
2. Elimina el historial de Git:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch PATH/TO/FILE" \
     --prune-empty --tag-name-filter cat -- --all
   
   git push origin --force --all
   ```
3. Usa [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) para limpiar el historial

### ¿Es seguro guardar credenciales en app.db?

Sí, siempre que:
- ✅ `app.db` esté en `.gitignore`
- ✅ No subas `app.db` a Git
- ✅ Hagas backups seguros de `app.db`
- ✅ Las credenciales estén cifradas (Calibre-Web lo hace)

### ¿Puedo usar un gestor de secretos?

Sí, para producción se recomienda:
- **AWS Secrets Manager**
- **Azure Key Vault**
- **HashiCorp Vault**
- **Docker Secrets**

---

**¡Mantén tus credenciales seguras!** 🔒
