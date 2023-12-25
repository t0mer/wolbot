import os
import re
import yaml
import shutil
import datetime
import subprocess
from os import path
from loguru import logger

class Wol:
    def __init__(self):
        self.computers = []
        self.config = "config/config.yaml"
        




    def get_computers(self):
        try:
            logger.info("computers kids list")
            if not path.exists(self.config_path):
                shutil.copy('config.yaml', self.config_path)
            with open("config/config.yaml",'r',encoding='utf-8') as stream:
                try:
                    self.computers = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    logger.error(exc)
        except Exception as e:
            logger.error(str(e))


    def ping(self,host):
        p = subprocess.Popen("fping -C1 -q "+ host +"  2>&1 | grep -v '-' | wc -l", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        status = re.findall('\d+', str(output))[0]
        if status=="1":
            return 'online'
        else:
            return 'offline'




