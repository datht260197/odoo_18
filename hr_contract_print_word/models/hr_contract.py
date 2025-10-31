# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
from io import BytesIO
import base64

try:
    from docxtpl import DocxTemplate
except Exception:
    DocxTemplate = None


class HrContract(models.Model):
    _inherit = 'hr.contract'

    def _compute_date_parts(self, date_value):
        if not date_value:
            return None, None, None
        d = fields.Date.to_date(date_value)
        return str(d.day), str(d.month), str(d.year)

    def _select_template_path(self):
        code = (self.type_id.code or '').upper() if self.type_id else ''
        candidates = []
        if code in ('HĐTV', 'HDTV'):
            candidates.append(('report', 'contract_template_trial.docx'))
        elif code in ('HĐLD', 'HDLD'):
            candidates.append(('report', 'contract_template_labor.docx'))
        candidates.append(('report', 'contract_template.docx'))
        for subdir, fname in candidates:
            path = get_module_resource('hr_contract_print_word', subdir, fname)
            if path:
                return path
        return None

    def action_print_word_contract(self):
        self.ensure_one()
        if DocxTemplate is None:
            raise UserError(_('Thiếu thư viện docxtpl. Vui lòng cài đặt: pip install docxtpl'))

        template_path = self._select_template_path()
        if not template_path:
            raise UserError(_('Không tìm thấy file mẫu hợp đồng trong module hr_contract_print_word/report'))

        # Split start/end date
        s_d, s_m, s_y = self._compute_date_parts(self.date_start)
        e_d, e_m, e_y = self._compute_date_parts(self.date_end)

        # allow override fields if existing in system
        sign_day = getattr(self, 'sign_day', s_d) or ''
        sign_month = getattr(self, 'sign_month', s_m) or ''
        sign_year = getattr(self, 'sign_year', s_y) or ''
        end_day = getattr(self, 'end_day', e_d) or ''
        end_month = getattr(self, 'end_month', e_m) or ''
        end_year = getattr(self, 'end_year', e_y) or ''

        employee = self.employee_id
        def fmt(d):
            return d and fields.Date.to_date(d).strftime('%d/%m/%Y') or ''

        context = {
            'employee_name': employee.name or '',
            'employee_pin': employee.pin or '',
            'contract_code': getattr(self, 'contract_code', '') or self.name or '',
            'job_title': getattr(self, 'job_title', '') or employee.job_title or '',
            'identification_id': getattr(self, 'identification_id', '') or employee.identification_id or '',
            'id_issue_date': getattr(self, 'id_issue_date', '') or fmt(getattr(employee, 'id_issue_date', False)),
            'id_issue_place': getattr(self, 'id_issue_place', '') or getattr(employee, 'id_issue_place', '') or '',
            'private_city': getattr(self, 'private_city', '') or employee.private_city or '',
            'date_start': fmt(self.date_start),
            'date_end': fmt(self.date_end),
            'type_code': (self.type_id.code or '').upper() if self.type_id else '',
            'sign_day': sign_day, 'sign_month': sign_month, 'sign_year': sign_year,
            'end_day': end_day, 'end_month': end_month, 'end_year': end_year,
        }

        try:
            doc = DocxTemplate(template_path)
            doc.render(context)
        except Exception as e:
            raise UserError(_('Lỗi render mẫu Word (kiểm tra biến trong template): %s') % e)

        out = BytesIO()
        doc.save(out)
        out.seek(0)

        filename = 'HopDong_%s.docx' % ((getattr(self, 'contract_code', None) or self.name or employee.name or 'contract').replace('/', '_'))
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(out.read()),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        })
        return {'type': 'ir.actions.act_url', 'url': '/web/content/%s?download=1' % attachment.id, 'target': 'self'}
