import datetime
import time
from threading import Timer


class TimedEvent:
    ''' TimedEvent receives entime as the time limit to continue executing 
        the callback passed'''
    def __init__(self, endtime, callback):
        self.endtime = endtime
        self.callback = callback
    
    def ready(self):
        ''' If the self.endtime has passed the callback can be
            executed '''
        return self.endtime <= datetime.datetime.now()


class Timer:
    def __init__(self):
        self.events = []
    
    def call_after(self, delay, callback):
        ''' Receives and callback and delay to create a new TimedEvent
            and add it to self.events list'''
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=delay)
        self.events.append(TimedEvent(end_time, callback))
    
    def run(self):
        while True:
            # If there are ready() events yield it in an iterator
            ready_events = (e for e in self.events if e.ready())
            # Iterate through the ready callbacks
            for event in ready_events:
                # Call the callback
                event.callback(self)
                self.events.remove(event)

           
def format_time(message, *args):
    # Shows the current time in certain format
    now = datetime.datetime.now().strftime("%I:%M:%S")
    print(message.format(*args, now=now))

def one(timer):
    format_time("{now}: Called One")

def two(timer):
    format_time("{now}: Called Two")

def three(timer):
    format_time("{now}: Called Three")

class Repeater:
    def __init__(self):
        self.count = 0
        
    def __call__(self, timer):
        format_time("{now}: repeat {0}", self.count)
        self.count += 1
        # pass itself again to call_after as a callable object
        timer.call_after(1, self)


timer = Timer()
timer.call_after(1, one)
timer.call_after(2, one)
timer.call_after(2, two)
timer.call_after(3, two)
timer.call_after(3, three)
timer.call_after(5, three)
# Creates a repeater object and pass it to call_after
timer.call_after(1, Repeater())
format_time("{now}: Starting")

# If the time more than one callback has passed call them at the same time
# This sleep defines it
time.sleep(10)

# Repeater's call is not effected by the sleep because it calls 
# timer.call_after inside itself (pseudo-infinite-recursion)
timer.run()