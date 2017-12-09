# -*- encoding: utf-8 -*-

from odoo import api, models, fields

INTERNAL_STATES = [
    ('assigned', 'Assigned'),
    ('wip', 'WIP'),
    ('code_completed', 'Code completed'),
    ('ready_to_deploy', 'Ready To Deploy'),
    ('in_qa', 'QA'),
    ('closed', 'Closed')
]
DELIVERY_STATUS = [
    ('in_development', 'In Development'),
    ('in_internal', 'In Internal'),
    ('ready_for_sandbox', 'Ready for Sanbox'),
    ('in_sandbox', 'In Sandbox'),
    ('in_live', 'In Live'),
    ('no_development', 'No Development')
]


class ProjectInternalTicket(models.Model):

    _inherit = "project.task"
    _name = "project.internal.ticket"
    _description = "Internal Ticket"
    _order = 'priority DESC'

    @api.depends('priority')
    def _get_priority(self):
        for ticket in self:
            if ticket.priority == 'very_high':
                ticket.sequence = 20
            elif ticket.priority == 'high':
                ticket.sequence = 15
            elif ticket.priority == 'normal':
                ticket.sequence = 10
            elif ticket.priority == 'low':
                ticket.sequence = 5
            else:
                ticket.sequence = 0

    id = fields.Integer(string='Ticket ID', readonly=True)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Very High'),
        ], default='1', index=True, string="Priority")
    project_id = fields.Many2one(required=True, track_visibility='onchange')
    closed_by = fields.Many2one(
        'res.users', string='Closed By', readonly=True)
    user_id = fields.Many2one(
        'res.users', 'Assignee', domain="[('is_internal','=',True)]",
        required=True, track_visibility='onchange')
    step_id = fields.Many2one(
        'project.step', 'Step',
        domain="[('project_id', '=', project_id)]",
        track_visibility='onchange')
    developer_id = fields.Many2one(
        'res.users', 'Developer', domain="[('is_internal','=',True)]",
        ondelete='restrict', readonly=True,
        track_visibility='onchange')

    commitment_id = fields.Many2one(
        'project.commitment', 'Commitment',
        domain="[('date_end','>',context_today().strftime('%Y-%m-%d'))]",
        track_visibility='onchange'
    )
    state = fields.Selection(INTERNAL_STATES, 'Status', default='assigned',
                             track_visibility='onchange')
    ticket_id = fields.Many2one(
        'project.ticket', 'Ticket'
    )
    workload = fields.Float(
        'Workload', track_visibility='onchange'
    )
    working_hour_ids = fields.One2many(
        'project.working.hour', 'internal_ticket_id',
        string='Working Hours',
    )
    sequence = fields.Integer(
        compute='_get_priority', string='Sequence', store=True
    )
    delivery_status = fields.Selection(
        DELIVERY_STATUS, 'Delivery Status', readonly=True,
        default='in_development'
    )
    step_number = fields.Char(
        related="step_id.number", string="Step", store=True
    )
    parent_internal_ticket_id = fields.Many2one(
        'project.internal.ticket', 'Parent Internal Ticket')
    child_internal_ticket_ids = fields.One2many(
        'project.internal.ticket', 'parent_internal_ticket_id',
        string='Parent Internal Ticket')

    @api.multi
    def name_get(self):
        res = [(rec.id, '[I#{:06d}] {}'.format(rec.id, rec.name))
               for rec in self]
        return res

    @api.multi
    def write(self, vals):
        if 'state' in vals:
            if vals['state'] == 'wip':
                vals.update({'developer_id': self.env.uid})
            elif vals['state'] == 'closed':
                vals.update({'closed_by': self.env.uid})
        return super(ProjectInternalTicket, self).write(vals)

    @api.multi
    def button_create_ticket(self):
        context = self._context and self._context.copy() or {}
        Ticket = self.env['project.ticket']
        current_user = self.env.user

        for ticket in self:
            vals = {}
            project = ticket.project_id
            vals['name'] = ticket.name or False
            vals['project_id'] = project.id
            vals['step_id'] = ticket.step_id and \
                ticket.step_id.id or False
            vals['priority'] = ticket.priority
            vals['state'] = 'new'
            vals['interal_ticket_id'] = ticket.id
            vals['user_id'] = current_user.id
            vals['customer_id'] = project.partner_id and \
                project.partner_id.id or False

            support = Ticket.create(vals)
            ticket.write({'ticket_id': support.id})
        return True
