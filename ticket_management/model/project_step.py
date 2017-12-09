# -*- coding: utf-8 -*-
##############################################################################
#
# OdooBro - odoobro.contact@gmail.com
#
##############################################################################

from odoo import api, models, fields


class ProjectStep(models.Model):

    _name = "project.step"
    _inherit = ['mail.thread']
    _description = "Step"

    project_id = fields.Many2one(
        'project.project', 'Project',
        required=True,
        track_visibility='onchange',
        default=lambda self: self._context.get('project_id')
    )
    name = fields.Char('Name', readonly=True, compute='_get_name', store=True)
    number = fields.Char(
        'Milestone Number', required=True,
        track_visibility='onchange')
    description = fields.Char(
        'Short Description',
        track_visibility='onchange')
    note = fields.Text(
        'Delivery Note'
    )
    state = fields.Selection(
        [('planned', 'Planned'),
         ('development', 'Development'),
         ('deployment', 'Deployment'),
         ('production', 'Production'),
         ('done', 'Done')],
        'Status', required=True,
        track_visibility='onchange'
    )
    date = fields.Date(
        'Commitment Date',
        track_visibility='onchange')
    internal_ticket_ids = fields.One2many(
        comodel_name='project.internal.ticket',
        inverse_name='step_id',
        string='Internal Tickets'
    )
    ticket_ids = fields.One2many(
        comodel_name='project.ticket',
        inverse_name='step_id',
        string='Tickets'
    )
    active = fields.Boolean(
        'Active', track_visibility='onchange', default=True)

    _sql_constraints = [('step_unique', 'unique (name)',
                         'This Step already exists!')]

    @api.multi
    def count_internal_ticket(self):
        IntTicket = self.env['project.internal.ticket']
        args = [('step_id', 'in', self.ids)]
        tickets = IntTicket.search(args)
        all = len(tickets)
        closed = len(tickets.filtered(lambda r: r.state == 'closed'))
        return all, closed

    @api.multi
    @api.depends('number', 'project_id', 'project_id.name', 'state')
    def _get_name(self):
        if not self:
            return []
        result = []
        current_user = self.env.user
        if current_user.is_internal:
            for step in self:
                all_tic, clo_tic = step.count_internal_ticket()
                step.name = '%s %s - %s (%s/%s)' % (step.project_id.name,
                                                    step.number, step.state,
                                                    clo_tic, all_tic)
        else:
            for step in self:
                step.name = '%s %s - %s' % (step.project_id.name,
                                            step.number, step.state)
