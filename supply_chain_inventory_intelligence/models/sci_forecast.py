# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SciForecast(models.Model):
    _name = 'sci.forecast'
    _description = 'Demand Forecast'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'period desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('sci.forecast') or 'New',
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
    forecast_qty = fields.Float(
        string='Forecast Quantity',
        default=0.0,
        tracking=True,
    )
    actual_qty = fields.Float(
        string='Actual Quantity',
        default=0.0,
        tracking=True,
    )
    forecast_accuracy = fields.Float(
        string='Forecast Accuracy (%)',
        compute='_compute_forecast_accuracy',
        store=True,
        readonly=False,
    )
    period = fields.Date(
        string='Period',
        required=True,
        tracking=True,
    )
    ai_confidence = fields.Float(
        string='AI Confidence (%)',
        default=0.0,
        tracking=True,
    )
    method = fields.Selection(
        selection=[
            ('moving_avg', 'Moving Average'),
            ('exponential', 'Exponential Smoothing'),
            ('ml_ensemble', 'ML Ensemble'),
        ],
        string='Forecast Method',
        default='moving_avg',
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
        ('name_uniq', 'unique(name)', 'The forecast reference must be unique.'),
    ]

    @api.depends('forecast_qty', 'actual_qty')
    def _compute_forecast_accuracy(self):
        for rec in self:
            if rec.forecast_qty and rec.actual_qty:
                error = abs(rec.forecast_qty - rec.actual_qty)
                rec.forecast_accuracy = max(0.0, 100.0 - (error / rec.forecast_qty) * 100.0)
            elif rec.forecast_qty and not rec.actual_qty:
                rec.forecast_accuracy = 0.0
            else:
                rec.forecast_accuracy = 0.0
