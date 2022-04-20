from odoo import models, fields, api, _


class TenderEstimation(models.Model):
    _name = "tender.estimation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Estimation'


    enq_number = fields.Many2one('tender.enquiry', string='Enq Number')
    contractor = fields.Char(related='enq_number.contractor', string='Contractor')
    estimator = fields.Char(string="Estimator")
    reviewer = fields.Char(string='Reviewer')
    currency = fields.Char(string='Currency')
    job_type = fields.Char(related='enq_number.job_type', string="Job Type")
    reference = fields.Char(string='Reference')
    total_estimation = fields.Float(string='Total Estimation')

    date = fields.Date(string="Date")
    submission = fields.Date(string="Submission")
    duration_from = fields.Date()
    duration_to = fields.Date()
    distance = fields.Float(string='Distance')
    street = fields.Char(inverse='_inverse_street')
    # street2 = fields.Char(inverse='_inverse_street2')
    zip = fields.Char(inverse='_inverse_zip')
    city = fields.Char(inverse='_inverse_city')

    country_id = fields.Many2one('res.country', inverse='_inverse_country',
                                 string="Country")
    state_id = fields.Many2one('res.country.state', inverse='_inverse_state',
                               string="Fed.State")

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
