import serial
ser = serial.Serial('/dev/tty.usbserial-A901QN3E')
print(ser.name)         # check which port was really used
ser.write(b'a')     # write a string
ser.close()             # close port