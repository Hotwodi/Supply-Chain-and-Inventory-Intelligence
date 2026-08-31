# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SciReplenishmentPlan(models.Model):
    _name = 'sci.replenishment.plan'
    _description = 'Replenishment Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('sci.replenishment.plan') or 'New',
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
    suggested_qty = fields.Float(
        string='Suggested Quantity',
        default=0.0,
        tracking=True,
    )
    current_stock = fields.Float(
        string='Current Stock',
        default=0.0,
        tracking=True,
    )
    lead_time = fields.Integer(
        string='Lead Time (days)',
        default=0,
        tracking=True,
    )
    ai_optimized_qty = fields.Float(
        string='AI Optimized Quantity',
        default=0.0,
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('ordered', 'Ordered'),
            ('received', 'Received'),
        ],
        string='State',
        default='draft',
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
        ('name_uniq', 'unique(name)', 'The replenishment plan reference must be unique.'),
    ]

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

    def action_order(self):
        for rec in self:
            rec.state = 'ordered'

    def action_receive(self):
        for rec in self:
            rec.state = 'received'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
