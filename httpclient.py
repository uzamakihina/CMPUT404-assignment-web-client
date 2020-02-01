#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse, urlencode
import time 




def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        
        addr = (host,port) 
        print(addr)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(addr)
        

        return
        
        

    def get_code(self, data):
        return None

    def get_headers(self,data):
        
        print(data.decode('utf-8').split('\r\n'))



    def get_body(self, data):
        
        lines = data.splitlines()

        start = 0
        while start < len(lines):
            if lines[start] != '':
                start += 1
            else:
                break

        return_string = ""

        for i in range(start+1,len(lines)):
            
            return_string += (lines[i] + '\n')

        return return_string
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):

        data = urlparse(url)
        port = data.port
        if port == None:
            port = 80
        path = data.path
        host = data.hostname
        
        self.connect(host, port)


        body = 'GET /'+path+ ' HTTP/1.1\r\n'
        body += 'Host: '+host+'\r\n'
        body += 'Accept: */*\r\n'
        body += 'User-Agent: curl/7.54.0\r\n'
        body += 'Connection: close\r\n\r\n'
        
        self.sendall(body)
        rply = self.recvall(self.socket)
        rply_body = self.get_body(rply)
        code = int(rply.split()[1])
        self.close()
        return HTTPResponse(code, rply_body)

    def POST(self, url, args=None):

        data = urlparse(url)
        port = data.port
        if port == None:
            port = 80
        path = data.path
        host = data.hostname
        self.connect(host, port)
        body = "POST /"+path+ " HTTP/1.1\r\n"
        body += "Host: "+host+"\r\n"
        body += "Accept: */*\r\n"
        body += "Content-Type: application/x-www-form-urlencoded\r\n"
        body += "Connection: close\r\n"

        if args == None:
            body += "Content-Length: 0\r\n\r\n"
        else:
            body += "Content-Length: "+str(len(urlencode(args)))+"\r\n\r\n"
            body += urlencode(args)
        



        
        self.sendall(body)
        rply = self.recvall(self.socket)
        rply_body = self.get_body(rply)
        code = int(rply.split()[1])

        return HTTPResponse(code, rply_body)

    def command(self, url, command="GET", args=None):
       
        
        if (command == "POST"):

            return self.POST( url, args )
        else:
            
            
            
            self.GET( url, args )
            
            
            
            

            # reply = self.recvall(self.socket)


            
           

    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
   
    
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(sys.argv)
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
