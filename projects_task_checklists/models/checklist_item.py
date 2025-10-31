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


class ChecklistItem(models.Model):
    """
    Mô hình cho các mục trong danh sách kiểm tra
    """
    _name = 'checklist.item'
    _description = "Mục danh sách kiểm tra"

    name = fields.Char(
        string="Tên mục",
        required=True,
        help="Tên của mục trong danh sách kiểm tra"
    )
    sequence = fields.Integer(
        string="Thứ tự",
        default=1,
        help="Số thứ tự của mục trong danh sách kiểm tra"
    )
    description = fields.Char(
        string="Mô tả",
        help="Mô tả chi tiết về mục trong danh sách kiểm tra"
    )
    checklist_id = fields.Many2one(
        'task.checklist',
        string="Danh sách kiểm tra",
        help="Danh sách kiểm tra mà mục này thuộc về"
    )
