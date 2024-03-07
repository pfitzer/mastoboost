import sys
from optparse import OptionParser

__version__ = '0.1'


def show_version(option, opt, value, parser):
    print("Version: %s" % __version__)
    sys.exit(0)


usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option("-r", "--register", action="store_true", dest="register", default=False, help="register app on a mastodon instance")
parser.add_option("-l", "--listen", action="store_true", dest="listen", default=False, help="start listening on a mastodon instance")
parser.add_option("-V", "--version", dest="version", help="show version and exit", action="callback",
                  callback=show_version)
(options, args) = parser.parse_args()