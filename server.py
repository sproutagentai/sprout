import socket
import sys
import traceback
import io
import logging
from contextlib import closing
import argparse

exec_globals = {}
exec_locals = {}

def execute_code(code):
    stdout = io.StringIO()
    stderr = io.StringIO()
    sys.stdout = stdout
    sys.stderr = stderr

    try:
        exec(code, exec_globals, exec_locals)
    except Exception as e:
        traceback.print_exc(file=stderr)
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    output = stdout.getvalue()
    error = stderr.getvalue()

    stdout.close()
    stderr.close()

    return output + error

def start_server(host, port):
    logging.info(f"Starting server on {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        logging.info(f"Server listening on {host}:{port}")
        while True:
            try:
                conn, addr = s.accept()
                with closing(conn):
                    logging.info(f"Connected by {addr}")
                    data = conn.recv(4096)  # Increased buffer size
                    if not data:
                        break
                    code = data.decode('utf-8')
                    output = execute_code(code)
                    conn.sendall(output.encode('utf-8'))
            except Exception as e:
                logging.error(f"Error during connection handling: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a simple Python code execution server.")
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=65432, help='Port to bind the server to (default: 65432)')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    start_server(args.host, args.port)
