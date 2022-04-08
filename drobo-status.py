#!/usr/bin/env python

import struct
import sys
import json
import xml.etree.ElementTree as ET
from socket import (
    socket as Socket,
    AF_INET, SOCK_STREAM,
)

from flask import Flask
from flask import jsonify
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True




# Reading Config
from configparser import RawConfigParser
import codecs
parser = RawConfigParser()
import codecs
parser.read('drobo-status.cfg', encoding='utf-8')
host = parser.get('drobo', 'host')


CHUNK_SIZE = 2048

def get_status(host):
    drobo_socket = Socket(
        AF_INET,
        SOCK_STREAM,
    )
    drobo_socket.connect((host, 5000))
    def read_bytes(message_length):
        chunks = []
        bytes_recd = 0
        while bytes_recd < message_length:
            chunk = drobo_socket.recv(min(message_length - bytes_recd, CHUNK_SIZE))
            if not chunk:
                raise RuntimeError("Could not read bytes")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)
    initial_message = read_bytes(16)
    assert len(initial_message) == 16
    status_packet_length = struct.unpack('>i', initial_message[-4:])[0]
    status_message = read_bytes(status_packet_length)
    status_message = struct.unpack('{0}sx'.format(status_packet_length-1), status_message)
    status_message = status_message[0].strip()
    doc = ET.fromstring(status_message)
    return doc

def calc_size(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


class DroboChecker():
    def data_drobo(self, host):
        self.update_node = get_status(host)
        def get_int(element_name):
            return int(self.update_node.find(element_name).text)
        total_capacity = get_int('mTotalCapacityProtected')
        used_capacity = get_int('mUsedCapacityProtected')
        free_capacity = get_int('mFreeCapacityProtected')
        def get_str(element_name):
            return str(self.update_node.find(element_name).text)
        name = get_str('mName')
        serial = get_str('mSerial')
        firmware = get_str('mVersion')
        def _get_drives(self):
            slots_node = self.update_node.find('mSlotsExp')
            drive_list = list()
            for child_node in list(slots_node):
                slot = child_node.find('mSlotNumber').text
                status = child_node.find('mStatus').text
                dcapacity = child_node.find('mPhysicalCapacity').text
                drive_data = {"sid": int(slot), "status": int(status), "capacity": calc_size(int(dcapacity)) }
                drive_list.append(drive_data)
            return drive_list
        drobo_data = '{"name":"' + name + '", "serial": "' + serial + '","firmware-version": "' + firmware + '","disk-total": "' + (calc_size(int(total_capacity))) + '","disk-used": "' + (calc_size(int(used_capacity))) + '","disk-free": "' + (calc_size(int(free_capacity))) + '", "drives": ' + json.dumps(_get_drives(self)) + '}'
        return drobo_data
         

@app.route("/",  methods=['GET'])
def main():
    dc = DroboChecker()
    return dc.data_drobo(host)

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0')
