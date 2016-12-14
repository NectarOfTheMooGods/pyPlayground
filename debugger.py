
import ptvsd
import sys
#import signal
#import time

def attachDebugger():
    
    try:
        print("waiting for debugger...")
        ptvsd.enable_attach(secret='JTG')
        ptvsd.wait_for_attach()
        print("debugger attached")

    except( KeyboardInterrupt, SystemExit):
        print("debugger - KeyboardInterrupt")
        raise
    except BaseException as e:
        print("error trying to attach Debugger -" + str(e))
        sys.exit(-1)
    
