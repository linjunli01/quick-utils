import logging
import socketserver
import traceback
import socket
from threading import Thread
import json

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def log_info(msg):
    logger.info(f'debugging Proxy:{msg}')


def log_err(msg):
    logger.error(f'debugging Proxy:{msg}')


class TCPServer(socketserver.TCPServer, Thread):
    def __init__(self, port, handler_class):
        socketserver.TCPServer.__init__(self, ('', port), handler_class, bind_and_activate=False)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.server_bind()
        self.server_activate()

        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)

        log_info(f'init proxy server port: {port}')

        Thread.__init__(self)
        self.start()

    def run(self) -> None:
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        self.server_close()
        self.shutdown()


class ThreadedTCPServer(socketserver.ThreadingMixIn, TCPServer): pass


class ProxyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        command = self.receive_command()
        try:
            result = self.handle_command(command)
            self.respond(success=True, message=str(result))
        except Exception:
            error = traceback.format_exc()
            log_info(f"tcp_handler error: {error}")
            self.respond(success=False, message=error)

    def handle_command(self, command):
        # result#{station}#{part_num}#{part_id}#{result}
        if command.startswith('result'):
            pass
        return ''

    def receive_command(self):
        data = self.rfile.readline().strip()
        log_info(f'proxy recv data:{data}')
        command = data.decode()
        return command

    def respond(self, success, message=''):
        success_response = json.dumps({'success': success, 'message': message})
        response = (success_response + '\n').encode()
        self.wfile.write(response)
