# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SciSupplierScore(models.Model):
    _name = 'sci.supplier.score'
    _description = 'Supplier Score'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'last_updated desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('sci.supplier.score') or 'New',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Supplier',
        required=True,
        tracking=True,
        domain="[('supplier_rank', '>', 0)]",
    )
    on_time_rate = fields.Float(
        string='On-Time Delivery Rate (%)',
        default=0.0,
        tracking=True,
    )
    quality_rate = fields.Float(
        string='Quality Acceptance Rate (%)',
        default=0.0,
        tracking=True,
    )
    cost_index = fields.Float(
        string='Cost Index',
        default=0.0,
        tracking=True,
        help='Relative cost index (lower is better).',
    )
    risk_score = fields.Float(
        string='Risk Score',
        default=0.0,
        tracking=True,
        help='Risk score from 0 (low) to 100 (high).',
    )
    ai_recommendation = fields.Text(
        string='AI Recommendation',
        tracking=True,
    )
    last_updated = fields.Datetime(
        string='Last Updated',
        default=fields.Datetime.now,
        tracking=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The supplier score reference must be unique.'),
    ]

    @api.depends('on_time_rate', 'quality_rate', 'cost_index', 'risk_score')
    def _compute_overall_score(self):
        for rec in self:
            rec.overall_score = (
                rec.on_time_rate * 0.4
                + rec.quality_rate * 0.4
                - rec.cost_index * 0.1
                - rec.risk_score * 0.1
            )

    overall_score = fields.Float(
        string='Overall Score',
        compute='_compute_overall_score',
        store=True,
    )
