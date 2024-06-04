import time

from libs import MicroPyServer
from utils import flash

# in1 = Pin(13, Pin.OUT)
# in2 = Pin(12, Pin.OUT)
# in3 = Pin(27, Pin.OUT)
# in4 = Pin(26, Pin.OUT)

flash()
time.sleep(1)


def hello_world(request):
    html = """<!DOCTYPE html>
    <html>
       <head>
         <title>Web Server On Tank </title>
         <link rel="stylesheet" href="https://unpkg.com/chota@latest">
       </head>
      <body>
          <h1>Tank Wireless Web Server</h1>
      </body>
    </html>
    """
    server.send(html)


server = MicroPyServer()
""" add route """
server.add_route("/", hello_world)
""" start server """
server.start()

