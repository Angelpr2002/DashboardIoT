[app]
title = IoT Dashboard
package.name = iotdashboard
package.domain = org.user
source.dir = .
source.include_exts = py
version = 1.0.0
requirements = 
    python3 ==3.10.13,
    kivy ==2.2.1,
    requests ==2.31.0,
    openssl,
    pyjnius ==1.5.0
    
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
p4a.branch = master
android.arch = armeabi-v7a  # Solo ARMv7 para mayor compatibilidad

[buildozer]
log_level = 1  # Reduce el tamaño del log
