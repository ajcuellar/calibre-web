# 📚 Documentación del Sistema de Notificaciones

## ⚡ NUEVO: Configuración desde el Panel de Administración

**¡La forma más fácil de configurar Evolution API!** 🎉

**👉 [CONFIGURACION_ADMIN_EVOLUTION.md](CONFIGURACION_ADMIN_EVOLUTION.md)** ⭐⭐⭐

Configura todo desde la interfaz web de Calibre-Web:
- ✅ Admin → Edit Basic Configuration
- ✅ Habilita Evolution API con un checkbox
- ✅ Introduce URL, API Key e Instance
- ✅ Los usuarios añaden su número de WhatsApp
- ✅ ¡Sin comandos, sin scripts, sin SQL!

**¿Prefieres otros métodos?** → Sigue leyendo las guías abajo

---

## 📖 Índice de Guías

### 🚀 Configuración (elige tu método)

1. **[CONFIGURACION_ADMIN_EVOLUTION.md](CONFIGURACION_ADMIN_EVOLUTION.md)** ⭐⭐⭐ **RECOMENDADO**
   - Configuración desde el panel de administración de Calibre-Web
   - La forma más fácil y visual
   - Sin comandos ni scripts
   - ¡Todo desde la interfaz web!

2. **[GUIA_RAPIDA_EVOLUTION.md](GUIA_RAPIDA_EVOLUTION.md)** ⭐⭐
   - 1 página, configuración rápida
   - Incluye script automático: `python configure_evolution_api.py`
   - Para cuando YA tienes Evolution API
   - Configuración en 3 pasos

3. **[CONFIGURAR_EVOLUTION_API.md](CONFIGURAR_EVOLUTION_API.md)** ⭐
   - Guía completa paso a paso
   - Métodos alternativos (SQL, manual)
   - Incluye solución de problemas
   - Ejemplos con curl

### 📋 Documentación Técnica

4. **[CAMBIOS_FINALES.md](CAMBIOS_FINALES.md)**
   - Resumen de todos los cambios realizados
   - Ventajas del nuevo sistema
   - Comparación Twilio vs Evolution API
   - Migración automática explicada

5. **[NOTIFICATIONS.md](NOTIFICATIONS.md)**
   - Documentación técnica completa
   - Todos los canales de notificación
   - Instalación y configuración detallada
   - API de programación

6. **[IMPLEMENTACION_NOTIFICACIONES.md](IMPLEMENTACION_NOTIFICACIONES.md)**
   - Guía de implementación
   - Archivos creados/modificados
   - Estadísticas del proyecto
   - Checklist de implementación

### 🔧 Configuración y Ejemplos

7. **[CONFIGURACION_NOTIFICACIONES.md](CONFIGURACION_NOTIFICACIONES.md)**
   - Ejemplos de configuración
   - Configuración para cada servicio
   - Plantillas de configuración
   - Costos y límites

### 🛠️ Scripts y Herramientas (avanzado)

8. **[configure_evolution_api.py](configure_evolution_api.py)**
   - Script alternativo para configurar desde línea de comandos
   - Para usuarios que prefieren automatización
   - **Nota**: Recomendamos usar el panel de administración (opción 1)

9. **[migrate_notifications.py](migrate_notifications.py)**
   - Script de migración manual (opcional)
   - La migración es automática, pero está disponible
   - Incluye backup automático

---

## 📌 Resumen Completo

### ¿Quieres ver todo lo que se ha implementado?
👉 **[RESUMEN_CONFIGURACION.md](RESUMEN_CONFIGURACION.md)** ⭐
- Vista general del sistema
- Archivos modificados
- Pasos de configuración
- Verificación de funcionamiento
- Solución de problemas

---

## 🎯 ¿Qué guía necesito?

### Quiero configurar Evolution API
👉 **[CONFIGURACION_ADMIN_EVOLUTION.md](CONFIGURACION_ADMIN_EVOLUTION.md)** ⭐⭐⭐ **RECOMENDADO**
   (Configuración desde panel de administración - ¡sin comandos!)

ó

👉 **[GUIA_RAPIDA_EVOLUTION.md](GUIA_RAPIDA_EVOLUTION.md)** (Script automático)  
👉 **[CONFIGURAR_EVOLUTION_API.md](CONFIGURAR_EVOLUTION_API.md)** (Métodos avanzados)

### Quiero entender todo el sistema
👉 **[NOTIFICATIONS.md](NOTIFICATIONS.md)**
👉 **[RESUMEN_CONFIGURACION.md](RESUMEN_CONFIGURACION.md)**

### Quiero ver qué cambió
👉 **[CAMBIOS_FINALES.md](CAMBIOS_FINALES.md)**

### Necesito ejemplos de configuración
👉 **[CONFIGURACION_NOTIFICACIONES.md](CONFIGURACION_NOTIFICACIONES.md)**

### Solo quiero usar Telegram
👉 **[NOTIFICATIONS.md](NOTIFICATIONS.md)** → Sección "Configuración de Telegram"

### Quiero detalles técnicos de implementación
👉 **[IMPLEMENTACION_NOTIFICACIONES.md](IMPLEMENTACION_NOTIFICACIONES.md)**

---

## ⚡ Configuración Ultra Rápida

**Método 1: Panel de Administración** (sin comandos) 🎯
```
1. Admin → Edit Basic Configuration
2. Evolution API → ☑ Enable
3. Introducir: URL, API Key, Instance
4. Save y reiniciar
```

