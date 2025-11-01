# -*- coding: utf-8 -*-
{
    "name": "HR Contract Print Word",
    "summary": "In hợp đồng lao động ra Word với đầy đủ thông tin nhân viên",
    "version": "18.0.1.1.0",
    "category": "Human Resources/Contracts",
    "license": "LGPL-3",
    "author": "Việt Hàn Solutions",
    "depends": ["hr_contract"],
    "data": [
        "views/hr_contract_views.xml",
    ],
    "external_dependencies": {"python": ["docxtpl"]},
    "installable": True,
    "application": False,
}
