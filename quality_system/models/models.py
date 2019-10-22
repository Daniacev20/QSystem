# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo import exceptions, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class DimensionalTest(models.Model):
    _name = 'dimensional.test'
    _description = 'Dimensional Test'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Number of Test", required=False, )
    production_id = fields.Many2one(comodel_name="production.order", string="Production Order", required=True, )
    lot_id = fields.Many2one(comodel_name="production.lot", string="Lot Number", required=False, related="production_id.lot_id")
    date = fields.Date(string="Start Date", required=True, default=datetime.today())
    sap_code = fields.Char(string="SAP Code", required=False, )
    line_production = fields.Char(string="Line of Production", required=False, )
    agreement = fields.Selection(string="Agreement", selection=[('agreed', 'Agreed'), ('no-agreed', 'No Agreed'), ], required=False, default='agreed')
    line_ids = fields.One2many(comodel_name="dimensional.test.line", inverse_name="test_id", string="Lines of Test", required=False, )
    note = fields.Text(string="Comments", required=False, )
    state = fields.Selection(string="State", selection=[('draft', 'Draft'),
                                                   ('open', 'Running'),
                                                   ('close', 'Close'),
                                                   ], required=False, default='draft')

    ## For report
    detected_by = fields.Selection(string="Detected by", selection=[('qa', 'QA'), ('mfg', 'MFG'), ], required=False, )
    description_agreement = fields.Text(string="Description of Non-Agreement", required=False, )
    responsable_id = fields.Many2one(comodel_name="res.users", string="Responsable", required=False, )
    shift = fields.Selection(string="Shift", selection=[
        ('morning', 'Morning'),
        ('after', 'Afternoon'),
        ('night', 'Night'), ], default='morning')
    date_agreement = fields.Date(string="Date Non-agreement", required=False, )
    impact = fields.Selection(string="Impact", selection=[('minor', 'Minor NC'),
                                                   ('major', 'Major NC'),
                                                   ('critical', 'Critical NC'),
                                                   ], required=False, default='minor')


    @api.onchange('agreement')
    def _onchange_agreement(self):

        if self.agreement == 'no-agreed':
            self.responsable_id = self.env.user.id
            self.date_agreement = datetime.today()

    @api.multi
    def write(self, values):
        # Add code here  
        values['responsable_id']= self.env.user.id
        return super(DimensionalTest, self).write(values)


    @api.model
    def create(self, values):
        # Add code here

        ids = self.env['dimensional.test'].search([('production_id', '=', values['production_id'])])
        if ids:
            raise exceptions.UserError(_("There is already a record with this production"))
        else:

            values['name'] = self.env['ir.sequence'].next_by_code('production.order') or 'New'

            ID = super(DimensionalTest, self).create(values)

            ID.production_id.dimensional_test_id = ID.id
            ID.production_id.state = 'open'

        return ID

    def open_this(self):

        self.state = 'open'

    def close_this(self):

        self.production_id.state = 'close'

        self.state = 'close'




class DismensinalTestLine(models.Model):
    _name = 'dimensional.test.line'
    _description = 'Dimensional Test Line'

    test_id = fields.Many2one(comodel_name="dimensional.test", string="Test", required=False, )
    type_id = fields.Many2one(comodel_name="test.type", string="Type of Test",
                              required=True, )
    process_id = fields.Many2one(comodel_name="process.test", string="Process", required=True,
                                   domain="[('type_id', '=', type_id)]")
    no_tool = fields.Char(string="Number of Tool", required=False, )
    die_date = fields.Date(string="Die Date", required=False, )
    min_tolerance = fields.Float(string="Minimum Tolerance", required=False, related="type_id.min_tolerance")
    max_tolerance = fields.Float(string="Maximum Tolerance", required=False, related="type_id.max_tolerance")
    time_start = fields.Datetime(string="Time Starting", required=True, )
    no_test = fields.Integer(string="Numbers of Test", required=False, default=1)
    shift = fields.Selection(string="Shift", selection=[
        ('morning', 'Morning'),
        ('after', 'Afternoon'),
        ('night', 'Night'), ], required=True, )



class TestType(models.Model):
    _name = 'test.type'
    _description = 'Test Type'

    name = fields.Char(string="Name", required=True, )
    process_ids = fields.One2many(comodel_name="process.test", inverse_name="type_id", string="Process", required=True, )
    note = fields.Text(string="Note", required=False, )
    min_tolerance = fields.Float(string="Minimum Tolerance",  required=False, default=0.0)
    max_tolerance = fields.Float(string="Maximum Tolerance",  required=False, default=1.0)


class ProcessTest(models.Model):
    _name = 'process.test'
    _description = 'Process Test'

    name = fields.Char(string="Name", required=True, )
    note = fields.Text(string="Note", required=False, )
    type_id = fields.Many2one(comodel_name="test.type", string="Type of Test",
                                             required=False, )


class ProductionOrder(models.Model):
    _inherit = 'production.order'

    dimensional_test_id = fields.Many2one(comodel_name="dimensional.test",
                                   string="Dimensional/Visual Test", required=False, )

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = 'Wizard Report of Quality'

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)
    report_name = fields.Char(string="Report name", required=False, )
    report_file = fields.Binary(string="Report", )

    @api.multi
    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        return self.env.ref('quality_system.non_agreement_report').report_action(self, data=data)


class ReportQuality(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.quality_system.non_agreement_report_view'

    @api.model
    def get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)
        date_diff = (date_end_obj - date_start_obj).days + 1

        docs = []
        dimensional_tests = self.env['dimensional.test'].search([
            ('agreement', '=', 'no-agreed'),
            ('date', '>=', date_start_obj.strftime(DATETIME_FORMAT)),
            ('date', '<=', date_end_obj.strftime(DATETIME_FORMAT)),
        ], )

        for d in dimensional_tests:

            docs.append(d)

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
        }








