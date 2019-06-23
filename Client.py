import socket
import json
import pandas as pd
import pickle


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

host_ip, server_port = "localhost", 9998

def work_with_server_train():
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_client.connect((host_ip, server_port))
        columns = ['number', 'date', 'Temperature', 'Humidity', 'Light', 'CO2', 'HumidityRatio', 'Occupancy']
        sensor_ = pd.DataFrame(columns=columns)
        i = 0
        while True:
            received = tcp_client.recv(1024)
            if not received: break
            received = json.loads(received)
            print(received)
            sensor_ = sensor_.append(received,ignore_index=True)
            i += 1
    finally:
        tcp_client.close()
    return (sensor_)


sensor = work_with_server_train()
x = sensor.loc[:, ['Temperature', 'Humidity', 'Light', 'CO2', 'HumidityRatio']]
y = sensor.loc[:, ['Occupancy']]



x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = .3, random_state = 43)

y_train = y_train.values.ravel().astype('int')
y_test = y_test.values.ravel().astype('int')

sensor_logit = LogisticRegression()
sensor_logit.fit(x_train, y_train)
y_train_predict = sensor_logit.predict(x_train)
y_test_predict = sensor_logit.predict(x_test)
y_train_acc = accuracy_score(y_train_predict, y_train)
y_test_acc = accuracy_score(y_test_predict, y_test)

y_train_acc = classification_report(y_train_predict, y_train)
y_test_acc = classification_report(y_test_predict, y_test)

print(y_train_acc)
print(y_test_acc)

filename = 'finalized_model.pkl'
pickle.dump(sensor_logit, open(filename, 'wb'))