def vehicle_info():
    i = 0
    vehicle_info = db(db.vehicle.id == request.args(0)).select(db.vehicle.ALL)      
    for info in vehicle_info:
        i = TABLE(*[
            TR(TD(B('Vehicle Info.'), _colspan = '2', _style = 'background: #e0e0e0' )),
            TR(TD('Reg.No.:'), TD(info.reg_no)),
            TR(TD('Company:'), TD(info.company_id.company), _class = 'pure-table-odd'),
            TR(TD('Division'), TD(info.division_id.division)),
            TR(TD('Department:'), TD(info.department.name), _class = 'pure-table-odd'),
            TR(TD('Chassis No:'), TD(info.chassis_no)), 
            TR(TD('Last Reading:'), TD(info.mileage), _class = 'pure-table-odd'),
            TR(TD('Model:'), TD(info.model))], 
            _border = '0', _align = 'center', _width = '100%',  _class = 'pure-table')         
    return dict(i = i) 

def comp():
    form = SQLFORM.factory(
        Field('company_id', 'reference company', requires = IS_IN_DB(db, db.company, '%(company)s', zero = 'Select Company'),
            represent = lambda id, row: db.company(id).company, label = 'Company'),
        Field('division_id', 'reference division', requires = IS_IN_DB(db(request.vars.company_id == db.division.company_id), 
            'division.company_id', '%(division)s', zero = 'Select Division'),
        represent = lambda id, row: (request.vars.company_id == db.division.company_id), label = 'Division'),
        Field('department_id', 'reference department', requires = IS_IN_DB(db(request.vars.division_id == db.department.division_id), 
               db.department, '%(name)s', zero = 'Select department'), represent = lambda id, row: db.department(id).name, label = 'Department'),
        keepopts=['country'])
    if form.accepts(request.vars,session):
        response.flash = 'ok na'
    return locals()
 
import locale
current_date = request.now
current_date = current_date.date()

def division():
    db.vehicle.division_id.requires = IS_IN_DB(db(db.division.company_id == request.args(1)), 'division.id', "%(division)s", zero = 'Choose division')
    form = SQLFORM(db.vehicle)
    text = "".join([t.xml() for t in form.custom.widget.division_id.elements("option")])
    return text

def cascade():
    companyID = db().select(db.company.company)
    if request.vars.company:
        divisionID = db(db.division.company_id == request.vars.company).select(db.division.division)
    return dict(divisionID = divisionID)

'''
def division():
    division = db(db.division.company_id == request.vars.company_id).select(db.division.division)
    result = ''
    for div in division:
        result += "<option value='" + str(division.id) + "'>" + division.division + "</option>"
    return XML(result)
'''

def companies():
    return dict()

def add_company():
    form = SQLFORM.factory(db.company, formstyle='bootstrap')
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('add_company', vars={'success':'ok'}))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        pass
    return dict(form=form)

def t():
    return locals()
def test():

#<div id="some_btn"><a class="btn btn-success btn-mini" data-target="#some_modal" data-toggle="modal"><i class="icon-search icon-white"></i>    
#links =[lambda row: A(SPAN(_class = 'icon icon-print'), _target = '_blank', _title = "Print", _href = URL('Reports', 'DriverReport', args=row.id),
#            _onclick="MyWindow=window.open = 'URL('Reports', 'DriverReport', args = row.id)' ")]
    return locals()

def loading():
    return dict(message = 'ok na')

def somepage():
    form = SQLFORM.factory(
        Field('somefield'),
        Field('anotherfield'),
        formname='some_form',
        formstyle='bootstrap')
    if form.process(session=None, formname='some_form').accepted:
        response.flash = None
        #...do what you need to do...
    elif form.errors:
        response.flash = None
        #...do what you need to do...
    return dict(form = form)    

def opps():
    return dict(msg = 'load na...')
    
export = {'xml':False, 'html':False, 'csv_with_hidden_cols':False,
          'csv':False, 'tsv_with_hidden_cols':False, 'json':False}
#onClick="window.location.reload( true )"
#<a data-toggle="modal" href="remote.html" data-target="#modal">Click me</a>
# onclick="refresh_grid();return false"
vid = LOAD('default','ControllerDetails.load', args = request.args(0), ajax = True, ajax_trap = True, user_signature = True,
        close_button = 'close', renderstyle = True)
