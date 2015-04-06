import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import socket
import json
import subprocess
from datetime import datetime
import time
import configparser

'''
Author: GYzheng, guanggyz@gmail.com

###Client Side
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
    def get_host_info(self):
        self.client_name = socket.gethostname()
        self.client_ip = socket.gethostbyname(socket.gethostname())
    def subscribe_msg(self):
        self.subscriber = mqtt.Client()
        self.subscriber.on_connect = self.on_connect
        self.subscriber.on_message = self.on_message
        self.is_connect = False #using this variable to wait for connect ready
        #Connect the broker, if fail, retry in 10 secs
        while True:
            try:
                self.subscriber.connect(self.host,self.port);#keep_alive=60 
                break
            except:
                time.sleep(10)
                pass
        self.subscriber.loop_start()
        while self.is_connect == False:
            pass#donothig...
    
    def send_msg(self,msg):
        publish.single(self.cs_topic,msg, hostname=self.host, port=self.port)
    
    def on_connect(self,client, userdata, flags, rc):
        self.is_connect = True
        #subscribe data from server
        client.subscribe(self.sc_topic);
        status = 'join'
        msg = self.json_generator(status)
        self.send_msg(msg)
    def on_message(self,client,user_data,msg):        
        try:
            tmp = json.loads(msg.payload.decode('utf-8','ignore'))
            server_name = tmp['name']
            server_ip = tmp['ip']
            server_status = tmp['status']
            server_cmd = tmp['cmd']
            print("[DEBUG] "+server_name+","+server_ip+","+server_status+","+server_cmd)
            #self.run_cmd(server_cmd) 
        except:
             print("Not Json format!")
        self.run_cmd(server_cmd)
    def run_cmd(self,cmd):
        child = subprocess.Popen([cmd],shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        try:
            result = child.communicate(timeout=30)[0].decode('utf-8','ignore')
        except:
            result = "TimeOut!"
        print(result)
        status = 'success'
        msg = self.json_generator(status,result)
        self.send_msg(msg)
        #return the output to server
    def json_generator(self,status,result='none'):
        msg = json.dumps({'name':self.client_name,'ip':self.client_ip,'timestamp':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'status':status,'result':result})
        return msg

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('client.conf')
    broker_ip = config['client.conf']['broker_ip']
    broker_port = config['client.conf']['broker_port']
    topic = config['client.conf']['topic']
    ch = command_handler(broker_ip,broker_port,topic);
    print("Client start! Broker IP = "+broker_ip+", Broker PORT = "+broker_port+", topic = "+topic)
    print("Waiting for command.....")
    while True:
        pass
