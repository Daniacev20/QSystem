# -*- coding: utf-8 -*-
{
    'name': "Quality System",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'order_productions'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'datas/sequences.xml',
        'views/views.xml',
        'report/report.xml',
        'report/report_template.xml',
        'views/templates.xml',
        'wizard/views.xml',
        'wizard/report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}