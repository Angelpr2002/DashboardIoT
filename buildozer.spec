[app]
title = Dashboard IoT
package.name = dashboardiot
package.domain = com.tudominio

# Versión de la app
version = 1.0.0

# Requerimientos
requirements = python3, kivy==2.2.1, requests==2.31.0, pyopenssl==24.1.0, cryptography==42.0.7

# Permisos de Android
android.permissions = INTERNET

# Orientación
orientation = portrait

# Archivos a incluir
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,json

# Entrada principal
main.py = main.py

# Configuración de SDK (versiones probadas)
android.sdk = 24
android.ndk = 25b
android.api = 33

# Logs detallados
log_level = 2