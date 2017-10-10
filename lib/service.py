
import time
import xbmc
import xbmcaddon

scriptAddon = xbmcaddon.Addon('script.cinemavision')

def LOG(msg):
    xbmc.log(msg, xbmc.LOGNOTICE)

class Service(xbmc.Monitor):
    def __init__(self):
        self._pollInterval = 300  #5 minutes
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
            self.updateContent()

    def poll(self):
        try:
            interval = int(scriptAddon.getSetting('service.database.update.interval')) * 3600  # 1 Hour
        except Exception:
            return

        last = self.getUpdateTime()
        now = time.time()

        if now - last < interval:
            return

        self.updateContent()

    def updateCVContent(self):
        if scriptAddon.getSetting('service.database.update.kodiStartup') == 'true':
            self.updateContent()

    def updateContent(self):
        self.markUpdateTime()
        xbmc.executebuiltin('RunScript(script.cinemavision,update.database)')

    def markUpdateTime(self):
        now = int(time.time())
        scriptAddon.setSetting('service.update.last', str(now))

    def getUpdateTime(self):
        try:
            return int(scriptAddon.getSetting('service.update.last'))
        except Exception:
            pass

        return 0

Service()
