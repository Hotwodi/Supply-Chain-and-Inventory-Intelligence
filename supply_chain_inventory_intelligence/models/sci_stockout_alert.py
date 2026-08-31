# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SciStockoutAlert(models.Model):
    _name = 'sci.stockout.alert'
    _description = 'Stockout Alert'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'ai_risk_level, days_until_stockout, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('sci.stockout.alert') or 'New',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        tracking=True,
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        required=True,
        tracking=True,
    )
    current_stock = fields.Float(
        string='Current Stock',
        default=0.0,
        tracking=True,
    )
    reorder_point = fields.Float(
        string='Reorder Point',
        default=0.0,
        tracking=True,
    )
    days_until_stockout = fields.Integer(
        string='Days Until Stockout',
        default=0,
        tracking=True,
    )
    ai_risk_level = fields.Selection(
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        string='AI Risk Level',
        default='low',
        required=True,
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('active', 'Active'),
            ('resolved', 'Resolved'),
        ],
        string='State',
        default='active',
        required=True,
        tracking=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The stockout alert reference must be unique.'),
    ]

    def action_resolve(self):
        for rec in self:
            rec.state = 'resolved'

    def action_reactivate(self):
        for rec in self:
            rec.state = 'active'
