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

@app.route('/I2CSend')
def I2CSend():
  address = int(request.args.get("address"), 16)
  data = bytes.fromhex(request.args.get("data"))
  length = len(data)

  BufferArray = c_byte * length

  dataArray = [d for d in data]
  buffer = BufferArray(*dataArray)

  ret = cp2112.WriteRequest(devicePtr, c_byte(address), byref(buffer), c_ushort(length))
  return "Status: "+str(ret)

@app.route('/I2CReceive')
def I2CReceive():
  address = int(request.args.get("address"), 16)
  length = int(request.args.get("length"))

  BufferArray = c_byte * cp2112.I2C_RECEIVE_BUFFER_SIZE_INT
  buffer = BufferArray()

  status = c_byte()
  numBytesRead = c_byte()

  cp2112.ReadRequest(devicePtr, c_byte(address), c_ushort(length))
  cp2112.ForceReadResponse(devicePtr)
  cp2112.GetReadResponse(devicePtr, byref(status), byref(buffer), byref(numBytesRead))

  value = 0
  for i in range(length):
    value = (value << 8) | (buffer[i] & 0xFF)

  return str(value)


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
