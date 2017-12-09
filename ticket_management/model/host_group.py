# -*- coding: utf-8 -*-
##############################################################################
#
# OdooBro - odoobro.contact@gmail.com
#
##############################################################################

from odoo import models, fields


class HostGroup(models.Model):

    _name = "host.group"
    _description = "Host Group"

    name = fields.Char('Group', required=True)
