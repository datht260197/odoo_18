# -*- coding: utf-8 -*-
from datetime import date
from odoo import api, fields, models

class HrContract(models.Model):
    _inherit = 'hr.contract'

    contract_type_id = fields.Many2one('hr.contract.type', string='Loại hợp đồng', required=True)
    contract_code = fields.Char(string='Mã hợp đồng', readonly=True, copy=False)

    id_number = fields.Char(string='Số CCCD', related='employee_id.identification_id', store=True)
    id_issue_date = fields.Date(string='Ngày cấp CCCD', related='employee_id.id_issue_date', store=True)
    id_issue_place = fields.Char(string='Nơi cấp CCCD', related='employee_id.id_issue_place', store=True)
    job_title = fields.Char(string='Chức danh', related='employee_id.job_title', store=True)

    def _build_contract_code(self):
        self.ensure_one()
        pin = (self.employee_id and self.employee_id.pin) or 'PIN'
        year_now = str(date.today().year)
        kind = (self.contract_type_id and self.contract_type_id.code) or ''
        return f"{pin}/{year_now}/{kind}"

    @api.onchange('employee_id', 'contract_type_id')
    def _onchange_generate_contract_code(self):
        for rec in self:
            if rec.employee_id and rec.contract_type_id:
                rec.contract_code = rec._build_contract_code()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if not rec.contract_code and rec.employee_id and rec.contract_type_id:
                rec.contract_code = rec._build_contract_code()
        return records

    def write(self, vals):
        res = super().write(vals)
        trigger_fields = {'employee_id', 'contract_type_id'}
        if trigger_fields & set(vals.keys()):
            for rec in self:
                if rec.employee_id and rec.contract_type_id:
                    rec.contract_code = rec._build_contract_code()
        return res
