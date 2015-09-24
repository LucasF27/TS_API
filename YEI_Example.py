__author__ = 'Wall-e'

## Communicating with a paired YEI 3-Space Sensor Wireless device and YEI
## 3-Space Sensor Dongle device wirelessly with Python 2.7, PySerial 2.6, and
## YEI 3-Space Python API
##  By Jason Ashworth


#*******************************************************************************#


#Set the BaudRate
baudrate = 115200

#set the Duration
# zero = infinite.
usrDur = 0

#Set the Interval, in Microseconds - Min = 1000
usrInt = 500000

#set How many seconds you want to stream for.
streamTime = 1


#***********************************************************************************#

import time
import threading
import datetime
import Queue

import threespace as ts_api



# device_list = ts_api.getComPorts(filter=ts_api.TSS_FIND_DNG)
device_list = ts_api.getComPorts(ts_api.TSS_FIND_DNG)

## Only one 3-Space Sensor device is needed so we are just going to take the
## first one from the list.
com_port = device_list[0]
dng_device = ts_api.TSDongle(com_port=com_port)


streaming = True
dt = datetime.datetime
dt = dt.now()
#print dt.date()
f = open('log' + str(dt.microsecond) + '.txt', 'w')
streamQueue = Queue.Queue(0)
f.write("Timestamp, Battery Level, Corrected Gyro X, Corrected Gyro Y, Corrected Gyro Z, Corrected Accel X, Corrected Accel Y, Corrected Accel Z, Corrected Compass X, Corrected Compass Y, Corrected Compass Z \n")

def logging2File():
    while streaming:
        if streamQueue.empty():
            continue
        else:
            g = streamQueue.get_nowait()
            if g is not None:
                ts = str(g[0])[:-1]
                data = str(g[1])
                f.write(ts +"," + data)
                f.write("\n")
            streamQueue.task_done()


def log(t):
    global streaming, streamQueue
    if dng_device is not None:
        print "There is a dongle"
        ## Now this assumes that the Wireless device and Dongle device have already
        ## been paired previously.
        wl_device = dng_device[1]

        if wl_device is not None:
            print "There is a device"
            # Setting up the streaming session
            # setStreamingTiming(interval, duration, delay) in microseconds
            wl_device.setStreamingTiming(interval=usrInt, duration=usrDur, delay=0)
            wl_device.setStreamingSlots(slot0='getBatteryPercentRemaining',
                                        slot1='getCorrectedGyroRate',
                                        slot2='getCorrectedAccelerometerVector',
                                        slot3='getCorrectedCompassVector'
                                        )
            wl_device.setFilterMode(mode=2)
            wl_device.baudrate = baudrate
            sl = wl_device.getStreamingSlots()
            print "Streaming Slots: ", sl
            st = wl_device.getStreamingTiming()
            print "Streaming Timing: ", st
            br = wl_device.baudrate
            print "Baud Rate: ", br
            # blah = raw_input("Press Enter to being Streaming and Logging")
            #Start the Thread
            t.start()
            wl_device.startStreaming()
            wl_device.startRecordingData()
            start_time = time.clock()
            while streaming and time.clock() - start_time < streamTime:
                #print wl_device.getLatestStreamData(timeout=4)
                streamQueue.put(wl_device.getLatestStreamData(timeout=0))
            streaming = False
            wl_device.stopStreaming()
            wl_device.stopRecordingData()
        ## Now close the port.
        dng_device.close()
        f.close()
    else:
        print "There was either No Dongle, or No Sensor connected to the Dongle."
        return


t = threading.Thread(target=logging2File)
log(t)
