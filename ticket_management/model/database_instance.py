# -*- coding: utf-8 -*-
##############################################################################
#
# OdooBro - odoobro.contact@gmail.com
#
##############################################################################

from odoo import fields, api, models


class DatabaseInstance(models.Model):

    _name = "database.instance"
    _description = "Instance Database"

    name = fields.Char("Database Name", required=1)
    password = fields.Char(string="Password")
    instance_id = fields.Many2one(
        'project.instance', string='Instance', required=1)
