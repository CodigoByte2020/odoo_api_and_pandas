# ---> WOULD + PRON + VERB + COMP ?
# WOULD THE PROGRAM RUN WITH ME ?

# THIS SHOULD NORMALLY RUN
# THE PYTHON CODE SHOULD NOT SUCCESSFULLY RUN

'''
    1. Juan estaría en la escuela.
       He would be in the school.
    2. Luisa no comería en su casa.
       She would not eat in her house.
    3. ¿Correrían ellos en el parque?
        Would they run in the park?
    4. Yo estudiaría inglés los sábados.
       I would study english on Saturdays.
    5. ¿Vendrías (tú) a mi casa con tu esposa?
       Would you come to my house with your wife?
    6. Nosotros no bailaríamos en la fiesta.
       We would not dance in the party.
'''

# WHEN I WAS A CHILD I COULD PLAY SOCCER IN A PROFESSIONAL TEAM
# I THINK THAT TOMORROW COULD BE IN THE PARK

import odoorpc

# PREPARE THE CONNECTION TO THE SERVER
# odoo = odoorpc.ODOO(host='https://odoo16migracion.universidadisep.com/', port=443, protocol='jsonrpc+ssl')
# odoo = odoorpc.ODOO(host='https://odoo16migracion.universidadisep.com/', port=443)
odoo = odoorpc.ODOO(host='http://localhost:8060/', port=8060)
# odoo = odoorpc.ODOO('164.92.91.213', port=443)
# odoo = odoorpc.ODOO(host='localhost', port=8060)

# CHECK AVAILABLE DATABASES
print(odoo.db.list())
print('LLEGO')

# CURRENT USER
# user = odoo.env.user
# print(user.name)  # ---> NAME OF THE USER CONNECTED
# print(user.company_id.name)  # ---> NAME OF ITS COMPANY
#
# # SIMPLE RAW QUERY
# user_data = odoo.execute('res.user', 'read', [user.id])
# print(user_data)


