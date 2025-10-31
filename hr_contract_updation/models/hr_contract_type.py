# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class HrContractType(models.Model):
    _name = 'hr.contract.type'
    _description = 'Loại hợp đồng'
    _order = 'sequence, id'

    name = fields.Char(string='Tên loại hợp đồng', required=True)
    code = fields.Selection(
        [('HĐLD', 'Hợp đồng Lao động'), ('HĐTV', 'Hợp đồng Thử việc')],
        string='Mã loại HĐ', required=True, help='Phân loại hợp đồng HĐLD hoặc HĐTV'
    )
    description = fields.Text(string='Ghi chú')
    active = fields.Boolean(string='Hiệu lực', default=True)
    
    # ⚙️ Bổ sung để tương thích toàn hệ thống Odoo
    sequence = fields.Integer(string='Thứ tự', default=10, help="Thứ tự hiển thị loại hợp đồng")
    country_id = fields.Many2one('res.country', string='Quốc gia', help='Quốc gia áp dụng (nếu có)')

    _sql_constraints = [
        ('unique_code', 'unique(code)', 'Mã loại hợp đồng đã tồn tại!'),
    ]

    def name_get(self):
        """Hiển thị mã + tên khi chọn loại hợp đồng"""
        result = []
        for rec in self:
            name = "[%s] %s" % (rec.code, rec.name or '')
            result.append((rec.id, name))
        return result
