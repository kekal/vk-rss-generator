import logging
import os
from time import strftime, gmtime
import sys


def get_wrk_path(argv):
    if not argv or not os.path.isdir(argv[0]):
        return os.path.dirname(__file__)

    return argv[0]


log_path = get_wrk_path(sys.argv[1:])

log_path = os.path.join(log_path, strftime("%Y.%m.%d ", gmtime())+'log.log')
logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(format=u'[%(asctime)s] %(message)s', level=logging.DEBUG, filename=log_path)
