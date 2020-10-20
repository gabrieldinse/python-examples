import gym
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlsplit
import json


var = -1
env = None


#**** Web server ***
# HTTPRequestHandler class
# curl http://localhost:8081?control=1
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
  
  # GET
  def getState(self):
     global env
     state = env.state
     #gerar lista com o estado
     l = []
     for i in state:
        l.append(i)
     return l

  def do_GET(self):
        global var
        global env
        o = urlparse(self.path) 
        answer = '' 
        params = parse_qs(urlsplit(self.path).query)
        params_dict = dict(params)
        if 'control' in params_dict:
           control = int(params_dict['control'][0])
           state, reward, done, _ = env.step(control)  #atualiza variaveis globais de estado
           var = control
           state = self.getState()
           answer = json.dumps({'state':state,'reward':reward,'done':done})
           if done==True:
              reset_environment(env)
        if 'state' in params_dict: #http://localhost:8081?state=0
           answer = json.dumps({'state':self.getState()})
   
    
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()  
        self.wfile.write(bytes(answer,"utf-8"))    
        return


server_address = ('127.0.0.1', 8081)
httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
def webserver():
   global httpd
   httpd.serve_forever()

####################################

def environment(envir):
   global var
   global env 
   env = envir
   while(1):
      while(var!=0): #var==0 means that a new state has been reached
         env.render()      
      var = -1
   env.close()

#########################

def start_environment(envir):
   global env
   env = envir
   start_environment_thread()

def reset_environment(envir):
   global env
   env = envir
   env.reset()

def start_environment_thread():   
   global env
   x = threading.Thread(target=environment, args=(env,))
   x.start()


y = threading.Thread(target=webserver)
y.start()


