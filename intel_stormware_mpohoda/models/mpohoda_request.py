# Copyright 2021 intelligenti.io - Tosin Komolafe
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime
import xml.etree.ElementTree as ET
import logging
import base64
import requests

_logger = logging.getLogger(__name__)


def dump_date(name, date):
    date_dump = str(date)

    date_dump_ = ET.Element(name)
    date_dump_.text = date_dump
    return date_dump_


def dump_string(name, string):
    string_dump = str(string)

    string_dump_ = ET.Element(name)
    string_dump_.text = string_dump
    return string_dump_


def load_boolean(boolean_dump):
    return boolean_dump.text == 'true'


def load_date(date_dump):
    datetime_ = datetime.datetime.strptime(date_dump.text, '%Y-%m-%d')
    return datetime_.date()


def load_double(double_dump):
    return float(double_dump.text)


def load_float(float_dump):
    return float(float_dump.text)


def load_integer(integer_dump):
    return int(integer_dump.text)


def load_string(string_dump):
    return string_dump.text


class MpohodaAPI():
    
    def __init__(self, host, port, user, password, registry):
        self.host = host
        self.port = port #666
        self.url = self.host + ':' + str(self.port) + '/xml'
        self.user = user #Admin
        self.password = password #Admin:1Juzepe1
        self.registry = registry #05744610
        self.authorization_code = ''
        if self.user and self.password:
            code = self.user+':'+self.password
            self.authorization_code =  base64.b64encode(code.encode('utf-8')).decode('utf-8')
    

    def get_payment_types(self):
        payload = """<?xml version="1.0" encoding="Windows-1250"?>
                        <dat:dataPack version="2.0" id="Ex008" ico="%s" application="StwTest" note="Žádost o seznamy" 
                        xmlns:dat="http://www.stormware.cz/schema/version_2/data.xsd" 
                        xmlns:lst="http://www.stormware.cz/schema/version_2/list.xsd">

                            <dat:dataPackItem id="SC001" version="2.0">
                        <lst:listBankAccountRequest version="2.0" bankAccountVersion="2.0">
                        <lst:requestBankAccount> </lst:requestBankAccount>
                        </lst:listBankAccountRequest>
                            </dat:dataPackItem>

                    </dat:dataPack>"""%self.registry
        headers = {
            'Stw-Authorization': 'Basic {}'.format(self.authorization_code),
            'Authorization': 'Basic {}'.format(self.authorization_code),
            'Content-Type': 'text/plain',
        }

        response = requests.post(self.url, data=payload.encode('Windows-1250'), headers=headers)
        if response.status_code == 200:
            bank_ids = []
            _logger.info(self.authorization_code)
            _logger.info(payload)
            _logger.info(response)
            _logger.info(response.text)
            tree = ET.ElementTree(ET.fromstring(response.text))
            root = tree.getroot()
            for bank_id in root.findall('bka:ids'):
                _logger.info(bank_id)
                _logger.info(bank_id.text)
                bank_ids.append(bank_id)
            return bank_ids
        return False



        

        



