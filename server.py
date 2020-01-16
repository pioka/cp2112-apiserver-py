from ctypes import *
import SLABHIDtoSMBUS

CP2112_VID = c_ushort(0x10C4)
CP2112_PID = c_ushort(0xEA90)

numDevices = c_uint(0)

SLABHIDtoSMBUS.dll.HidSmbus_GetNumDevices(byref(numDevices), CP2112_VID, CP2112_PID)
print(numDevices)
