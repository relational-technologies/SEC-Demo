import base64
import json
import math
import re

from werkzeug import urls

from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError
from odoo.http import content_disposition, Controller, request, route
from odoo.tools import consteq


@route(['/store_document'], type='http', auth='user', website=True)
def account(self, redirect=None, **post):
    partner = request.env.user.partner_id

    Attachments = request.env['ir.attachment']

    name = post.get('attachment').filename

    file = post.get('attachment')
    print("yes working")

    attachment_id = Attachments.create({

        'name': name,

        'type': 'binary',

        'datas': base64.b64encode(file.read()),

        'res_model': partner._name,

        'res_id': partner.id

    })

    partner.update({

        'attachment': [(4, attachment_id.id)],

    })
