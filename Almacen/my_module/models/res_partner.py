from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    write_date=fields.Date("Fecha")

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    date_local = fields.Datetime(string='Fecha Local')