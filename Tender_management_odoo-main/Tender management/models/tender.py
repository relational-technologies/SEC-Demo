from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Tendertenders(models.Model):
    _name = "tender.tender"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Tender records'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('pass', 'Pass'),
    ], string='Status', readonly=True, default='draft')

    def action_open(self):
        for rec in self:
            rec.state = 'open'

    def action_pass(self):
        for rec in self:
            rec.state = 'pass'

    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '%s' % (rec.tender_code)))
        return res

    @api.model
    def create(self, vals):
        if vals.get('tender_code', _('New')) == _('New'):
            vals['tender_code'] = self.env['ir.sequence'].next_by_code('tender.code.sequence') or _('New')
        result = super(Tendertenders, self).create(vals)
        return result

    tender_code = fields.Char(string='tender_code', required=True, copy=False, readonly=True,
                              index=True, default=lambda self: _('New'))
    tender_name = fields.Char(string='tender', required=True, track_visibility="always")

    street = fields.Char(inverse='_inverse_street')
    # street2 = fields.Char(inverse='_inverse_street2')
    zip = fields.Char(inverse='_inverse_zip')
    city = fields.Char(inverse='_inverse_city')

    country_id = fields.Many2one('res.country', inverse='_inverse_country',
                                 string="Country")
    state_id = fields.Many2one('res.country.state', inverse='_inverse_state',
                               string="Fed.State")

    department = fields.Many2one('tender.department',string='Department')
    opening_date = fields.Date(string='Opening Date')
    bid_from = fields.Date(string='Bid From')
    bid_to = fields.Date(string='Bid To')
    active = fields.Boolean("Active", default=True)
    total_budget= fields.Float(string='Total Budget')
    earnest_money = fields.Float(string='Earnest Money Deposit')
    performance_security = fields.Float(string='Performance Security Deposit')
    liquidated_damage = fields.Float(string='Liquidated Damage')
    unliquidated_damage = fields.Float(string='Unliquidated Damage')

    html_filed = fields.Html(string='Pre-bid meeting MOM')
    meeting_date = fields.Date(string='Pre-bid meeting date')

    attachment = fields.Many2many('ir.attachment', 'attach_rel', 'doc_id', 'attach_id3',

                                  string="Documents",

                                  help='You can attach the copy of your document', copy=False)

    # document_title = fields.Char(string="Title")
    # document = fields.Binary(string='Document', attachment=True)

    #
    # @api.constrains('document')
    # def _check_file(self):
    #     if str(self.document_title.split(".")[1]) != 'pdf':
    #         raise ValidationError("Cannot upload file different from .pdf file")

    # material_line_one2many = fields.One2many('material.line', 'xyz', string='Material Line')

    #
    # @api.model
    # def _get_user_currency(self):
    #     currency_id = self.env['res.users'].browse(self._uid).company_id.currency_id
    #     return currency_id or self._get_euro()
    #
    # def _compute_address(self):
    #     for company in self.filtered(lambda company: company.partner_id):
    #         address_data = company.partner_id.sudo().address_get(adr_pref=['contact'])
    #         if address_data['contact']:
    #             partner = company.partner_id.browse(address_data['contact']).sudo()
    #             company.update(company._get_company_address_fields(partner))

    def _inverse_street(self):
        for rec in self:
            rec.street = rec.street if rec.street else False

    def _inverse_street2(self):
        for rec in self:
            rec.street2 = rec.street2 if rec.street2 else False

    def _inverse_zip(self):
        for rec in self:
            rec.zip = rec.zip if rec.zip else False

    def _inverse_city(self):
        for rec in self:
            rec.city = rec.city if rec.city else False

    def _inverse_state(self):
        for rec in self:
            rec.state_id = rec.state_id if rec.state_id else False

    def _inverse_country(self):
        for rec in self:
            rec.country_id = rec.country_id if rec.country_id else False

    @api.onchange('state_id')
    def _onchange_state(self):
        if self.state_id.country_id:
            self.country_id = self.state_id.country_id

    # def on_change_country(self, country_id):
    #     # This function is called from account/models/chart_template.py, hence decorated with `multi`.
    #     self.ensure_one()
    #     currency_id = self._get_user_currency()
    #     if country_id:
    #         currency_id = self.env['res.country'].browse(country_id).currency_id
    #     return {'value': {'currency_id': currency_id.id}}

    @api.onchange('country_id')
    def _onchange_country_id_wrapper(self):
        res = {'domain': {'state_id': []}}
        if self.country_id:
            res['domain']['state_id'] = [('country_id', '=', self.country_id.id)]
        #     values = self.on_change_country(self.country_id.id)['value']
        #     for fname, value in values.items():
        #         setattr(self, fname, value)
        return res

    def open_enquiry(self):
        return {
            'name': _('Enquiry'),
            'domain': [],
            'res_model': 'tender.enquiry',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    enquiry_lines = fields.One2many('enquiry.line', 'enquiry_id', string='enquiry Lines',Default=open_enquiry)
    question_lines = fields.One2many('questionnaires.line', 'question_id', string='Questionnaires Lines')


class tenderDepartment(models.Model):
    _name = 'tender.department'
    # _description = ''

    department_name = fields.Char(string="Name", required=True)



    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '%s' % (rec.department_name)))
        return res




#
# class material_line(models.Model):
#     _name = "material.line"
#     _description = "Material line"
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     # _inherit = ['product.product','mail.mixin']
#
#
#     def compute_amt(self):
#         for i in self:
#             i.amount = i.quantity * i.pricee
#             # print("amount========",i.amount)
#
#
#     xyz = fields.Many2one('tender.tender', string="XYZ")
#     name = fields.Many2one('product.product', string='Product Name')
#     price = fields.Float(string='Price', related='name.lst_price')
#     prod_description = fields.Text(related='name.description',  string='Description')
#     quantity = fields.Integer(string='Quantity')
#     note = fields.Text(string='Note')
#     amount = fields.Float(string='Amount', compute='compute_amt')



class Attachment(models.Model):

    _inherit = 'ir.attachment'

    attach_rel = fields.Many2many('res.partner', 'attachment', 'attachment_id3', 'document_id',string="Attachment", invisible=1 )




class tenderQuestionnaires(models.Model):
    _name = 'tender.questionnaires'
    _description = ''

    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '%s' % (rec.question)))
        return res

    question = fields.Char(string="Question", required=True)
    answer = fields.Char()



class enquiryLine(models.Model):
    _name = "enquiry.line"


    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty = fields.Integer(string="Quantity")
    sequence = fields.Integer(string="Sequence")
    enquiry_id = fields.Many2one('tender.enquiry', string='Tender_name')


class questionnairesLine(models.Model):
    _name = "questionnaires.line"



    question_id = fields.Many2one('tender.questionnaires', string='Question')
    answer_id = fields.Text(string="Answer")






