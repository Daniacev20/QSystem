# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions, _
from datetime import datetime

class OrderOroductions(models.Model):
    _name = 'production.order'
    _description = 'Production Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string="Name", required=False, )
    product_id = fields.Many2one(comodel_name="product.product", string="Item Product", required=True, )
    lot_id = fields.Many2one(comodel_name="production.lot", string="Lot #", required=True, )
    qty = fields.Integer(string="Quantity", required=False, default=0)
    description = fields.Char(string="Description", required=False, )
    start_date = fields.Date(string="Start Date", required=True, default=datetime.today())
    end_date = fields.Date(string="End Date", required=False, )
    state = fields.Selection(string="State", selection=[
        ('draft', 'Draft'),
        ('open', 'Processing'),
        ('close', 'Close'),
    ], required=False,default='draft')



    @api.model
    def create(self, values):
        # Add code here

        values['name'] = self.env['ir.sequence'].next_by_code('production.order') or 'New'


        return super(OrderOroductions, self).create(values)

class ProductionLot(models.Model):
    _name = 'production.lot'
    _description = 'Production Lot'

    name = fields.Char(string="Number of Lot", required=True, )