'''
links = [
lambda row: A(SPAN(_class = 'icon icon-wrench'), _title="Repair & Maintenance", _href=URL("default","VehicleMaintenance", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-filter'), _title="Fuel Expenses", _href=URL("default","FuelExpenses", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-road'), _title="Monthly Mileage", _href=URL("default","Odometer", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-file'), **{'_title':'Insurance Detail', '_data-target':'#InsDetails', '_data-toggle':'modal', '_href':URL("default","VehicleInsDetail", args = row.id)}),
lambda row: A(SPAN(_class = 'icon icon-star'),  **{'_title':'Advertisement','_data-target':'#AdsDetails','_data-toggle':'modal' ,'_href':URL("default","AdsDetails", args = row.id)}),
lambda row: A(SPAN(_class = 'icon icon-camera'), _title="Photos", _target = '_blank', _href=URL("Reports","Photos", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-user'), **{ '_title':'Controller','_data-target':'#myModal','_data-toggle':'modal', '_href':URL('default', 'ControllerDetails', args = row.id)}),
lambda row: A(SPAN(_class = 'icon icon-print'), _title="Print", _target="_blank", _href=URL("Reports","VehicleProfileReport", args = row.id))
]          
'''
links = [
lambda row: A(SPAN(_class = 'icon icon-wrench'), _title="Repair & Maintenance", _href=URL("default","VehicleMaintenance", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-filter'), _title="Fuel Expenses", _href=URL("default","FuelExpenses", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-road'), _title="Monthly Mileage", _href=URL("default","Odometer", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-file'), _title='Insurance Detail', _href=URL("default","VehicleInsDetail", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-star'),  _title='Advertisement', _href=URL("default","AdsDetails", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-camera'), _title="Photos", _target = '_blank', _href=URL("Reports","Photos", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-user'), _title='Controller', _href=URL('default', 'ControllerDetails', args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-print'), _title="Print", _target="_blank", _href=URL("Reports","VehicleProfileReport", args = row.id))
]          


def callback():
    """ a generic callback """
    return cache.ram(request.args(0),lambda:None,None)(**request.vars)

@auth.requires_login()
def index():
    response.flash = 'Welcome to Fleet Management System'
    fields = [db.vehicle.company_id, db.vehicle.division_id, db.vehicle.department, db.vehicle.vehicle_code,
    db.vehicle.reg_no, db.vehicle.plate_type, db.vehicle.category_id, db.vehicle.model, db.vehicle.mileage,
    db.vehicle.date_mileage, db.v_photos.road_permit, db.v_photos.photo, db.v_photos.photo2, db.v_photos.photo3,
    db.v_photos.photo4]
    grid = SQLFORM.grid(db.vehicle.status_id != 1, fields = fields, left = db.v_photos.on(db.vehicle.id == db.v_photos.reg_no_id), 
        showbuttontext=False, csv = False, user_signature = True, searchable = True, exportclasses = export,
        create = False, details = False, deletable = False, editable = False)
    return dict(grid = grid, renderstyle = True)
    
#####################################################################
#####       A D M I N I S T R A T O R   A C C O U N T       #########
#####################################################################

################   MANAGEMENT SECTION (Main Menu)   #################


@auth.requires_membership('level_1_user')
def GroupCompany():
    db.company.id.readable = False    
    db.company.company.label = 'Company'
    row_id = request.args(0)
    form = SQLFORM.factory(db.company)
    if form.accepts(request.vars, session):
        db.company.insert(company = form.vars.company)
        response.flash = 'Record Inserted'
    links=[lambda row: A('Division', _href=URL("default","Division", args = row.id))]
    grid = SQLFORM.grid(db.company, fields = [db.company.company, db.company.cr], user_signature=False,
                        csv = False, create = False, orderby = db.company.company, maxtextlength = 100,
                        links = links, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/GroupCompany.html'
        form = ''

    return dict(form = form, grid = grid)

@auth.requires_membership('level_1_user')
def Division():
    row_id = request.args(0)
    db.division.id.readable = False
    form = SQLFORM.factory(db.division)
    if form.process().accepted:
        db.division.insert(company_id = row_id, division = form.vars.division_id)
        response.flash = 'Record Inserted'
    links=[lambda row: A('Department', _href=URL("default","Department", args = row.id))]
    grid = SQLFORM.grid(db.division.company_id == row_id, user_signature=False,
        csv = False, create = False, orderby = db.division.division, links = links, 
        searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/Division.html'
        form = ''
    return dict(form = form, grid = grid)

@auth.requires_membership('level_1_user')
def Department():
    row_id = request.args(0)
    db.department.id.readable = False
    db.department.division_id.readable = False
    form = SQLFORM.factory(db.department)
    if form.process().accepted:
        db.department.insert(division_id = row_id, name = form.vars.name)
        response.flash = 'Record Inserted'
    grid = SQLFORM.grid(db.department.division_id == row_id, user_signature=False,
        csv = False, create = False, orderby = db.department.name,
        searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/Department.html'
        form = ''
    return dict(form = form, grid = grid)

@auth.requires_membership('level_1_user')
def vehicle_type():
    db.vehicel_type.id.readable = False
    form = SQLFORM(db.vehicle_type).process()
    if form.accepted:
        response.flash = 'Vehicle Type Inserted'
    grid = SQLFORM.grid(db.vehicle_type, user_signature=False, csv = False, create = False,
        maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/vehicle_type.html'
        form = ''
    return dict(form = form, grid = grid)

@auth.requires_membership('level_1_user')
def manufacturer():
    db.vehicle_type.id.readable = False
    form = SQLFORM(db.vehicle_type).process()
    if form.accepted:
        response.flash = 'Vehicle Manufacturer Inserted'
    grid = SQLFORM.grid(db.vehicle_type, user_signature=False, csv = False, create = False,
        maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/manufacturer.html'
        form = ''
    return dict(form = form, grid = grid)
    
@auth.requires_membership('level_1_user')
def vehicle_category():
    db.vehicle_category.id.readable = False
    form = SQLFORM(db.vehicle_category).process()
    if form.accepted:
        response.flash = 'Vehicle Category Inserted'
    grid = SQLFORM.grid(db.vehicle_category, user_signature=False, csv = False, create = False,
        maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/vehicle_category.html'
        form = ''
    return dict(form = form, grid = grid)

@auth.requires_membership('level_1_user')
def vehicle_status():
    db.vehicle_status.id.readable = False
    form = SQLFORM(db.vehicle_status).process()
    if form.accepted:
        response.flash = 'Vehicle Status Inserted'
    grid = SQLFORM.grid(db.vehicle_status, user_signature=False, csv = False, create = False,
                                    maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/vehicle_status.html'
        form = ''
    return dict(form = form, grid = grid)

@auth.requires_membership('level_1_user')
def insurance():
    db.vehicle_insurance.id.readable = False
    form = SQLFORM(db.vehicle_insurance).process()
    if form.accepted:
        response.flash = 'Insurance Inserted'
    grid = SQLFORM.grid(db.vehicle_insurance, user_signature=False, csv = False, create = False,
                                    maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/insurance.html'
        form = ''
    return dict(form = form, grid = grid)

@auth.requires_membership('level_1_user')
def authorized_vehicle_category():
    db.authorized_vehicle_category.id.readable = False
    form = SQLFORM(db.authorized_vehicle_category).process()
    if form.accepted:
        response.flash = 'Authorized Vehicle Category Inserted'
    grid = SQLFORM.grid(db.authorized_vehicle_category, user_signature=False, csv = False, create = False,
                                    maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/authorized_vehicle_category.html'
        form = ''
    return dict(form = form, grid = grid)
    
@auth.requires_membership('level_1_user')
def category_expenses():
    db.category_expenses.id.readable = False
    form = SQLFORM(db.category_expenses).process()
    if form.accepted:
        response.flash = 'Category Expenses Inserted'
    grid = SQLFORM.grid(db.category_expenses, user_signature=False, csv = False, create = False,
                                    maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/category_expenses.html'
        form = ''
    return dict(form = form, grid = grid)

@auth.requires_membership('level_1_user')
def vehicle_purpose():
    db.vehicle_purpose.id.readable = False
    form = SQLFORM(db.vehicle_purpose).process()
    if form.accepted:
        response.flash = 'Vehicle Purpose Inserted'
    grid = SQLFORM.grid(db.vehicle_purpose, user_signature=False, csv = False, create = False,
                                    maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/vehicle_purpose.html'
        form = ''
    return dict(form = form, grid = grid)    
   
@auth.requires_membership('level_1_user')
def workshop():
    db.workshop_done.id.readable = False
    form = SQLFORM(db.workshop_done).process()
    if form.accepted:
        response.flash = 'Workshop Inserted'
    grid = SQLFORM.grid(db.workshop_done, user_signature=False, csv = False, create = False,
                                    maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/workshop.html'
        form = ''
    return dict(form = form, grid = grid)    


@auth.requires_membership('level_1_user')
def owner():
    db.owner.id.readable = False
    form = SQLFORM(db.owner).process()
    if form.accepted:
        response.flash = 'Workshop Inserted'
    grid = SQLFORM.grid(db.owner, user_signature=False, csv = False, create = False,
                                    maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/owner.html'
        form = ''
    return dict(form = form, grid = grid)    

@auth.requires_membership('level_1_user')
def driver_position():
    db.driver_position.id.readable = False
    form = SQLFORM(db.driver_position).process()
    if form.accepted:
        response.flash = 'Driver Position Inserted'
    grid = SQLFORM.grid(db.driver_position, user_signature=False, csv = False, create = False,
                                    maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/driver_position.html'
        form = ''
    return dict(form = form, grid = grid)  

@auth.requires_membership('level_1_user')
def InsPolStatus():
    db.ins_pol_status.id.readable = False
    form = SQLFORM(db.ins_pol_status).process()
    if form.accepted:
        response.flash = 'Insurance Policy Status Inserted'
    grid = SQLFORM.grid(db.ins_pol_status, user_signature=False, csv = False, create = False,
                                    maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/InsPolStatus.html'
        form = ''
    return dict(form = form, grid = grid)  

@auth.requires_membership('level_1_user')
def AdsStatus():
    db.ads_status.id.readable = False
    form = SQLFORM(db.ads_status).process()
    if form.accepted:
        response.flash = 'Advertisement Status Inserted'
    grid = SQLFORM.grid(db.ads_status, user_signature=False, csv = False, create = False,
                                    maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/AdsStatus.html'
        form = ''
    return dict(form = form, grid = grid)  

@auth.requires_membership('level_1_user')
def AdsStatus():
    db.ads_status.id.readable = False
    form = SQLFORM(db.ads_status).process()
    if form.accepted:
        response.flash = 'Advertisement Status Inserted'
    grid = SQLFORM.grid(db.ads_status, user_signature=False, csv = False, create = False,
                                    maxtextlength=64, searchable = False, showbuttontext = False)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/AdsStatus.html'
        form = ''
    return dict(form = form, grid = grid)      



################  MANAGEMENT SECTION END #################         
@auth.requires_membership('level_1_user')
def VehicleProfileForm():
    form = SQLFORM(db.vehicle)
    if form.process().accepted:
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            a_code = '1', action = 'created reg.no. %s company vehicle.' % form.vars.reg_no)              
        response.flash = 'Form accepted.'
    return dict(grid = form)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Browse():
    db.vehicle.id.readable = False
    
    fields = [db.vehicle.company_id, db.vehicle.division_id, db.vehicle.department, db.vehicle.owner, db.vehicle.vehicle_code,
    db.vehicle.reg_no, db.vehicle.vehicle_name_id, db.vehicle.model, db.vehicle.exp_date, db.vehicle.category_id]
    query = db.vehicle.status_id != 1     
    grid = SQLFORM.grid(query, user_signature=False, fields = fields, deletable = False,
        exportclasses = export, details=False, editable = auth.has_membership('level_1_user'),
        searchable = True, links = links, onupdate = update_v_record, oncreate = create_v_record,
        showbuttontext=False, maxtextlength=12, create = False, formstyle = 'bootstrap')
    if request.args(0) == 'edit':
        response.view = 'default/VehicleProfileForm.html'
        grid = grid.update_form
    return dict(grid = grid)


 
# --------------   OTHERS ---------------------- #
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Cancelled(): # --------------   CANCELLED VEHICLE'S ---------------------- # 
    fields = [db.vehicle.company_id, db.vehicle.division_id, db.vehicle.department, db.vehicle.owner, db.vehicle.vehicle_code,
    db.vehicle.reg_no, db.vehicle.vehicle_name_id, db.vehicle.model, db.vehicle.exp_date, db.vehicle.category_id]
    grid = SQLFORM.grid(db.vehicle.status_id == 1, user_signature=False, fields = fields, exportclasses = export, 
        details=False, create = False, searchable = True, links = links, 
        showbuttontext=False, maxtextlength=12, deletable = auth.has_membership('level_1_user'), 
        editable = auth.has_membership('level_1_user'), 
        ondelete = delete_cv_record, onupdate = update_cv_record,)
    if request.args(0) == 'edit':
        response.view = 'default/VehicleProfileForm.html'
        grid = grid.update_form
    return dict(grid = grid)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def InsPolHistory(): # --------------   INSURANCE POLICY NON ACTIVE ---------------------- #
    form = ''
    db.insurance_policy.id.readable = False
    links=[lambda row: A('Insured Vehicles', _href=URL("default","InsuredVehicles", args = row.id)),
           lambda row: A('Print', _target="blank", _href=URL("Reports","InsuredVehiclesReport", args = row.id))]
    query = db.insurance_policy.status_id == 2
    query |= db.insurance_policy.status_id == None
    grid = SQLFORM.grid(query, user_signature=False, exportclasses = export, details=False,
        searchable = False, links = links, create = False, showbuttontext=False)
    if request.args(0) == 'edit':
        response.view = 'default/InsurancePolicy.html'
        grid = grid.update_form
        form = ''
    return dict(form = form, grid = grid)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def AdsHistory(): # --------------   ADVERTISEMENT HISTORY ---------------------- #
    db.advertisement.id.readable = False
    links=[lambda row: A('Ads Vehicles', _href=URL("default","AdsVehicles", args = row.id)),
           lambda row: A('Print', _target="blank", _href=URL("Reports","InsuredVehiclesReport", args = row.id))]
    query = db.advertisement.status_id == 2
    query |= db.advertisement.status_id == None
    grid = SQLFORM.grid(query, user_signature = False, exportclasses = export, links = links,
        searchable = False, showbuttontext=False, details = False, create = False)
    if request.args(0) == 'edit':
        response.view = 'default/AdvertisementGrid.html'
        grid = grid.update_form
    return dict(grid = grid)


# --------------   OTHERS ---------------------- #
@auth.requires_login()
def VehicleInsDetail():
    row_id = request.args(0)
    policy = db.insured_vehicles.reg_no_id == row_id   
    policy &= db.insurance_policy.status_id == 1
    policy &= db.insured_vehicles.policy_no_id == db.insurance_policy.id
    details = i = None

    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
        _onclick = "javascript:PrintContent()"))

    vehicle_info = db(db.vehicle.id == request.args(0)).select(db.vehicle.ALL)
        
    for info in vehicle_info:
        i = TABLE(*[
            TR(TD(B('Vehicle Info.'), _colspan = '2', _style = 'background: #e0e0e0' )),
            TR(TD('Reg.No.:'), TD(info.reg_no)),
            TR(TD('Company:'), TD(info.company_id.company), _class = 'pure-table-odd'),
            TR(TD('Division'), TD(info.division_id.division)),
            TR(TD('Department:'), TD(info.department.name), _class = 'pure-table-odd'),
            TR(TD('Chassis No:'), TD(info.chassis_no)), 
            TR(TD('Last Reading:'), TD(info.mileage), _class = 'pure-table-odd'),
            TR(TD('Model:'), TD(info.model))], 
            _border = '0', _align = 'center', _width = '100%',  _class = 'pure-table')

    for p in db(policy).select(db.insured_vehicles.ALL, db.insurance_policy.ALL):
        details = TABLE(*[
            TR(TD(B('Insurance Details'), _colspan = '2', _style = 'background: #e0e0e0' )),
            TR(TD('Insurance Company:'), TD(p.insurance_policy.insurance_company_id.name)),
            TR(TD('Policy:'), TD(p.insurance_policy.policy_no), _class = 'pure-table-odd'),
            TR(TD('Fr.Pe.Covered:'), TD(p.insurance_policy.from_period_covered)),
            TR(TD('To.Pe.Covered:'), TD(p.insurance_policy.period_covered), _class = 'pure-table-odd'),
            TR(TD('Amount:'), TD(locale.format('%.2F', p.insured_vehicles.amount, grouping = True))),
            TR(TD('Status:'), TD(p.insurance_policy.status_id.status), _class = 'pure-table-odd')],
            _border = '0', _align = 'center', _width = '100%',  _class = 'pure-table')
    return dict(i = i, img_report = img_report, details = details)

'''
    group_id = auth.id_group('<role name>')
    all_users_in_group = db(db.auth_membership.group_id==group_id)._select(db.auth_membership.user_id)
    users = db(~db.auth_user.id.belongs(all_users_in_group)).select()

    auth.has_membership(auth.id_group('Member'),auth.user.id):

def myGroups():
    groups = []
    rows = db((db.auth_user.email == auth.user.email)&(db.auth_membership.user_id == auth.user_id)&(db.auth_group.id==db.auth_membership.group_id)).select(db.auth_group.ALL)
    for row in rows:
        groups.append(row.role)
    return (groups)

'''
def group():
    group_id = auth.id_group('level_2_user')
    all_users_in_group = db(db.auth_membership.group_id==group_id)._select(db.auth_membership.user_id)
    users = db(db.auth_user.id.belongs(all_users_in_group)).select(orderby = db.auth_user.division_id)



    #all_users_in_group = db(db.auth_membership.group_id == group_id)._select(db.auth_membership.user_id)
    #query = db.auth_user.id.belongs(all_users_in_group)
    #query &= db.auth_user.division_id == 13
    #users = db(query).select()


    #all_users_in_group = db(query)._select(db.auth_membership.user_id)
    #query = db(db.auth_user.id.belongs(all_users_in_group)).select()
    #query = db(query).select(db.auth_user.ALL)
    return dict(query = users)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def ControllerDetails():
    i = 'to many'
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
        _onclick = "javascript:PrintContent()"))

    
    group_id = auth.id_group('level_2_user')
    all_users_in_group = db(db.auth_membership.group_id == group_id)._select(db.auth_membership.user_id)
    query = db.auth_user.id.belongs(all_users_in_group)
    query &= db.vehicle.id == request.args(0)       
    query &= db.auth_user.division_id == db.vehicle.division_id
    
    cnt = db(query).count()
    if cnt > 1:        
        
        head = THEAD(TR(TH('Last Name'), TH('First Name'), TH('P.O. Box'),
            TH('Mobile No.'), TH('Office No'), TH('Fax No.'), TH('Email')))

        r = []
        for c in db(query).select(db.auth_user.ALL):
            r.append(TR(TD(c.last_name), TD(c.first_name), TD(c.po_box), TD(c.mobile_no),
                TD(c.office_no), TD(c.fax_no), TD(c.email)))

        body = TBODY(*r)
        table = TABLE(*[head, body], _border = '0', _align = 'center', _width = '100%', 
            _class = 'pure-table')
        return dict(i = table, img_report = img_report)

    else:
        for c in db(query).select(db.auth_user.ALL):
            i = TABLE(*[
                TR(TD(B('Controller Details'), _colspan = '2', _style = 'background: #e0e0e0')), 
                TR(TD('Last Name:'), TD(c.last_name)),
                TR(TD('First Name:'), TD(c.first_name), _class = 'pure-table-odd'),
                TR(TD('Division:'), TD(c.division_id.division)),
                TR(TD('P.O. Box:'), TD(c.po_box), _class = 'pure-table-odd'),
                TR(TD('Mobile No.:'), TD(c.mobile_no)),
                TR(TD('Office No.:'), TD(c.office_no), _class = 'pure-table-odd'),
                TR(TD('Fax No.:'), TD(c.fax_no)),
                TR(TD('Email:'), TD(c.email), _class = 'pure-table-odd')],
                _border = '0', _align = 'center', _width = '100%',  _class = 'pure-table')
    

        return dict(i = i, img_report = img_report)
    


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Controller():
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",
        _src=URL('static','images/printButton.png'), _onclick = "javascript:PrintContent()"))    
       
    headers = {'auth_user.first_name':'First Name',
    'auth_user.last_name':'Last Name',
    'auth_user.division_id':'Division',
    
    'auth_user.email':'Email',
    'auth_user.po_box':'PO Box',
    'auth_user.mobile_no':'Mobile No.',
    'auth_user.office_no':'Office No.',
    'auth_user.fax_no':'Fax No.' }
    rows = db(db.auth_user.id != 6).select(db.auth_user.first_name, db.auth_user.last_name,
        db.auth_user.division_id,  db.auth_user.email,
        db.auth_user.po_box, db.auth_user.mobile_no, db.auth_user.office_no, db.auth_user.fax_no,
        orderby = ~db.auth_user.division_id)
    table = SQLTABLE(rows, headers = headers, _width = '100%', _class = 'pure-table')
    return dict(table = table, img_report = img_report)


    '''

    head = THEAD(TR(TH('No.'),TH('First Name'), TH('Last Name'), TH('Email'), 
            TH('Division'),TH('Department'),TH('PO BOX'),TH('Mobile No.'), TH('Office No.'),
            TH('Fax No.'), _bgcolor='#E0E0E0'))

    r = []
    query = db(db.auth_user).select(db.auth_user.ALL, orderby = db.auth_user.last_name)
    n = 0
    for q in query: 
        row = len(query)
        n += 1
        r.append(TR(TD(n),TD(q.first_name), TD(q.last_name), TD(q.email), TD(q.division_id),
            TD(q.department_id), TD(q.po_box), TD(q.mobile_no), TD(q.office_no), TD(q.fax_no)))
        
    body = TBODY(*r)
        
    table = TABLE(*[head, body],  _align="center", _width="100%", _class = 'pure-table')
    return dict(table = table, img_report = img_report)       
    '''

@auth.requires_login()
def AdsDetails():
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
        _onclick = "javascript:PrintContent()"))
    i = None
    row_id = request.args(0)
    ad =  db.advertisement.id == db.ads_vehicle.license_no_id
    ad &= db.ads_vehicle.reg_no_id == row_id
    ads = db(ad).select(db.advertisement.ALL, db.ads_vehicle.ALL)
    v_ads = db(db.ads_vehicle.reg_no_id == row_id).select(db.ads_vehicle.ALL)
    
    query = db.ads_vehicle.reg_no_id == request.args(0)
    query &= db.ads_vehicle.license_no_id == db.advertisement.id

    for d in db(query).select(db.ads_vehicle.ALL, db.advertisement.ALL):
        i = TABLE(*[
            TR(TD(B('Advertisement Details'), _colspan = '2', _style = 'background: #e0e0e0')),
            TR(TD('Ads:'), TD(d.advertisement.ads)),
            TR(TD('Logo:'), TD(d.advertisement.logo), _class = 'pure-table-odd'),
            TR(TD('License No.:'), TD(d.advertisement.license_no)),
            TR(TD('Expiration Date:'), TD(d.advertisement.expiry_date), _class = 'pure-table-odd'),
            TR(TD('Amount Expenses:'), TD(d.ads_vehicle.amount))],
            _border = '0', _align = 'center', _width = '100%',  _class = 'pure-table')
    return dict(i = i, ads = ads, v_ads = v_ads, img_report = img_report)
# -----------  COMPANY/DIVISION VEHICLE CRUD END HERE.   ------------- #    

# -----------  ADVERTISEMENT VEHICLE CRUD START HERE.   ------------- #    
@auth.requires_membership('level_1_user')
def AdvertisementForm():
    db.advertisement.id.readable = False
    form = SQLFORM(db.advertisement, deletable = False)
    if form.process().accepted:
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = 'created advertisement vehicle with license no. %s' % (request.vars.license_no))
        response.flash = 'Form created.'
    return dict(grid = form)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Advertisement():
    db.advertisement.id.readable = False
    
    links=[lambda row: A('Ads Vehicles', _href=URL("default","AdsVehicles", args = row.id)),
           lambda row: A(SPAN(_class = 'icon icon-print'), _title = 'Print', _target="blank", _href=URL("Reports","AdvertisementReport", args = row.id))]
    grid = SQLFORM.grid(db.advertisement.status_id == 1, user_signature = False, exportclasses = export, links = links,
        showbuttontext=False, details = False, create = False, ondelete = delete_ads_record,
        onupdate = update_ads_record, editable = auth.has_membership('level_1_user'), 
        deletable = auth.has_membership('level_1_user'))
    if request.args(0) == 'edit':
        response.view = 'default/AdvertisementForm.html'
        grid = grid.update_form
    return dict(grid = grid)        

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def NonActiveAdvertisement():
    db.advertisement.id.readable = False
    
    links=[lambda row: A('Ads Vehicles', _href=URL("default","AdsVehicles", args = row.id)),
           lambda row: A(SPAN(_class = 'icon icon-print'), _title = 'Print', _target="blank", _href=URL("Reports","AdvertisementReport", args = row.id))]
    grid = SQLFORM.grid(db.advertisement.status_id == 2, user_signature = False, exportclasses = export, links = links,
        showbuttontext=False, details = False, create = False, ondelete = delete_ads_record,
        onupdate = update_ads_record, editable = auth.has_membership('level_1_user'), 
        deletable = auth.has_membership('level_1_user'))
    if request.args(0) == 'edit':
        response.view = 'default/AdvertisementForm.html'
        grid = grid.update_form
    return dict(grid = grid)  

def ads_vehicle_process(form):
    value = db.ads_vehicle.license_no_id == request.vars.license_no_id
    value &= db.ads_vehicle.reg_no_id == request.vars.reg_no_id
    record = db(value).select(db.ads_vehicle.ALL).first()
    if record:
        form.errors.license_no_id = 'already exist!'
        form.errors.reg_no_id = 'already exist!'
        print 'already exist'
    else:
        response.flash = 'Form created.'

@auth.requires_membership('level_1_user')
def AdsVehiclesForm():
    db.ads_vehicle.id.readable = False
    form = SQLFORM(db.ads_vehicle)
    if form.process(onvalidation = ads_vehicle_process).accepted:
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        licens = db(form.vars.license_no_id == db.advertisement.id).select(db.advertisement.ALL).first()
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = 'created reg.no. %s vehicle ads with license no. %s' %(record.reg_no, licens.license_no))
        response.flash = 'Form created.'
    return dict(grid = form)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def AdsVehiclesInfo():
    for info in db(db.advertisement.id == request.args(0)).select(db.advertisement.ALL):
        i = TABLE(*[THEAD(TR(TH('Advertisement:'), TH('Logo:'),TH('License No.:'),TH('Fr.Exp.Date:'),
            TH('To.Exp.Date:'), TH('Amount:'),TH('Status:'), _bgcolor='#E0E0E0')),
            TR(TD(info.ads), TD(info.logo), TD(info.license_no), TD(info.from_expiry_date),
            TD(info.expiry_date),TD(locale.format('%.2F', info.amount or 0, grouping = True)), 
            TD(info.status_id.status))], _border = '0', _align = 'center', _width = '100%', _class = 'pure-table')
    return dict(i = i)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def AdsVehicles():
    row_id = request.args(0)
    db.ads_vehicle.id.readable = False
    fields = [db.ads_vehicle.reg_no_id, db.ads_vehicle.amount]
    grid = SQLFORM.grid(db.ads_vehicle.license_no_id == row_id, fields = fields, user_signature = False, exportclasses = export, 
        showbuttontext=False, details = False, create = False, editable = auth.has_membership('level_1_user'),
        deletable = auth.has_membership('level_1_user'), ondelete = delete_av_record, onupdate = update_av_record,
        oncreate = create_av_record, args = [row_id], searchable = False, paginate = 20)
    if request.args(0) == 'edit':
        response.view = 'default/AdsVehiclesForm.html'
        grid = grid.update_form
    return dict(grid = grid)    
# -----------  ADVERTISEMENT VEHICLE CRUD END HERE.   ------------- #    

# -----------  COMPANY/DIVISION VEHICLE CRUD EXPENDITURES STARTS HERE.   ------------- #
@auth.requires_membership('level_1_user')
def MaintenanceExpensesForm():
    form = SQLFORM(db.repair_history, deletable = False)
    if form.process().accepted:
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = 'created reg.no. %s maintenance expenses with invoice number %s' % (record.reg_no, form.vars.invoice_number))
        response.flash = 'Form created.'
    return dict(grid = form)
   

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def VehicleMaintenance():   
    row_id = request.args(0)
    db.repair_history.id.readable = False
    db.repair_history.reg_no_id.readable = False

    links = [lambda row: A(SPAN(_class = 'icon icon-print'), _title="Print", _target = "_blank",  
        _href=URL("MaintenanceReports","MaintenanceReport", args = row.id))]

    grid = SQLFORM.grid(db.repair_history.reg_no_id == row_id, user_signature = False, links = links,
        exportclasses = export, details = False, searchable = False, showbuttontext = False, 
        paginate = 20, orderby = ~db.repair_history.invoice_date, 
        sortable = False, editable=auth.has_membership('level_1_user'), create = False, #auth.has_membership('level_1_user'), 
        deletable = auth.has_membership('level_1_user'), oncreate = create_vm_record, 
        onupdate = update_me_record, ondelete = delete_me_record)
    if request.args(0) == 'edit':
        grid = grid.update_form
        response.view = 'default/MaintenanceExpensesForm.html'
        form = ''
    return dict(grid = grid)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def FuelExpenses():   
    row_id = request.args(0)
    db.fuel_expenses.id.readable = False
    db.fuel_expenses.reg_no_id.readable = False
    links = [lambda row: A(SPAN(_class = 'icon icon-print'), _title="Print", _target = "_blank", 
        _href=URL("FuelReports","FuelReport", args = row.id))]

    grid = SQLFORM.grid(db.fuel_expenses.reg_no_id == row_id, user_signature = False, links = links,
        exportclasses = export, details = False, searchable = False, showbuttontext = False, 
        paginate = 20, orderby = ~db.fuel_expenses.date_expense, args = [request.args(0)],
        onupdate = update_fe_record, sortable = False, editable=auth.has_membership('level_1_user'), 
        create = False,deletable = auth.has_membership('level_1_user'), ondelete = delete_fe_record)
    if request.args(0) == 'edit':
        response.view = 'default/FuelExpensesForm.html'
        grid = grid.update_form
    return dict(grid = grid)


@auth.requires_membership('level_1_user')
def FuelExpensesForm():
    db.fuel_expenses.id.readable = False
    form = SQLFORM(db.fuel_expenses)
    if form.accepts(request.vars, session):
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = 'created reg.no. %s fuel expenses amounted QR %s' % (record.reg_no, 
                str(locale.format('%.2f', form.vars.amount, grouping = True))))
        response.flash = 'Form created.'
    return dict(grid = form)
   
# -----------  COMPANY/DIVISION VEHICLE CRUD EXPENDITURES END HERE.      ------------- #

# -----------  COMPANY/DIVISION VEHICLE CRUD ODOMETER STARTS HERE.      ------------- #          
    
def oo():
    reg_no = db().select(db.km_used.reg_no_id, groupby = db.km_used.reg_no_id)
    km_rec = db(db.km_used.id > 0).count()
    idx = 1
    while (idx < km_rec):
        
        for row in reg_no:
            last_rec = db(db.km_used.reg_no_id == row.reg_no_id).select(db.km_used.ALL, orderby = db.km_used.given_month).last()
            
            db(db.vehicle.id == last_rec.reg_no_id).update(mileage = last_rec.current_mil)
            db(db.vehicle.id == last_rec.reg_no_id).update(date_mileage = last_rec.given_month)

        idx += 1    

    return locals()

@auth.requires_membership('level_1_user')
def OdometerForm():
    form = SQLFORM(db.km_used, deletable = False) 
    if form.process().accepted:
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name), 
            action = 'created reg.no. %s odometer for the month of %s' % (record.reg_no, str((request.now).strftime('%B %Y'))))
        response.flash = 'Form created.'

    rows = db(db.km_used.reg_no_id == form.vars.reg_no_id).select(orderby = db.km_used.given_month)
    r = 1
    row = len(rows)
    while (r < row):
        rows[r].update_record(consumed_mil = rows[r].current_mil - rows[r-1].current_mil)
        r +=1              
    return dict(grid = form)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Odometer():   
    db.km_used.id.readable = False
    db.km_used.reg_no_id.readable = False
     
    grid = SQLFORM.grid(db.km_used.reg_no_id == request.args(0), user_signature = False, 
        editable=auth.has_membership('level_1_user'), deletable = auth.has_membership('level_1_user'), 
        create = False, details = False, exportclasses = export, searchable = False, showbuttontext = False, 
        orderby = ~db.km_used.given_month, onupdate = update_od_record, 
        sortable = False, paginate = 20, ondelete = delete_od_record)    
    if request.args(0) == 'edit':       
        response.view = 'default/OdometerForm.html'
        grid = grid.update_form  
    return dict(grid = grid)

def last():
    last_ = db(db.km_used.reg_no_id == request.args(0)).select(db.km_used.ALL, orderby = ~db.km_used.given_month).first()
    #row = last_.reg_no_id
    
    if last_:
        db(db.vehicle.id == last_.reg_no_id).update(mileage = last_.current_mil)
        db(db.vehicle.id == last_.reg_no_id).update(date_mileage = last_.given_month)
        
    else:
        response.flash = 'Empty Mileage.'    
        None
    return locals()

def CompanyInfo():
    last_ = db(db.km_used.reg_no_id == request.args(0)).select(db.km_used.ALL, orderby = ~db.km_used.given_month).first()
    if last_:
        db(db.vehicle.id == last_.reg_no_id).update(mileage = last_.current_mil)
        db(db.vehicle.id == last_.reg_no_id).update(date_mileage = last_.given_month)
    else:
        response.flash = 'Empty Mileage.'
        None

    for info in db(db.vehicle.id == request.args(0)).select(db.vehicle.ALL):
        i = TABLE(*[THEAD(TR(TH('Reg.No.:'), TH('Company:'),TH('Division:'),TH('Department:'),TH('Chassis No:'), TH('Last Reading:'),TH('Model:'), _bgcolor='#E0E0E0')),
            TR(TD(info.reg_no), TD(info.company_id.company), TD(info.division_id.division), TD(info.department.name),
            TD(info.chassis_no),TD(str(locale.format('%d', info.mileage or 0, grouping = True)) + ' Km.'), TD(info.model))], _border = '0', _align = 'center', _width = '100%', _class = 'pure-table')
    return dict(i = i)

# -----------  COMPANY/DIVISION VEHICLE CRUD ODOMETER ENDS HERE.        ------------- #                

# -----------  COMPANY/DIVISION VEHICLE CRUD PHOTOS STARTS HERE.        ------------- #
@auth.requires_membership("level_1_user") 
def PhotoForm():
    form = SQLFORM(db.v_photos)
    if form.accepts(request.vars, session):
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name), 
            action = 'created reg.no. %s photo\'s.' % (record.reg_no))
        response.flash = 'Form created.'
    return dict(form = form)

   
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def upload_photos():
    db.v_photos.id.readable = False
    grid = SQLFORM.grid(db.v_photos, user_signature=False, exportclasses = export, 
        showbuttontext=False, details = False, orderby = db.v_photos.reg_no_id,
        searchable = True, create = auth.has_membership('level_1_user'),
        editable = auth.has_membership('level_1_user'), deletable = auth.has_membership('level_1_user'),
        oncreate = create_vp_record, onupdate = update_vp_record, ondelete = delete_vp_record)      
    if request.args(0) == 'new':
        grid = grid.create_form
        response.view = 'default/PhotoForm.html'
    if request.args(0) == 'edit':
        response.view = 'default/PhotoForm.html'
        grid = grid.update_form
    return dict(form = '', grid = grid, renderstyle = True)

   
# -----------  COMPANY/DIVISION VEHICLE CRUD PHOTOS ENDS HERE.          ------------- #

# -----------  COMPANY/DIVISION VEHICLE CRUD INSURANCE POLICY STARTS HERE.    ------------- #                    

@auth.requires_membership("level_1_user") 
def InsurancePolicyForm():
    db.insurance_policy.id.readable = False
    form = SQLFORM(db.insurance_policy, deletable = False)
    if form.process().accepted:
        db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name,auth.user.last_name),
        action = 'created insurance policy no %s' % (form.vars.policy_no))
        response.flash = 'Form Accepted'
    return dict(grid = form)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def InsurancePolicy():
    db.insurance_policy.id.readable = False
    links=[lambda row: A('Insured Vehicles', _href=URL("default","InsuredVehicles", args = row.id)),
           lambda row: A(SPAN(_class = 'icon icon-print'), _title = 'Print', _target="blank", _href=URL("Reports","InsuredVehiclesReport", args = row.id))]
    grid = SQLFORM.grid(db.insurance_policy.status_id == 1, user_signature=False, exportclasses = export, details=False,
        links = links, create = False, editable=auth.has_membership('level_1_user'),
        deletable=auth.has_membership('level_1_user'), showbuttontext=False, onupdate = update_ip_record, 
        ondelete = delete_ip_record, oncreate = create_ip_record)
    if request.args(0) == 'edit':
        response.view = 'default/InsurancePolicyForm.html'
        grid = grid.update_form
    return dict(grid = grid)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def NonActiveInsurancePolicy():
    db.insurance_policy.id.readable = False
    links=[lambda row: A('Insured Vehicles', _href=URL("default","InsuredVehicles", args = row.id)),
           lambda row: A(SPAN(_class = 'icon icon-print'), _title = 'Print', _target="blank", _href=URL("Reports","InsuredVehiclesReport", args = row.id))]
    grid = SQLFORM.grid(db.insurance_policy.status_id == 2, user_signature=False, exportclasses = export, details=False,
        links = links, create = False, editable=auth.has_membership('level_1_user'),
        deletable=auth.has_membership('level_1_user'), showbuttontext=False, onupdate = update_ip_record, 
        ondelete = delete_ip_record, oncreate = create_ip_record)
    if request.args(0) == 'edit':
        response.view = 'default/InsurancePolicyForm.html'
        grid = grid.update_form
    return dict(grid = grid)

