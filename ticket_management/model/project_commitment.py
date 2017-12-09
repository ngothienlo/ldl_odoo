# -*- encoding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date, timedelta
from odoo.exceptions import Warning


class ProjectCommitment(models.Model):

    _name = "project.commitment"
    _description = "Commitment"
    _order = "date_start desc"

    def _get_date_start(self, date_start):
        date_start = self.date_start or datetime.now()
        date_start = isinstance(
            date_start,
            date) and str(
            date_start.strftime('%Y-%m-%d')) or date_start
        date_end = (
            datetime.strptime(
                str(date_start),
                '%Y-%m-%d') +
            timedelta(
                days=6)).strftime('%Y-%m-%d')
        return {'value': {'date_end': date_end, 'name': date_end}}

    @api.onchange('date_start')
    def on_change_date_start(self):
        res = self._get_date_start(self.date_start)
        self.name = res['value']['name']
        self.date_end = res['value']['date_end']

    @api.onchange('date_end')
    def on_change_date_end(self):
        date_end = self.date_end or datetime.now()
        date_end = isinstance(
            date_end,
            date) and str(
            date_end.strftime('%Y-%m-%d')) or date_end
        name = datetime.strptime(date_end, '%Y-%m-%d').strftime('%Y-%m-%d')
        self.name = name

    @api.model
    def _get_default_date_start(self):
        self._cr.execute('select max(date_end) from project_commitment')
        res = self._cr.fetchall()
        if res:
            result = [x[0] for x in res if x[0]]
            if result:
                date_start = (
                    datetime.strptime(
                        result[0],
                        '%Y-%m-%d') +
                    timedelta(
                        days=1)).strftime('%Y-%m-%d')
                return date_start
        return date.today().strftime('%Y-%m-%d')

    @api.multi
    @api.depends('date_end')
    def _get_date_end_year(self):
        for commitment in self:
            if commitment.date_end:
                commitment.date_end_year = commitment.date_end[:4]

    @api.multi
    @api.depends('date_end')
    def _get_date_end_month(self):
        for commitment in self:
            if commitment.date_end:
                commitment.date_end_month = commitment.date_end[5:7]

    # Columns
    name = fields.Char(
        'commitment Name', size=512, required=True)
    description = fields.Text(
        'Description / Content / priorities')
    date_start = fields.Date(
        'Start', required=True, default=_get_default_date_start)
    date_end = fields.Date(
        'End', required=True)
    date_end_year = fields.Char(
        compute=_get_date_end_year,
        string='Year Of Date End',
        store=True)
    date_end_month = fields.Char(
        compute=_get_date_end_month,
        string='Month of Date End',
        store=True)
    next_priority = fields.Text(
        'Next Priorities')
