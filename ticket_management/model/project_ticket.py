# -*- encoding: utf-8 -*-
from odoo import api, models, fields


class ProjectTicket(models.Model):
    '''Project ticket'''
    _inherit = "project.internal.ticket"
    _name = "project.ticket"
    _description = "Ticket"

    LIST_TICKET_TYPE = [
        ('unclassified', 'Unclassified'),
        ('initial_project', 'Initial Project'),
        ('functional_support', 'Functional Support'),
        ('evolution', 'Evolution'),
        ('adjustment', 'Adjustment'),
        ('defect', 'Defect'), ('other', 'Other')
    ]
    LIST_STATES = [
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('planned_for_delivery', 'Planned for delivery'),
        ('delivered', 'Delivered in Sandbox'),
        ('ok_for_live', 'OK for Live'),
        ('ok_to_close', 'OK to close'),
        ('closed', 'Closed')
    ]

    @api.multi
    def name_get(self):
        res = [(rec.id, '[T#{:06d}] {}'.format(rec.id, rec.name))
               for rec in self]
        return res

    ticket_type = fields.Selection(
        LIST_TICKET_TYPE, 'Ticket type', required=True, default='unclassified')
    internal_ticket_id = fields.Many2one(
        'project.internal.ticket', 'Internal ticket')
    state = fields.Selection(
        selection=LIST_STATES, string='Status', required=True, default='new')
    working_hour_ids = fields.One2many(
        'project.working.hour',
        'ticket_id',
        string='Working hours')

    @api.multi
    def button_create_internal_ticket(self):
        '''Button create internal ticket'''
        self.ensure_one()
        internal_ticket_obj = self.env['project.internal.ticket']
        ticket = self

        vals = {}
        project = ticket.project_id
        vals['name'] = ticket.name or False
        vals['description'] = ticket.description or False
        vals['project_id'] = project.id
        vals['tag_ids'] = [(6, 0, ticket.tag_ids.ids)]
        vals['ticket_id'] = ticket.id
        vals['step_id'] = ticket.step_id.id
        vals['priority'] = ticket.priority
        vals['user_id'] = self.env.uid

        internal_ticket = internal_ticket_obj.create(vals)
        return ticket.write({'internal_ticket_id': internal_ticket.id})
