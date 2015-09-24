__author__ = 'Wall-e'

import threespace as ts
import time

print 'hello!'

ts_ports = ts.getComPorts(ts.TSS_FIND_DNG)
print ts_ports

dng = ts.TSDongle(com_port=ts_ports[0][0])
if dng is not None:
    s1 = dng[1]
    # quat = s1.getTaredOrientationAsQuaternion()
    s1.setStreamingTiming(500,0,0)
    print s1.getStreamingSlots()
    print s1.getStreamingTiming()

    s1.startStreaming()
    s1.startRecordingData()
    i = 0
    while i < 10:
        # time.sleep(0.5)
        i += 1
        print s1.getLatestStreamData(timeout=10)
    s1.stopStreaming()
    s1.stopRecordingData()
    dng.close()

