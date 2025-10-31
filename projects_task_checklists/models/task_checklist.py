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
from odoo import fields, models


class TaskChecklist(models.Model):
    """
    Mô hình đại diện cho danh sách kiểm tra của công việc.
    """
    _name = 'task.checklist'
    _description = 'Danh sách kiểm tra công việc'

    name = fields.Char(
        string='Tên danh sách',
        help='Tên của danh sách kiểm tra'
    )
    description = fields.Char(
        string='Mô tả',
        help='Mô tả chi tiết về danh sách kiểm tra'
    )
    task_id = fields.Many2one(
        'project.task',
        string='Công việc',
        help='Tên của công việc được liên kết với danh sách kiểm tra này'
    )
    checklist_ids = fields.One2many(
        'checklist.item',
        'checklist_id',
        string='Các mục kiểm tra',
        required=True,
        help='Danh sách các mục cần kiểm tra trong danh sách này'
    )
