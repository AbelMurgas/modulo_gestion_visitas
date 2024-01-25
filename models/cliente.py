from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Cliente(models.Model):
    _name = 'gestion_visitas.cliente'
    _inherit = 'mail.thread'
    _description = 'Cliente para Gestion de Visitas'

    rutero_id = fields.Many2one('res.users', string='Rutero Asignado')
    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True, ondelete='restrict')
    linea = fields.Selection([
        ('repuestos', 'Repuestos'),
        ('llantas', 'Llantas'),
        ('lubricantes', 'Lubricantes'),
    ], string='Linea del cliente', tracking=True)

    _sql_constraints = [
        ('cliente_rutero_unique', 'UNIQUE(cliente_id, rutero_id, linea)', 'Un cliente solo puede tener un rutero asignado.')
    ]

    @api.constrains('rutero_id', 'cliente_id', 'linea')
    def _check_unique_rutero_cliente(self):
        for cliente in self:
            if cliente.rutero_id and cliente.cliente_id and cliente.linea:
                domain = [
                    ('rutero_id', '=', cliente.rutero_id.id),
                    ('cliente_id', '=', cliente.cliente_id.id),
                    ('linea', '=', cliente.linea),
                ]
                existing_clientes = self.search(domain)
                if existing_clientes and len(existing_clientes) > 1:
                    raise ValidationError('Este cliente ya está asignado a otro rutero con la misma línea.')