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
response.subtitle = T('Fleet Management System')
 
## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'HILARIO B. VILLAR <tribo.ni.eila@gmail.com>'
response.meta.description = 'Diversified into a spectrum of industrial activities, including trading, construction, mmunication, manufacturing, petroleum and industrial services and travel.'
response.meta.keywords = 'kassem, darwish, darwish group'
response.meta.generator = 'KASSEM DARWISH FAKHRO & SONS'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

if (auth.user_id != None) & (auth.has_membership(role = 'level_1_user') | (auth.has_membership(role = 'level_3_user'))):
    response.menu = [
    #((I(_class = 'icon-home'), T('Home')), False, URL('default', 'index')),
    #[TAG[''](IMG(_src=URL(r=request, c='static', f='images/overview.png'), 'Overview')), False, URL(request.application, 'default', 'index')],

    ((SPAN(_class = 'glyphicon glyphicon-home'), T('Home')), False, URL('default', 'index')),
    #(T('Contact'), False, URL('default', 'contact')),
    #(T('KDS/DTC'), False, URL('default', 'index'),
    # [
    #    (T('Company'), False, URL('default', 'GroupCompanies')), 
    #    (T('Division'), False, URL('default', 'DTCDivision'))
    #    ]),
    (T('Browse'), False, URL('#'),
        [
            (T('Vehicles'), False, URL('default', 'Browse')),
            (T('Exp. Notification'), False, URL('Reports', 'ExpirationNotification'),
                [
                    (T('Road Permit'), False, URL('Reports', 'RoadPermitNotification')),
                    (T('Insurance Policy'), False, URL('Reports', 'InsPolicyNotification')),
                    (T('Driving License'), False, URL('Reports', 'DriverNotification')),
                ]),           

            (T('Insurance Policy'), False, URL('default', 'index'),
                [
                    (T('Active'), False, URL('default', 'InsurancePolicy')),   
                    (T('Non-Active'), False, URL('default', 'NonActiveInsurancePolicy')),   
                ]),
            (T('Advertisement'), False, URL('default', 'index'),
                [
                    (T('Active'), False, URL('default', 'Advertisement')),   
                    (T('Non-Active'), False, URL('default', 'NonActiveAdvertisement')),
                    (T('Without Ads'), False, URL('default', 'WithoutAdvertisement')),   
                ]),   
            (T('Cancelled'), False, URL('default', 'Cancelled')),
            (T('Hand-Over'), False, URL('default', 'HandOver')),
        ]),
    (T('Create'), False, URL('default', 'index'),
        [
            (T('New Vehicle'), False, URL('default', 'VehicleProfileForm')),
            (T('Vehicle Expenses'), False, URL('default', 'index'),
                [
                    (T('Maintenance Expenses'), False, URL('default', 'MaintenanceExpensesForm')),
                    (T('Fuel Expenses'), False, URL('default', 'FuelExpensesForm')),
                    (T('Mileage'), False, URL('default', 'OdometerForm')),
                ]),
            (T('Insurance'), False, URL('default', 'index'),
                [
                    (T('Insurance Policy'), False, URL('default', 'InsurancePolicyForm')),
                    (T('Insured Vehicle'), False, URL('default', 'InsuredVehiclesForm')),
                ]),
            (T('Advertisement'), False, URL('default', 'index'),
                [
                    (T('License No.'), False, URL('default', 'AdvertisementForm')),
                    (T('Ads Vehicle'), False, URL('default', 'AdsVehiclesForm')),
                ]),   
            (T('Upload Photo\'s'), False, URL('default', 'upload_photos')),
            (T('Hand Over'), False, URL('default', 'HandOverForm')),
        ]),
    (T('Driver'), False, URL('default', 'Driver')),
    (T('Data Management'), False, URL('default', 'index'),    
         [
            (T('Companies'), False, URL('default', 'GroupCompany')),
            (T('Controller'), False, URL('default', 'Controller')),
            (T('Owner Name'), False, URL('default', 'owner')),
            (T('Manufacturer'), False, URL('default', 'manufacturer')),
            (T('Vehicle Category'), False, URL('default', 'vehicle_category')),
            (T('Vehicle Purpose'), False, URL('default', 'vehicle_purpose')),
            (T('Vehicle Status'), False, URL('default', 'vehicle_status')),
            (T('Vehicle Insurance'), False, URL('default', 'insurance')),
            (T('Workshop'), False, URL('default', 'workshop')),
            (T('Insurance Pol. Status'), False, URL('default', 'InsPolStatus')),
            (T('Advertisement Status'), False, URL('default', 'AdsStatus')),
            (T('Authorized Vehicle'), False, URL('default', 'authorized_vehicle_category')),
            (T('Driver Position'), False, URL('default', 'driver_position')),
        ]),
    (T('Reports'), False, URL('default', 'index'),
         [
            (T('Summary'), False, URL('Reports', 'VehicleSummaryReport')),
            (T('Vehicles'), False, URL('default', 'index'),
                [
                    (T('Company'), False, URL('Reports', 'CompanyVehiclesReport')),
                    (T('Division'), False, URL('Reports', 'DivisionVehiclesReport')),
                    (T('Department'), False, URL('Reports', 'DepartmentVehiclesReport')),
                ]),
            (T('Fuel Expenses'), False, URL('default', 'index'),
             [
                (T('Summary'), False, URL('FuelReports', 'CompanySummaryFuelReport')),
                (T('Vehicle'), False, URL('FuelReports', 'VehicleFuelExpensesReport')),
                (T('Company'), False, URL('FuelReports', 'CompanyFuelExpensesReport')),
                (T('Division'), False, URL('FuelReports', 'DivisionFuelExpensesReport')),
                (T('Department'), False, URL('FuelReports', 'DepartmentFuelExpensesReport')),
                ]),
            (T('Repair Expenses'), False, URL('default', 'index'),
                [
                    (T('Summary'), False, URL('MaintenanceReports', 'CompanyMaintenanceSummaryReport')),
                    (T('Vehicle'), False, URL('MaintenanceReports', 'VehicleMaintenanceReport')),
                    (T('Company'), False, URL('MaintenanceReports', 'CompanyMaintenanceReport')),
                    (T('Division'), False, URL('MaintenanceReports', 'DivisionMaintenanceReport')),
                    (T('Department'), False, URL('MaintenanceReports', 'DepartmentMaintenanceReport')),
                ]),
            (T('Hand-Over'), False, URL('Reports', 'VehicleMaintenanceReport'),
                [
                    (T('Reg.No.'), False, URL('Reports', 'RegNoHandoverReport')),
                    (T('Driver'), False, URL('Reports', 'DriverHandoverReport')),
                ]),

            (T('Mileage'), False, URL('Reports', 'VehicleMileageReport')),
            (T('Exp. Notification'), False, URL('default', 'index'),
                [
                    (T('Road Permit'), False, URL('default', 'index'),
                        [
                            (T('Company'), False, URL('Notification', 'RoadPermitNotification')),
                            (T('Division'), False, URL('Notification', 'RodPerNotDiv')),
                            (T('Department'), False, URL('Notification', 'RodPerNotDept')),
                        ]),
                    (T('Insurance Policy'), False, URL('Notification', 'InsPolicyNotification')),
                    (T('Driving License'), False, URL('Notification', 'DriverNotification')),

                ]),
            (T('Advertisement'), False, URL('default', 'index'),
                [
                    (T('With Advertisement'), False, URL('default', 'index'),
                        [
                            (T('By Company'), False, URL('Reports', 'WAdsCompanyReport')),
                            (T('By Division'), False, URL('Reports', 'WAdsDivisionReport')),
                            (T('By Department'), False, URL('Reports', 'WAdsDepartmentReport')),
                        ]),
                    (T('Without Advertisement'), False, URL('default', 'index'),
                        [
                            (T('By Company'), False, URL('Reports', 'WOAdsCompanyReport')),
                            (T('By Division'), False, URL('Reports', 'WOAdsDivisionReport')),
                            (T('By Department'), False, URL('Reports', 'WOAdsDepartmentReport')),
                        ]),
                ]),
            (T('Form Download'), False, URL('default', 'FormDownload')),
            (T('Activity'), False, URL('Reports', 'Activity')),
    ]),       
] 
elif (auth.user_id != None) & (auth.has_membership(role = 'level_2_user')):
    response.menu = [
        (T('Home'), False, URL('Company', 'index')),
        (T('Maintenance Expenses'), False, URL('Company', 'MaintenanceExpenses')),
        (T('Fuel Expenses'), False, URL('Company', 'FuelExpenses')),
        (T('Mileage'), False, URL('Company', 'Mileage')),
        (T('Hand-Over'), False, URL('Company', 'HandOver')),
        (T('Reports'), False, URL('Company', 'index'),
            [
                (T('Summary'), False, URL('Company', 'VehicleSummaryReport')),
                (T('Vehicles'), False, URL('default', 'index'),
                    [
                        (T('Company'), False, URL('Company', 'CompanyVehiclesReport')),
                        (T('Division'), False, URL('Company', 'DivisionVehiclesReport')),
                        (T('Department'), False, URL('Company', 'DepartmentVehiclesReport')),
                    ]),

                (T('Repair Expenses'), False, URL('Company', 'DivisionMaintenanceReport')),
                (T('Fuel Expenses'), False, URL('Company', 'DivisionFuelReport')),
                (T('Mileage'), False, URL('Company', 'DivisionMileageReport')),
                (T('Hand-Over'), False, URL('Company', 'DivisionHandOverReport')),
            ]
        ),
    ]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def breadcrumbs(arg_title=None):
       "Create breadcrumb links for current request"
       # make links pretty by capitalizing and using 'home' instead of 'default'
       pretty = lambda s: s.replace('default', 'Início').replace('_', ' ').capitalize()
       menus = [A(T('Home'), _href=URL(r=request, c='default', f='index'))]
       if request.controller != 'default':
           # add link to current controller
           menus.append(A(T(pretty(request.controller)), _href=URL(r=request, c=request.controller, f='index')))
           if request.function == 'index':
               # are at root of controller
               menus[-1] = A(T(I(pretty(request.controller)), _href=URL(r=request, c=request.controller, f=request.function), _class="ace-icon fa fa-home home-icon"))
           else:
               # are at function within controller
               menus.append(A(T(pretty(request.function)), _href=URL(r=request, c=request.controller, f=request.function)))
           # you can set a title putting using breadcrumbs('My Detail Title') 
           if request.args and arg_title:
               menus.append(A(T(arg_title)), _href=URL(r=request, c=request.controller, f=request.function,args=[request.args]))
       else:
           #menus.append(A(pretty(request.controller), _href=URL(r=request, c=request.controller, f='index')))
           if request.function == 'index':
               # are at root of controller
               #menus[-1] = pretty(request.controller)
               pass
               #menus.append(A(pretty(request.controller), _href=URL(r=request, c=request.controller, f=request.function)))
           else:
               # are at function within controller
               menus.append(A(T(pretty(request.function)), _href=URL(r=request, c=request.controller, f=request.function)))
           # you can set a title putting using breadcrumbs('My Detail Title') 
           if request.args and arg_title:
               menus.append(A(T(arg_title), _href=URL(r=request, f=request.function,args=[request.args])))

       return XML(' > '.join(str(m) for m in menus))