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
        self.default_url = self.host + ':' + str(self.port)
        self.url = self.default_url + '/xml'
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
            id = []
            ids = []
            bank_ids = []
            #_logger.info(self.authorization_code)
            # _logger.info(payload)
            # _logger.info(response)
            _logger.info(response.text)
            tree = ET.ElementTree(ET.fromstring(response.text))
            root = tree.getroot()
            # _logger.info([elem.tag for elem in root.iter()])
            for bank_id in root.iter('{http://www.stormware.cz/schema/version_2/bankAccount.xsd}id'):
                id.append(bank_id.text)
            for bank_id in root.iter('{http://www.stormware.cz/schema/version_2/bankAccount.xsd}ids'):
                ids.append(bank_id.text)
            
            if id and ids:
                for i in range(0, len(ids)):
                    bank_ids.append((id[i], ids[i]))
            return bank_ids
        return False
    
    
    def get_invoice_types(self):
        payload = """<?xml version="1.0" encoding="Windows-1250"?>
                        <dat:dataPack version="2.0" id="Ex008" ico="%s" application="StwTest" note="Žádost o seznamy" 
                        xmlns:dat="http://www.stormware.cz/schema/version_2/data.xsd" 
                        xmlns:lst="http://www.stormware.cz/schema/version_2/list.xsd">

                            <dat:dataPackItem id="SC001" version="2.0">
                                <lst:listNumericSeriesRequest version="1.1">
                                </lst:listNumericSeriesRequest>
                            </dat:dataPackItem>

                        </dat:dataPack>"""%self.registry
                        # <lst:agendas>
                        #     <lst:agenda>issuedInvoice</lst:agenda>
                        # </lst:agendas>
        headers = {
            'Stw-Authorization': 'Basic {}'.format(self.authorization_code),
            'Authorization': 'Basic {}'.format(self.authorization_code),
            'Content-Type': 'text/plain',
        }

        response = requests.post(self.url, data=payload.encode('Windows-1250'), headers=headers)
        if response.status_code == 200:
            invoice_ids = []
            #_logger.info(self.authorization_code)
            # _logger.info(payload)
            # _logger.info(response)
            _logger.info(response.text)
            tree = ET.ElementTree(ET.fromstring(response.text))
            root = tree.getroot()
            # _logger.info([elem.tag for elem in root.iter()])
            for series in root.iter('{http://www.stormware.cz/schema/version_2/list.xsd}itemNumericSeries'):
                # _logger.info(series.text)
                invoice_ids.append((series.get('id'), series.get('name')))
            return invoice_ids
        return False

    
    def get_invoice(self, invoice_number):
        payload = """<?xml version="1.0" encoding="Windows-1250"?>
                        <dat:dataPack id="001" ico="%s" application="StwTest" version = "2.0" note="Požadavek na export výběru faktur"         
                        xmlns:dat="http://www.stormware.cz/schema/version_2/data.xsd"   
                        xmlns:ftr="http://www.stormware.cz/schema/version_2/filter.xsd"      
                        xmlns:lst="http://www.stormware.cz/schema/version_2/list.xsd"         
                        xmlns:typ="http://www.stormware.cz/schema/version_2/type.xsd"  >
                        
                        <dat:dataPackItem id="li1" version="2.0">
                        <!-- export faktur  -->
                            <lst:listInvoiceRequest version="2.0" invoiceType="issuedInvoice" invoiceVersion="2.0">
                            <lst:requestInvoice>
                            <ftr:filter>
                                <ftr:selectedNumbers>
                                <ftr:number>
                                <typ:numberRequested>%s</typ:numberRequested>
                                </ftr:number>
                                </ftr:selectedNumbers>
                                
                            </ftr:filter>
                            </lst:requestInvoice>
                            </lst:listInvoiceRequest>
                        </dat:dataPackItem>
                        </dat:dataPack>"""%(self.registry, invoice_number)
        
        



        

        





        

        



