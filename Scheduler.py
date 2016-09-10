import logging
import os, errno

FORMAT = '%(asctime)-15s %(module)s:%(lineno)d %(message)s'

logging.basicConfig(format=FORMAT, datefmt='%Y/%m/%d %H:%M:%S')

logger = logging.getLogger()

isDebug = os.getenv('DEBUG', False)

if isDebug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


import platform
if platform.system() == 'Linux':
    from twisted.internet import epollreactor
    epollreactor.install()
else:
    from twisted.internet import selectreactor
    selectreactor.install()

from twisted.internet import reactor, threads


from yaml import load
from utils.VideoManager import video_manager
from twisted.internet.task import LoopingCall, deferLater, Clock
from utils.DownloadManager import download_manager

from taskrunner.InfoScanner import info_scanner
from taskrunner.FeedScanner import FeedScanner
from taskrunner.DmhyScanner import DmhyScanner
from taskrunner.AcgripScanner import AcgripScanner

class Scheduler:

    def __init__(self):
        fr = open('./config/config.yml', 'r')
        config = load(fr)
        self.interval = int(config['task']['interval']) * 60
        self.base_path = config['download']['location']
        self.feedparser = config['feedparser']
        try:
            if not os.path.exists(self.base_path):
                os.makedirs(self.base_path)
                logger.info('create base dir %s successfully', self.base_path)
        except OSError as exception:
            if exception.errno == errno.EACCES:
                # permission denied
                raise exception
            else:
                logger.error(exception)

    def start(self):
        self.start_scan_dmhy()
        deferLater(Clock(), int(self.interval / 2), self.start_scan_acgrip)

    def start_scan_dmhy(self):
        dmhy_scanner = DmhyScanner(self.base_path)
        dmhy_lc = LoopingCall(dmhy_scanner.scan_bangumi)
        dmhy_lc.start(self.interval)

    def start_scan_acgrip(self):
        acgrip_scanner = AcgripScanner(self.base_path)
        acgrip_lc = LoopingCall(acgrip_scanner.scan_bangumi)
        acgrip_lc.start(self.interval)

    def start_scan_feed(self):
        feed_scanner = FeedScanner(self.base_path)
        feed_scanner.start()


scheduler = Scheduler()

video_manager.set_base_path(scheduler.base_path)

def on_connected(result):
    # logger.info(result)
    scheduler.start()
    info_scanner.start()
    scheduler.start_scan_feed()


def on_connect_fail(result):
    logger.error(result)
    reactor.stop()

d = download_manager.connect()
d.addCallback(on_connected)
d.addErrback(on_connect_fail)

reactor.run()
