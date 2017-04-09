import detectModule, gameModule, os, platform, sys

detectModule.runThread()
gameModule.main(detectModule.curFreq)
detectModule.terminate()