**Método 2: Script Automático**
```bash
# Si prefieres línea de comandos
cd /ruta/a/calibre-web
python configure_evolution_api.py
```

# 2. Reinicia Calibre-Web
python cps.py

# 3. Usuario configura número: +34612345678

# 4. ¡Listo! Sube un libro y recibirás WhatsApp
```

**Configuración manual** (si prefieres):
```bash
# Opción manual con SQLite
sqlite3 app.db "UPDATE settings SET 
  config_use_evolution_api=1,
  config_evolution_api_url='http://tu-servidor:8080',
  config_evolution_api_key='tu_key',
  config_evolution_api_instance='tu_instancia';"
```

---

## 🔍 Búsqueda Rápida

| Necesito... | Ver |
|------------|-----|
| **Configurar Evolution API (automático)** | `python configure_evolution_api.py` ⚡ |
| Conectar Evolution API que ya tengo | [GUIA_RAPIDA_EVOLUTION.md](GUIA_RAPIDA_EVOLUTION.md) |
| Solucionar error 401/404 | [CONFIGURAR_EVOLUTION_API.md](CONFIGURAR_EVOLUTION_API.md#-solución-de-problemas) |
| Configurar Telegram | [NOTIFICATIONS.md](NOTIFICATIONS.md#3-configuración-de-telegram) |
| Formato de número de teléfono | [GUIA_RAPIDA_EVOLUTION.md](GUIA_RAPIDA_EVOLUTION.md#-formato-de-número) |
| Ejemplos de curl | [CONFIGURAR_EVOLUTION_API.md](CONFIGURAR_EVOLUTION_API.md#-paso-4-probar-que-funciona) |
| Ver todos los cambios | [CAMBIOS_FINALES.md](CAMBIOS_FINALES.md) |
| API de notificaciones | [NOTIFICATIONS.md](NOTIFICATIONS.md#api-de-notificaciones) |
| Migración de BD | [CAMBIOS_FINALES.md](CAMBIOS_FINALES.md#3-migración-automática-de-base-de-datos-) |

---

## 📦 Estructura del Proyecto

```
calibre-web/
├── 📄 README_NOTIFICACIONES.md          ← Este archivo
├── ⭐ GUIA_RAPIDA_EVOLUTION.md          ← Empieza aquí (1 página)
├── ⭐ CONFIGURAR_EVOLUTION_API.md       ← Guía completa
├── 📋 CAMBIOS_FINALES.md                ← Qué cambió
├── 📋 NOTIFICATIONS.md                  ← Documentación técnica
├── 📋 IMPLEMENTACION_NOTIFICACIONES.md  ← Detalles implementación
├── 📋 CONFIGURACION_NOTIFICACIONES.md   ← Ejemplos configuración
├── ⚡ configure_evolution_api.py       ← Script configuración (NUEVO)
├── 🔧 migrate_notifications.py          ← Script migración (opcional)
├── 🔧 notifications-requirements.txt    ← Dependencias opcionales
└── cps/
    ├── notifications.py                 ← Servicios de notificación
    ├── config_sql.py                    ← Configuración
    └── ub.py                            ← Migración automática
```

---

## 🎯 Canales Disponibles

| Canal | Estado | Costo | Dificultad | Guía |
|-------|--------|-------|------------|------|
| **Email** | ✅ Listo | Gratis | Fácil | Ya configurado |
| **WhatsApp** | ✅ Listo | Gratis | Media | [GUIA_RAPIDA_EVOLUTION.md](GUIA_RAPIDA_EVOLUTION.md) |
| **Telegram** | ✅ Listo | Gratis | Fácil | [NOTIFICATIONS.md](NOTIFICATIONS.md) |
| **Web Push** | 🔧 Básico | Gratis | Alta | En desarrollo |

---

## ❓ Preguntas Frecuentes

**P: ¿Necesito instalar Evolution API?**  
R: No si ya lo tienes. Solo conéctalo siguiendo [GUIA_RAPIDA_EVOLUTION.md](GUIA_RAPIDA_EVOLUTION.md)

**P: ¿La migración de BD es automática?**  
R: Sí, se ejecuta al iniciar Calibre-Web. Ver [CAMBIOS_FINALES.md](CAMBIOS_FINALES.md#3-migración-automática-de-base-de-datos-)

**P: ¿Qué formato tiene el número de teléfono?**  
R: `+34612345678` (código país + número, sin espacios)

**P: ¿Funciona con mi WhatsApp personal?**  
R: Sí, no necesitas WhatsApp Business

**P: ¿Es gratis?**  
R: Sí, todo es gratis (Email, WhatsApp con Evolution API, Telegram)

---

## 🆘 Soporte

1. **Problemas con Evolution API** → Ver [CONFIGURAR_EVOLUTION_API.md](CONFIGURAR_EVOLUTION_API.md#-solución-de-problemas)
2. **Errores de configuración** → Ver logs: `tail -f calibre-web.log`
3. **Dudas técnicas** → Lee [NOTIFICATIONS.md](NOTIFICATIONS.md)

---

## 🎉 ¡Listo para empezar!

1. **¿Tienes Evolution API?** → [GUIA_RAPIDA_EVOLUTION.md](GUIA_RAPIDA_EVOLUTION.md)
2. **¿Quieres Telegram?** → [NOTIFICATIONS.md](NOTIFICATIONS.md#3-configuración-de-telegram)
3. **¿Solo email?** → Ya funciona si tienes SMTP configurado

---

**Última actualización**: 8 de febrero de 2026  
**Versión**: 2.0.0  
**Licencia**: GPL v3