@auth.requires_membership("level_1_user") 
def Ins_Veh_Process(form):
    value = db.insured_vehicles.policy_no_id == request.vars.policy_no_id
    value &= db.insured_vehicles.reg_no_id == request.vars.reg_no_id
    record = db(value).select(db.insured_vehicles.ALL).first()
    if record:
        form.errors.policy_no_id = 'already exist!'
        form.errors.reg_no_id = 'already exist!'
        print 'already exist'
    else:
        response.flash = 'Form created.'


@auth.requires_membership("level_1_user") 
def InsuredVehiclesForm():
    row_id = request.args(0)
    db.insured_vehicles.id.readable = False
    form = SQLFORM(db.insured_vehicles, deletable = False)
    if form.process(onvalidation = Ins_Veh_Process).accepted:
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        policy = db(form.vars.policy_no_id == db.insurance_policy.id).select(db.insurance_policy.ALL).first()
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = "created reg.no. %s insured vehicle with policy no. %s" % (record.reg_no, policy.policy_no))       
        response.flash = 'Form Accepted'   
    return dict(grid = form)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def InsuredVehicles():
    row_id = request.args(0)
    db.insured_vehicles.id.readable = False
    db.insured_vehicles.policy_no_id.readable = False
    query = db.insured_vehicles.policy_no_id == row_id
    grid = SQLFORM.grid(query, user_signature=False, exportclasses = export, orderby = ~db.insured_vehicles.reg_no_id,
        details=False, create = False,  editable = auth.has_membership('level_1_user'), searchable = False,
        deletable = auth.has_membership('level_1_user'), sortable = True, oncreate = create_iv_record,
        showbuttontext=False, paginate=20, args = [row_id], onupdate = update_iv_record, ondelete = delete_iv_record)       
    if request.args(0) == 'edit':
        response.view = 'default/InsuredVehiclesForm.html'
        grid = grid.update_form
       
    return dict(grid = grid)

