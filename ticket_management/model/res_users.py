# -*- coding: utf-8 -*-
##############################################################################
#
# OdooBro - odoobro.contact@gmail.com
#
##############################################################################

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_internal = fields.Boolean(
        string='Internal Member?')
