# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.addons.intel_stormware_mpohoda.models.mpohoda_request import MpohodaAPI
import logging
import requests
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    mpohoda_status = fields.Selection(
        [('ready','Ready'),('sent','Sent'),('error','Error')],
        string='Mpohoda Status',
        default='ready',
        track_visibility='onchange',
        required=True)
    
    mpohoda_type_id = fields.Many2one(
        comodel_name='mpohoda.payment.type', 
        string='Mpohoda Payment Type',
        default=lambda self: self.env['mpohoda.payment.type'].search([],limit=1),
        required=False)
    

    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        for invoice in self:
            try:
                _logger.info('Sending invoice %s to MPOHODA'%invoice.number)
                invoice.generate_invoice()
                invoice.mpohoda_status = 'sent'
                _logger.info('Generated invoice %s from MPOHODA'%invoice.number)
            except Exception as e:
                invoice.mpohoda_status = 'error'
                _logger.info('Error for invoice %s from MPOHODA: %s'%(invoice.name,e))

        return res
    
    def generate_invoice(self):
        invoice_type = self.env['mpohoda.invoice.type'].sudo().search([('journal_id','=',self.journal_id.id)],limit=1)
        confirmation_date = ''
        if self.origin:
            sale = self.env['sale.order'].sudo().search([('name','=',self.origin)],limit=1)
            if sale.confirmation_date:
                confirmation_date = str(sale.confirmation_date).split(' ')[0]
        is_vat_payer = 'false'
        if self.company_id.is_vat_payer:
            is_vat_payer = 'true'

        payload_item = ''
        mpohoda_vat = 'none'
        for line in self.invoice_line_ids:
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
                            </inv:invoiceItem>"""%(line.id, line.name,line.quantity, line.uom_id.name, is_vat_payer, mpohoda_vat, line.price_unit)
            
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
                        <inv:number>
                        <typ:id>%s</typ:id>
                        </inv:number>
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
                        </dat:dataPack> """%(self.company_id.company_registry, self.number, self.date_invoice, self.date_invoice, self.date_invoice,\
                                            self.date_due, invoice_type.mpohoda_code, self.partner_id.name, self.partner_id.city,\
                                            self.partner_id.street, self.partner_id.zip, self.partner_id.company_id.company_registry, \
                                            self.partner_id.vat, self.partner_shipping_id.name, self.partner_shipping_id.city, self.partner_shipping_id.street, \
                                            self.partner_shipping_id.zip, self.company_id.name, self.company_id.city, self.company_id.street, self.company_id.zip,\
                                            self.company_id.company_registry, self.company_id.vat, self.origin, confirmation_date, payload_item, \
                                            self.company_id.mserver_document_path+"\%s.pdf"%(self.number))
        
        company = self.company_id
        mpohoda = MpohodaAPI(company.mserver_host, company.mserver_port, company.mserver_user, \
            company.mserver_password, company.company_registry)

        headers = {
            'Stw-Authorization': 'Basic {}'.format(mpohoda.authorization_code),
            'Authorization': 'Basic {}'.format(mpohoda.authorization_code),
            'Content-Type': 'text/plain',
        }
        _logger.info('Payload %s'%payload)
        response = requests.post(mpohoda.url, data=payload.encode('Windows-1250'), headers=headers)
        if response.status_code == 200:
            response_document = requests.get(mpohoda.default_url+'/documents/%s.pdf'%self.number, headers=headers)
            _logger.info(response_document)
            _logger.info(response_document.text)
        return True
    
    @api.multi
    def action_mpohoda_invoice_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref('account.email_template_edi_invoice', False)
        compose_form = self.env.ref('account.account_invoice_send_wizard_form', False)
        # have model_description in template language
        lang = self.env.context.get('lang')
        if template and template.lang:
            lang = template._render_template(template.lang, 'account.invoice', self.id)
        self = self.with_context(lang=lang)
        TYPES = {
            'out_invoice': _('Invoice'),
            'in_invoice': _('Vendor Bill'),
            'out_refund': _('Credit Note'),
            'in_refund': _('Vendor Credit note'),
        }
        ctx = dict(
            default_model='account.invoice',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            model_description=TYPES[self.type],
            custom_layout="mail.mail_notification_paynow",
            force_email=True
        )
        return {
            'name': _('Send Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }


    

    

    