def InsuranceInfo():
    for info in db(db.insurance_policy.id == request.args(0)).select(db.insurance_policy.ALL):
        i = TABLE(*[THEAD(TR(TH('Company:'), TH('Insurance Company:'),TH('Policy No.:'),TH('Period Covered:'),TH('Amount:'), TH('Status:'), _bgcolor='#E0E0E0')),
            TR(TD(info.company_id.company), TD(info.insurance_company_id.name), TD(info.policy_no), TD(info.period_covered),
            TD(locale.format('%.2f',info.amount, grouping = True)),TD(info.status_id.status))], _border = '0', _align = 'center', _width = '100%', _class = 'pure-table')
    return dict(i = i)

# -----------  COMPANY/DIVISION VEHICLE CRUD INSURANCE POLICY ENDS HERE.    ------------- #                    


# -----------  COMPANY/DIVISION DRIVER CRUD STARTS HERE.    ------------- #
@auth.requires_membership('level_1_user')
def DriverForm():
    form = SQLFORM(db.driver)
    if form.process().accepted:
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = 'created %s driver profile.' % (form.vars.driver_name))
        response.flash = 'Form accepted'
    return dict(grid = form)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Driver():      
    db.driver.id.readable = False
    links =[lambda row: A(SPAN(_class = 'icon icon-print'), _target = '_blank', _title = "Print", 
        _href = URL('Reports', 'DriverReport', args=row.id))]
    grid = SQLFORM.grid(db.driver, user_signature=False, exportclasses = export, onupdate = update_d_record,
        links = links, showbuttontext=False, details = False, maxtextlength = 18,
        ondelete = delete_d_record, create = auth.has_membership('level_1_user'), 
        editable = auth.has_membership('level_1_user'), deletable = auth.has_membership('level_1_user')) 
    if request.args(0) == 'new':
    	response.view = 'default/DriverForm.html'
        grid = grid.create_form
    if request.args(0) == 'edit':
        response.view = 'default/DriverForm.html'  
        grid = grid.update_form
    return dict(grid = grid)

