# -*- coding: utf-8 -*-
from openerp import models, api, fields


class AccountMoveValidate(models.TransientModel):

    _name = 'account.move.validate'
    _description = 'Mass validate account moves'

    account_moves = fields.Many2many('account.move')

    @api.model
    def default_get(self, fields):
        res = super(AccountMoveValidate, self).default_get(fields)

        account_move_ids = self._context['active_ids']

        account_moves = self.env['account.move'].search([
            ('id', 'in', account_move_ids),
            ('state', '=', 'draft'),
        ])

        res['account_moves'] = account_moves.ids
        res['active_ids'] = account_moves.ids

        return res

    @api.multi
    def move_validate(self):
        if 'active_ids' not in self._context:
            return False

        account_move_ids = self._context['active_ids']

        account_moves = self.env['account.move'].search([
            ('id', 'in', account_move_ids),
            ('state', '=', 'draft'),
        ])

        account_moves.button_validate()
