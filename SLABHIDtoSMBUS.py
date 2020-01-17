import os
import struct
from ctypes import *

#dll.HidSmbus_GetNumDevices.restype = c_int
#dll.HidSmbus_GetNumDevices.argtypes = (byref(c_uint), c_ushort, c_ushort)

class HidSmbus:
  I2C_RECEIVE_BUFFER_SIZE = c_byte(61)

  def __init__(self):
    """__init__

    アーキテクチャ(32bit?64bit?)を判定し、対応するDLLをロードする
    """

    if struct.calcsize(str('P')) * 8 == 64:
      arch = "x64"
    else:
      arch = "x86"

    dllPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "native", arch, "SLABHIDtoSMBus.dll")
    self.__dll = cdll.LoadLibrary(dllPath)

  def GetNumDevices(self, refNumDevices:pointer, vid:c_ushort, pid:c_ushort):
    """GetNumDevices
      refNumDevice is c_uint pointer
    """

    ret = self.__dll.HidSmbus_GetNumDevices(refNumDevices, vid, pid)
    return ret

  def Open(self, refDevice:pointer, deviceNum:c_uint, vid:c_ushort, pid:c_ushort):
    """Open
      refDevice is c_int pointer
    """

    ret = self.__dll.HidSmbus_Open(refDevice, deviceNum, vid, pid)
    return ret

  def SetGpioConfig(self , refDevice:pointer, direction:c_byte, mode:c_byte, function:c_byte, clkDiv:c_byte):
    """SetGpioConfig
    """

    ret = c_int()
    ret = self.__dll.HidSmbus_SetGpioConfig(refDevice, direction, mode, function, clkDiv)
    return ret

  def WriteLatch(self, refDevice:pointer, latchValue:c_byte, latchMask:c_byte):
    """WriteLatch
    """
    ret = c_int()
    ret = self.__dll.HidSmbus_WriteLatch(refDevice, latchValue, latchMask)
    return ret

  def WriteRequest(self, refDevice:pointer, slaveAddress:c_byte, refBuffer:pointer, numBytesToWrite:c_ushort):
    """WriteRequest
    Note:
      refBuffer: is c_byte pointer
    """

    ret = self.__dll.HidSmbus_WriteRequest(refDevice, slaveAddress, refBuffer, numBytesToWrite)
    return ret

  def ReadRequest(self, refDevice:pointer, slaveAddress:c_byte, numBytesToRead:c_ushort):
    """ReadRequest
    """

    ret = self.__dll.HidSmbus_ReadRequest(refDevice, slaveAddress, numBytesToRead)
    return ret

  def ForceReadRequest(self, refDevice:pointer):
    """ForceReadRequest
    """

    ret = self.__dll.HidSmbus_ForceReadRequest(refDevice, self.I2C_RECEIVE_BUFFER_SIZE)
    return ret

  def GetReadResponse(self, refDevice:pointer, refStatus:pointer,  refBuffer:pointer, refNumBytesRead):
    """GetReadResponse
      refStatus is c_byte pointer
      refBuffer is c_byte pointer
      refNumBytesRead is c_byte pointer
    """

    ret = self.__dll.HidSmbus_GetReadResponse(refDevice, refStatus, refBuffer, self.I2C_RECEIVE_BUFFER_SIZE, refNumBytesRead)
    return ret
