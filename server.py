from ctypes import *
from flask import Flask, request
from flask_cors import CORS
from SLABHIDtoSMBUS import HidSmbus

CP2112_VID = c_ushort(0x10C4)
CP2112_PID = c_ushort(0xEA90)

cp2112 = HidSmbus()
devicePtr = pointer(c_int())
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return "OK"

@app.route('/WriteLatch')
def WriteLatch():
  port = int(request.args.get("port"))
  value = int(request.args.get("value"))

  if (port < 0 or port > 7):
    return "Bad Request", 400

  mask = c_byte(1 << port)
  if (value == 0):
    cp2112.WriteLatch(devicePtr, c_byte(0x00), mask)
  else:
    cp2112.WriteLatch(devicePtr, c_byte(0xFF), mask)
  return "OK"


if __name__ == '__main__':
  refNumDevices = c_uint()
  cp2112.GetNumDevices(byref(refNumDevices), CP2112_VID, CP2112_PID)

  if refNumDevices.value != 1:
    print("ERROR: No Device Connected")
    exit()

  # Open device
  ret = cp2112.Open(byref(devicePtr), c_uint(0), CP2112_VID, CP2112_PID)
  print(ret)

  # Turn on all GPIO port
  ret = cp2112.SetGpioConfig(devicePtr, c_byte(0xFF), c_byte(0x00), c_byte(0x00), c_byte(0x00))
  print(ret)
  ret = cp2112.WriteLatch(devicePtr, c_byte(0x00), c_byte(0xFF))
  print(ret)

  app.run()
