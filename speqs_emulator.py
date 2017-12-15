import serial
import time

speed_up = 10

ser = serial.Serial('/dev/ttyUSB1', 115200)

dummy_frame = ''.join([chr(i) for i in range(241)])

state = 'INIT'

ser.flushInput()

print "Read"
data = ser.read(5)

ser.flushInput()

while True:
    if state == 'INIT':
        print "State INIT, sleep 60"
        time.sleep(60/speed_up)
        print "State INIT, write frame"
        ser.write(dummy_frame)
        print "State INIT, frame written"
        print ''
        state = 'HK'
    elif state == 'HK':
        print "State HK, sleep 60"
        time.sleep(60/speed_up)
        print "State HK, write frame"
        ser.write(dummy_frame)
        print "State HK, frame written"
        print ''
        state = 'THERMAL'
    elif state == 'THERMAL':
        print "State THERMAL, sleep 60"
        time.sleep(60/speed_up)
        print "State THERMAL, write frame"
        ser.write(dummy_frame)
        print "State THERMAL, frame written"
        print ''
        state = 'SYS_CAL'
    elif state == 'SYS_CAL':
        print "State SYS_CAL, sleep 60"
        time.sleep(60/speed_up)
        print "State SYS_CAL, write frame"
        ser.write(dummy_frame)
        print "State SYS_CAL, frame written"
        print ''
        state = 'PROFILE'
    elif state == 'PROFILE':
        print "State PROFILE, sleep 60"
        time.sleep(60/speed_up)
        print "State PROFILE, write frame"
        ser.write(dummy_frame)
        print "State PROFILE, frame written"
        print ''
        state = 'EXPERIMENT'    
    elif state == 'EXPERIMENT':
        print "State EXPERIMENT, sleep 600"
        time.sleep((60 * 10) / speed_up)
        print "State EXPERIMENT, write frame"
        ser.write(dummy_frame)
        print "State EXPERIMENT, frame written"
        print ''
        state = 'DATA'
    elif state == 'DATA':
        ser.flushInput()
        print "State DATA, sleep 2"
        time.sleep(2 / speed_up)
        print "State DATA, write frame"
        ser.timeout = 1
        for i in range(5000):
            ser.write(dummy_frame)
            print ser.read(2), i
        print "State DATA, frame written"
        print ''
        state = 'OUT'
    elif state == 'OUT':
        break


ser.close()
