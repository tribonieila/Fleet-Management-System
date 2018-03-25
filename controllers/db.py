# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https() 
import locale
locale.setlocale(locale.LC_ALL,'')
if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline' 

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

response.generic_patterns = ['*'] if request.is_local else []
response.generic_patterns = ['load']
## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'mail.darwish-group.com:143'
mail.settings.sender = 'hilario@darwish-group.com'
mail.settings.login = 'hilario:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
auth.enable_record_versioning(db)


    
db = DAL('postgres://root:admin@localhost:5432/kds','postgres://root:admin@localhost:5432/kds_backup')
auth = Auth(globals(),db)

#auth.settings.actions_disabled.append('register')
auth.settings.actions_disabled=['register', 'request_reset_password','retrieve_username']
if request.controller != 'appadmin': auth.settings.actions_disabled +=['register']

db.define_table('company', 
    Field('company', requires = IS_UPPER()), 
    Field('cr', 'upload', label = 'Company ID'), format = '%(company)s')

db.define_table('division',
    Field('company_id', db.company, readable = False, writable = False), 
    Field('division', requires = IS_UPPER(), label = 'Division'),format = '%(division)s')

db.define_table('department', 
    Field('division_id', db.division, readable = False, writable = False),
    Field('name', requires = IS_UPPER(),label = 'Department'), format = '%(name)s')

#auth.settings.extra_fields['auth_user'] = [Field('department_id', writable = False, readable = False, label = 'Department',
#                                                 requires = IS_IN_DB(db, db.department.id,'%(name)s',zero= '-- Choose department --'))]
###################################
db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default=''),
    Field('last_name', length=128, default=''),
    Field('username', unique = True, readable = False, writable = False),
    Field('email', length=128, default='', unique=True), # required
    Field('division_id', db.division, label = 'Division', writable = False, readable = False),
    #Field('department_id', db.department, label = 'Department', writable = False, readable = False),
    Field('password', 'password', length=512,            # required
          readable=False, label='Password', writable = False),
    Field('po_box', label = 'PO Box'),
    Field('mobile_no'),
    Field('office_no'),
    Field('fax_no'),
    Field('registration_key', length=512,                # required
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,              # required
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,                 # required
          writable=False, readable=False, default=''))

## do not forget validators
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [CRYPT()]
custom_auth_table.email.requires = [
  IS_EMAIL(error_message=auth.messages.invalid_email),
  IS_NOT_IN_DB(db, custom_auth_table.email)]

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table

####################################
auth.define_tables(username = True)
crud = Crud(globals(),db)

db.define_table('vehicle_type', Field('vehicle_name'), format = '%(vehicle_name)s')

db.define_table('vehicle_category', Field('category'),
    Field('description', 'text',represent=lambda text, row: PRE(text)), format = '%(category)s' )

db.define_table('tyre_brand', Field('name'), format = '%(name)s')

db.define_table('vehicle_status', Field('status'), format = '%(status)s')

db.define_table('vehicle_insurance', Field('name'), format = '%(name)s')

db.define_table('vehicle_purpose', Field('purpose'), format = '%(purpose)s')

db.define_table('owner', Field('name'), format = '%(name)s')
today = request.now

