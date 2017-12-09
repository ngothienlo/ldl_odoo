# -*- coding: utf-8 -*-
##############################################################################
#
# OdooBro - odoobro.contact@gmail.com
#
##############################################################################

from odoo import api, fields, models


HOST_TYPE = [
    ('live', 'Product'),
    ('sandbox', 'Sandbox'),
    ('internal', 'Internal'),
    ('demo', 'Demo')]


class ProjectInstance(models.Model):
    _name = "project.instance"
    _inherit = ['mail.thread']

    name = fields.Char('Instance Name', required=True,
                       track_visibility='onchange')
    project_id = fields.Many2one('project.project', 'Project',
                                 required=True, track_visibility='onchange')

    step_id = fields.Many2one(
        'project.step', 'Step',
        track_visibility='onchange',
        required=True)

    host_id = fields.Many2one('project.host', 'Host',
                              required=True, track_visibility='onchange')

    physical_host_id = fields.Many2one('project.host',
                                       related='host_id.physical_host_id',
                                       string="Node", store=True)

    server_type = fields.Selection(
        HOST_TYPE, 'Server Type', required=True,
        track_visibility='onchange')

    url = fields.Char('URL', required=True,
                      track_visibility='onchange')

    ssh_port = fields.Char('SSH port', track_visibility='onchange')
    xmlrpc_port = fields.Char('xmlrpc port', track_visibility='onchange')

    psql_host = fields.Char('PostgreSQL Host', required=True,
                            track_visibility='onchange',
                            default='localhost')

    psql_port = fields.Char('PostgreSQL Port', required=True,
                            track_visibility='onchange',
                            default='5432')

    psql_user = fields.Char('PostgreSQL User', required=True,
                            track_visibility='onchange')

    psql_pass = fields.Char('PostgreSQL Pass', required=True,
                            track_visibility='onchange')

    is_set_up_domain = fields.Boolean(
        'Domain',
        help='Create the instance for: {projectname}.com')

    is_set_up_http_authentication = fields.Boolean(
        'Http Authentication',
        help='Set http authentication to '
        '{projectname}.com')

    is_set_up_https = fields.Boolean('https')

    is_set_up_xmlrpc = fields.Boolean('xmlrpc')

    note = fields.Text('Note')

    last_error = fields.Text('Last Error')

    instance_database_ids = fields.One2many('database.instance',
                                               'instance_id',
                                               string='Databases')

    active = fields.Boolean('Active', default=True)

    https_login = fields.Char('HTTP Authen Test Login')
    https_password = fields.Char('HTTP Authen Test Pwd')

    backend_ip = fields.Char('Backend IP')

    backend_port = fields.Char('Backend Port',  default='8069')

    ssl = fields.Boolean('SSL')

    htpasswd_file = fields.Char('htpasswd file')

    user_ids = fields.Many2many(
        comodel_name='res.users',
        string="Users",
        help="list users who can access to this instance")

    xmlrpc_url = fields.Char(compute='compute_xmlrpc_url',
                             string="XML-RPC URL")

    _sql_constraints = [
        ('instance_unique', 'unique (name)', 'This instance already exists!'),
    ]

    @api.multi
    def compute_xmlrpc_url(self):
        for instance in self:
            if instance.xmlrpc_port:
                uri_base = '%s:%s' % (instance.url, instance.xmlrpc_port)

                if uri_base[:4] != 'http':
                    uri_base = 'http://%s' % uri_base
            else:
                uri_base = '%s:443' % instance.url
                if uri_base[:5] != 'https':
                    uri_base = 'https://' + uri_base

            instance.xmlrpc_url = uri_base

    @api.onchange('server_type')
    def on_change_server_type(self):
        for instance in self:
            project = instance.project_id
            server_type = instance.server_type
            if not project or not server_type:
                return {}
            name = 'odoo-%s-%s' % (project.name, server_type)
            if server_type == 'production':
                url = '%s.com' % (project.name)
            else:
                url = '%s-%s.com' % (project.name, server_type)
            instance.name = name
            instance.url = url
            instance.psql_user = name
            instance.psql_pass = name
            # F#13799 - htpasswd_file field on instance should be editable
            if project and server_type:
                htpasswd_file = '/usr/local/var/auth/htpasswd_%s_%s' %\
                    (project.name, server_type)
                instance.htpasswd_file = htpasswd_file

    @api.onchange('project_id')
    def on_change_project_id(self):
        for instance in self:
            project = instance.project_id
            server_type = instance.server_type
            # F#13799 - htpasswd_file field on instance should be editable
            if project and server_type:
                htpasswd_file = '/usr/local/var/auth/htpasswd_%s_%s' %\
                    (project.name, server_type)
                instance.htpasswd_file = htpasswd_file

    @api.onchange('host_id')
    def on_change_host(self):
        for instance in self:
            host = instance.host_id
            if host:
                instance.ssh_port = host.port
            else:
                instance.backend_ip = False
                instance.ssh_port = False
