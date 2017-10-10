
import xbmc
import xbmcaddon

scriptAddon = xbmcaddon.Addon('script.cinemavision')

def LOG(msg):
    xbmc.log(msg, xbmc.LOGNOTICE)

class Service(xbmc.Monitor):
    def __init__(self):
        self._pollInterval = 60  # One minute
        LOG('SERVICE START')
        self.start()
        LOG('SERVICE STOP')

    def start(self):
        self.onKodiStarted()
        while not self.waitForAbort(self._pollInterval):
            self.poll()

    def onKodiStarted(self):
        self.updateCVContent()

    def onScanFinished(self, library):
        if library == 'video' and scriptAddon.getSetting('service.database.update.scanFinished') == 'true':
            xbmc.executebuiltin('RunScript(script.cinemavision,update.database)')

    def poll(self):
        pass

    def updateCVContent(self):
        if scriptAddon.getSetting('service.database.update.kodiStartup') == 'true':
            xbmc.executebuiltin('RunScript(script.cinemavision,update.database)')

Service()