db.define_table('vehicle',
    Field('company_id', 'reference company', requires = IS_IN_DB(db, db.company, '%(company)s', zero = 'Choose company'), 
        represent = lambda id, r: db.company(id).company, label = 'Company'),
    Field('division_id', 'reference division', requires = IS_IN_DB(db, db.division, '%(division)s', zero = 'Choose division'),
        represent = lambda id, r: db.division(id).division, label = 'Division'),
    Field('department', 'reference department', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose department'), 
        represent = lambda id, r: db.department(id).name, label = 'Department'),
    Field('owner', 'reference owner', requires = IS_IN_DB(db, db.owner, '%(name)s', zero = 'Choose owner'),
        represent = lambda id, r: db.owner(id).name, label = 'Owner'),
    Field('vehicle_code', requires = IS_NOT_IN_DB(db, 'vehicle.vehicle_code', error_message = 'Vehicle code already exist or empty!') ,label = 'VEH.CD.'),
    Field('reg_no', requires = (IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'vehicle.reg_no', error_message = 'Registration No already exist or empty!')),
        ondelete = 'CASCADE'),
    Field('vehicle_name_id', 'reference vehicle_type', requires = IS_IN_DB(db, db.vehicle_type, '%(vehicle_name)s', zero = 'Choose brand'), 
        represent = lambda id, r: db.vehicle_type(id).vehicle_name, label = 'Brand'),
    Field('invoice', label = 'PO/Invoice'),
    Field('model'),
    Field('chassis_no', requires = (IS_UPPER(), IS_NOT_IN_DB(db, 'vehicle.chassis_no', error_message = 'Chassis No. already exist or empty!'))),
    Field('exp_date', 'date', requires = IS_NOT_EMPTY(), label = 'RPEx Date'),
    Field('datetoalert', 'date'),                
    Field('reg_date', 'date', label = '1st Reg.Date'),
    Field('value_purchase', 'decimal(10,2)'),
    Field('date_of_sale', 'date'),
    Field('depreciation_value', 'decimal(10,2)'),
    Field('mileage', 'integer', default = 0, label = 'Mil.'),
    Field('date_mileage', 'date', default = request.now, label = 'D8 Mil.'),
    Field('car_type', label = 'Vehicle description'),
    Field('plate_type'),
    Field('cylinder_count'),
    Field('transmission', requires = IS_IN_SET(['Automatic', 'Manual'], zero = 'Transmission Type')),
    Field('ext_color_code'),
    Field('accessories'),
    Field('category_id', 'reference vehicle_category', requires = IS_IN_DB(db, db.vehicle_category, '%(category)s', zero = 'Choose category'), 
        represent = lambda id, r: db.vehicle_category(id).category ,label = 'Category'),
    Field('tyre_size',label = 'Tyre Size'),
    Field('purpose', 'reference vehicle_purpose', requires = IS_IN_DB(db, db.vehicle_purpose, '%(purpose)s', zero = 'Choose purpose'),
        represent = lambda id, r: db.vehicle_purpose(id).purpose, label = 'Purpose'),
    Field('status_id', 'reference vehicle_status', requires = IS_IN_DB(db, db.vehicle_status, '%(status)s', zero = 'Choose status'),
        represent = lambda id, r: db.vehicle_status(id).status, label = 'Status'),
    Field('remarks'),
    Field('log_date', 'datetime', default = request.now, writable = False, readable = False),
    Field('focal_person', db.auth_user, default=auth.user_id, readable=False, writable=False), format = '%(reg_no)s')
    #Field('is_active','boolean', writable=False,readable=False,default=True), format = '%(reg_no)s')

'''
db.vehicle.division_id.widget = options_widget(
    'vehicle_company_id__selected', 'vehicle.company_id__unselected',
    lambda company_id: (db.division.division == company_id),
    request.vars.company_id,
    orderby = db.division.division,
    user_signature = True,
    field = db.vehicle.division_id
    )
'''
def company_widget(field, value):
    widget = SQLFORM.widgets.options.widget(field, value)
    widget.attributes["_onchange"] = 'updateMyDivision(jQuery("[name = company_id]").val());'
    return widget

def division_widget(field, value):
    _id="%s_%s" % (field._tablename, field.name)
    if value:
        company_id = db.division[value].company_id
        # filter the ranks when there's an actual value recorded
        field.requires = IS_IN_DB(db(db.division.company_id == company_id), db.division, "%(division)s", zero = 'Choose division')
        

    elif not request.function == "division":
        # create an empty select if no rank was selected
        # unless there's an options request
        field.requires = IS_IN_SET([])

    script = SCRIPT("""
    function updateMyDivision(companyID){
        // remove the ye olde options
        jQuery("[name=%(fieldname)s]").html("");
        // fish the new ones
        web2py_component("%(url)s/division/" + companyID, "%(_id)s");
    }
    """ % dict(fieldname=field.name, _id=_id, url=URL(c="default", f="division", extension="load")))
    return DIV(script, SQLFORM.widgets.options.widget(field, value))
    
#db.vehicle.company_id.widget = company_widget
#db.vehicle.division_id.widget = division_widget

db.vehicle.days_to_expire = Field.Method(lambda row: today - row.vehicle.exp_date)
                                       
