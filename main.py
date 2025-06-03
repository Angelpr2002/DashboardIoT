from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import requests
import json
import os
from datetime import datetime
from kivy.utils import platform

# Agrega esto ANTES de crear la aplicación
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.INTERNET])
# Manejo de permisos para Android
try:
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.INTERNET])
except:
    pass  # Para modo escritorio

THINGSBOARD_TOKEN = os.getenv('THINGSBOARD_TOKEN', 'pCNDucPvl95tmuzPzNzE')
THINGSBOARD_URL = f"https://thingsboard.cloud/api/v1/{THINGSBOARD_TOKEN}/telemetry"

class IoTDashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 10
        
        # Campo para IP del dispositivo
        self.ip_input = TextInput(
            text='192.168.4.1',
            hint_text="IP del dispositivo IoT",
            size_hint=(1, None),
            height=45,
            multiline=False,
            write_tab=False
        )
        self.add_widget(self.ip_input)

        # Área de visualización de datos
        self.data_display = TextInput(
            text='Presione "Obtener Datos" para comenzar...\n',
            size_hint=(1, 0.7),
            readonly=True,
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            font_size='14sp'
        )
        self.add_widget(self.data_display)

        # Botones de control
        btn_layout = BoxLayout(size_hint=(1, 0.15), spacing=10, padding=5)
        self.get_btn = Button(
            text="Obtener Datos",
            background_color=(0.3, 0.7, 0.3, 1),
            on_press=self.get_json_data
        )
        self.send_btn = Button(
            text="Enviar a ThingsBoard",
            background_color=(0.13, 0.59, 0.95, 1),
            on_press=self.send_to_tb,
            disabled=True
        )
        btn_layout.add_widget(self.get_btn)
        btn_layout.add_widget(self.send_btn)
        self.add_widget(btn_layout)
        
        self.meter_data = {}

    def update_display(self, message):
        self.data_display.text += f"\n{message}"
        # Scroll automático al final
        self.data_display.scroll_y = 0

    def get_json_data(self, instance):
        self.update_display("\n[⏳] Solicitando datos...")
        self.send_btn.disabled = True
        Clock.schedule_once(lambda dt: self.fetch_data(), 0.1)

    def fetch_data(self):
        try:
            device_ip = self.ip_input.text.strip()
            if not device_ip:
                self.update_display("\n[❌] Error: Ingrese una dirección IP válida")
                self.send_btn.disabled = True
                return
                
            url = f"http://{device_ip}/METER"
            self.update_display(f"Conectando a: {url}")
            
            response = requests.get(url, timeout=40)
            response.raise_for_status()
            
            try:
                self.meter_data = json.loads(response.content.decode())
            except json.JSONDecodeError:
                self.update_display("\n[❌] Error: Respuesta inválida del dispositivo (no es JSON)")
                self.send_btn.disabled = True
                return
            
            self.update_display("\n[✅] Datos obtenidos correctamente:")
            for key, label in [('horas', 'Horas'), ('dias', 'Días'), ('meses', 'Meses')]:
                if key in self.meter_data:
                    self.update_display(f"- {label}: {self.meter_data[key]}")
            
            if 'ultima_actualizacion' in self.meter_data:
                try:
                    timestamp = datetime.fromtimestamp(self.meter_data['ultima_actualizacion'])
                    self.update_display(f"- Última actualización: {timestamp.strftime('%d/%m/%Y %H:%M')}")
                except Exception as e:
                    self.update_display(f"- Error en timestamp: {str(e)}")

            self.send_btn.disabled = False

        except Exception as e:
            self.update_display(f"\n[❌] Error: {str(e)}")
            self.send_btn.disabled = True

    def send_to_tb(self, instance):
        if not self.meter_data:
            self.update_display("\n[⚠️] Error: No hay datos para enviar")
            return
            
        self.update_display("\n[🚀] Enviando a ThingsBoard...")
        self.send_btn.disabled = True
        Clock.schedule_once(lambda dt: self.upload_data(), 0.1)

    def upload_data(self):
        try:
            response = requests.post(THINGSBOARD_URL, json=self.meter_data, timeout=40)
            response.raise_for_status()
            self.update_display(f"[✅] Envío exitoso (Código: {response.status_code})")
        except Exception as e:
            self.update_display(f"[❌] Error de envío: {str(e)}")
        finally:
            self.send_btn.disabled = False

class MainApp(App):
    def build(self):
        self.title = "Dashboard IoT"
        return IoTDashboard()

if __name__ == "__main__":
    MainApp().run()
