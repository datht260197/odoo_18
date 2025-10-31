# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Dhanya B (odoo@cybrosys.com)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
################################################################################
from odoo import api, fields, models


class ProjectTask(models.Model):
    """Kế thừa model project.task để thêm các trường liên quan đến danh sách kiểm tra"""
    _inherit = 'project.task'

    start_date = fields.Datetime(
        string='Ngày bắt đầu',
        help="Ngày bắt đầu của công việc"
    )
    end_date = fields.Datetime(
        string='Ngày kết thúc',
        help="Ngày kết thúc của công việc"
    )
    progress = fields.Float(
        compute='_compute_progress',
        string='Tiến độ (%)',
        help="Phần trăm tiến độ hoàn thành công việc"
    )
    checklist_ids = fields.Many2many(
        'task.checklist',
        compute='_compute_checklist_ids',
        string='Danh sách kiểm tra',
        help="Các danh sách kiểm tra liên quan đến công việc này"
    )
    checklist_id = fields.Many2one(
        'task.checklist',
        string='Danh sách kiểm tra',
        help="Chọn danh sách kiểm tra áp dụng cho công việc"
    )
    checklists_ids = fields.One2many(
        'checklist.item.line',
        'projects_id',
        string='Các mục kiểm tra',
        required=True,
        help='Thêm các mục kiểm tra vào công việc'
    )

    @api.onchange('checklist_id')
    def _onchange_checklist_id(self):
        """
        Kích hoạt khi trường 'Danh sách kiểm tra' thay đổi.
        Hệ thống sẽ tìm danh sách kiểm tra tương ứng và tự động
        cập nhật các mục kiểm tra trong trường 'Các mục kiểm tra'.

        :return: None
        """
        checklist = self.env['task.checklist'].search(
            [('name', '=', self.checklist_id.name)])
        self.checklists_ids = False
        self.checklists_ids = [(0, 0, {
            'check_list_item_id': rec.id,
            'state': 'todo',
            'checklist_id': self.checklist_id.id,
        }) for rec in checklist.checklist_ids]

    def _compute_checklist_ids(self):
        """
        Hàm tính toán để cập nhật trường 'Danh sách kiểm tra'.
        Lấy danh sách kiểm tra có liên kết với công việc hiện tại.

        :return: None
        """
        for rec in self:
            self.checklist_ids = self.env['task.checklist'].search(
                [('task_id', '=', rec.id)])

    def _compute_progress(self):
        """
        Hàm tính toán phần trăm tiến độ công việc.
        Duyệt qua các mục kiểm tra và tính tỉ lệ phần trăm
        các mục đã hoàn thành, đang thực hiện hoặc đã hủy.

        :return: None
        """
        for rec in self:
            total_completed = 0
            for activity in rec.checklists_ids:
                if activity.state in ['cancel', 'done', 'in_progress']:
                    total_completed += 1
            if total_completed:
                rec.progress = float(total_completed) / len(
                    rec.checklists_ids) * 100
            else:
                rec.progress = 0.0
