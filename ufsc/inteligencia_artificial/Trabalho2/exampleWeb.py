from random import randint
import json
import requests
import time

episodes = 10
current_episode = 0
URL = "http://localhost:8081/?state=0"
response = requests.get(url=URL) #get the initial state from the server
state = response.json()['state'] #interpreting the response value
print("Initial state: ", state)
done = False
while current_episode<episodes:
   a = randint(0,1) #choose a random action
   URL = "http://localhost:8081/?control=" + str(a) #builds the web address
   start = time.time()
   response = requests.get(url=URL).json()  #submit the control signal to the webserver
   print(f'{(time.time() - start):.2} seconds')
   #interpreting the response values:
   new_state = response['state']
   reward = response['reward']
   done = response['done']
   print("Action ", a, " in state ", state, " leads to state", new_state, " and returns reward ", reward)   
   state = new_state #update the state variable to the new achieved state
   if done==True: #if the episode is over
      current_episode+=1 #start a new episode
      
               

