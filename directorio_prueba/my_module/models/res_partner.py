from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    write_date=fields.Date("Fecha")