# -----------  COMPANY/DIVISION DRIVER CRUD ENDS HERE.      ------------- #

# -----------  COMPANY/DIVISION VEHICLE CRUD HAND-OVER STARTS HERE.    ------------- #

@auth.requires_membership('level_1_user')
def HandOverForm():  #[Hand over form]
    form = SQLFORM(db.vehicles_hand_over,(request.args(0)))
    if form.process().accepted: 
        
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()

        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = "created reg.no. %s hand-over." % (record.reg_no))       
        response.flash = 'Form Accepted'   
    return dict(grid = form)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def HandOver(): #[Hand over grid]
    db.vehicles_hand_over.id.readable = False    
    links=[lambda row: A(SPAN(_class = 'icon icon-print'), _title="Print", _target="_blank", _href=URL("Reports","HandOverReport", args = row.id))]
    grid = SQLFORM.grid(db.vehicles_hand_over, user_signature=False, exportclasses = export,
        details = False, orderby = db.vehicles_hand_over.date_and_time, showbuttontext = False, links = links, 
        onupdate = update_ho_record, ondelete = delete_ho_record,
        create = False, editable = auth.has_membership('level_1_user'), 
        deletable = auth.has_membership('level_1_user'))
    if request.args(0) == 'new':
        response.view = 'default/HandOverForm.html'
        grid = grid.create_form
    if request.args(0) == 'edit':
        response.view = 'default/HandOverForm.html'
        grid = grid.update_form
    return dict(grid = grid)    

# -----------  COMPANY/DIVISION VEHICLE CRUD HAND-OVER ENDS HERE.    ------------- #                    

def FormDownload(): #[Vehicle form download]
    import os
    fullpath = os.path.join(request.folder,'uploads', 'VehicleForm.pdf')
    response.stream(os.path.join(request.folder, fullpath))


# -----------  DEPARTMENT CONTROLLER CRUD ENDS HERE.    ------------- #                    

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


