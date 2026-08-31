# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SciDemandPattern(models.Model):
    _name = 'sci.demand.pattern'
    _description = 'Demand Pattern'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'period desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('sci.demand.pattern') or 'New',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        tracking=True,
    )
    pattern_type = fields.Selection(
        selection=[
            ('trend', 'Trend'),
            ('seasonal', 'Seasonal'),
            ('cyclical', 'Cyclical'),
            ('irregular', 'Irregular'),
        ],
        string='Pattern Type',
        default='trend',
        required=True,
        tracking=True,
    )
    seasonality_index = fields.Float(
        string='Seasonality Index',
        default=0.0,
        tracking=True,
    )
    trend_slope = fields.Float(
        string='Trend Slope',
        default=0.0,
        tracking=True,
    )
    ai_pattern_confidence = fields.Float(
        string='AI Pattern Confidence (%)',
        default=0.0,
        tracking=True,
    )
    period = fields.Date(
        string='Period',
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
        ('name_uniq', 'unique(name)', 'The demand pattern reference must be unique.'),
    ]
