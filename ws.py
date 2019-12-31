#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 16:38:46 2019

@author: parashar
"""


from websocket import create_connection
import ssl
import time

for _ in range(1,5):
    
    ws = create_connection("wss://echo.websocket.org", sslopt={"cert_reqs": ssl.CERT_NONE})
    for i in range(1,10):
        ws.send("{}--python hello {}".format(time.time(),i))
    print ( "{}--{}".format(time.time() ,ws.recv()))
    ws.close()
