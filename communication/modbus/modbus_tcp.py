import socket
from umodbus.client import tcp
from threading import RLock


class ModbusTcp:
    def __init__(self, host, port):
        super(ModbusTcp, self).__init__()
        self.client_host = host
        self.client_port = port
        self.lock = RLock()
        self.is_connected = False

    def heartbeat_check(self):
        return self._socket.fileno() != -1

    def create_connection(self):
        self.__enter__()

    def read(self, slave_id, addr, quantity=1):
        if self.is_connected:
            try:
                message = tcp.read_holding_registers(slave_id=slave_id, starting_address=addr, quantity=quantity)
                response = tcp.send_message(message, self._socket)
                return response[:quantity]
            except Exception as e:
                raise e
        else:
            raise Exception('need to connect a tcp server')

    def write(self, slave_id, addr, val):
        if self.is_connected:
            try:
                message = tcp.write_single_register(slave_id=slave_id, address=addr, value=val)
                response = tcp.send_message(message, self._socket)
                if response == val:
                    return True
                else:
                    return False
            except Exception as e:
                raise e
        else:
            raise Exception('need to connect a tcp server')

    def __enter__(self):
        self._socket = socket.create_connection(address=(self.client_host, self.client_port), timeout=60)
        self.is_connected = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket.close()
        self.is_connected = False
