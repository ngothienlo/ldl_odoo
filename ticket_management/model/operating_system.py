# -*- coding: utf-8 -*-
##############################################################################
#
# OdooBro - odoobro.contact@gmail.com
#
##############################################################################

from odoo import models, fields


class OperatingSystem(models.Model):

    _name = "operating.system"
    _description = "Operating system"

    name = fields.Char('Operating system', required=True)
