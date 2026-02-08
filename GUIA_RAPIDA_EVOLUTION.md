# ⚡ Guía Rápida: Conectar Evolution API
## (Para cuando ya tienes el servidor)

---

## 🎯 3 Pasos Simples

### 1️⃣ Datos de tu Evolution API
```
URL:      http://tu-servidor:8080
API Key:  [la que configuraste en AUTHENTICATION_API_KEY]
Instancia: [crea una nueva o usa existente]
```

### 2️⃣ Configurar en Calibre-Web

### 2.1. Método Manual A: Base de datos SQL

**Si prefieres hacerlo manualmente**:

```bash
sqlite3 app.db

UPDATE settings SET 
  config_use_evolution_api = 1,
  config_evolution_api_url = 'http://tu-servidor:8080',
  config_evolution_api_key = 'tu_api_key',
  config_evolution_api_instance = 'calibre-web';
```

### 2.2. Método Manual B: Código (Desarrollo)

**Si estás desarrollando**:
```python
config_use_evolution_api = True
config_evolution_api_url = "http://tu-servidor:8080"
config_evolution_api_key = "tu_api_key"
config_evolution_api_instance = "calibre-web"
```

### 3️⃣ Usuario añade su número
```
Perfil → Notification Settings
Phone Number: +34612345678
☑️ WhatsApp
```

---

## ✅ Probar
```bash
# Prueba manual
curl -X POST "http://tu-servidor:8080/message/sendText/calibre-web" \
  -H "Content-Type: application/json" \
  -H "apikey: tu_api_key" \
  -d '{"number":"34612345678","textMessage":{"text":"Test"}}'

# Prueba real
# → Sube un libro en Calibre-Web
# → Deberías recibir un WhatsApp
```

---

## 🔧 Variables de Configuración

| Variable | Ejemplo | Descripción |
|----------|---------|-------------|
| `config_use_evolution_api` | `True` | Activar/desactivar |
| `config_evolution_api_url` | `http://192.168.1.100:8080` | URL de tu servidor |
| `config_evolution_api_key` | `abc123xyz789` | API Key (AUTHENTICATION_API_KEY) |
| `config_evolution_api_instance` | `calibre-web` | Nombre de instancia |

---

## 📱 Formato de Número

✅ **Correcto**:
- `+34612345678` (España)
- `+5215512345678` (México)
- `+5491112345678` (Argentina)

❌ **Incorrecto**:
- `612345678` (sin código)
- `+34 612 345 678` (con espacios)
- `34-612-345-678` (con guiones)

---

## 🐛 Problemas Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `401 Unauthorized` | API Key incorrecta | Verifica la key |
| `404 Not Found` | Instancia incorrecta | Verifica el nombre |
| `Connection refused` | Evolution no corre | Verifica URL y servidor |
| No llegan mensajes | Número mal formado | Usa formato +34612345678 |

---

## 📦 Estructura del Mensaje API

Evolution API espera:
```json
{
  "number": "34612345678",
  "textMessage": {
    "text": "Tu mensaje aquí"
  }
}
```

Calibre-Web envía automáticamente:
```json
{
  "number": "34612345678",
  "textMessage": {
    "text": "📚 New book available!\n\nTitle: Don Quijote\nAuthor(s): Cervantes\n\n🔗 https://..."
  }
}
```

---

## 📍 Ubicación de Archivos

```
calibre-web/
├── app.db                          ← Base de datos con config
├── cps/
│   ├── config_sql.py              ← Configuración (código)
│   ├── notifications.py           ← Servicio WhatsApp
│   └── ub.py                      ← Migración automática
└── CONFIGURAR_EVOLUTION_API.md    ← Guía completa
```

---

## 🚀 Inicio Rápido

```bash
# 1. Verificar Evolution API
curl http://tu-servidor:8080/

# 2. Configurar Calibre-Web (elegir método):

## Método A: Base de datos
sqlite3 app.db "UPDATE settings SET config_use_evolution_api=1, config_evolution_api_url='http://tu-servidor:8080', config_evolution_api_key='tu_key', config_evolution_api_instance='calibre-web';"

## Método B: Código (editar config_sql.py)
# Ver ejemplo arriba

# 3. Reiniciar Calibre-Web
python cps.py

# 4. Configurar usuario
# → Perfil → Phone Number: +34612345678 → ☑️ WhatsApp

# 5. Probar
# → Subir un libro
# → ¡Recibir WhatsApp!
```

---

## ℹ️ Información Adicional

**Ver guía completa**: `CONFIGURAR_EVOLUTION_API.md`  
**Documentación técnica**: `NOTIFICATIONS.md`  
**Ejemplos configuración**: `CONFIGURACION_NOTIFICACIONES.md`

---

**Fecha**: 8 de febrero de 2026
