
from picamera import PiCamera
from time import sleep
from datetime import datetime
from gpiozero import Button
from subprocess import Popen,PIPE
import glob
import ptvsd

print("waiting for debugger...")
ptvsd.enable_attach(secret='JTG')
ptvsd.wait_for_attach()
print("debugger attached")


#procs=[]
photoPath = '/home/pi/photobooth/'

def createMontage(baseName):
    path = baseName + '*.jpg'
    files = glob.glob(baseName + '__image*.jpg')
    files.sort()
    cmd = 'montage '
    cmd += ' '.join(files)
    cmd += ' -geometry 480x270+10+10 -shadow '
    cmd += baseName + '_montage.jpg'
    #FIXME add to log
    print(cmd)
    # fire and forget.. just let the process happen as the os see's fit
    proc = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)

    
try:

    camera = PiCamera()
    button = Button(17)

    camera.rotation = 180
    camera.resolution = (1920,1080)
    camera.framerate = 30

    #camera.start_preview()
    #camera.start_recording(photoPath + '%s__vid.h264' %(baseTime))
    
    #while True:
    if True:

        camera.annotate_text = "Press Button!!"
        camera.annotate_text_size = 50
    
        button.wait_for_press()
        baseTime = str(datetime.now().strftime('%Y-%m-%d_%H%M%S'))
        
        for i in range(4):
            camera.annotate_text = "Taking picture " + str(i+1)
            sleep(3)
            camera.annotate_text = ""
            fileName = '%s%s__image%d.jpg' %(photoPath,baseTime,i+1)
            camera.capture(fileName)
            print("taking picture " + fileName)

        createMontage(photoPath + baseTime)


finally:
    print ("finally")
    #camera.stop_recording()    
    #camera.stop_preview()

