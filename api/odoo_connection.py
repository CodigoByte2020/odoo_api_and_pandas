import xmlrpc.client

# CONNECTION DATA ODOO 12
URL_ODOO12 = 'https://odoo12migracion.universidadisep.com'
DB_ODOO12 = 'final'
USER_NAME_ODOO12 = 'admin_miguel'
PASSWORD_ODOO12 = '12345678'

# # CONNECTION DATA ODOO 16
# URL_ODOO16 = 'https://odoo16migracion.universidadisep.com'
# DB_ODOO16 = 'UniversidadISep2'
# USER_NAME_ODOO16 = 'admin_miguel'
# PASSWORD_ODOO16 = '12345678'
# API_KEY_ODOO16 = 'aa73c825128ec71f64e4594a649a34ccd8f58d0f'

# CONNECTION DATA ODOO 16 - PRODUCTION
URL_ODOO16 = 'https://app.universidadisep.com/'
DB_ODOO16 = 'UniversidadISep2'
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


uid_odoo12, models_odoo12 = connect_to_odoo(URL_ODOO12, DB_ODOO12, USER_NAME_ODOO12, PASSWORD_ODOO12)
uid_odoo16, models_odoo16 = connect_to_odoo(URL_ODOO16, DB_ODOO16, USER_NAME_ODOO16, API_KEY_ODOO16)
