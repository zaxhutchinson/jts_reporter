import configparser
import logging

class Cfg:
    def __init__(self, cfg_filename):

        self.config_filename = cfg_filename
        self.config = configparser.ConfigParser()
        self.config.read(cfg_filename)

    def GetCfg(self, *args):

        d = self.config

        for a in args:
            if a in d:
                d = d[a]
            else:
                return None
        return d

