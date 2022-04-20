from odoo import models, fields, api, _


class TenderEnquiries(models.Model):
    _name = "tender.enquiry"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Enquiry records'



    enquiry_code = fields.Char(string='Enquiry Code', required=True, copy=False, readonly=True,
                              index=True, default=lambda self: _('New'))
    contractor = fields.Char(string='Contractor')
    currency = fields.Char(string='Currency')
    job_type = fields.Char(string='Job Type')
    reference = fields.Char(string='Reference')
    tender = fields.Many2one("tender.tender", string="Tender")
    total_score = fields.Integer(string='Total Score')
    date = fields.Date(string='Date')


    attachment1 = fields.Many2many('ir.attachment', 'attach1_rel', 'doc_id1', 'attach_id3',

                                  string="Documents",

                                  help='You can attach the copy of your document', copy=False)




    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Review'),
        ('qualified', 'Qualified'),
        ('disqualified', 'Disqualified'),
        ('won', 'Won'),
    ], string='Status', readonly=True, default='draft')


    def action_review(self):
        for rec in self:
            rec.state = 'review'

    def action_qualify(self):
        for rec in self:
            rec.state = 'qualified'

    def action_disqualify(self):
        for rec in self:
            rec.state = 'disqualified'

    def action_won(self):
        for rec in self:
            rec.state = 'won'


    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '%s' % (rec.enquiry_code)))
        return res



    @api.model
    def create(self, vals):
        if vals.get('enquiry_code', _('New')) == _('New'):
            vals['enquiry_code'] = self.env['ir.sequence'].next_by_code('tender.enquiry.sequence') or _('New')
        result = super(TenderEnquiries, self).create(vals)
        return result
    #
    # @api.depends('tender')
    # def _compute_tender_code(self):
    #     for rec in self:
    #         tenders = self.env['tender.tender'].search([('tender_code')], limit=1)
    #         return tenders


