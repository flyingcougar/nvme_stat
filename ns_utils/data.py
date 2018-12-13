

import logging
import os
import re

core_path = "/sys/block"
nvm_dev_pattern = "nvm"


def check_devices(raw_dev_list):
    dev_list = [dev.strip() for dev in raw_dev_list.split(',')]
    if not len(dev_list):
        raise ValueError('Device list is empty')

    if len(dev_list) == 1 and dev_list[0] == "all":
        return detect_all_devs(nvm_dev_pattern)
    else:
        for dev in dev_list:
            if not os.path.isdir(os.path.join(core_path, dev)):
                raise ValueError('Device {} does not exist'.format(dev))


def detect_all_devs(pattern):
    return [dev for dev in os.listdir(core_path) if re.match(pattern,dev)]

def gather(nvm_dev_list):
    if not len(nvm_dev_list):
        logging.fatal("[data]: Empty device list")


