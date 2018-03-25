# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="brand",_href="http://www.darwish-group.com/")
#response.title = ''.join(
#    word.capitalize() for word in request.application.split('_'))
response.title = T('Darwish Group') 
response.subtitle = T('Vehicle Management System')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'HILARIO B. VILLAR <tribo.ni.eila@gmail.com>'
response.meta.description = 'Diversified into a spectrum of industrial activities, \
                            including trading, construction, communication, \
                            manufacturing, petroleum and industrial services and travel.'
response.meta.keywords = 'kassem, darwish, darwish group'
response.meta.generator = 'KASSEM DARWISH FAKHRO & SONS'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################
'''
response.menu = [
    (T('Home'), False, URL('default', 'index')),
    #(T('About'), False, URL('default', 'about')),
    #(T('Contact'), False, URL('default', 'contact')),
    (T('Division'), False, URL('default', 'division_list')),
    (T('Vehicle'), False, URL('default', 'index'),
        [
            (T('Insert'), False, URL('default', 'new_vehicle')),
            (T('Browse'), False, URL('default', 'vehicle'))
        ]
    ),
        #(T('Repair History'), False, URL('default', 'repairs')),
        #(T('Log Sheet'), False, URL('default', 'log_sheet')),
        (T('Driver'), False, URL('default', 'driver')),
        (T('Data Management'), False, URL('default', 'data_management'),    
         [
            (T('KDS-Management'), False, URL('default', 'division')),
            (T('Subdivision'), False, URL('default', 'subdivision')),
            (T('Manufacturer'), False, URL('default', 'manufacturer')),
            (T('Vehicle Category'), False, URL('default', 'vehicle_category')),
            (T('Tyre Brand'), False, URL('default', 'tyre_brand')),
            (T('Vehicle Status'), False, URL('default', 'vehicle_status')),
            (T('Vehicle Insurance'), False, URL('default', 'insurance')),
            ]),
        (T('Alerts!'), False, URL('default', 'alerts')),
        (T('Messages'), False, URL('default', 'messages')),
]
div = ([
    (1, 'KDS-Management'),(2, 'Darwish Trading Co. W.L.L.'),(3, 'Darwish Petroleum & Industrial Services'),
    (4, 'Darwish Mechanical & Electrical Co. W.L.L.'),(5, 'Darwish Contracting Co. W.L.L.'),
    (6, 'Darwish Elevators Co. W.L.L. (OTIS)'),(7, 'Gulf Timber & Joinery Co. W.L.L.'),
    (8, 'Qatar Communication Co. W.L.L.'),(9, ''),
    (10, ''),(11, ''),
    (12, ''),(13, ''),
    (14, ''),(15, ''),(16, ''),
    (17, ''),(18, ''),(19, ''),
    (20, '')])



        [
            (T('KDS-Management'), False, URL('division', 'kds_management')),
            (T('Darwish Trading Co. W.L.L.'), False, URL('division', 'division_list')),
            (T('Darwish Petroleum & Industrial Services'), False, URL('division', 'division_list')),
            (T('Darwish Mechanical & Electrical Co. W.L.L.'), False, URL('division', 'division_list')),
            (T('Darwish Contracting Co. W.L.L.'), False, URL('division', 'division_list')),
            (T('Arabesque GRC, Qatar'), False, URL('division', 'division_list')),
            (T('Gulf Aluminium Co. W.L.L.'), False, URL('division', 'division_list')),
            (T('Real Estate Investment'), False, URL('division', 'division_list')),
            (T('Oasis Hotel & Beach Club'), False, URL('division', 'division_list')),
            (T('Darwish Travel Co. W.L.L.'), False, URL('division', 'division_list')),
            (T('Darwish Travel Bureau'), False, URL('division', 'division_list')),
            (T('Qatar Tours'), False, URL('division', 'division_list')),
            (T('Qatar Travels'), False, URL('division', 'division_list')),
            (T('Q.N.T. Cargo'), False, URL('division', 'division_list')),
            (T('Darwish Holidays'), False, URL('division', 'division_list')),
            (T('Airport Services'), False, URL('division', 'division_list')),
            (T('Gulf Automobiles & Trading Co. W.L.L.'), False, URL('division', 'division_list')),
        ]),




'''
if (auth.user_id != None) & (auth.has_membership(role = 'admin')):
    response.menu = [
    (T('Home'), False, URL('default', 'index')),
    #(T('About'), False, URL('default', 'about')),
    #(T('Contact'), False, URL('default', 'contact')),
    (T('Group Company'), False, URL('default', 'group_companies')),
#     [
#        (T('ARABESQUE GRC, QATAR'), False, URL('default', 'new_vehicle')),
#        (T('DARWISH CONTRACTING CO. W.L.L.'), False, URL('default', 'new_vehicle')),
#        (T('DARWISH MECHANICAL & ELECTRICAL CO. W.L.L. '), False, URL('default', 'new_vehicle')),
#        (T('DARWISH PETROLEUM & INDUSTRIAL SERVICES'), False, URL('default', 'new_vehicle')),
#        (T('GULF AUTOMOBILES & TRADING CO. W.L.L.'), False, URL('default', 'new_vehicle')),
#        (T('GULF TIMBER & JOINERY CO. W.L.L.'), False, URL('default', 'new_vehicle')),
#        (T('HR/PERSONAL DEPARTMENT'), False, URL('default', 'new_vehicle')),
#        (T('DARWISH ELEVATORS CO. W.L.L. (OTIS) '), False, URL('default', 'new_vehicle')),
#        (T('QATAR COMMUNICATION CO. W.L.L.'), False, URL('default', 'new_vehicle'))
#     ]),
    (T('DTC Division'), False, URL('default', 'dtc_division')),
    (T('Vehicles'), False, URL('default', 'index'),
        [
            #(T('New Vehicle'), False, URL('default', 'new_vehicle')),
            #(T('KM Used'), False, URL('default', 'km_used')),
            (T('Hand-Over'), False, URL('default', 'hand_over')),
            (T('Upload Photo\'s'), False, URL('default', 'upload_photos')),
            (T('Browse All'), False, URL('default', 'vehicles'))
        ]
    ),
    
        (T('Insurance Policy'), False, URL('default', 'insurance_policy')),
        #(T('Log Sheet'), False, URL('default', 'log_sheet')),
        (T('Driver'), False, URL('default', 'driver')),
        (T('Data Management'), False, URL('default', 'index'),    
         [
            (T('Group Companies'), False, URL('default', 'group')),
            (T('DTC Division'), False, URL('default', 'group_division')),
            (T('Department'), False, URL('default', 'department')),
            (T('Owner Name'), False, URL('default', 'owner')),
            (T('Manufacturer'), False, URL('default', 'manufacturer')),
            (T('Vehicle Category'), False, URL('default', 'vehicle_category')),
            (T('Vehicle Purpose'), False, URL('default', 'vehicle_purpose')),
            (T('Vehicle Status'), False, URL('default', 'vehicle_status')),
            (T('Vehicle Insurance'), False, URL('default', 'insurance')),
            (T('Workshop'), False, URL('default', 'workshop')),
            (T('Authorized Vehicle'), False, URL('default', 'authorized_vehicle_category')),
            (T('Driver Position'), False, URL('default', 'driver_position')),
            
            ]),
#        (T('Alerts!'), False, URL('default', 'alerts')),
        (T('Reports'), False, URL('reports', 'fuel_report'),
         [
            (T('Summary'), False, URL('default', 'vehicle_summary_report')),
            (T('Driver'), False, URL('default', 'driver_log_sheet_report')),
            (T('Fuel Expenses'), False, URL('default', 'index'),
             [
                (T('Vehicle'), False, URL('default', 'vehicle_fuel_expenses_report')),
                (T('Company'), False, URL('default', 'company_fuel_expenses_report')),
                (T('Department'), False, URL('default', 'department_fuel_expenses_report')),
                
                ]),
            (T('Repair Expenses'), False, URL('default', 'vehicle_maintenance_report'))
            ])


]
elif (auth.user_id != None) & (auth.has_membership(role = 'user_div')):
    response.menu = [
        (T('Home'), False, URL('gc_div', 'index')),
#        (T('Vehicle'), False, URL('default', 'vehicle'),
#         [
#            (T('Insert Vehicle'), False, URL('default', 'new_vehicle'))
#            ]),
        (T('Log Sheet'), False, URL('gc_div', 'log_sheet')),
        (T('Driver'), False, URL('gc_div', 'driver'))
#        (T('Subdivision'), False, URL('default', 'subdivision')),
#        (T('Alerts!'), False, URL('default', 'alerts')),
#        (T('Messages'), False, URL('default', 'contact'))
        ]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

