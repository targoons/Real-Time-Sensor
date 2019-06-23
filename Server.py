import socketserver
import numpy as np
import pandas as pd
from time import sleep
import json

class Handler_TCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            sensor = pd.read_csv('censortraining.csv')
            for index, row in sensor.iterrows():
                self.request.sendall(json.dumps(row.to_dict()).encode())
                sleep(0.05)
        except:
            pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 9998
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)
    tcp_server.serve_forever()