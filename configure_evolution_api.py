#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de Configuración de Evolution API para Calibre-Web
Configura automáticamente Evolution API en la base de datos de Calibre-Web

Uso:
    python configure_evolution_api.py
"""

import sqlite3
import os
import sys
from pathlib import Path


def find_database():
    """Encuentra la base de datos app.db de Calibre-Web"""
    possible_paths = [
        'app.db',
        './app.db',
        '../app.db',
        os.path.expanduser('~/.config/calibre-web/app.db'),
        '/var/lib/calibre-web/app.db',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def verify_database(db_path):
    """Verifica que la base de datos tenga la estructura correcta"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar que exista la tabla settings
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings'")
        if not cursor.fetchone():
            print("❌ Error: No se encontró la tabla 'settings'")
            conn.close()
            return False
        
        # Verificar/crear columnas de Evolution API
        cursor.execute("PRAGMA table_info(settings)")
        columns = [col[1] for col in cursor.fetchall()]
        
        missing_columns = []
        if 'config_use_evolution_api' not in columns:
            missing_columns.append('config_use_evolution_api')
        if 'config_evolution_api_url' not in columns:
            missing_columns.append('config_evolution_api_url')
        if 'config_evolution_api_key' not in columns:
            missing_columns.append('config_evolution_api_key')
        if 'config_evolution_api_instance' not in columns:
            missing_columns.append('config_evolution_api_instance')
        
        if missing_columns:
            print(f"⚠️  Faltan columnas en la base de datos: {', '.join(missing_columns)}")
            print("    Estas se crearán automáticamente al iniciar Calibre-Web.")
            print("    O puedes ejecutar el script migrate_notifications.py primero.")
            
            response = input("\n¿Continuar de todos modos? (sí/no): ").strip().lower()
            if response not in ['sí', 'si', 's', 'y', 'yes']:
                conn.close()
                return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar base de datos: {e}")
        return False


def get_current_config(db_path):
    """Obtiene la configuración actual"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                config_use_evolution_api,
                config_evolution_api_url,
                config_evolution_api_key,
                config_evolution_api_instance
            FROM settings 
            WHERE id = 1
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'enabled': bool(result[0]),
                'url': result[1] or '',
                'key': result[2] or '',
                'instance': result[3] or ''
            }
        return None
        
    except sqlite3.OperationalError:
        # Columnas no existen aún
        return None
    except Exception as e:
        print(f"⚠️  No se pudo leer configuración actual: {e}")
        return None


def configure_evolution_api(db_path, url, api_key, instance):
    """Configura Evolution API en la base de datos"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Intentar actualizar
        cursor.execute("""
            UPDATE settings 
            SET 
                config_use_evolution_api = 1,
                config_evolution_api_url = ?,
                config_evolution_api_key = ?,
                config_evolution_api_instance = ?
            WHERE id = 1
        """, (url, api_key, instance))
        
        conn.commit()
        conn.close()
        
        return True
        
    except sqlite3.OperationalError as e:
        if 'no column' in str(e).lower():
            print("\n⚠️  Las columnas de Evolution API no existen todavía.")
            print("    Inicia Calibre-Web una vez para que se creen automáticamente,")
            print("    o ejecuta: python migrate_notifications.py")
            return False
        else:
            print(f"❌ Error al configurar: {e}")
            return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def main():
    print("=" * 70)
    print("  🔧 Configuración de Evolution API para Calibre-Web")
    print("=" * 70)
    print()
    
    # Encontrar base de datos
    print("📂 Buscando base de datos (app.db)...")
    db_path = find_database()
    
    if not db_path:
        print("❌ No se encontró app.db automáticamente")
        db_path = input("\n   Introduce la ruta a app.db: ").strip()
        if not os.path.exists(db_path):
            print("❌ El archivo no existe")
            sys.exit(1)
    
    print(f"✅ Base de datos encontrada: {db_path}")
    print()
    
    # Verificar base de datos
    if not verify_database(db_path):
        print("\n❌ La base de datos no es válida")
        sys.exit(1)
    
    # Mostrar configuración actual
    current = get_current_config(db_path)
    if current:
        print("📋 Configuración actual:")
        print(f"   Estado: {'✅ Activado' if current['enabled'] else '❌ Desactivado'}")
        print(f"   URL: {current['url'] or '(no configurada)'}")
        print(f"   API Key: {'***' + current['key'][-4:] if len(current['key']) > 4 else '(no configurada)'}")
        print(f"   Instancia: {current['instance'] or '(no configurada)'}")
        print()
    
    # Solicitar datos
    print("📝 Introduce los datos de tu servidor Evolution API:")
    print()
    
    # URL
    url = input("   URL del servidor (ej: http://localhost:8080): ").strip()
    if not url:
        print("❌ URL es obligatoria")
        sys.exit(1)
    
    if not url.startswith('http://') and not url.startswith('https://'):
        print("⚠️  La URL debe empezar con http:// o https://")
        url = 'http://' + url
        print(f"   Usando: {url}")
    
    # Quitar slash final si existe
    url = url.rstrip('/')
    
    # API Key
    api_key = input("   API Key (AUTHENTICATION_API_KEY): ").strip()
    if not api_key:
        print("❌ API Key es obligatoria")
        sys.exit(1)
    
    # Instancia
    default_instance = current['instance'] if current and current['instance'] else 'calibre-web'
    instance = input(f"   Nombre de instancia [{default_instance}]: ").strip()
    if not instance:
        instance = default_instance
    
    print()
    
    # Confirmar
    print("=" * 70)
    print("Resumen de configuración:")
    print("=" * 70)
    print(f"  URL:        {url}")
    print(f"  API Key:    {'*' * (len(api_key)-4)}{api_key[-4:]}")
    print(f"  Instancia:  {instance}")
    print("=" * 70)
    print()
    
    confirm = input("¿Guardar esta configuración? (sí/no): ").strip().lower()
    if confirm not in ['sí', 'si', 's', 'y', 'yes']:
        print("❌ Configuración cancelada")
        sys.exit(0)
    
    print()
    print("💾 Guardando configuración...")
    
    # Configurar
    if configure_evolution_api(db_path, url, api_key, instance):
        print("✅ ¡Configuración guardada exitosamente!")
        print()
        print("=" * 70)
        print("Próximos pasos:")
        print("=" * 70)
        print()
        print("1. 🔄 Reinicia Calibre-Web:")
        print("   python cps.py")
        print()
        print("2. 👤 Configura el usuario:")
        print("   - Ir a Perfil → Notification Settings")
        print("   - Phone Number: +34612345678 (con código de país)")
        print("   - ☑️ Activar WhatsApp")
        print()
        print("3. 🧪 Probar con curl:")
        print(f"   curl -X POST '{url}/message/sendText/{instance}' \\")
        print(f"     -H 'Content-Type: application/json' \\")
        print(f"     -H 'apikey: {api_key}' \\")
        print(f"     -d '{{\"number\":\"34612345678\",\"textMessage\":{{\"text\":\"Test\"}}}}'")
        print()
        print("4. 📚 Subir un libro para recibir la notificación")
        print()
        print("=" * 70)
        print()
        print("📖 Más información:")
        print("   - Guía rápida: GUIA_RAPIDA_EVOLUTION.md")
        print("   - Guía completa: CONFIGURAR_EVOLUTION_API.md")
        print()
        
    else:
        print("❌ Error al guardar configuración")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
