# -*- coding: utf-8 -*-
{
    'name': 'Supply Chain & Inventory Intelligence',
    'version': '18.0.1.0.0',
    'summary': 'AI-powered supply chain and inventory intelligence suite',
    'description': """
Supply Chain & Inventory Intelligence
=====================================

AI-powered demand forecasting, supplier scoring, stockout alerts,
demand pattern analysis and replenishment planning for modern
supply chain operations.

Features:
- Demand Forecasting (moving average, exponential smoothing, ML ensemble)
- Supplier Performance Scoring with AI recommendations
- Stockout Risk Alerts with AI risk levels
- Demand Pattern Analysis (trend, seasonal, cyclical, irregular)
- AI-optimized Replenishment Planning
""",
    'author': 'SoftaiDev',
    'website': 'https://softaidev.pages.dev',
    'category': 'Productivity/AI',
    'license': 'LGPL-3',
    'price': 749.99,
    'application': True,
    'installable': True,
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/sci_forecast_views.xml',
        'views/sci_supplier_score_views.xml',
        'views/sci_stockout_alert_views.xml',
        'views/sci_demand_pattern_views.xml',
        'views/sci_replenishment_plan_views.xml',
        'views/menu.xml',
    ],
    'assets': {},
    'images': ['static/description/cover.png'],
}
