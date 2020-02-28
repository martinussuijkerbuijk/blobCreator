"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import udp_client


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=5005,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  x = 0
  #for x in range(1):
  while True:

      if x == 5:
        client.send_message("/blender/toggle", 1)
        print("ON!")
        client.send_message("/blender/noise", random.random())
        print("Next")
        client.send_message("/blender/strength", random.random())
        time.sleep(1)
        print("Done!")
        x = 0
      else:
          client.send_message("/blender/toggle", 0)
          print("OFF!")
          client.send_message("/blender/noise", random.random())
          print("Next")
          client.send_message("/blender/strength", random.random())
          time.sleep(1)
          print("Done!")
          x += 1
