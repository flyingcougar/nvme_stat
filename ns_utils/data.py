

import logging
import os
import re
import threading

core_path = "/sys/block"
nvm_dev_pattern = "nvm"


class NVMStats:
    def __init__(self, init_devs):
        self.lock = threading.Lock()
        self.stats = {}
        self.core_path = "/sys/block"
        self.nvm_dev_pattern = "nvm"

        if not len(init_devs):
            raise ValueError('Device list is empty')

        if len(init_devs) == 1 and init_devs[0] == "all":
            self.devices = [dev for dev in os.listdir(self.core_path) if
                            re.match(self.nvm_dev_pattern, dev)]
        else:
            for dev in init_devs:
                if not os.path.isdir(os.path.join(self.core_path, dev)):
                    raise ValueError('Device {} does not exist'.format(dev))
            self.devices = init_devs

    def get_devices(self):
        return self.devices

    def gather_all_dev_stats(self):
        new_stats = {}
        ## TODO: use separate threads per device

        for device in self.devices:
            new_stats[device] = self.__gather_stats(device)
        self.lock.acquire()
        self.stats = new_stats
        self.lock.release()


    def __gather_stats(self,device):
        dev_stats = {}
        #get qeueu id's
        queue_path = os.path.join(self.core_path, device, "mq")
        queue_list = [q for q in os.listdir(queue_path)]
        for queue in queue_list:
            dev_stats[queue] = {}
            cpus_path = os.path.join(queue_path, queue)
            cpus_list = [c for c in os.listdir(cpus_path)
                        if os.path.isdir(os.path.join(cpus_path, c))]
            for cpu in cpus_list:
                cpu_path = os.path.join(cpus_path, cpu)
                io = self.__get_cpu_comp_io(cpu_path)
                dev_stats[queue][cpu] = io
        return dev_stats


    def __get_cpu_comp_io(self, cpu_path):
        fd = open(os.path.join(cpu_path, "completed"), "r")
        raw_data = fd.read()
        fd.close()
        return sum([int(x) for x in raw_data.split(' ')])

    #stats[device][queue_id][cpu] = io num
    def print_stats(self):
        self.lock.acquire()
        sts = self.stats
        self.lock.release()
        for dev in sts:
            print("Device \"{}\" info:".format(dev))
            cores = 0
            for q in sts[dev]:
                cores = cores + len(sts[dev][q])
            print("Queue count: {}\t Core count: {}".format(len(sts[dev]), cores))
            line = ""
            for q in sts[dev]:
                line = "Q:{}\t".format(q)
                for c in sts[dev][q]:
                    line = line + c + ": " + str(sts[dev][q][c]) + "\t"
                print(line)









