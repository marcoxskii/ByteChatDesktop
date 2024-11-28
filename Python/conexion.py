import socket

class Conexion:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def enviar_mensaje(self, mensaje):
        self.client_socket.sendall(mensaje.encode())
        response = self.client_socket.recv(1024)
        return response.decode()

    def cerrar(self):
        self.client_socket.close()