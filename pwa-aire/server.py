#!/usr/bin/env python3
"""
Servidor Local para la PWA de Control de Aire Mabe
Sirve los archivos estáticos de la PWA y provee endpoint API para transmisión IR
"""

import http.server
import socketserver
import json
import os
import socket

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class PWAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/api/send-ir':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                state = data.get('state', {})
                print(f"[*] Senal IR recibida: Modo={state.get('mode')}, Temp={state.get('temp')}C, Power={state.get('power')}")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "success"}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    local_ip = get_local_ip()
    print("=" * 60)
    print(" SERVIDOR PWA - CONTROL DE AIRE ACONDICIONADO MABE")
    print("=" * 60)
    print(f"[*] Acceso en tu PC:        http://localhost:{PORT}")
    print(f"[*] Acceso desde tu POCO:    http://{local_ip}:{PORT}")
    print("=" * 60)
    print("Presiona Ctrl + C para detener el servidor.\n")
    
    with socketserver.TCPServer(("", PORT), PWAHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")

