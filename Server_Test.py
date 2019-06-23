import socketserver
import json
import pandas as pd
from time import sleep

class Handler_TCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            sensor = pd.read_csv('censortest.csv')
            for index, row in sensor.iterrows():
                self.request.sendall(json.dumps(row.to_dict()).encode())
                sleep(0.02)
        except:
            pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)
    tcp_server.serve_forever()