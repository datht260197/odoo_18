# -*- coding: utf-8 -*-
#############################################################################
#    A part of OpenHRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from datetime import timedelta
from odoo import api, fields, models, _


class HrEmployee(models.Model):
    """Mở rộng model Nhân viên để bổ sung các trường và chức năng nâng cao."""
    _inherit = 'hr.employee'

    # --- Thông tin liên hệ & ngày vào làm ---
    personal_mobile = fields.Char(
        string='Di động cá nhân',
        related='private_phone',
        store=True,
        help="Số điện thoại di động cá nhân của nhân viên."
    )
    joining_date = fields.Date(
        compute='_compute_joining_date',
        string='Ngày vào làm',
        store=True,
        help="Ngày nhân viên bắt đầu làm việc (tính từ hợp đồng đầu tiên)."
    )

    # --- Thông tin giấy tờ tùy thân ---
    identification_id = fields.Char(
        string='Số CCCD',
        help="Số căn cước công dân của nhân viên."
    )
    id_issue_date = fields.Date(
        string="Ngày cấp CCCD",
        help="Ngày cấp căn cước công dân."
    )
    id_issue_place = fields.Char(
        string="Nơi cấp CCCD",
        help="Nơi cấp căn cước công dân."
    )
    ethnicity = fields.Char(
        string="Dân tộc",
        help="Dân tộc của nhân viên."
    )
    id_expiry_date = fields.Date(
        string='Ngày hết hạn CCCD',
        help='Ngày hết hạn của căn cước công dân.'
    )
    passport_id = fields.Char(
        string='Số hộ chiếu',
        help='Số hộ chiếu của nhân viên.'
    )
    passport_expiry_date = fields.Date(
        string='Ngày hết hạn hộ chiếu',
        help='Ngày hết hạn của hộ chiếu.'
    )

    identification_attachment_ids = fields.Many2many(
        'ir.attachment',
        'id_attachment_rel',
        'id_ref', 'attach_ref',
        string="Đính kèm CCCD",
        help='Đính kèm bản sao căn cước công dân.'
    )
    passport_attachment_ids = fields.Many2many(
        'ir.attachment',
        'passport_attachment_rel',
        'passport_ref', 'attach_ref1',
        string="Đính kèm hộ chiếu",
        help='Đính kèm bản sao hộ chiếu.'
    )

    # --- Thông tin gia đình ---
    family_info_ids = fields.One2many(
        'hr.employee.family',
        'employee_id',
        string='Người phụ thuộc',
        help='Thông tin người phụ thuộc của nhân viên.'
    )

    # ----------------------------------------------------------
    # COMPUTE & ONCHANGE
    # ----------------------------------------------------------
    @api.depends('contract_id.date_start')
    def _compute_joining_date(self):
        """Tính ngày vào làm dựa trên hợp đồng sớm nhất của nhân viên."""
        for employee in self:
            dates = employee.contract_id.mapped('date_start')
            employee.joining_date = min(dates) if dates else False

    @api.onchange('spouse_complete_name', 'spouse_birthdate')
    def _onchange_spouse_complete_name(self):
        """Tự động thêm thông tin vợ/chồng vào danh sách người phụ thuộc."""
        relation = self.env.ref('hr_employee_updation.employee_relationship', raise_if_not_found=False)
        if self.spouse_complete_name and self.spouse_birthdate and relation:
            self.family_info_ids = [(0, 0, {
                'member_name': self.spouse_complete_name,
                'relation_id': relation.id,
                'birth_date': self.spouse_birthdate,
            })]

    # ----------------------------------------------------------
    # REMINDER: EMAIL NOTIFICATION
    # ----------------------------------------------------------
    def expiry_mail_reminder(self):
        """Gửi email nhắc nhở khi CCCD hoặc hộ chiếu sắp hết hạn."""
        current_date = fields.Date.context_today(self)
        employees = self.search(['|', ('id_expiry_date', '!=', False),
                                      ('passport_expiry_date', '!=', False)])
        for emp in employees:
            # --- CCCD ---
            if emp.id_expiry_date:
                exp_date = emp.id_expiry_date - timedelta(days=14)
                if current_date >= exp_date:
                    mail_content = (
                        f"Xin chào {emp.name},<br/>"
                        f"CCCD số {emp.identification_id or ''} của bạn sẽ hết hạn vào ngày "
                        f"{emp.id_expiry_date}.<br/>Vui lòng gia hạn trước khi hết hạn."
                    )
                    self.env['mail.mail'].sudo().create({
                        'subject': _('CCCD %s sắp hết hạn') % (emp.identification_id or ''),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': emp.work_email,
                    }).send()
            # --- Hộ chiếu ---
            if emp.passport_expiry_date:
                exp_date = emp.passport_expiry_date - timedelta(days=180)
                if current_date >= exp_date:
                    mail_content = (
                        f"Xin chào {emp.name},<br/>"
                        f"Hộ chiếu {emp.passport_id or ''} của bạn sẽ hết hạn vào ngày "
                        f"{emp.passport_expiry_date}.<br/>Vui lòng gia hạn trước khi hết hạn."
                    )
                    self.env['mail.mail'].sudo().create({
                        'subject': _('Hộ chiếu %s sắp hết hạn') % (emp.passport_id or ''),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': emp.work_email,
                    }).send()
