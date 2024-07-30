import socket
import threading
import json
from src.network.protocol import encode_message, decode_message

class P2PServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.clients = {}
        self._stop_event = threading.Event()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        threading.Thread(target=self._accept_connections, daemon=True).start()

    def stop(self):
        self._stop_event.set()
        if self.socket:
            self.socket.close()

    def _accept_connections(self):
        while not self._stop_event.is_set():
            try:
                client_socket, address = self.socket.accept()
                threading.Thread(target=self._handle_client, args=(client_socket, address), daemon=True).start()
            except socket.error:
                break

    def _handle_client(self, client_socket, address):
        self.clients[address] = client_socket
        try:
            while not self._stop_event.is_set():
                data = client_socket.recv(4096)
                if not data:
                    break
                message = decode_message(data)
                self._process_message(message, address)
        finally:
            client_socket.close()
            del self.clients[address]

    def _process_message(self, message, sender_address):
        # Implement message processing logic
        pass

    def broadcast_resources(self, resources):
        message = encode_message({
            "type": "resource_update",
            "resources": resources
        })
        self._broadcast(message)

    def distribute_training_task(self, task):
        message = encode_message({
            "type": "training_task",
            "task": task
        })
        self._broadcast(message)

    def _broadcast(self, message):
        for client_socket in self.clients.values():
            try:
                client_socket.send(message)
            except socket.error:
                # Handle disconnected client
                pass