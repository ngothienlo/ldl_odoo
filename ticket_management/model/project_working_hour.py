# -*- encoding: UTF-8 -*-
from odoo import fields, models
import time


class ProjectWorkingHour(models.Model):

    _name = "project.working.hour"
    _description = "Working hour"
    _order = "date desc, name"

    date = fields.Date('Date', required=True,
                       default=lambda self: time.strftime('%Y-%m-%d'))
    user_id = fields.Many2one(
        comodel_name='res.users', string='User',
        default=lambda self: self._uid)
    ticket_id = fields.Many2one(
        comodel_name='project.ticket', string='Ticket',
#         default=lambda self: self._context.get('ticket_id')
    )
    internal_ticket_id = fields.Many2one(
        comodel_name='project.internal.ticket', string='Internal Ticket',
#         default=lambda self: self._context.get('internal_ticket_id')
    )
    name = fields.Char(
        'Description', required=True,
    )
    duration_hour = fields.Float('Duration (hours)', required=True)
