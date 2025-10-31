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


class ChecklistItemLine(models.Model):
    """
    Mô hình cho các dòng mục trong danh sách kiểm tra
    """
    _name = 'checklist.item.line'
    _description = 'Dòng mục danh sách kiểm tra'

    check_list_item_id = fields.Many2one(
        'checklist.item',
        string="Mục kiểm tra",
        required=True,
        help='Mục thuộc danh sách kiểm tra'
    )
    description = fields.Char(
        string="Mô tả",
        help="Mô tả chi tiết về mục kiểm tra này"
    )
    projects_id = fields.Many2one(
        'project.task',
        string="Công việc",
        help="Tên của công việc hoặc dự án liên quan"
    )
    checklist_id = fields.Many2one(
        'task.checklist',
        string="Danh sách kiểm tra",
        help="Danh sách kiểm tra mà mục này thuộc về"
    )
    state = fields.Selection(
        string='Trạng thái',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        selection=[
            ('todo', 'Cần làm'),
            ('in_progress', 'Đang thực hiện'),
            ('done', 'Hoàn thành'),
            ('cancel', 'Đã hủy')
        ],
        default='todo',
        help="Trạng thái hiện tại của mục kiểm tra"
    )

    def action_approve_and_next(self):
        """
        Phương thức chuyển trạng thái của mục kiểm tra sang 'Đang thực hiện'.
        Hành động này được sử dụng khi phê duyệt và chuyển sang bước tiếp theo.

        :return: None
        """
        self.state = 'in_progress'

    def action_mark_completed(self):
        """
        Phương thức đánh dấu mục kiểm tra là 'Hoàn thành'.
        Hành động này cho biết công việc hoặc bước đã được hoàn tất thành công.

        :return: None
        """
        self.state = 'done'

    def action_mark_canceled(self):
        """
        Phương thức đánh dấu mục kiểm tra là 'Đã hủy'.
        Hành động này cho biết công việc hoặc bước đã bị hủy bỏ hoặc dừng lại.

        :return: None
        """
        self.state = 'cancel'
