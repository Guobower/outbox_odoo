# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Ap(models.Model):
    _name = 'ap'
    _description = 'AP'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(
        string="Nome do AP",
        size=250,
        required=True,
        track_visibility='onchange')

    nas_name = fields.Char(
        string="IP do AP",
        size=250,
        required=True,
        track_visibility='onchange')

    type = fields.Selection(
        string="Tipo",
        selection=[('mikrotik', 'Mikrotik'),
                   ('other', 'PFSense')],
        required=True,
        track_visibility='onchange'
    )

    secret = fields.Char(
        string="Senha",
        size=250,
        required=True,
        track_visibility='onchange')

    description = fields.Text(
        string="Descrição",
        track_visibility='onchange'
    )

    @api.model
    def create(self, values):
        record = super(Ap, self).create(values)

        self.env.cr.execute("INSERT INTO nas("
                            "id, nasname, shortname, type, ports, secret, server, community, description)"
                            "VALUES (" + str(record["id"]) + ", '" + record["nas_name"] + "', '" + record["name"] + "', '" + record[
                                "type"] + "', Null, '" + record["secret"] + "', Null, Null, '" + record[
                                "description"] + "');")

        return record

    @api.multi
    def write(self, values):
        record = super(Ap, self).write(values)

        self.env.cr.execute("UPDATE nas set "
                            "nasname = '" + self.nas_name + "', shortname = '" + self.name + "', type = '"
                            + self.type + "', secret = '" + self.secret + "', description = '" + self.description + "'"
                            " where id = " + str(self.id))

        return record