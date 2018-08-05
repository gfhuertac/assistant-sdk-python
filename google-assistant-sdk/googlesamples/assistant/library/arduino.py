import serial
import serial.tools.list_ports
from apscheduler.schedulers.background import BackgroundScheduler

def led():
    current = 0
    leds = [7,8,9]
    while True:
        yield leds[current]
        current = (current + 1) % len(leds)

class Arduino(object):

  def __init__(self):
      self.sched = BackgroundScheduler()
      self.sched.start()
      self.leds = led()
      self.previous = None
      self.current = None
      arduino_ports = [
          p.device
          for p in serial.tools.list_ports.comports()
          if 'ACM' in p.description
      ]
      self.arduino=None
      if arduino_ports and len(arduino_ports) == 1:
          self.arduino = serial.Serial(arduino_ports[0])

  def turn_on(self):
      if self.arduino is not None:
          self.arduino.write('7H'.encode()) 
          self.arduino.write('8H'.encode()) 
          self.arduino.write('9H'.encode()) 

  def turn_off(self):
      if self.arduino is not None:
          self.arduino.write('7L'.encode()) 
          self.arduino.write('8L'.encode()) 
          self.arduino.write('9L'.encode()) 

  def play(self):
      if self.previous is not None:
          self.arduino.write('{}L'.format(self.previous).encode())
      self.previous = self.current
      self.current = next(self.leds)
      self.arduino.write('{}H'.format(self.current).encode())

  def start(self):
      if self.arduino is not None:
          self.sched.add_job(self.play, 'interval', seconds=3, id='leds_show')

  def stop(self):
      if self.arduino is not None:
          self.sched.remove_job('leds_show')
