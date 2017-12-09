# -*- coding: utf-8 -*-
##############################################################################
#
# OdooBro - odoobro.contact@gmail.com
#
##############################################################################

from odoo import api, models, fields
from .project_instance import HOST_TYPE

class ProjectHost(models.Model):

    _name = "project.host"
    _description = "Host"
    _inherit = ['mail.thread']

    name = fields.Char('Host Name', required=True,
                       track_visibility='onchange')
    host_address = fields.Char('Host Address', required=True,
                               track_visibility='onchange')
    port = fields.Char('SSH Port', required=True,
                       track_visibility='onchange')
    ip = fields.Char('IP')
    operating_system_id = fields.Many2one(
        'operating.system', string='Operating System',
        track_visibility='onchange')

    service = fields.Char('Services')
    group_ids = fields.Many2many('host.group',
        string='Groups',
        track_visibility='onchange')
    user_ids = fields.Many2many('res.users',
        string='Users', track_visibility='onchange')
    instance_ids = fields.One2many(
        'project.instance', 'host_id', string='Instances')
    type = fields.Selection(HOST_TYPE,
        string='Type', required=True, track_visibility='onchange')
    virtual_machine = fields.Boolean('Virtual Machine',
                                     track_visibility='onchange')
    physical_host_id = fields.Many2one('project.host', string='Physical Host',
                                       track_visibility='onchange')
    virtual_host_ids = fields.One2many('project.host', 'physical_host_id',
                                       string='Virtual Machines')
    state = fields.Selection([
            ('active', 'Active'), ('exception', 'Exception'),
            ('asleep', 'Asleep'), ('deleted', 'Deleted')],
        string='Status', track_visibility='onchange')
    we_care = fields.Boolean(
        string='We take care?', track_visibility='onchange')
    # Resources
    processors = fields.Integer(string='Processors')
    ram = fields.Integer(string='Memory (RAM in MB)')
    disk_size = fields.Integer(string='Disk Size (GB)')
    swap = fields.Integer(string='Swap (MB)')

    _sql_constraints = [
        ('host_unique', 'unique(name)', 'This host already exists!'),
        ('host_add_unique', 'unique(host_address)',
         'This host address already exists!'),
    ]

    _defaults = {
        'state': 'active',
        'we_care': True,
    }

    @api.onchange('virtual_machine')
    def onchange_virtual_machine(self):
        """
        when change virtual machine, clear value of field physical host
        or virtual host
        """
        res = {}
        if self.id:
            machine_ids = self._search([('physical_host_id', '=', self.id)],
                                       limit=1)
            if machine_ids:
                res.update({'warning': {'title': 'Error',
                                        'message': '''
                    Remove all virtual machines which link to this host'''}})
                self.virtual_machine = False
        return res

    @api.multi
    def name_get(self):
        return [(host.id, u"{0} ({1})".format(
            host.name, host.physical_host_id.name)) if host.physical_host_id
            else (host.id, u"{0}".format(host.name)) for host in self]
