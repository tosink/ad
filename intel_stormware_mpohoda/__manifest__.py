# Copyright 2013 Nicolas Bessi (Camptocamp SA)
# Copyright 2014 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stormware POHODA",
    "summary": "Stormware POHODA",
    "version": "14.0.0.0.6",
    "author": "Intelligenti.io",
    "license": "AGPL-3",
    "maintainer": "Intelligenti.io",
    "category": "Extra Tools",
    "website": "https://www.intelligenti.io",
    "depends": ["sale"],
    "data": [
        "views/base_config_view.xml",
        "views/account_tax.xml",
        "views/account_invoice.xml",
        "wizard/account_invoice_send.xml",
        "security/ir.model.access.csv",
    ],
    "auto_install": False,
    "installable": True,
}
