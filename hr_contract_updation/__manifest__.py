# -*- coding: utf-8 -*-
{
    'name': 'Cập nhật Hợp đồng Nhân sự (VN)',
    'version': '1.0.0',
    'summary': 'Mã HĐ = [PIN]/[Năm]/[HĐLD|HĐTV]; kế thừa CCCD & chức danh; loại HĐ',
    'author': 'Bạn & ChatGPT',
    'category': 'Human Resources',
    'website': 'https://odoo.com',
    'license': 'LGPL-3',
    'depends': ['hr', 'hr_contract', 'hr_employee_updation', 'mail'],
    'data': [
        'data/hr_contract_type_data.xml',
        'views/hr_contract_type_views.xml',
        'views/hr_contract_views.xml',
    ],
    'installable': True,
    'application': False,
}
