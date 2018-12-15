#!/usr/bin/env python

"""nvme_stat
Usage:
    nvme_stat (-h | --help)
    nvme_stat get [--dev=<devices>]

Options:
    -h --help           Show help
    --dev=<devices>     List of comma separated nvme devices to gather stats from [default: all]
"""  # noqa: E501


from docopt import docopt
import os
import logging
import sys
from ns_utils import data


def setup_logging():
    level = os.getenv("NVM_STAT_LOG", logging.INFO)
    logging.basicConfig(level=level)


def main():
    args = docopt(__doc__)
    setup_logging()
    if args["get"]:

        dev_list = [dev.strip() for dev in args["--dev"].split(',')]
        collector = data.NVMStats(dev_list)
        if not len(collector.get_devices()):
            logging.error("No nvme devices detected, exiting")
        collector.gather_all_dev_stats()
        collector.print_stats()





if __name__ == "__main__":
    try:
        main()

    except RuntimeError as e:
        logging.error(e)
        sys.exit(1)



