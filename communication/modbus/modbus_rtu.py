import serial
from umodbus.client.serial import rtu
from threading import RLock


class ModbusRtu:
    def __init__(self, port, to=1, br=9600):
        super(ModbusRtu, self).__init__()
        print(f'try init modbus rtu from {port}')
        self.client_port = port
        self.to = to
        self.br = br
        self.lock = RLock()
        try:
            self._serial_handle = serial.Serial(
                port=port,
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=to
            )
        except Exception as e:
            raise Exception(f"Failed to open serial port:{port} exception:{e}")
        print(f'connected to modbus rtu {port}')

    def read(self, slave_id, addr, quantity=1):
        try:
            message = rtu.read_holding_registers(slave_id=slave_id, starting_address=addr, quantity=quantity)
            response = rtu.send_message(message, self._serial_handle)
            return response[:quantity]
        except Exception as e:
            raise e

    def write(self, slave_id, addr, val):
        try:
            message = rtu.write_single_register(slave_id=slave_id, address=addr, value=val)
            response = rtu.send_message(message, self._serial_handle)
            if response == val:
                return True
            else:
                return False
        except Exception as e:
            raise e
