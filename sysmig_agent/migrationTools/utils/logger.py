from codecs import encode
import logging
import logging.handlers
import os

from sysmig_agent.migrationTools.utils.config import PathConf


class Logger(object):
    def __init__(self, name, ch_level=logging.INFO, fh_level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        log_file = PathConf.log_file
        ch = logging.StreamHandler()
        ch.setLevel(ch_level)
        fh = logging.handlers.RotatingFileHandler(log_file,
                                                  encoding='utf-8',
                                                  maxBytes=1024 * 1024 * 10,
                                                  backupCount=5,
                                                  delay=True)
        fh.setLevel(fh_level)
        if not self.logger.handlers:
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)

        chfmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fhfmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(chfmt)
        fh.setFormatter(fhfmt)

    ## make sure the log dir is exist, if not, create it
    def _check_log_dir(self):
        log_dir = PathConf.log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def info(self, msg):
        self._check_log_dir()
        self.logger.info(msg)

    def debug(self, msg):
        self._check_log_dir()
        self.logger.debug(msg)

    def warning(self, msg):
        self._check_log_dir()
        self.logger.warning(msg)

    def error(self, msg):
        self._check_log_dir()
        self.logger.error(msg)

    def critical(self, msg):
        self._check_log_dir()
        self.logger.critical(msg)
