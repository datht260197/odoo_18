# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.modules.module import get_module_path
import base64
import os

try:
    from docxtpl import DocxTemplate
except Exception:
    DocxTemplate = None


class HrContract(models.Model):
    _inherit = "hr.contract"

    def _get_template_filename(self):
        code = (self.type_id.code or "").upper() if self.type_id else ""
        if "TV" in code:
            return "contract_template_trial.docx"
        return "contract_template.docx"

    def _get_template_path(self):
        module_path = get_module_path("hr_contract_print_word")
        return os.path.join(module_path, "static", "template", self._get_template_filename())

    def _get_render_values(self):
        self.ensure_one()
        emp = self.employee_id
        code_suffix = (self.type_id.code or "HĐLĐ")
        contract_code = f"{emp.pin or 'NA'}/{fields.Date.today().year}/{code_suffix}"
        vals = {
            "employee_name": emp.name or "",
            "job_title": emp.job_title or "",
            "cccd": emp.identification_id or "",
            "ngay_cap": emp.id_issue_date.strftime("%d/%m/%Y") if getattr(emp, "id_issue_date", False) else "",
            "noi_cap": getattr(emp, "id_issue_place", "") or "",
            "thuong_tru": emp.private_city or "",
            "contract_code": contract_code,
            "contract_type": self.type_id.name or "",
            "date_start": self.date_start.strftime("%d/%m/%Y") if self.date_start else "",
            "date_end": self.date_end.strftime("%d/%m/%Y") if self.date_end else "",
            "wage": "{:,.0f}".format(self.wage or 0).replace(",", "."),
            "company_name": self.company_id.name or "",
            "company_street": self.company_id.street or "",
            "company_city": self.company_id.city or "",
            "company_vat": self.company_id.vat or "",
            "na": "",
        }
        return vals

    def action_print_word_contract(self):
        self.ensure_one()
        if DocxTemplate is None:
            raise UserError(_("Thiếu thư viện python 'docxtpl'. Hãy cài: pip install docxtpl"))

        template_path = self._get_template_path()
        if not os.path.exists(template_path):
            raise UserError(_("Không tìm thấy file mẫu hợp đồng: %s") % template_path)

        tpl = DocxTemplate(template_path)
        tpl.render(self._get_render_values())

        module_path = get_module_path("hr_contract_print_word")
        out_dir = os.path.join(module_path, "static", "output")
        os.makedirs(out_dir, exist_ok=True)
        safe_emp = (self.employee_id.name or "employee").replace("/", "-")
        out_name = f"HĐ_{safe_emp}.docx"
        out_path = os.path.join(out_dir, out_name)
        tpl.save(out_path)

        with open(out_path, "rb") as f:
            data = f.read()
        attachment = self.env["ir.attachment"].create({
            "name": out_name,
            "datas": base64.b64encode(data),
            "res_model": self._name,
            "res_id": self.id,
            "mimetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        })
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }
