import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import socket
import json
from datetime import datetime
import configparser

'''
Author: GYzheng, guanggyz@gmail.com

###Server side

We have two topic, one is from client to server, the other one is from client to server
1. Server->Client : sc_topic   
2. Client->Server : cs_topic
'''
class command_handler:
    def __init__(self,host,port,topic):
        self.host = host
        self.port = int(port)
        self.sc_topic = 'sc_'+topic
        self.cs_topic = 'cs_'+topic
        self.get_host_info()
        self.subscribe_msg()
    def send_command(self,cmd):
        msg = self.json_generator(cmd,'run')#cmd,status
        self.send_msg(msg)

    def get_host_info(self):
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(socket.gethostname())
    def subscribe_msg(self):
        self.subscriber = mqtt.Client()
        self.subscriber.on_connect = self.on_connect
        self.subscriber.on_message = self.on_message
        self.is_connect = False #using this variable to wait for connect ready
        self.subscriber.connect(self.host,self.port);#keep_alive=60 
        self.subscriber.loop_start()
        while self.is_connect == False:
            pass#donothig...
    
    def send_msg(self,msg):
        publish.single(self.sc_topic,msg, hostname=self.host, port=self.port)
    
    def on_connect(self,client, userdata, flags, rc):
        self.is_connect = True
        #subscribe data from server
        client.subscribe(self.cs_topic);
    def on_message(self,client,user_data,msg):        
        try:
            tmp = json.loads(msg.payload.decode('utf-8','ignore'))
            client_name = tmp['name']
            client_ip = tmp['ip']
            client_status = tmp['status']
            client_result = tmp['result']
            print(client_name+","+client_ip+","+client_status)
            print(client_result)
        except:
            print("Not Json format!")
    
    def json_generator(self,cmd,status):
        msg = json.dumps({'name':self.host_name,'ip':self.host_ip,'timestamp':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'status':status,'cmd':cmd})
        return msg

#main function
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('server.conf')
    broker_ip = config['server.conf']['broker_ip']
    broker_port = config['server.conf']['broker_port']
    topic = config['server.conf']['topic']  
    ch = command_handler(broker_ip,broker_port,topic);
    print("Server start! Broker IP = "+broker_ip+", Broker PORT = "+broker_port+", topic = "+topic)
    while True:
        cmd = input("Please input command:\n")
        ch.send_command(cmd)
        pass
