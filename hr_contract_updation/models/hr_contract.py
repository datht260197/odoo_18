# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime


class HrContract(models.Model):
    _inherit = 'hr.contract'

    contract_code = fields.Char(string="Mã hợp đồng", readonly=True, copy=False)
    birthday = fields.Date(string="Ngày sinh", related='employee_id.birthday', store=True, readonly=True)
    identification_id = fields.Char(related='employee_id.identification_id', string='Số CCCD', store=True, readonly=True)
    id_issue_date = fields.Date(related='employee_id.id_issue_date', string='Ngày cấp CCCD', store=True, readonly=True)
    id_issue_place = fields.Char(related='employee_id.id_issue_place', string='Nơi cấp CCCD', store=True, readonly=True)
    private_city = fields.Char(related='employee_id.private_city', string='Thường trú', store=True, readonly=True)
    job_title = fields.Char(related='employee_id.job_title', string='Chức danh', store=True, readonly=True)

    # --- Tự động sinh mã hợp đồng ---
    @api.model
    def create(self, vals):
        record = super(HrContract, self).create(vals)
        record._generate_contract_code()
        return record

    @api.onchange('employee_id', 'type_id')
    def _generate_contract_code(self):
        """Sinh mã hợp đồng dạng: [PIN]/[Năm]/[HĐLD hoặc HĐTV]"""
        for rec in self:
            if rec.employee_id:
                pin = rec.employee_id.pin or '0000'
                year = str(fields.Date.today().year)
                type_code = (rec.type_id.code or 'HĐLD').upper()
                rec.contract_code = f"{pin}/{year}/{type_code}"
            else:
                rec.contract_code = ''

    # --- Hàm hỗ trợ tách ngày/tháng/năm ký & kết thúc ---
    def _get_date_parts(self, date_value):
        if not date_value:
            return '', '', ''
        d = fields.Date.to_date(date_value)
        return str(d.day), str(d.month), str(d.year)

    # --- Biến context để xuất ra Word / PDF ---
    def get_print_context(self):
        self.ensure_one()
        start_d, start_m, start_y = self._get_date_parts(self.date_start)
        end_d, end_m, end_y = self._get_date_parts(self.date_end)

        return {
            'contract_code': self.contract_code or '',
            'employee_name': self.employee_id.name or '',
            'birthday': self.employee_id.birthday and fields.Date.to_date(self.employee_id.birthday).strftime('%d/%m/%Y') or '',
            'identification_id': self.employee_id.identification_id or '',
            'id_issue_date': self.employee_id.id_issue_date and fields.Date.to_date(self.employee_id.id_issue_date).strftime('%d/%m/%Y') or '',
            'id_issue_place': self.employee_id.id_issue_place or '',
            'private_city': self.employee_id.private_city or '',
            'job_title': self.employee_id.job_title or '',
            'sign_day': start_d,
            'sign_month': start_m,
            'sign_year': start_y,
            'end_day': end_d,
            'end_month': end_m,
            'end_year': end_y,
        }
