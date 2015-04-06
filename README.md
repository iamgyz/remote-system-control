# remote-system-control
A simple remote system control daemon using Python. For Windows/Linux/Mac.

###Description
This is a simple remote control daemon. You can send the command in server, and all the client that subscribing the same topic will run the command immediately and then return back the result to server.

###Features
1. one-to-many diagram, one server can remote control more than 1 client in the same time
2. Support multiple OS (Tested in Windows/Linux/Mac)

###Dependency
paho-mqtt

`pip install paho-mqtt`

###Install
`git clone https://github.com/iamgyz/remote-system-control.git`
`cd remote-system-control`
For server
`python3 server.py`
For client
`python3 client.py

###Configuration
Setting up the broker ip, port and your own topic in both server.conf/client.conf
The default broker will use 'iot.eclipse.org:1883' which is a public mqtt broker, you can use your own broker for the safety.
