import xmlrpc.client
from pprint import pprint

# CONNECTION DATA ODOO 16 - DEV
URL_ODOO16 = 'https://dev.odoo.universidadisep.com/'
DB_ODOO16 = 'UniversidadISep'
# USER_NAME_ODOO16 = 'gcontreras@universidadisep.com'
# API_KEY_ODOO16 = 'b98c1991b6699ff62dec5a7020bc48f54ed1441d'
# PASSWORD_ODOO16 = '12345678'
USER_NAME_ODOO16 = 'admin_copia'
API_KEY_ODOO16 = '47bd7099eb31149dd8aa6de2d348f4381a46403f'
PASSWORD_ODOO16 = '12345678'


def connect_to_odoo(url, db, user_name, password):
    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/common', allow_none=True)
        uid = common.authenticate(db, user_name, password, {})
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', allow_none=True)
        return uid, models
    except Exception as exception:
        print(f'********** EXCEPTION ********** {exception = }')


uid_odoo16, models_odoo16 = connect_to_odoo(URL_ODOO16, DB_ODOO16, USER_NAME_ODOO16, API_KEY_ODOO16)

active_companies = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'res.company', 'search_read', [[]],
                                            {'fields': ['id', 'name']})
inactive_companies = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'res.company', 'search_read',
                                              [[['active', '=', False]]], {'fields': ['id', 'name']})

pprint(active_companies)
print()
pprint(inactive_companies)
