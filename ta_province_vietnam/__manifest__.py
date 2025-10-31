{
    'name': 'Vietnam Province Merge 2025 | Cập nhật 34 tỉnh thành Việt Nam',
    'summary': 'Update 34 provinces of Vietnam according to Resolution 202/2025/QH15',
    'version': '18.0.1.0.0',
    'category': 'Localization',
    'author': 'Mountain Tran',
    'support': 'mountaintran2021@gmail.com',
    'website': 'https://mountain-coder.com',
    'license': 'OPL-1',
    'price': 0,
    'currency': 'EUR',
    'description': """
Vietnam Province Merge 2025
===========================
This module updates the list of Vietnamese provinces from 63 to 34 provinces 
according to Resolution No. 202/2025/QH15 of the National Assembly.

Features:
- Update the list to 34 new provinces
- Cron job to migrate old province data to the new structure
- Only allow selection of new provinces in the system
    """,
    'depends': ['base'],
    'data': [
        'data/vietnam_states_data.xml',
        'data/ir_cron_data.xml',
    ],
    'images': [
        'static/description/banner.gif',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}