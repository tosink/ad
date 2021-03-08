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
            #_logger.info(self.authorization_code)
            # _logger.info(payload)
            # _logger.info(response)
            # _logger.info(response.text)
            tree = ET.ElementTree(ET.fromstring(response.text))
            root = tree.getroot()
            # _logger.info([elem.tag for elem in root.iter()])
            for bank_id in root.iter('{http://www.stormware.cz/schema/version_2/bankAccount.xsd}ids'):
                # _logger.info(bank_id.text)
                bank_ids.append(bank_id.text)
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
    

    def generate_invoice(self, invoice):
        invoice_type = self.env['mpohoda.invoice.type'].sudo().search([('journal_id','=',invoice.journal_id.id)],limit=1)
        confirmation_date = ''
        if invoice.origin:
            sale = self.env['sale.order'].sudo().search([('name','=',invoice.origin)],limit=1)
            if sale.confirmation_date:
                confirmation_date = sale.confirmation_date.split(' ')[0]
        is_vat_payer = 'false'
        if self.invoice.company_id.is_vat_payer:
            is_vat_payer = 'true'

        payload_item = ''
        for line in invoice.invoice_line_ids:
            if line.invoice_line_tax_ids:
            mpohoda_vat = line.invoice_line_tax_ids[0].mpohoda_vat
            payload_item += """<inv:invoiceItem>
                            <inv:id>%s</inv:id>
                            <inv:text>%s</inv:text>
                            <inv:quantity>%s</inv:quantity>
                            <inv:unit>%s</inv:unit>
                            <inv:coefficient>1.0</inv:coefficient>
                            <inv:payVAT>%s</inv:payVAT>
                            <inv:rateVAT>%s</inv:rateVAT>
                            <inv:discountPercentage>0.0</inv:discountPercentage>
                            <inv:homeCurrency>
                            <typ:unitPrice>%s</typ:unitPrice>
                            </inv:homeCurrency>
                            <inv:PDP>false</inv:PDP>
                            </inv:invoiceItem>"""%(line.id, line.name,line.quantity, line.uom_id.name, is_vat_payer, mpohoda_vat, line.unit_price)
            
        payload = """<?xml version="1.0" encoding="Windows-1250"?>
                        <dat:dataPack id="fa001" ico="%s" application="StwTest" version = "2.0" note="Import FA"        
                        xmlns:dat="http://www.stormware.cz/schema/version_2/data.xsd"        
                        xmlns:inv="http://www.stormware.cz/schema/version_2/invoice.xsd"        
                        xmlns:typ="http://www.stormware.cz/schema/version_2/type.xsd"
                        xmlns:prn="http://www.stormware.cz/schema/version_2/print.xsd">
                        <dat:dataPackItem id="AD001" version="2.0">
                        <inv:invoice version="2.0">
                        <inv:invoiceHeader>
                        <inv:invoiceType>issuedInvoice</inv:invoiceType>
                        <inv:date>%s</inv:date>
                        <inv:dateTax>%s</inv:dateTax>
                        <inv:dateAccounting>%s</inv:dateAccounting>
                        <inv:dateDue>%s</inv:dateDue>
                        <inv:accounting>
                        <typ:id>%s</typ:id>
                        </inv:accounting>
                        <inv:text>Fakturujeme Vám:</inv:text>
                        <inv:partnerIdentity>
                        <typ:address>
                        <typ:company>%s</typ:company>
                        <typ:city>%s</typ:city>
                        <typ:street>%s</typ:street>
                        <typ:zip>%s</typ:zip>
                        <typ:ico>%s</typ:ico>
                        <typ:dic>%s</typ:dic>
                        </typ:address>
                        <typ:shipToAddress>
                        <typ:company>%s</typ:company>
                        <typ:city>%s</typ:city>
                        <typ:street>%s </typ:street>
                        <typ:zip>%s</typ:zip>
                        </typ:shipToAddress>
                        </inv:partnerIdentity>
                        <inv:myIdentity>
                        <typ:address>
                        <typ:company>%s</typ:company>
                        <typ:city>%s</typ:city>
                        <typ:street>%s</typ:street>
                        <typ:zip>%s</typ:zip>
                        <typ:ico>%s</typ:ico>
                        <typ:dic>%s</typ:dic>
                        </typ:address>
                        </inv:myIdentity>
                        <inv:numberOrder>%s</inv:numberOrder>
                        <inv:dateOrder>%s</inv:dateOrder>
                        <inv:account>
                        <typ:id>3</typ:id>
                        </inv:account>
                        <inv:symConst>0308</inv:symConst> 
                        <inv:markRecord>false</inv:markRecord>
                        </inv:invoiceHeader>
                        <inv:invoiceDetail>
                            %s
                        </inv:invoiceDetail>
                        <inv:print>
                        <prn:printerSettings>
                        <prn:report>
                        <prn:id>190</prn:id>
                        </prn:report>
                        <prn:pdf>
                        <prn:fileName>%s</prn:fileName>
                        </prn:pdf>
                        </prn:printerSettings>
                        </inv:print>
                    
                        </inv:invoice>
                        </dat:dataPackItem>
                        </dat:dataPack> """%(self.registry, invoice.date_invoice, invoice.date_invoice, invoice.date_invoice,\
                                            invoice.date_due, invoice_type.mpohoda_code, invoice.partner_id.company_id.name, invoice.partner_id.city,\
                                            invoice.partner_id.street, invoice.partner_id.zip, invoice.partner_id.company_id.company_registry \
                                            invoice.partner_id.vat, invoice.partner_shipping_id.company_id.name, invoice.partner_shipping_id.city, invoice.partner_shipping_id.street, \
                                            invoice.partner_shipping_id.zip, invoice.company_id.name, invoice.company_id.city, invoice.company_id.street, invoice.company_id.zip,\
                                            invoice.company_id.company_registry, invoice.company_id.vat, invoice.origin, confirmation_date, payload_item, \
                                            invoice.company_id.mserver_document_path+'\%s.pdf'%(invoice.name))
        return True



        

        





        

        



