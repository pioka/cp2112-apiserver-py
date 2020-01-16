import os
from ctypes import *

dllPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SLABHIDtoSMBus.dll")
dll = cdll.LoadLibrary(dllPath)

#dll.HidSmbus_GetNumDevices.restype = c_int
#dll.HidSmbus_GetNumDevices.argtypes = (byref(c_uint), c_ushort, c_ushort)
