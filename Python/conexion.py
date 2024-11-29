import socket
import time

class Conexion:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.client_socket = None
        self.message_queue = []  # Cola de mensajes
        self.conectar()

    def conectar(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            print("Conectado al servidor")
            self.reenviar_mensajes()  # Reenviar mensajes en la cola al reconectar
        except socket.error as e:
            print(f"Error al conectar: {e}")
            self.reconectar()

    def reconectar(self):
        while True:
            try:
                self.client_socket.close()  # Cerrar el socket anterior
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crear un nuevo socket
                print("Intentando reconectar...")
                self.client_socket.connect((self.host, self.port))
                print("Reconectado al servidor")
                self.reenviar_mensajes()  # Reenviar mensajes en la cola al reconectar
                break
            except socket.error as e:
                print(f"Error al reconectar: {e}")
                time.sleep(5)  # Esperar 5 segundos antes de intentar reconectar nuevamente

    def enviar_mensaje(self, mensaje):
        try:
            self.client_socket.sendall(mensaje)  # Enviar directamente el mensaje en bytes
            response = self.client_socket.recv(1024)
            return response.decode()
        except socket.error as e:
            print(f"Error al enviar mensaje: {e}")
            self.message_queue.append(mensaje)  # Almacenar el mensaje en la cola
            self.reconectar()

    def reenviar_mensajes(self):
        while self.message_queue:
            mensaje = self.message_queue.pop(0)
            try:
                self.client_socket.sendall(mensaje)
                print("Mensaje reenviado:", mensaje)
            except socket.error as e:
                print(f"Error al reenviar mensaje: {e}")
                self.message_queue.insert(0, mensaje)  # Volver a poner el mensaje en la cola
                break

    def cerrar(self):
        if self.client_socket:
            self.client_socket.close()