db.define_table('v_photos',
    Field('reg_no_id', 'reference vehicle', requires = IS_IN_DB(db, db.vehicle, '%(reg_no)s', zero = 'Choose reg.no.'), 
        represent = lambda id, r: db.vehicle(id).reg_no, label = 'Reg. No.'),
    Field('road_permit', 'upload', label = 'Road Permit'),
    Field('photo', 'upload', label = 'Front Photo'),
    Field('photo2', 'upload', label = 'Rear Photo'),
    Field('photo3', 'upload', label = 'Left Photo'),
    Field('photo4', 'upload', label = 'Right Photo'),
    Field('focal_person', db.auth_user, default=auth.user_id, readable=False, writable=False),
    Field('log_date', 'datetime', label = 'Date & Time Created', default = request.now,
        writable = False, readable = True))

db.v_photos.reg_no_id.requires = IS_IN_DB(db, db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.')
    
#db.v_photos.reg_no_id.requires = IS_NOT_IN_DB(db, 'v_photos.reg_no_id',  error_message = 'Reg.No. is already exist or empty!')

db.define_table('ins_pol_status', Field('status'), format = '%(status)s')

db.define_table('insurance_policy',
    Field('company_id', 'reference company', requires = IS_IN_DB(db, db.company, '%(company)s', zero = 'Choose company'), 
        represent = lambda id, r: db.company(id).company, label = 'Company'),
    Field('insurance_company_id', 'reference vehicle_insurance', requires = IS_IN_DB(db, db.vehicle_insurance, '%(name)s', 
        zero = 'Choose insurance company'), represent = lambda id, r: db.vehicle_insurance(id).name, label = 'Insurance Company'),
    Field('policy_no'),
    Field('from_period_covered', 'date', default = request.now, label = 'Fr.Pe.Covered', comment = 'Starting period.'),
    Field('period_covered', 'date', default = request.now, label = 'To.Pe.Covered', comment = 'Ending period.'),
    Field('datetoalert', 'date', readable = False, writable = False),
    Field('amount', 'decimal(10,2)', default = 0.0),
    Field('status_id', 'reference ins_pol_status', requires = IS_IN_DB(db, db.ins_pol_status, '%(status)s', zero = 'Choose status'), 
        represent = lambda id, r: db.ins_pol_status(id).status,label = 'Status'),
    Field('focal_person', db.auth_user, default=auth.user_id, readable=False, writable=False),
    Field('log_date', 'datetime', default = request.now, writable = False, readable = False), format = '%(policy_no)s' )

db.insurance_policy.amount.represent = lambda value, row: DIV(locale.format('%.2F', value, grouping = True), _style = 'text-align: right')

db.define_table('insured_vehicles',
    Field('policy_no_id', 'reference insurance_policy', requires = IS_IN_DB(db(db.insurance_policy.status_id == 1), db.insurance_policy, '%(policy_no)s', zero = 'Choose Policy No.'), 
        represent = lambda id, r: db.insurance_policy(id).policy_no, label = 'Policy No.'),
    Field('reg_no_id', 'reference vehicle', requires = IS_IN_DB(db, db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.'), 
        represent = lambda id, r: db.vehicle(id).reg_no, label = 'Reg.No.'), 
    Field('passenger_covered'),
    Field('amount_insured', 'decimal(10,2)', default = 0.0, 
        represent = lambda value, row: locale.format('%.2F' or 0, value, grouping = True)),
    Field('excess', 'decimal(10,2)', default = 0.0, 
        represent = lambda value, row: locale.format('%.2F' or 0, value, grouping = True)),
    Field('amount', 'decimal(10,2)', default = 0.0, 
        represent = lambda value, row: locale.format('%.2F' or 0, value, grouping = True)),
    Field('focal_person', 'reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('log_date', 'datetime', default = request.now, writable = False, readable = False))

#db.repair_history.running_expenses.represent = lambda value, row: DIV(locale.format('%.2F', value, grouping = True), _style = 'text-align: right')
#db.insured_vehicles.reg_no_id.widget = SQLFORM.widgets.autocomplete(request, db.vehicle.reg_no, id_field = db.vehicle.id, limitby = (0,10), min_length=2)
#db.vehicle.chassis_no.requires = IS_NOT_IN_DB(db, 'vehicle.chassis_no', error_message = 'Chassis number is already existing or empty!')
#db.insured_vehicles.reg_no_id.requires = IS_NOT_IN_DB(db, 'insured_vehicles.reg_no_id', error_message = 'Reg.No. is already exist or empty!')

#db.insured_vehicles.insurance_id.requires = IS_IN_DB(db, db.insurance_policy, '%(insurance_company_id)s', zero = 'Choose insurance')

db.define_table('category_expenses', Field('name'), format = '%(name)s' )

db.define_table('workshop_done', Field('workshop'), format = '%(workshop)s' )

db.define_table('ads_status', Field('status'), format = '%(status)s')

db.define_table('advertisement',
    Field('ads', requires = IS_IN_SET(['Company','Commercial'], zero = 'Choose advertisement')),
    Field('logo'),
    Field('license_no'),
    Field('from_expiry_date', 'date', default = request.now, label = 'Fr.Exp.Date', comment = 'From expiry date.'),
    Field('expiry_date', 'date', default = request.now, label = 'To.Exp.Date', comment = 'To expiry date.'),
    Field('amount', 'decimal(10,2)', default = 0.0),
    Field('status_id', 'reference ads_status', requires = IS_IN_DB(db, db.ads_status, '%(status)s', zero = 'Choose status'),
        represent = lambda id, r: db.ads_status(id).status, label = 'Status'),
    Field('focal_person', db.auth_user, default=auth.user_id, readable=False, writable=False),
    Field('log_date', 'datetime', default = request.now, writable = False,
                      readable = False), format = '%(license_no)s')

db.advertisement.license_no.requires = IS_NOT_IN_DB(db, 'advertisement.license_no', error_message = 'License No. is already exist or empty!')
db.advertisement.amount.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')

db.define_table('ads_vehicle',
    Field('license_no_id', db.advertisement, requires = IS_IN_DB(db(db.advertisement.status_id != 2), db.advertisement, '%(license_no)s', 
        zero = 'Choose license no.'), label = 'License No', represent = lambda id, r: db.advertisement(id).license_no),
    Field('reg_no_id', db.vehicle, requires = IS_IN_DB(db, db.vehicle, '%(reg_no)s', zero = 'Choose reg.no.'), 
        label = 'Reg.No.', represent = lambda id, r: db.vehicle(id).reg_no),
    Field('amount', 'decimal(10,2)'),
    Field('log_date', 'datetime', default = request.now, writable = False, readable = False))

db.ads_vehicle.amount.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')

db.define_table('repair_history',
    Field('reg_no_id', 'reference vehicle', requires = IS_IN_DB(db, db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.'), 
        represent = lambda id, r: db.vehicle(id).reg_no, label = 'Reg.No.'),
    Field('invoice_number',label = 'Invoice #', requires = (IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'repair_history.invoice_number', 
        error_message = 'invoice no. already exist!'))),
    Field('invoice_date', 'date', default = request.now, label = 'Date Invoice'),
    Field('workshop_done', 'reference workshop_done', requires = IS_IN_DB(db, db.workshop_done, '%(workshop)s', zero = 'Choose workshop'), 
        represent = lambda id, r: db.workshop_done(id).workshop, label = 'Workshop'),
    Field('date_time_in', 'date', default = request.now, label = 'Date Begin'),
    Field('date_time_out', 'date', default = request.now, label = 'Date End'),
    Field('no_days_time', compute = lambda dt: dt['date_time_out'] - dt['date_time_in'], label = 'Duration'), 
    Field('mileage', 'integer', default = 0, represent = lambda value, row: locale.format('%d', value or 0, grouping = True)), 
    Field('regular_maintenance','decimal(10,2)',default = 00.00, label = 'LAB', comment = 'Service, Oil/Filter Change',
        represent = lambda value, row: locale.format('%.2F', value, grouping = True)),
    Field('spare_parts', 'decimal(10,2)', default = 00.00, label = 'SP', 
        represent = lambda value, row: locale.format('%.2F', value, grouping = True)),                
    Field('statutory_expenses','decimal(10,2)',default = 00.00,label = 'SE', comment = 'Insurance, Road Permit Renewal, Advertisement License',
        represent = lambda value, row: locale.format('%.2F', value, grouping = True)),
    Field('accident_repair','decimal(10,2)',default = 00.00, label = 'AR', 
        represent = lambda value, row: locale.format('%.2F', value, grouping = True)),
    Field('total_amount','decimal(10,2)', represent = lambda value, row: locale.format('%.2F', value or 0, grouping = True),
        compute = lambda p: p['regular_maintenance'] + p['accident_repair'] + p['statutory_expenses'] + p['spare_parts']),
    Field('details','text', requires = IS_UPPER()),
    Field('focal_person', db.auth_user, default=auth.user_id, readable=False, writable=False),
    Field('log_date', 'datetime', default = request.now, writable = False, readable = False))


def multiselect_widget(f,v):
    import uuid
    d_id = "multiselect-" + str(uuid.uuid4())[:8]
    wrapper = DIV(_id=d_id)
    inp = SQLFORM.widgets.options.widget(f,v)
    inp['_multiple'] = 'multiple'
    inp['_style'] = 'min-width: %spx;' % (len(f.name) * 20 + 50)
    if v:
        if not isinstance(v,list): v = str(v).split('|')
        opts = inp.elements('option')
        for op in opts:
            if op['_value'] in v:
                op['_selected'] = 'selected'            
    scr = SCRIPT('jQuery("#%s select").multiSelect({'\
                 'noneSelected:"Select accessories"});' % (d_id))
    wrapper.append(inp)
    wrapper.append(scr)
    if request.vars.get(inp['_id']+'[]',None):
        var = request.vars[inp['_id']+'[]']
        if not isinstance(var,list): var = [var]
        request.vars[f.name] = var
        del request.vars[inp['_id']+'[]']
    return wrapper

db.define_table('authorized_vehicle_category', Field('name'), format = '%(name)s' )

db.define_table('driver_position', Field('name'), format = '%(name)s')

db.define_table('driver',
    Field('company_id', 'reference company', requires = IS_IN_DB(db, db.company, '%(company)s', zero = 'Choose company'), 
        represent = lambda id, r: db.company(id).company, label = 'Company'),
    Field('division_id', 'reference division', requires = IS_IN_DB(db, db.division, '%(division)s', zero = 'Choose division'), 
        represent = lambda id, r: db.division(id).division, label = 'Division'),
    Field('department_id', 'reference department', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose department'), 
        represent = lambda id, r: db.department(id).name, label = 'Department'),
    Field('employee_number', requires = IS_UPPER(), label = 'Emp.#'),
    Field('driver_name', requires = IS_UPPER()),
    Field('position_id', 'reference driver_position', requires = IS_IN_DB(db, db.driver_position, '%(name)s', zero = 'Choose position'),  
        represent = lambda id, r: db.driver_position(id).name, label = 'Position'), 
    Field('driver_id', label = 'License No.'),
    Field('expiry_date','date'),
    Field('alertdate', 'date', writable = False, readable = False),
    Field('license_category_id', 'list:reference authorized_vehicle_category', 
        label = 'Category Name'),
    Field('contact_no'),
    Field('driver_license', 'upload', label = 'Driver License', required=False),
    Field('focal_person', db.auth_user, default=auth.user_id, readable=False, writable=False),
    Field('log_date', 'datetime', default = request.now, writable = False, readable = False),
        format = '%(driver_name)s')
#db.item.discounted_total = Field.Method(lambda row, discount=0.0:        row.item.unit_price*row.item.quantity*(1.0-discount/100))
#db.driver.alert = Field.Method(compute = lambda row: (row['driver.expiry_date'] + row['driver.expiry_date']))

db.driver.license_category_id.requires = IS_IN_DB(db, 'authorized_vehicle_category.id', '%(name)s', multiple = True)
#db.driver.license_category_id.represent = lambda value, row: ', '.join(row.name for row in value or [])
db.driver.license_category_id.represent = lambda value, row: ', '.join(db.authorized_vehicle_category(i).name for i in value or [])

vehicles_accessories = IS_IN_SET(['Original Keys', 'Original Road Permit', 'Pertol Card',
    'Spare Tyre', 'Tools (jack)'], multiple = True)

db.define_table('vehicles_hand_over',
    Field('reg_no_id', 'reference vehicle', requires = IS_IN_DB(db, db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.'),
        represent = lambda id, r: db.vehicle(id).reg_no, label = 'Reg.No.'),
    Field('date_and_time', 'datetime', default = request.now), 
    Field('from_department_id', 'reference department', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose from department'), 
        represent = lambda id, r: db.department(id).name if id else '',label = 'From Department'),
    Field('to_department_id', 'reference department', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose to department'), 
        represent = lambda id, r: db.department(id).name if id else '', label = 'To Department'),
    Field('from_driver_id', 'reference driver', requires = IS_IN_DB(db, db.driver, '%(driver_name)s', zero = 'Choose from driver'), 
        represent = lambda id, r: db.driver(id).driver_name, label = 'From Driver'),
    Field('to_driver_id', 'reference driver', requires = IS_IN_DB(db, db.driver, '%(driver_name)s', zero = 'Choose to driver'), 
        represent = lambda id, r: db.driver(id).driver_name, label = 'To Driver'),
    Field('mileage'),
    Field('vehicles_acc', 'list:string', requires = vehicles_accessories, widget = SQLFORM.widgets.checkboxes.widget),
    Field('remarks', 'text'),
    Field('focal_person', db.auth_user, default=auth.user_id, readable=False, writable=False),
    Field('log_date', 'datetime', writable = False, readable = False))


db.define_table('fuel_expenses',
    Field('reg_no_id', 'reference vehicle', requires = IS_IN_DB(db, db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.'), 
        represent = lambda id, r: db.vehicle(id).reg_no, label = 'Reg.No.'),
    Field('date_expense', 'date', default = request.now, label = 'Date'),
    Field('amount', 'decimal(10,2)', default = 00.00, label = 'Amount Filled',
        represent = lambda value, row: locale.format('%.2F', value, grouping = True)),
    Field('paid_by', requires = IS_IN_SET(['Cash','Credit','Fuel Card'], zero = 'Choose paid by')),
    Field('station'),
    Field('remarks'),
    Field('focal_person', db.auth_user, default=auth.user_id, readable=False, writable=False),
    Field('log_date', 'datetime', default = request.now, writable = False, readable = False))

db.define_table('km_used',
    Field('reg_no_id', 'reference vehicle', requires = IS_IN_DB(db, db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.'),
        represent = lambda id, r: db.vehicle(id).reg_no, label = 'Reg.No.'),                
    Field('log_date', 'datetime', default = request.now, writable = False, readable = False),
    Field('given_month', 'date', label = 'Given Month', default = request.now.date, requires  = IS_NOT_EMPTY()), 
    Field('current_mil','integer', default = 0, label = 'Given Odometer',
        represent = lambda value, row: locale.format('%d', value or 0, grouping = True),
        requires = IS_INT_IN_RANGE(1, 1000000) ),
    Field('consumed_mil','integer', default = 0, label = 'Diff. Odometer',writable = False,
        represent = lambda value, row: locale.format('%d', value or 0, grouping = True)),
    Field('focal_person', db.auth_user, default=auth.user_id, readable=False, writable=False),
    Field('log_date', 'datetime', writable = False, readable = False))

#db.km_used.current_mil.represent = lambda value, row: DIV(locale.format('%d', value or 0, grouping = True), _style = 'text-align: right')
#db.km_used.consumed_mil.represent = lambda value, row: DIV(locale.format('%d', value or 0, grouping = True), _style = 'text-align: right')  
db.km_used.given_month.requires = IS_NOT_EMPTY()

db.define_table('activities',
    Field('log_date', 'datetime'),
    Field('person', label = 'Focal Person'),
    Field('action', label = 'Action Done'),
    Field('a_code', 'integer', label = 'Details'))


db.vehicle.mileage.represent = lambda value, row: DIV(locale.format('%d', value or 0, grouping = True), _style = 'text-align: right')
#db.repair_history.mileage.represent = lambda value, row: DIV(locale.format('%d', value or 0, grouping = True), _style = 'text-align: right')
#db.vehicles_hand_over.date_and_time.represent = lambda x, row: x.strftime("%d/%m/%Y %I:%M:%S %p")

db.driver.expiry_date.requires = IS_NOT_EMPTY()
db.driver.license_category_id.widget = SQLFORM.widgets.checkboxes.widget
db.driver.license_category_id.requires = IS_IN_DB(db, db.authorized_vehicle_category, '%(name)s', multiple = True),
db.driver.employee_number.requires = (IS_UPPER(),IS_NOT_IN_DB(db, 'driver.employee_number', error_message = 'Employee number is already existing or empty!'))
db.driver.driver_id.requires = (IS_UPPER(),IS_NOT_IN_DB(db, 'driver.driver_id', error_message = 'License number is already existing or empty!'))

rows = db(db.km_used.reg_no_id == db.vehicle(request.args(0))).select(orderby = db.km_used.given_month)
r = 1
row = len(rows)
while (r < row):
    rows[r].update_record(consumed_mil = rows[r].current_mil - rows[r-1].current_mil)
    r +=1
 