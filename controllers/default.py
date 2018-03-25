
form_success = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Record save.', _class='white'),_class='alert alert-success') 
form_error = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
form_info = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Kindly fill the form', _class='white'),_class='alert alert-info') 
form_warning = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-exclamation-triangle smaller-130'),B(' Warning: '), 'Other user has changed record before you did', _class='white'),_class='alert alert-warning') 

    
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

def Parent():
    return locals()
def Modal():
    return locals()
def Company():
    import json
    c = db().select(db.company.ALL)
    table = SQLTABLE(c, _class='table', _id='company-table')
    return dict(table = table)
    #table = json.dumps(db(db.company).select().as_list())
    #return dict(table=XML(table))



def test_click():
    page.include("http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.min.js")
    # or  page.google_load("jqueryui", "1.7.2")
    page.include("http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/ui-darkness/jquery-ui.css")   
    d = DIV("Click Me",_id="clickme")
    event.listen("click",d,handle_it)
    return dict(d=d)
#<div id="some_btn"><a class="btn btn-success btn-mini" data-target="#some_modal" data-toggle="modal"><i class="icon-search icon-white"></i>    
#links =[lambda row: A(SPAN(_class = 'icon icon-print'), _target = '_blank', _title = "Print", _href = URL('Reports', 'DriverReport', args=row.id),
#            _onclick="MyWindow=window.open = 'URL('Reports', 'DriverReport', args = row.id)' ")]
    #return locals()
def handle_it():
    return jq("#clickme").append(DIV(_id="dialog"))() + \
           jq("#dialog").html("%s")() % str(request.now) + \
           jq("#dialog").dialog(dict(title="Server Time"))()


def callback():
    """ a generic callback """
    return cache.ram(request.args(0),lambda:None,None)(**request.vars)

def show():
    from datetime import date
    '''
    rep_sta = db().select(db.repair_history.ALL).first()
    rep_end = db().select(db.repair_history.ALL).last()
    
    fil_dat = db.vehicle.company_id == db.company.id
    fil_dat &= db.vehicle.reg_no == db.repair_history.reg_no_id
    #fil_dat &= db.repair_history.invoice_date >= rep_sta.invoice_date
    #fil_dat &= db.repair_history.invoice_date <= rep_end.invoice_date

    rep_sum = db.repair_history.total_amount.sum().coalesce_zero()
    rep_exp = db(fil_dat).select(rep_sum).first()[rep_sum]

    query = db(fil_dat).select(db.company.company), orderby=db.company.company, groupby=db.company.company)
    
    #return query
    '''
    rep_sta = db().select(db.repair_history.ALL, orderby=db.repair_history.invoice_date).first()
    rep_end = db().select(db.repair_history.ALL,  orderby=db.repair_history.invoice_date).last()


    fil_dat = db.vehicle.company_id == db.company.id
    fil_dat &= db.vehicle.id == db.repair_history.reg_no_id
    ran_dat = db.repair_history.invoice_date >= rep_sta.invoice_date
    ran_dat &= db.repair_history.invoice_date <= rep_end.invoice_date
    #fil_dat &= db.vehicle.id == db.insured_vehicles.reg_no_id

    rep_sum = db.repair_history.total_amount.sum().coalesce_zero()
    ful_sum = db.fuel_expenses.amount.sum().coalesce_zero()
    ins_sum = db.insured_vehicles.amount.sum().coalesce_zero()

    rep_exp = db(fil_dat).select(rep_sum).first()[rep_sum]

    range_date = db(ran_dat).select(db.repair_history.invoice_date.year(), orderby=db.repair_history.invoice_date.year(), distinct = True)
    
    d_r = [2007,2010,2011,2012,2013,2014,2015,2016]

    #print range_date
    #query = db(fil_dat).select(db.company.company, rep_sum, ful_sum, ins_sum, orderby=db.company.company, groupby=db.company.company, left=[db.repair_history.on(db.vehicle.id == db.repair_history.reg_no_id), db.fuel_expenses.on(db.vehicle.id == db.fuel_expenses.reg_no_id), db.insured_vehicles.on(db.vehicle.id == db.insured_vehicles.reg_no_id)])
    #query = db(fil_dat).select(db.company.company, db.repair_history.invoice_date.year(), rep_sum,  distinct=True,orderby=db.company.company | db.repair_history.invoice_date.year(), groupby=db.company.company | db.repair_history.invoice_date.year(), left=db.repair_history.on(db.vehicle.id==db.repair_history.reg_no_id))
    #query = db(fil_dat).select(db.company.id, db.company.company, orderby=db.company.company, groupby=db.company.id |db.company.company, left=db.repair_history.on(db.vehicle.id==db.repair_history.reg_no_id))
    
    #rows = db(db.repair_history.invoice_date.year().belongs(d_r)).select(rep_sum)
    #print rows
    
    for c in db(fil_dat).select(db.company.id, db.company.company, orderby=db.company.company, groupby=db.company.id |db.company.company, left=db.repair_history.on(db.vehicle.id==db.repair_history.reg_no_id)):
        print c.company
        #rows=db(dv.autos.id.belongs(id_list)).select()
        for y in db(fil_dat &( c.id == db.company.id)).select(db.repair_history.invoice_date.year(), rep_sum, orderby=db.repair_history.invoice_date.year(),groupby=db.repair_history.invoice_date.year(), 
            left=db.repair_history.on(db.repair_history.invoice_date.year().belongs(d_r))):
            if y[db.repair_history.invoice_date.year()] != d_r:
                y = 0
                print '                    ',y 
            else:
                y = y[db.repair_history.invoice_date.year()]
                print '                    ',  y#,  y[rep_sum]
    
    return range_date
'''
def check_membership():
    if not auth.has_membership(group_id='fornitori'):
        redirect(URL('default', 'other'))

@auth.requires(check_membership)
def index():
    etc.
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
'''
def check_membership():
    if auth.has_membership(group_id='level_2_user'):
        redirect(URL('Company','Dashboard'))
    elif auth.has_membership(group_id='level_1_user'):
        redirect(URL('default','Dashboard'))

@auth.requires_login()
def index():
    if auth.has_membership(group_id='level_2_user'):
        redirect(URL('Company','Dashboard'))
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Welcome '), 'to our latest Fleet Management System.', _class='white'),_class='alert alert-success') 
    return locals()

@auth.requires_login()
def Dashboard():
    from datetime import date
    today = datetime.date.today()

    active = db(db.vehicle.status_id == 3).count()
    non_active = db(db.vehicle.status_id == 2).count()
    cancelled = db(db.vehicle.status_id == 1).count()

    expired_reg_no = db((db.vehicle.status_id == 3)&(db.vehicle.exp_date <= request.now)).count()

    expired_lic_no = db(db.driver.expiry_date <= request.now).count()

    expired_ins = db((db.insurance_policy.status_id == 1)&(db.insurance_policy.period_covered <= request.now)).count()

    total = active + non_active + cancelled
    act_per = float(active) / total * 100
    non_per = float(non_active) / total * 100
    can_per = float(cancelled) / total * 100

    ctr_query = db.auth_user.id == db.auth_membership.user_id
    ctr_query &= db.auth_membership.group_id == 3

    mai = db.repair_history.focal_person.count()
    fue = db.fuel_expenses.focal_person.count()
    mil = db.km_used.focal_person.count()

    mai_que = db(ctr_query).select(db.auth_user.last_name, db.auth_user.division_id, mai, orderby=db.auth_user.division_id | db.auth_user.last_name, groupby=db.auth_user.division_id | db.auth_user.last_name, left=db.repair_history.on(db.auth_user.id == db.repair_history.focal_person))
    fue_que = db(ctr_query).select(db.auth_user.last_name, db.auth_user.division_id, fue, orderby=db.auth_user.division_id | db.auth_user.last_name, groupby=db.auth_user.division_id | db.auth_user.last_name, left=db.fuel_expenses.on(db.auth_user.id == db.fuel_expenses.focal_person))#.as_list()
    mil_que = db(ctr_query).select(db.auth_user.last_name, db.auth_user.division_id, mil, orderby=db.auth_user.division_id | db.auth_user.last_name, groupby=db.auth_user.division_id | db.auth_user.last_name, left=db.km_used.on(db.auth_user.id == db.km_used.focal_person))#.as_list()
 
    #act_que = db().select(db.activities.ALL, ~orderby=db.activities.log_date)
    #ctr_dat = db(ctr_query).select()#.count()
    #print ctr_dat


    #wks_tra = date(today.year, today.month, today.day).weekday() == 4
    #wks_tra = today - 

    #man_tra = db((db.repair_history.log_date >= wks_tra) & (db.repair_history.log_date <= wks_tra)).count()
    #ful_tra = db((db.fuel_expenses.log_date >= wks_tra) & (db.fuel_expenses.log_date <= wks_tra)).count()
    #mil_tra = db((db.km_used.log_date >= wks_tra) & (db.km_used.log_date <= wks_tra)).count()
    
    '''
    today = datetime.date.today()
    saturday = today - datetime.timedelta(today.weekday()+2)

    for i in range(6):
        tmp_date = saturday + datetime.timedelta(i)
        print tmp_date.toordinal()%6 + 1, '==', tmp_date.strftime('%A')
    print ''
    '''
    # line chart
    rep_sta = db().select(db.repair_history.ALL, orderby=db.repair_history.invoice_date).first()
    rep_end = db().select(db.repair_history.ALL,  orderby=db.repair_history.invoice_date).last()


    fil_dat = db.vehicle.company_id == db.company.id
    fil_dat &= db.vehicle.id == db.repair_history.reg_no_id
    fil_dat &= db.repair_history.invoice_date >= rep_sta.invoice_date
    fil_dat &= db.repair_history.invoice_date <= rep_end.invoice_date
    #fil_dat &= db.vehicle.id == db.insured_vehicles.reg_no_id

    rep_sum = db.repair_history.total_amount.sum().coalesce_zero()
    ful_sum = db.fuel_expenses.amount.sum().coalesce_zero()
    ins_sum = db.insured_vehicles.amount.sum().coalesce_zero()

    rep_exp = db(fil_dat).select(rep_sum).first()[rep_sum]
    #query = db(fil_dat).select(db.company.company, rep_sum, ful_sum, ins_sum, orderby=db.company.company, groupby=db.company.company, left=[db.repair_history.on(db.vehicle.id == db.repair_history.reg_no_id), db.fuel_expenses.on(db.vehicle.id == db.fuel_expenses.reg_no_id), db.insured_vehicles.on(db.vehicle.id == db.insured_vehicles.reg_no_id)])
    lin_que = db(fil_dat).select(db.company.id, db.company.company, orderby=db.company.company, groupby=db.company.id |db.company.company, left=db.repair_history.on(db.vehicle.id==db.repair_history.reg_no_id))
    lin_com = db(fil_dat).select(db.company.id, db.company.company, orderby=db.company.company, groupby=db.company.id |db.company.company, left=db.repair_history.on(db.vehicle.id==db.repair_history.reg_no_id))
    lin_yer = db(fil_dat).select(db.repair_history.invoice_date.year(), rep_sum, orderby=db.repair_history.invoice_date.year(), groupby=db.repair_history.invoice_date.year(),left=db.repair_history.on(db.vehicle.id==db.repair_history.reg_no_id))
    row = []
    for c in lin_que:
        row.append(c.company)
        for y in db(fil_dat &( c.id == db.company.id)).select(db.repair_history.invoice_date.year(), rep_sum, orderby=db.repair_history.invoice_date.year(), groupby=db.repair_history.invoice_date.year(),left=db.repair_history.on(db.vehicle.id==db.repair_history.reg_no_id)):
            row.append(y[db.repair_history.invoice_date.year()])
            row.append(y[rep_sum])
    fil_dat = db.vehicle.company_id == db.company.id
    rep_sum = db.repair_history.total_amount.sum().coalesce_zero()
    ful_sum = db.fuel_expenses.amount.sum().coalesce_zero()
    ins_sum = db.insured_vehicles.amount.sum().coalesce_zero()
    bar_que = db(fil_dat).select(db.company.company, rep_sum, ful_sum, ins_sum, orderby=db.company.company, groupby=db.company.company, left=[db.repair_history.on(db.vehicle.id == db.repair_history.reg_no_id), db.fuel_expenses.on(db.vehicle.id == db.fuel_expenses.reg_no_id), db.insured_vehicles.on(db.vehicle.id == db.insured_vehicles.reg_no_id)])
    return dict(fil_dat=fil_dat,lin_com=lin_com, lin_yer=lin_yer, bar_que=bar_que, mai_que=mai_que,fue_que=fue_que, mil_que=mil_que,active=active, non_active=non_active, cancelled=cancelled, act_per=act_per, non_per=non_per, 
        can_per=can_per, expired_reg_no=expired_reg_no, expired_lic_no=expired_lic_no, expired_ins=expired_ins)
        #man_tra=man_tra, ful_tra=ful_tra, mil_tra=mil_tra)


@auth.requires_login()
def dashboard_1():
    active = db(db.vehicle.status_id == 3).count()
    non_active = db(db.vehicle.status_id == 2).count()
    cancelled = db(db.vehicle.status_id == 1).count()

    expired_reg_no = db((db.vehicle.status_id == 3)&(db.vehicle.exp_date <= request.now)).count()

    expired_lic_no = db(db.driver.expiry_date <= request.now).count()

    expired_ins = db((db.insurance_policy.status_id == 1)&(db.insurance_policy.period_covered <= request.now)).count()

    total = active + non_active + cancelled
    act_per = float(active) / total * 100
    non_per = float(non_active) / total * 100
    can_per = float(cancelled) / total * 100    

    rep_sta = db().select(db.repair_history.ALL, orderby=db.repair_history.invoice_date).first()
    rep_end = db().select(db.repair_history.ALL,  orderby=db.repair_history.invoice_date).last()


    fil_dat = db.vehicle.company_id == db.company.id
    fil_dat &= db.vehicle.id == db.repair_history.reg_no_id
    fil_dat &= db.repair_history.invoice_date >= rep_sta.invoice_date
    fil_dat &= db.repair_history.invoice_date <= rep_end.invoice_date
    #fil_dat &= db.vehicle.id == db.insured_vehicles.reg_no_id

    rep_sum = db.repair_history.total_amount.sum().coalesce_zero()
    ful_sum = db.fuel_expenses.amount.sum().coalesce_zero()
    ins_sum = db.insured_vehicles.amount.sum().coalesce_zero()

    rep_exp = db(fil_dat).select(rep_sum).first()[rep_sum]
    
    lin_que = db(fil_dat).select(db.company.id, db.company.company, orderby=db.company.company, groupby=db.company.id |db.company.company, left=db.repair_history.on(db.vehicle.id==db.repair_history.reg_no_id))
    lin_com = db(fil_dat).select(db.company.id, db.company.company, orderby=db.company.company, groupby=db.company.id |db.company.company, left=db.repair_history.on(db.vehicle.id==db.repair_history.reg_no_id))
    lin_yer = db(fil_dat).select(db.repair_history.invoice_date.year(), rep_sum, orderby=db.repair_history.invoice_date.year(), groupby=db.repair_history.invoice_date.year(),left=db.repair_history.on(db.vehicle.id==db.repair_history.reg_no_id))

    return dict(lin_que=lin_que,lin_com=lin_com,lin_yer=lin_yer,fil_dat= fil_dat,active=active,non_active=non_active,cancelled=cancelled,act_per=act_per,non_per=non_per,can_per=can_per,expired_reg_no=expired_reg_no,expired_lic_no=expired_lic_no,expired_ins=expired_ins)

@auth.requires_login()
def dashboard_2():
    ctr_query = db.auth_user.id == db.auth_membership.user_id
    ctr_query &= db.auth_membership.group_id == 3

    mai = db.repair_history.reg_no_id.count()
    fue = db.fuel_expenses.reg_no_id.count()
    mil = db.km_used.reg_no_id.count()

    mai_que = db().select(db.division.division, mai, orderby=db.division.division, groupby=db.division.division, left=[db.vehicle.on(db.vehicle.division_id == db.division.id), db.repair_history.on(db.repair_history.reg_no_id == db.vehicle.id)])
    fue_que = db().select(db.division.division, fue, orderby=db.division.division, groupby=db.division.division, left=[db.vehicle.on(db.vehicle.division_id == db.division.id), db.fuel_expenses.on(db.fuel_expenses.reg_no_id == db.vehicle.id)])
    mil_que = db().select(db.division.division, mil, orderby=db.division.division, groupby=db.division.division, left=[db.vehicle.on(db.vehicle.division_id == db.division.id), db.km_used.on(db.km_used.reg_no_id == db.vehicle.id)])

    return dict(mai_que = mai_que, fue_que = fue_que, mil_que = mil_que)


@auth.requires_login()
def dashboard_3():
    return dict()

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Browse():
    row = []
    
    #print 'request var ', request.args

    
    if request.args(0):
        if request.args(0) == '4':
            status_id = (db.vehicle.status_id == 3)&(db.vehicle.exp_date <= request.now)            
        elif request.args(0) == '5':
            status_id = (db.insurance_policy.status_id == 1) &  (db.insured_vehicles.policy_no_id == db.insurance_policy.id) & (db.insured_vehicles.reg_no_id == db.vehicle.id) # insurance vehicles
        else:
            status_id = db.vehicle.status_id == request.args(0)       
    else:
        status_id = db.vehicle.id > 0
    
        #status_id = db.vehicle.exp_date <= request.now

    #expired_reg_no = db((db.vehicle.status_id == 3)&(db.vehicle.exp_date <= request.now)).count()

    #expired_lic_no = db(db.driver.expiry_date <= request.now).count()

    #expired_ins = db((db.insurance_policy.status_id == 1)&(db.insurance_policy.period_covered <= request.now)).count()

    
    query = db(status_id).select(db.vehicle.ALL, db.v_photos.ALL, left=db.v_photos.on(db.vehicle.id==db.v_photos.reg_no_id))
    head = THEAD(TR(TH(_class='sorting_disabled'),TH('Reg.No.'),TH('Code'),TH('Division'),TH('Mileage'),TH('Model'),TH('RP'),TH('FT'),TH('RR'),TH('LF'),TH('RT'),TH(_class='sorting_disabled')))
    for n in query:
        view = A(SPAN(_class = 'fa fa-search bigger-120 blue'), _tabindex='0', _role='button', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Fleet Info','_data-content': fleet_info(n.vehicle.id)})
        prin = A(SPAN(_class = 'fa fa-print bigger-120 blue'), _title="Print",_target='blank', _href=URL("Reports","VehicleProfileReport", args=n.vehicle.id))
        edit = A(SPAN(_class = 'fa fa-pencil bigger-120 blue'), _title="Edit", _href=URL("default","edit_VehicleProfileForm", args=n.vehicle.id))
        main = A(SPAN(_class = 'fa fa-wrench bigger-120 blue'), _title="Maintenance", _href=URL("default","VehicleMaintenance", args=n.vehicle.id))
        fuel = A(SPAN(_class = 'fa fa-tint bigger-120 blue'), _title="Fuel", _href=URL("default","Fuel", args=n.vehicle.id))
        mile = A(SPAN(_class = 'fa fa-road bigger-120 blue'), _title="Milage", _href=URL("default","Odometer", args=n.vehicle.id))
        insu = A(SPAN(_class = 'fa fa-medkit bigger-120 blue'), _tabindex='0', _role='button', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Insurance Info','_data-content': insur_info(n.vehicle.id)})
        adve = A(SPAN(_class = 'fa fa-play-circle-o bigger-120 blue'), _tabindex='0', _role='button', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Advertisement Info','_data-content': adve_info(n.vehicle.id)})
        phot = A(SPAN(_class = 'fa fa-camera bigger-120 blue'), _title="Photo", _href=URL("default","edit_PhotosForm", args=n.v_photos.id))
        cont = A(SPAN(_class = 'fa fa-user-circle-o bigger-120 blue'), _tabindex='0', _role='button', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Fleet Controller Info','_data-content': cont_info(n.vehicle.id)})
        btn_lnks = DIV(view, prin, edit, main, fuel, mile, insu, adve, phot, cont, _class="hidden-sm hidden-xs action-buttons")

        if n.vehicle.status_id == 1: # cancelled vehicles     SPAN(_class='ace-icon fa fa-car')       
            row.append(TR(TD(A(SPAN(_class='fa fa-flag red bigger-130 tooltip-error', _title='', _role='button',**{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Cancelled Fleet'}))),
                TD(n.vehicle.reg_no),TD(n.vehicle.vehicle_code),TD(n.vehicle.division_id.division), TD(locale.format('%d',n.vehicle.mileage or 0, grouping = True)),TD(n.vehicle.model),

                TD(A(SPAN(_class='ace-icon fa fa-drivers-license'), _class='blue',_title='Road Permit', _href = URL('default', 'download', args= n.v_photos.road_permit),**{'_data-rel':'colorbox'}) if n.v_photos.road_permit else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Front Side Photo', _href = URL('default', 'download', args= n.v_photos.photo),**{'_data-rel':'colorbox'}) if n.v_photos.photo else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Rear Side Photo', _href = URL('default', 'download', args= n.v_photos.photo2),**{'_data-rel':'colorbox'}) if n.v_photos.photo2 else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Left Side Photo', _href = URL('default', 'download', args= n.v_photos.photo3),**{'_data-rel':'colorbox'}) if n.v_photos.photo3 else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Right Side Photo', _href = URL('default', 'download', args= n.v_photos.photo4),**{'_data-rel':'colorbox'}) if n.v_photos.photo4 else "", _class='ace-thumbnails clearfix'),
                TD(btn_lnks)))       
        elif (n.vehicle.exp_date <= datetime.date.today()): # reg.no. expired                             
            row.append(TR(TD(A(SPAN(_class='fa fa-flag orange bigger-130 tooltip-warning', _title='', _role='button',**{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Expired Reg.No.'}))),
                TD(n.vehicle.reg_no),TD(n.vehicle.vehicle_code),TD(n.vehicle.division_id.division), TD(locale.format('%d',n.vehicle.mileage or 0, grouping = True)),TD(n.vehicle.model),
                TD(A(SPAN(_class='ace-icon fa fa-drivers-license'), _class='blue', _title='Road Permit', _href = URL('default', 'download', args= n.v_photos.road_permit), **{'_data-rel':'colorbox'}) if n.v_photos.road_permit else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue', _title='Front Side Photo', _href = URL('default', 'download', args= n.v_photos.photo),**{'_data-rel':'colorbox'}) if n.v_photos.photo else "",  _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue', _title='Rear Side Photo', _href = URL('default', 'download', args= n.v_photos.photo2),**{'_data-rel':'colorbox'}) if n.v_photos.photo2 else "",  _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue', _title='Left Side Photo', _href = URL('default', 'download', args= n.v_photos.photo3),**{'_data-rel':'colorbox'}) if n.v_photos.photo3 else "",  _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue', _title='Right Side Photo', _href = URL('default', 'download', args= n.v_photos.photo4),**{'_data-rel':'colorbox'}) if n.v_photos.photo4 else "",  _class='ace-thumbnails clearfix'),
                TD(btn_lnks)))       
        elif (db.insurance_policy.status_id == 1) &  (db.insured_vehicles.policy_no_id == db.insurance_policy.id) & (db.insured_vehicles.reg_no_id == n.vehicle.id): # insurance vehicles
            row.append(TR(TD(A(SPAN(_class='fa fa-flag blue bigger-130 tooltip-info', _title='', _role='button',**{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Expired Fleet Insurance'}))),
                TD(n.vehicle.reg_no),TD(n.vehicle.vehicle_code),TD(n.vehicle.division_id.division), TD(locale.format('%d',n.vehicle.mileage or 0, grouping = True)),TD(n.vehicle.model),
                TD(A(SPAN(_class='ace-icon fa fa-drivers-license'), _class='blue',_title='Road Permit', _href = URL('default', 'download', args= n.v_photos.road_permit),**{'_data-rel':'colorbox'}) if n.v_photos.road_permit else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Front Side Photo', _href = URL('default', 'download', args= n.v_photos.photo),**{'_data-rel':'colorbox'}) if n.v_photos.photo else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Rear Side Photo', _href = URL('default', 'download', args= n.v_photos.photo2),**{'_data-rel':'colorbox'}) if n.v_photos.photo2 else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Left Side Photo', _href = URL('default', 'download', args= n.v_photos.photo3),**{'_data-rel':'colorbox'}) if n.v_photos.photo3 else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Right Side Photo', _href = URL('default', 'download', args= n.v_photos.photo4),**{'_data-rel':'colorbox'}) if n.v_photos.photo4 else "", _class='ace-thumbnails clearfix'),
                TD(btn_lnks)))       
        else:
            row.append(TR(TD(A(SPAN(_class='fa fa-flag green bigger-130 tooltip-success', _title='', _role='button',**{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Good Fleet Status'}))),
                TD(n.vehicle.reg_no),TD(n.vehicle.vehicle_code),TD(n.vehicle.division_id.division), TD(locale.format('%d',n.vehicle.mileage or 0, grouping = True)),TD(n.vehicle.model),
                TD(A(SPAN(_class='ace-icon fa fa-drivers-license'), _class='blue',_title='Road Permit', _href = URL('default', 'download', args= n.v_photos.road_permit),**{'_data-rel':'colorbox'}) if n.v_photos.road_permit else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Front Side Photo', _href = URL('default', 'download', args= n.v_photos.photo),**{'_data-rel':'colorbox'}) if n.v_photos.photo else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Rear Side Photo', _href = URL('default', 'download', args= n.v_photos.photo2),**{'_data-rel':'colorbox'}) if n.v_photos.photo2 else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Left Side Photo', _href = URL('default', 'download', args= n.v_photos.photo3),**{'_data-rel':'colorbox'}) if n.v_photos.photo3 else "", _class='ace-thumbnails clearfix'),
                TD(A(SPAN(_class='ace-icon fa fa-car'), _title='Right Side Photo', _href = URL('default', 'download', args= n.v_photos.photo4),**{'_data-rel':'colorbox'}) if n.v_photos.photo4 else "", _class='ace-thumbnails clearfix'),
                TD(btn_lnks)))       
    body = TBODY(*row)
    table = TABLE(*[head, body], _class="table table-striped table-bordered table-hover")
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(table = table)

def fleet_info(z = request.args(0)):
    for x in db(db.vehicle.id == z).select():
        i = TABLE(*[
            TR(TD('Company: '), TD(x.company_id.company)),
            TR(TD('Division: '), TD(x.division_id.division)),
            TR(TD('Department: '), TD(x.department.name)),
            TR(TD('Owner: '), TD(x.owner.name)),
            TR(TD('Chassis No.: '), TD(x.chassis_no)),
            TR(TD('RPEx Date:'),TD(x.exp_date)),
            TR(TD('Invoice:'),TD(x.invoice or None)),
            TR(TD('Value:'),TD(x.value_purchase)),
            TR(TD('Dt. Sale:'),TD(x.date_of_sale)),
            TR(TD('Dep.Value:'),TD(x.depreciation_value)),
            TR(TD('Dt. Mileage:'),TD(x.date_mileage)),
            TR(TD('Type:'),TD(x.car_type)),
            TR(TD('Plate:'),TD(x.plate_type)),
            TR(TD('Cylinder:'),TD(x.cylinder_count)),
            TR(TD('Accessories:'),TD(x.accessories or None)),
            TR(TD('Tyre:'),TD(x.tyre_size or None)),
            TR(TD('Purpose:'),TD(x.purpose.purpose)),
            TR(TD('Status:'),TD(x.status_id.status)),
            TR(TD('Remarks:'),TD(x.remarks or None)),])
    table = str(XML(i, sanitize=False))
    return table


def insur_info(x = request.args(0)):
    rows = 'No Insurance covered'
    policy = db.insured_vehicles.reg_no_id == x
    policy &= db.insurance_policy.status_id == 1
    policy &= db.insured_vehicles.policy_no_id == db.insurance_policy.id    
    for row in db(policy).select(db.insured_vehicles.ALL, db.insurance_policy.ALL):
        rows = TABLE(*[
            TR(TD('Company:'),TD(row.insurance_policy.insurance_company_id.name or None)),
            TR(TD('Policy:'),TD(row.insurance_policy.policy_no or None)),
            TR(TD('Fr.Pe.Covered:'),TD(row.insurance_policy.from_period_covered or None)),
            TR(TD('To.Pe.Covered:'),TD(row.insurance_policy.period_covered or None)),
            TR(TD('Amount:'),TD(row.insured_vehicles.amount or None)),
            TR(TD('Status:'),TD(row.insurance_policy.status_id.status or None))])
    table = str(XML(rows, sanitize=False))
    return table

def adve_info(x = request.args(0)):
    rows = 'No Advertisement issued'
    query = db.ads_vehicle.reg_no_id == x
    query &= db.ads_vehicle.license_no_id == db.advertisement.id
    for row in db(query).select(db.ads_vehicle.ALL, db.advertisement.ALL):
        rows = TABLE(*[
            TR(TD('Advertisement:'),TD(row.advertisement.ads)),
            TR(TD('Logo:'),TD(row.advertisement.logo)),
            TR(TD('License No.:'),TD(row.advertisement.license_no)),
            TR(TD('Expiration Date:'),TD(row.advertisement.expiry_date)),
            TR(TD('Amount:'),TD(row.ads_vehicle.amount))])
    table = str(XML(rows, sanitize=False))
    return table

def cont_info(x = request.args(0)):
    rows = 'No assigned fleet controller yet!'
    group_id = auth.id_group('level_2_user')
    all_users_in_group = db(db.auth_membership.group_id == group_id)._select(db.auth_membership.user_id)
    query = db.auth_user.id.belongs(all_users_in_group)
    query &= db.vehicle.id == x
    query &= db.auth_user.division_id == db.vehicle.division_id
    cnt = db(query).count()
    if cnt > 1:        
        rows = []
        for row in db(query).select(db.auth_user.ALL):
            rows.append(TR(TD('Name'),TD(B(str(row.last_name +', ' + row.first_name)))))
            rows.append(TR(TD('PO Box:'),TD(row.po_box)))
            rows.append(TR(TD('Mobile:'),TD(row.mobile_no)))
            rows.append(TR(TD('Office:'),TD(row.office_no)))
            rows.append(TR(TD('Fax:'),TD(row.fax_no)))
            rows.append(TR(TD('Email:'),TD(row.email)))
            rows.append(TR(TD('----------'),TD()))
        body = TBODY(*rows)
        table = TABLE(*[body])
        return table
    else:
        for row in db(query).select(db.auth_user.ALL):
            rows = TABLE(*[
                TR(TD('Last Name:'),TD(row.last_name)),
                TR(TD('First Name:'),TD(row.first_name)),
                TR(TD('P.O. Box:'),TD(row.po_box)),
                TR(TD('Mobile No.:'),TD(row.mobile_no)),
                TR(TD('Office No.:'),TD(row.office_no)),
                TR(TD('Fax No.:'),TD(row.fax_no)),
                TR(TD('Email:'),TD(row.email))])

        return str(XML(rows, sanitize=False))

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def ControllerDetails():
    i = ''
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), _onclick = "javascript:PrintContent()"))

    group_id = auth.id_group('level_2_user')
    all_users_in_group = db(db.auth_membership.group_id == group_id)._select(db.auth_membership.user_id)
    #query = db.auth_user.id.belongs(all_users_in_group)
    query = db.vehicle.id == request.args(0)       
    query &= db.auth_user.division_id == db.vehicle.division_id
        
    head = THEAD(TR(TH('Last Name'), TH('First Name'), TH('P.O. Box'),TH('Mobile No.'), TH('Office No'), TH('Fax No.'), TH('Email')))

    r = []
    for c in db(query).select(db.auth_user.ALL):
        r.append(TR(TD(c.last_name), TD(c.first_name), TD(c.po_box), TD(c.mobile_no),TD(c.office_no), TD(c.fax_no), TD(c.email)))
    body = TBODY(*r)
    table = TABLE(*[head, body], _border = '0', _align = 'center', _width = '100%', _class = 'table')
    return dict(i = table, img_report = img_report)

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
            TR(TH('Ads:'),TH('Logo:'),TH('License No.:'),TH('Expiration Date:'),TH('Amount Expenses:')),
            TR(TD(d.advertisement.ads),TD(d.advertisement.logo),TD(d.advertisement.license_no),TD(d.advertisement.expiry_date),
                TD(d.ads_vehicle.amount))], _class = 'table')
    return dict(i = i, ads = ads, v_ads = v_ads, img_report = img_report)

def view_rp(x = request.args(0)):
    i = ''
    for p in db(db.v_photos.id == x).select(db.v_photos.ALL):
        i = TABLE(*[TR(TD(IMG(_width='100%', _height='100%', _src=URL(r=request, c='default', f='download', args = p.road_permit))))])
    table = str(XML(i, sanitize=False))
    return table



@auth.requires_membership('level_1_user')
def VehicleProfileForm():             
    form = SQLFORM(db.vehicle)
    if form.process().accepted:
        response.flash = form_success
    elif form.errors:
        response.flash = form_error
    else: 
        response.flash = form_info
    return dict(grid = form)

@auth.requires_membership('level_1_user')
def edit_VehicleProfileForm():
    record = db.vehicle(request.args(0)) or redirect(URL('error'))         
    form = SQLFORM(db.vehicle, record, showid = False)
    form.process(detect_record_change=True)
    if form.record_changed:
        response.flash = form_warning
        db.activities.insert(log_date = request.now,person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'updated reg.no. %s company vehicle.' % request.vars.reg_no)              
    elif form.accepted:
        response.flash = form_success
        db.activities.insert(log_date = request.now,person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'updated reg.no. %s company vehicle.' % request.vars.reg_no)              
    elif form.errors:
        response.flash = form_error
    else: 
        response.flash = form_info
    return dict(form = form)


# --------------   OTHERS ---------------------- #
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Cancelled(): # --------------   CANCELLED VEHICLE'S ---------------------- # 
    row = []
    query = db(db.vehicle.status_id == 1).select(db.vehicle.ALL, db.v_photos.ALL, left=db.v_photos.on(db.vehicle.id==db.v_photos.reg_no_id))
    head = THEAD(TR(TH(_class='sorting_disabled'),TH('Reg.No.'),TH('Code'),TH('Division'),TH('Type'),TH('Category'),TH('Model'),TH('Mileage'),TH('PM'),TH('FT'),TH('RR'),TH('LF'),TH('RT'),TH(_class='sorting_disabled')))
    for n in query:
        action = DIV(BUTTON('Action',I(_class='ace-icon fa fa-angle-down icon-on-right'),_class='btn btn-primary btn-minier dropdown-toggle', 
            **{'_data-toggle':'dropdown','_aria-expanded':'false'}),
            UL(LI(A('Maintenance', _href=URL('default', 'VehicleMaintenance', args=n.vehicle.id))),
                LI(A('Fuel', _href=URL('default', 'Fuel', args=n.vehicle.id))),
                LI(A('Mileage', _href=URL('default', 'Odometer', args=n.vehicle.id))),
                LI(A('Insurance', _href=URL('default', 'VehicleInsDetail', args=n.vehicle.id))),
                LI(A('Advertisement', _href=URL('default', 'AdsDetails', args=n.vehicle.id))),
                LI(A('Photos', _href=URL('Reports', 'Photos', args=n.vehicle.id))),
                LI(A('Controller', _href=URL('default', 'ControllerDetails', args=n.vehicle.id))),
                LI(A('Print', _href="#",_onclick="pdf()")),
                LI(_class='divider'),
                LI(A('Update', _href=URL('default', 'VehicleProfileForm', args=n.vehicle.id))),
                _class='dropdown-menu dropdown-menu-right', **{'aria-labelledby':'dLabel'}),
            _class='btn-group')        
        
        row.append(TR(TD(A(SPAN(_class='fa fa-flag red bigger-130 tooltip-error', _title='', _role='button',**{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Cancelled Fleet'}))),
            TD(n.vehicle.reg_no),TD(n.vehicle.vehicle_code),TD(n.vehicle.division_id.division),TD(n.vehicle.plate_type[:10]),TD(n.vehicle.category_id.category[:10]),TD(n.vehicle.model),TD(n.vehicle.mileage),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Road Permit', _href = URL('default', 'download', args= n.v_photos.road_permit),**{'_data-rel':'colorbox'}) if n.v_photos.road_permit else "", _class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Front Side Photo', _href = URL('default', 'download', args= n.v_photos.photo),**{'_data-rel':'colorbox'}) if n.v_photos.photo else "", _class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Rear Side Photo', _href = URL('default', 'download', args= n.v_photos.photo2),**{'_data-rel':'colorbox'}) if n.v_photos.photo2 else "", _class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Left Side Photo', _href = URL('default', 'download', args= n.v_photos.photo3),**{'_data-rel':'colorbox'}) if n.v_photos.photo3 else "", _class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _class='blue',_title='Right Side Photo', _href = URL('default', 'download', args= n.v_photos.photo4),**{'_data-rel':'colorbox'}) if n.v_photos.photo4 else "", _class='ace-thumbnails clearfix'),
            TD(action)))       
    body = TBODY(*row)
    table = TABLE(*[head, body], _class="table table-striped table-bordered table-hover")
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(table = table)
    


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
    grid = SQLFORM.grid(query, user_signature = True, exportclasses = export, links = links,
        searchable = False, showbuttontext=False, details = False, create = False)
    if request.args(0) == 'edit':
        response.view = 'default/AdvertisementGrid.html'
        grid = grid.update_form
    return dict(grid = grid)



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
    users = 'none'
    db.auth_user.division_id.readable = True
    group_id = auth.id_group('level_2_user')
    #all_users_in_group = db(db.auth_membership.group_id==group_id)._select(db.auth_membership.user_id)
    #users = db(db.auth_user.id.belongs(all_users_in_group)).select()



    all_users_in_group = db(db.auth_membership.group_id == group_id)._select(db.auth_membership.user_id)
    query = db.auth_user.id.belongs(all_users_in_group)
    query &= db.auth_user.division_id == 13
    users = db(query).select()


    #all_users_in_group = db(query)._select(db.auth_membership.user_id)
    #query = db(db.auth_user.id.belongs(all_users_in_group)).select()
    #query = db(query).select(db.auth_user.ALL)
    return dict(query = users)

links = [
lambda row: A(SPAN(_class = 'icon icon-wrench'), _title="Repair & Maintenance", _href=URL("default","VehicleMaintenance", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-filter'), _title="Fuel Expenses", _href=URL("default","FuelExpenses", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-road'), _title="Monthly Mileage", _href=URL("default","Odometer", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-file'), _title='Insurance Detail', _target='_blank',_href=URL("default","VehicleInsDetail", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-star'),  _title='Advertisement', _target='_blank' ,_href=URL("default","AdsDetails", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-camera'), _title="Photos", _target='_blank', _href=URL("Reports","Photos", args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-user'), _title='Controller', _target='_blank',_href=URL('default', 'ControllerDetails', args = row.id)),
lambda row: A(SPAN(_class = 'icon icon-print'), _title="Print", _target="_blank", _href=URL("Reports","VehicleProfileReport", args = row.id))
]   

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Controller():
    #view = A(SPAN(_class = 'fa fa-search bigger-110 blue'), _tabindex='0', _role='button', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Maintenance Info','_data-content': main_info(n.id)})
    #prin = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print", 
    #_href=URL("MaintenanceReports","MaintenanceReport", args=n.id))
    
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank", _src=URL('static','images/printButton.png'), _onclick = "javascript:PrintContent()"))    
    extracolumns = [{'label':'',
                    'class': 'sorting_disabled', #class name of the header
                    'width':'', #width in pixels or %
                    'content':lambda row, rc: A(SPAN(_class='fa fa-print bigger-110 blue'), _href='edit/%s'%row.id),
                    #'content': links ,

                    'selected': False #agregate class selected to this column
                    }]
    
    headers = {'auth_user.id':'#','auth_user.first_name':'First Name',
    'auth_user.last_name':'Last Name',
    'auth_user.division_id':'Division',
    'auth_user.email':'Email',
    'auth_user.mobile_no':'Mobile No.',
    'auth_user.office_no':'Office No.'}
  
    rows = db(db.auth_user.id != 6).select(db.auth_user.id, db.auth_user.first_name, db.auth_user.last_name,
        db.auth_user.division_id,  db.auth_user.email,
        db.auth_user.mobile_no, db.auth_user.office_no,
        orderby = ~db.auth_user.division_id)
    table = SQLTABLE(rows, headers=headers, extracolumns = extracolumns, _width = '100%', _class = 'table table-striped table-bordered table-hover')
    
    '''    
    row = []
    head = THEAD(TR(TH('#'),TH('First Name'),TH('Last Name'),TH('Division'),TH('Email'),TH('Mobile No.'),TH('Office No.')))
    for c in db(db.auth_user.id != 6).select(db.auth_user.ALL):
        row.append(TR(TD(),TD(c.last_name.upper()),TD(c.first_name.upper()),TD(c.division_id),TD(c.email),TD(c.mobile_no),TD(c.office_no)))
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table table-striped table-bordered table-hover')
    '''
    return dict(table = table)
    




# -----------  COMPANY/DIVISION VEHICLE CRUD END HERE.   ------------- #    

# -----------  ADVERTISEMENT VEHICLE CRUD START HERE.   ------------- #    

@auth.requires_membership('level_1_user')
def AdvertisementForm():
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Kindly fill the form', _class='white'),_class='alert alert-info') 
    return dict()

@auth.requires_membership('level_1_user')
def AdvertisementForm_():
    form_ads = SQLFORM(db.advertisement, request.args(0))
    if form_ads.process().accepted:
        db.activities.insert(log_date = request.now,person = '%s %s' % (auth.user.first_name, auth.user.last_name),action = 'created advertisement vehicle with license no. %s' % (request.vars.license_no))
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Advertisement record save.', _class='white'),_class='alert alert-success') 
    elif form_ads.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
    else: 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Kindly fill the form', _class='white'),_class='alert alert-info') 
    return dict(form_ads = form_ads)

@auth.requires_membership('level_1_user')
def edit_AdvertisementForm():
    record = db.advertisement(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.advertisement, record, showid = False)
    form.process(detect_record_change = True)
    if form.record_changed:
        response.flash = form_warning
    elif form.accepted:
        response.flash = form_success
        db.activities.insert(log_date = request.now,person = '%s %s' % (auth.user.first_name, auth.user.last_name),action = 'updated advertisement vehicle with license no. %s' % (request.vars.license_no))       
    elif form.errors:
        response.flash = form_error
    else: 
        response.flash = form_info
    return dict(form = form)

@auth.requires_membership('level_1_user')
def edit_FleetAds():
    record = db.ads_vehicle(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.ads_vehicle, record, showid = False)
    form.process(detect_record_change = True)
    if form.record_changed:
        response.flash = form_warning
    elif form.accepted:
        response.flash = form_success
        db.activities.insert(log_date = request.now,person = '%s %s' % (auth.user.first_name, auth.user.last_name),action = 'updated reg.no.  %s fleet advertisement.' % (request.vars.reg_no_id))       
    elif form.errors:
        response.flash = form_error
    else: 
        response.flash = form_info
    return dict(form = form)


@auth.requires_membership('level_1_user')
def AdsVehiclesForm_():
    db.ads_vehicle.id.readable = False
    form_fle = SQLFORM(db.ads_vehicle, request.args(0))
    if form_fle.process(onvalidation = ads_vehicle_process).accepted:
        record = db(form_fle.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        licens = db(form_fle.vars.license_no_id == db.advertisement.id).select(db.advertisement.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'created reg.no. %s vehicle ads with license no. %s' %(record.reg_no, licens.license_no))
        response.flash = form_success
    elif form_fle.errors:
        response.flash = form_error
    else:
        response.flash = form_info
    return dict(form_fle = form_fle)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Advertisement():
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict()

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def ActiveAdvertisement():
    active_query = db(db.advertisement.status_id == 1).select(db.advertisement.ALL)
    head = THEAD(TR(TH('#'),TH('Ads'),TH('Logo'),TH('License No'),TH('Fr.Exp.Date'),TH('To.Exp.Date'),TH('Amount'),TH('Status'),TH(_class='sorting_disabled')))
    row = []
    for a in active_query:
        '''
        a_prin = A(SPAN(_class='glyphicon glyphicon-print'),_title='Print',_href=URL('default','AdvertisementForm',args=a.id),_class='btn btn-default btn-sm')
        a_edit = A(SPAN(_class='glyphicon glyphicon-pencil'),_title='Edit',_href=URL('default','AdvertisementForm',args=a.id),_class='btn btn-default btn-sm')
        a_list = A(SPAN(_class='glyphicon glyphicon-road'), callback=URL('AdsVehicles',args=a.id), **{'_title':'View List','_class':'btn btn-default btn-sm',
        '_role':'button','_data-toggle':'collapse','_data-target':'#collapseExample' , '_aria-expanded':'false', '_aria-controls':'collapseExample'})
        a_dele = A(SPAN(_class='glyphicon glyphicon-trash'),_title='Delete',_href=URL('default','AdvertisementForm',args=a.id),_class='btn btn-default btn-sm')
        '''
        pr_v = A(I(_class = 'fa fa-print bigger-130 blue'), _title="Print", _target='blank', _href=URL("Reports","AdvertisementReport", args=a.id, extension = False))
        in_v = A(I(_class = 'fa fa-car bigger-130 blue'), _title='Vehicles', _href=URL('default','AdsVehicles', args = a.id, extension = False))
        edit = A(I(_class = 'fa fa-pencil bigger-130 blue'), _title="Edit", _href=URL('default','edit_AdvertisementForm', args = a.id, extension = False))
        btn_lnks = DIV(pr_v, in_v, edit, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(a.ads),TD(a.logo),TD(a.license_no),TD(a.from_expiry_date),TD(a.expiry_date),TD(locale.format('%.2F',a.amount, grouping=True)),TD(a.status_id.status),TD(btn_lnks)))
    body = TBODY(*row)
    active_table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    return dict(active_table = active_table)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def NonActiveAdvertisement():
    head = THEAD(TR(TH('#'),TH('Ads'),TH('Logo'),TH('License No'),TH('Fr.Exp.Date'),TH('To.Exp.Date'),TH('Amount'),TH('Status'),TH(_class='sorting_disabled')))
    non_active_query = db(db.advertisement.status_id == 2).select(db.advertisement.ALL)
    n_row = []
    for a in non_active_query:
        pr_v = A(I(_class = 'fa fa-print bigger-130 blue'), _title="Print", _target='blank', _href=URL("Reports","AdvertisementReport", args=a.id, extension = False))
        in_v = A(I(_class = 'fa fa-car bigger-130 blue'), _title='Vehicles', _href=URL('default','AdsVehicles', args = a.id, extension = False))
        edit = A(I(_class = 'fa fa-pencil bigger-130 blue'), _title="Edit", _href=URL('default','edit_AdvertisementForm', args = a.id, extension = False))
        btn_lnks = DIV(pr_v, in_v, edit, _class="hidden-sm hidden-xs action-buttons")
        n_row.append(TR(TD(),TD(a.ads),TD(a.logo),TD(a.license_no),TD(a.from_expiry_date),TD(a.expiry_date),TD(locale.format('%.2F',a.amount, grouping=True)),TD(a.status_id.status),TD(btn_lnks)))
    non_active_body = TBODY(*n_row)
    non_active_table = TABLE(*[head, non_active_body], _class='table table-striped table-bordered table-hover', _width='100%')    
    return dict(non_active_table=non_active_table)    
    '''
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
    '''

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def WithoutAdvertisement():
    wo_head = THEAD(TR(TH('#'),TH('Company'),TH('Division'),TH('Deparment'),TH('Reg.No.'),TH('Brand'),TH('Chassis No.'),TH('Last Reading'),TH('Model')))
    wo_row = []
    wo_ads = db.vehicle.id == db.ads_vehicle.reg_no_id
    #wo_ads &= db.advertisement.status_id != 1
    wo_query = db(~(db.vehicle.id.belongs(wo_ads))).select(db.vehicle.ALL)
    for w in wo_query:
        wo_row.append(TR(TD(),TD(w.company_id.company),TD(w.division_id.division),TD(w.department.name),TD(w.reg_no),TD(w.vehicle_name_id.vehicle_name),TD(w.chassis_no),TD(locale.format('%d',w.mileage or 0, grouping=True)),TD(w.model)))
    wo_table_body = TBODY(*wo_row)
    wo_table = TABLE(*[wo_head, wo_table_body],_class='table table-hover table-striped table-bordered table-condensed', _width='100%')
    return dict(wo_table = wo_table)
    '''    
    head = THEAD(TR(TH('Company', _colspan = '8')))
    wo_ads = db.vehicle.id == db.ads_vehicle.reg_no_id
    query = db(~(db.vehicle.id.belongs(wo_ads))).select(db.vehicle.ALL, groupby = db.vehicle.ALL)
    row = []
    for c in db(~(db.vehicle.id.belongs(wo_ads))).select(db.vehicle.company_id, groupby = db.vehicle.company_id):
        row.append(TR(TD(c.company_id.company), TH('Division', _colspan = '7')))
        for d in db(db.vehicle.company_id == c.company_id).select(db.vehicle.division_id, groupby = db.vehicle.division_id):
            row.append(TR(TD(),TD(d.division_id.division), TH('Department', _colspan = '7')))
            for p in db(db.vehicle.division_id == d.division_id).select(db.vehicle.department, groupby = db.vehicle.department):
                row.append(TR(TD(),TD(),TD(p.department.name), TH('Reg.No.'), TH('Brand'), TH('Chassis No.'), TH('Last Reading'), 
                    TH('Model')))
                for r in db(~(db.vehicle.id.belongs(wo_ads))&(db.vehicle.department == p.department)).select(db.vehicle.reg_no, db.vehicle.vehicle_name_id, 
                    db.vehicle.model, db.vehicle.chassis_no,  db.vehicle.mileage,
                    groupby = db.vehicle.reg_no | db.vehicle.model | db.vehicle.chassis_no | db.vehicle.mileage | db.vehicle.vehicle_name_id):
                    row.append(TR(TD(), TD(),TD(),TD(r.reg_no),TD(r.vehicle_name_id.vehicle_name), TD(r.chassis_no), 
                        TD(str(locale.format('%d', r.mileage or 0, grouping = True)) + ' km.'), TD(r.model)))
    body = TBODY(*row) 
    table = TABLE(*[head, body],_class = 'table')
    return dict(table = table)
    '''
def ads_vehicle_process(form):
    value = db.ads_vehicle.license_no_id == request.vars.license_no_id
    value &= db.ads_vehicle.reg_no_id == request.vars.reg_no_id
    record = db(value).select(db.ads_vehicle.ALL).first()
    if record:
        form.errors.license_no_id = 'already exist!'
        form.errors.reg_no_id = 'already exist!'
        #print 'already exist'
    else:
        response.flash = form_success


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def AdsVehicles():
    row = []
    head = THEAD(TR(TH('#'),TH('Reg.No.'),TH('Amount'),TH(_class='sorting_disabled')))
    for v in db(db.ads_vehicle.license_no_id == request.args(0)).select(db.ads_vehicle.ALL):#callback=URL( args=v.id)
        pr_v = A(SPAN(_class = 'fa fa-print bigger-130 blue'), _title="Print", _target='blank', _href=URL("Reports","FleetAdvertisementReport", args=v.id, extension = False))
        edit = A(SPAN(_class = 'fa fa-pencil bigger-130 blue'), _title="Edit", _href=URL('default','edit_FleetAds', args = v.id, extension = False))
        dele = A(SPAN(_class = 'fa fa-trash bigger-130 blue'), _name='btndel',_title="Delete", callback=URL( args=v.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(v.id)})
        btn_lnks = DIV(pr_v, edit, dele, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(v.reg_no_id.reg_no),TD(locale.format('%.2F',v.amount or 0, grouping = True),TD(btn_lnks))))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered')
    response.flash = form_info
    return dict(table = table)

def del_ads_fleet():   
    rep = db(db.ads_vehicle.id == request.args(1)).select(db.ads_vehicle.ALL).first()
    fle = db(db.vehicle.id == rep.reg_no_id).select(db.vehicle.ALL).first()
    vehi_a = db(db.advertisement.id == rep.license_no_id).select(db.advertisement.ALL).first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted reg.no. %s vehicle ads with license no. %s' % (fle.reg_no, vehi_a.license_no))    
    db(db.ads_vehicle.id == request.args(1)).delete()
    


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Advertisement_():
    '''
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
    '''

    active_query = db(db.advertisement.status_id == 1).select(db.advertisement.ALL)
    head = THEAD(TR(TH('#'),TH('Ads'),TH('Logo'),TH('License No'),TH('Fr.Exp.Date'),TH('To.Exp.Date'),TH('Amount'),TH('Status'),TH()))
    row = []
    for a in active_query:
        a_prin = A(SPAN(_class='glyphicon glyphicon-print'),_title='Print',_href=URL('default','AdvertisementForm',args=a.id),_class='btn btn-default btn-sm')
        a_edit = A(SPAN(_class='glyphicon glyphicon-pencil'),_title='Edit',_href=URL('default','AdvertisementForm',args=a.id),_class='btn btn-default btn-sm')
        #lambda row: A(SPAN(_class = 'icon icon-file'), **{'_title':'Insurance Detail', '_data-target':'#InsDetails', '_data-toggle':'modal', '_href':URL("default","VehicleInsDetail", args = row.id)}),
        #<a class="btn btn-primary" role="button" data-toggle="collapse" href="#collapseExample" aria-expanded="false" aria-controls="collapseExample">  Link with href</a>
        #callback=URL('add_item', vars=dict(id=row.id, action='add'))),
        a_list = A(SPAN(_class='glyphicon glyphicon-road'), callback=URL('AdsVehicles',args=a.id), **{'_title':'View List','_class':'btn btn-default btn-sm',
        '_role':'button','_data-toggle':'collapse','_data-target':'#collapseExample' , '_aria-expanded':'false', '_aria-controls':'collapseExample'})
        a_dele = A(SPAN(_class='glyphicon glyphicon-trash'),_title='Delete',_href=URL('default','AdvertisementForm',args=a.id),_class='btn btn-default btn-sm')
        row.append(TR(TD(),TD(a.ads),TD(a.logo),TD(a.license_no),TD(a.from_expiry_date),TD(a.expiry_date),
            TD(locale.format('%.2F',a.amount, grouping=True)),TD(a.status_id.status),TD(a_edit,' ',a_list,' ',a_dele)))
    body = TBODY(*row)
    active_table = TABLE(*[head, body], _class='table table-hover table-striped table-bordered table-condensed', _width='100%')


    non_active_query = db(db.advertisement.status_id == 2).select(db.advertisement.ALL)
    n_row = []
    for a in non_active_query:
        n_row.append(TR(TD(),TD(a.ads),TD(a.logo),TD(a.license_no),TD(a.from_expiry_date),TD(a.expiry_date),TD(locale.format('%.2F',a.amount,grouping=True)),TD(a.status_id.status),TD()))
    non_active_body = TBODY(*n_row)
    non_active_table = TABLE(*[head, non_active_body], _class='table table-hover table-striped table-bordered table-condensed', _width='100%')    

    wo_head = THEAD(TR(TH('#'),TH('Company'),TH('Division'),TH('Deparment'),TH('Reg.No.'),TH('Brand'),TH('Chassis No.'),TH('Last Reading'),TH('Model')))
    wo_row = []
    wo_ads = db.vehicle.id == db.ads_vehicle.reg_no_id
    #wo_ads &= db.advertisement.status_id != 1
    wo_query = db(~(db.vehicle.id.belongs(wo_ads))).select(db.vehicle.ALL)
    for w in wo_query:
        #row.append(TR(TD(),TD(),TD(),TD(r.reg_no),TD(r.vehicle_name_id.vehicle_name),TD(r.chassis_no),TD(str(locale.format('%d', r.mileage or 0, grouping = True)) + ' km.'), TD(r.model)))
        wo_row.append(TR(TD(),TD(w.company_id.company),TD(w.division_id.division),TD(w.department.name),TD(w.reg_no),TD(w.vehicle_name_id.vehicle_name),TD(w.chassis_no),TD(locale.format('%d',w.mileage or 0, grouping=True)),TD(w.model)))
    wo_table_body = TBODY(*wo_row)
    wo_table = TABLE(*[wo_head, wo_table_body],_class='table table-hover table-striped table-bordered table-condensed', _width='100%')

    
    ads_head = THEAD(TR(TH('#'),TH('Reg.No.'),TH('Amount')))
    ads_row = []
    ads_query = db(db.ads_vehicle.license_no_id == request.vars.id).select(db.ads_vehicle.ALL)
    for v in ads_query:
        ads_row.append(TR(TD(),TD(v.reg_no_id.reg_no),TD(v.amount)))
    ads_table_body = TBODY(*ads_row)
    ads_table = TABLE(*[ads_head, ads_table_body], _class='table', _width='100%')

    #response.js =  "jQuery('#collapseExample').get(0).reload();"
    #return dict(active_table=active_table,non_active_table=non_active_table,wo_table=wo_table, ads_table=ads_table)    
    return locals()    
# -----------  ADVERTISEMENT VEHICLE CRUD END HERE.   ------------- #    


# -----------  COMPANY/DIVISION VEHICLE CRUD EXPENDITURES STARTS HERE.   ------------- #

@auth.requires_membership('level_1_user')
def ExpensesForm():
    db.km_used.consumed_mil.readable = False
    main_form = SQLFORM(db.repair_history, request.args(0))
    if main_form.process().accepted:
        record = db(db.vehicle.id == main_form.vars.reg_no_id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'created maintenance expenses with invoice number %s' % (main_form.vars.invoice_number))
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Maintenance expenses record save.', _class='white'),_class='alert alert-success')    
    elif main_form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
    else: 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 

    fuel_form = SQLFORM(db.fuel_expenses, request.args(0))
    if fuel_form.process().accepted:
        record = db(db.vehicle.id == fuel_form.vars.reg_no_id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'created reg.no. %s fuel expenses amounted QR %s' % (record.reg_no, str(locale.format('%.2f', fuel_form.vars.amount, grouping = True))))
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Fuel expenses record save.', _class='white'),_class='alert alert-success')    
    elif fuel_form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
    else: 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 

    odom_form = SQLFORM(db.km_used, request.args(0))
    if odom_form.process().accepted:
        record = db(db.vehicle.id == odom_form.vars.reg_no_id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'created reg.no. %s odometer for the month of %s' % (record.reg_no, str((request.now).strftime('%B %Y'))))
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Odometer record save.', _class='white'),_class='alert alert-success')    
    elif odom_form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
    else: 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(main_form=main_form, fuel_form=fuel_form, odom_form=odom_form)    

@auth.requires_membership('level_1_user')
def MaintenanceExpensesForm():
    form = SQLFORM(db.repair_history)
    if form.process().accepted:    
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'created reg.no. %s maintenance expenses with invoice number %s' % (record.reg_no, form.vars.invoice_number))    
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Maintenance expenses record save.', _class='white'),_class='alert alert-success')    
    elif form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
    else: 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(form = form)   


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def VehicleMaintenance():     
    row =[]
    query = db(db.repair_history.reg_no_id == request.args(0)).select(db.repair_history.ALL, orderby = ~db.repair_history.invoice_date)
    head = THEAD(TR(TH('#'),TH('Date'),TH('Invoice'),TH('Reg.No.'),TH('Workshop'),TH('Duration'),TH('Mileage'),TH('Amount'),TH(_class='sorting_disabled')))
    for n in query:
        view = A(SPAN(_class = 'fa fa-search bigger-110 blue'), _tabindex='0', _role='button', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Maintenance Info','_data-content': main_info(n.id)})
        prin = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print", _href=URL("MaintenanceReports","MaintenanceReport", args=n.id))
        edit = A(SPAN(_class = 'fa fa-pencil bigger-110 blue'), _title="Edit", _href=URL("default","EditMaintenanceExpensesForm", args=n.id ))
        dele = A(SPAN(_class = 'fa fa-trash bigger-110 blue'), _name='btndel',_title="Delete", callback=URL( args=n.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(n.id), '_data-in':(n.invoice_number)})
        btn_lnks = DIV(view, prin, edit, dele, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(n.invoice_date),TD(n.invoice_number),TD(n.reg_no_id.reg_no),TD(n.workshop_done.workshop),TD(n.no_days_time),TD(locale.format('%d',n.mileage or 0, grouping = True)),TD(locale.format('%.2f',n.total_amount or 0, grouping = True),_style = 'text-align: right'),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(table = table)

@auth.requires_membership('level_1_user')
def EditMaintenanceExpensesForm():
    form = SQLFORM(db.repair_history, request.args(0),deletable=True, showid=False, delete_label='Check to delete')
    if form.process().accepted:    
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'updated reg.no. %s maintenance expenses with invoice number %s' % (record.reg_no, form.vars.invoice_number))    
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Maintenance expenses record save.', _class='white'),_class='alert alert-success')    
    elif form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
    else: 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(form = form)   


def main_delete():
    rep = db(db.repair_history.id == request.args(1)).select(db.repair_history.ALL).first()
    fle = db(db.vehicle.id == rep.reg_no_id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'deleted reg.no. %s maintenance expenses with invoice number %s' % (fle.reg_no, rep.invoice_number))    
    db(db.repair_history.id == request.args(1)).delete()

def fuel_delete():
    ful = db(db.fuel_expenses.id == request.args(1)).select(db.fuel_expenses.ALL).first()
    fle = db(db.vehicle.id == ful.reg_no_id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'deleted reg.no. %s fuel expenses dated %s' % (fle.reg_no, ful.date_expense))    
    db(db.fuel_expenses.id == request.args(1)).delete()

def odom_delete():
    odo = db(db.km_used.id == request.args(1)).select(db.km_used.ALL).first()
    fle = db(db.vehicle.id == odo.reg_no_id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'deleted reg.no. %s odometer dated %s' % (fle.reg_no, odo.given_month))    
    db(db.km_used.id == request.args(1)).delete()        

def main_info(z = request.args(0)):
    for x in db(db.repair_history.id == z).select():
        i = TABLE(*[
            TR(TD('Start Date: '),TD(x.date_time_in, _style = 'text-align: right' )),
            TR(TD('End Date: '),TD(x.date_time_out, _style = 'text-align: right')), 
            #TR(TD('Duration: '),TD(T('%s %%{day}',abs(x.date_time_out - x.date_time_in).days), _style = 'text-align: right')),
            TR(TD('Duration: '),TD(x.no_days_time), _style = 'text-align: right'),
            TR(TD('LAB: '),TD(locale.format('%.2F',x.regular_maintenance or 0, grouping = True), _style = 'text-align: right')),
            TR(TD('SP: '),TD(locale.format('%.2F', x.spare_parts or 0, grouping = True), _style = 'text-align: right')),
            TR(TD('SE:'),TD(locale.format('%.2F', x.statutory_expenses or 0, grouping = True ), _style = 'text-align: right')),
            TR(TD('AR:'),TD(locale.format('%.2F',x.accident_repair or 0, grouping = True), _style = 'text-align: right')),
            TR(TD('Amount:'),TD(locale.format('%.2F',x.total_amount or 0, grouping = True), _style = 'text-align: right')),
            TR(TD('Details:'),TD(x.details, _style = 'text-align: right'))])
    table = str(XML(i, sanitize=False))
    return table

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Fuel():   
    row =[]
    query = db(db.fuel_expenses.reg_no_id == request.args(0)).select(db.fuel_expenses.ALL, orderby = ~db.fuel_expenses.date_expense)
    head = THEAD(TR(TH('#'),TH('Date'),TH('Reg.No.'),TH('Amount'),TH('Paid By'),TH('Station'),TH('Remarks'),TH(_class='sorting_disabled')))
    for n in query:
        view = A(SPAN(_class = 'fa fa-search bigger-110 blue'), _tabindex='0', _role='button', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Fuel Info','_data-content': fuel_info(n.id)})
        prin = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print", _href=URL("FuelReports","FuelReport", args=n.id))
        edit = A(SPAN(_class = 'fa fa-pencil bigger-110 blue'), _title="Edit", _href=URL("default","EditFuelExpensesForm", args=n.id ))
        dele = A(SPAN(_class = 'fa fa-trash bigger-110 blue'), _name='btndel',_title="Delete", callback=URL( args=n.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(n.id)})
        btn_lnks = DIV(view, prin, edit, dele, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(n.date_expense),TD(n.reg_no_id.reg_no),TD(locale.format('%.2F', n.amount or 0, grouping = True)),TD(n.paid_by),TD(n.station),TD(n.remarks),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(table = table)

def fuel_info(z = request.args(0)):
    for x in db(db.fuel_expenses.id == z).select():
        i = TABLE(*[
            TR(TD('Date: '),TD(x.date_expense, _style = 'text-align: right' )),
            TR(TD('Amount:'),TD(locale.format('%.2F',x.amount or 0, grouping = True), _style = 'text-align: right')),
            TR(TD('Paid By: '),TD(x.paid_by, _style = 'text-align: right')), 
            TR(TD('Station: '),TD(x.station, _style = 'text-align: right')),             
            TR(TD('Remarks:'),TD(x.remarks, _style = 'text-align: right'))])
    table = str(XML(i, sanitize=False))
    return table


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def FuelExpensesBatchForm():   
    form = FORM(DIV(LABEL('Paid By: ',_class='col-sm-2'),SELECT('Cash','Credit','Fuel Card', _type='text', _id='paid_by', _name='paid_by',_placeholder='Paid By' ,_class='col-sx-10')),
        DIV(_class='space space-8'),
        DIV(LABEL('Station: ',_class='col-sm-2'),INPUT(_type='text', _id='station',_name='station', _placeholder='Station')),DIV(_class='space space-8'),
        TABLE(THEAD(TR(TH('#'),TH('Date'),TH('Reg.No.'),TH('Amount'),TH('Remarks'),TH())),
        TBODY(TR(TD(SPAN(_id='sheepItForm_label')),
            TD(INPUT(_class='date col-xs-10 col-sm-10', _value=request.now.date(), _id='date_expense', _name="date_expense")),
            TD(SELECT(_class='col-xs-10 col-sm-10', _id='reg_no_id', _name='reg_no_id', *[OPTION(r.reg_no, _value=r.id) for r in db().select(db.vehicle.ALL, orderby=db.vehicle.reg_no)])),
            TD(INPUT(_class='col-xs-10 col-sm-10', _id='amount', _value=0, _name='amount')),
            TD(INPUT(_class='col-xs-10 col-sm-15', _id='remarks',_type='text', _name='remarks')),
            TD(INPUT(_id='counter',_type='hidden', _name='counter')),
            TD(A(SPAN(_class='ace-icon fa fa-times-circle bigger-120 '),_class='btn btn-danger btn-xs', _id='sheepItForm_remove_current', _name = 'sheepItForm_remove_current')),_id="sheepItForm_template"),TR(TD('No Entry Field',_colspan='6'),_id="sheepItForm_noforms_template"),_id="sheepItForm"),
        TFOOT(TR(TD(DIV(
            DIV(A(SPAN(' Add',_class='ace-icon fa fa-plus-circle bigger-120'),_class='btn btn-success btn-xs'), _id='sheepItForm_add'),
            DIV(A(SPAN(' Remove',_class='ace-icon fa fa-minus-circle bigger-120'),_class='btn btn-danger btn-xs'),_id='sheepItForm_remove_last'),
            DIV(A(SPAN(' Remove All', _class='ace-icon fa fa-times-circle bigger-120'),_class='btn btn-danger btn-xs'),_id='sheepItForm_remove_all'),_id='sheepItForm_controls'),_colspan='6'))),_class='table table-striped'),
    DIV(_class='space space-8'),
    INPUT(_type='submit', _value='submit', _class='btn btn-primary'))
    if form.process().accepted:
        #print ' - '
        _range = xrange(len(request.vars['counter']))
        #print _range
        if len(_range) <= 1:
            #print form.vars.reg_no_id
            #response.flash = 'success'
            rec_id = db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL).first()
            db.fuel_expenses.insert(reg_no_id = form.vars.reg_no_id,
                date_expense = form.vars.date_expense,
                amount = form.vars.amount,
                paid_by = form.vars.paid_by,
                station = form.vars.station,
                remarks = form.vars.remarks)
            
            db.activities.insert(log_date = request.now,
                person = '%s %s' % (auth.user.first_name, auth.user.last_name),
                action = 'created reg.no. %s fuel expenses amounted QR %s' % (rec_id.reg_no, form.vars.amount))   
            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'New fuel expenses record save.', _class='white'),_class='alert alert-success')     
        else:
            for v in _range:
                rec_ids = db(db.vehicle.id == form.vars['reg_no_id'][v]).select(db.vehicle.ALL).first()
                db.fuel_expenses.insert(reg_no_id = form.vars['reg_no_id'][v],
                    date_expense = form.vars['date_expense'][v],
                    amount = form.vars['amount'][v],
                    paid_by = form.vars.paid_by,
                    station = form.vars.station,
                    remarks = form.vars['remarks'][v])
                
                db.activities.insert(log_date = request.now,
                    person = '%s %s' % (auth.user.first_name, auth.user.last_name),
                    action = 'created reg.no. %s fuel expenses amounted QR %s' % (rec_ids.reg_no, form.vars['amount'][v]))       
                response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'New fuel expenses record save.', _class='white'),_class='alert alert-success') 
    elif form.errors.clear():
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(form = form)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def FuelExpensesOneForm():   
    form = SQLFORM(db.fuel_expenses)
    if form.process().accepted:  
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = 'created reg.no. %s fuel expenses amounted QR %s' % (record.reg_no, form.vars.amount ))       
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'New fuel expenses record save.', _class='white'),_class='alert alert-success') 
    elif form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger')         
    else:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(form=form)
  
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def EditFuelExpensesForm():   
    form = SQLFORM(db.fuel_expenses, request.args(0),deletable=True, showid=False, delete_label='Check to delete')
    if form.process().accepted:  
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'updated reg.no. %s fuel expenses amounted QR %s' % (record.reg_no, form.vars.amount ))       
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'New fuel expenses record save.', _class='white'),_class='alert alert-success') 
    elif form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger')         
    else:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(form=form)
# -----------  COMPANY/DIVISION VEHICLE CRUD EXPENDITURES END HERE.      ------------- #

# -----------  COMPANY/DIVISION VEHICLE CRUD ODOMETER STARTS HERE.      ------------- #          
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Odometer():   
    row = []
    query = db(db.km_used.reg_no_id == request.args(0)).select(db.km_used.ALL, orderby = ~db.km_used.given_month)
    head = THEAD(TR(TH('#'),TH('Month'),TH('Reg.No.'),TH('Odometer'),TH('Difference'),TH(_class='sorting_disabled')))
    for n in query:
        view = A(SPAN(_class = 'fa fa-search bigger-110 blue'), _tabindex='0', _role='button', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Odometer Info','_data-content': odo_info(n.id)})
        prin = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _title="Print",_target='blank', _href=URL("Mileage","VehicleMileageReport", args=n.id))
        edit = A(SPAN(_class = 'fa fa-pencil bigger-110 blue'), _title="Edit", _href=URL("default","EditOdometerForm", args=n.id ))
        dele = A(SPAN(_class = 'fa fa-trash bigger-110 blue'), _name='btndel',_title="Delete", callback=URL( args=n.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(n.id)})
        btn_lnks = DIV(view, prin, edit, dele, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(n.given_month.strftime('%Y - %B')),TD(n.reg_no_id.reg_no),TD(locale.format('%d', n.current_mil or 0, grouping = True)),
            TD(locale.format('%d',n.consumed_mil or 0, grouping = True)),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(table = table)

def odo_info(z = request.args(0)):
    for x in db(db.km_used.id == z).select():
        i = TABLE(*[
            TR(TD('Month: '),TD(x.given_month.strftime('%Y - %B'), _style = 'text-align: right' )),
            TR(TD('Reg.No.: '),TD(x.reg_no_id.reg_no, _style = 'text-align: right' )), 
            TR(TD('Odometer:'),TD(locale.format('%d',x.current_mil or 0, grouping = True), _style = 'text-align: right')),
            TR(TD('Difference: '),TD(locale.format('%d',x.consumed_mil or 0, grouping = True), _style = 'text-align: right'))])
    table = str(XML(i, sanitize=False))
    return table
  


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
    db.km_used.consumed_mil.readable = False
    form = SQLFORM(db.km_used)
    if form.process().accepted:
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        record.update_record(mileage = form.vars.current_mil)
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name), 
            action = 'created reg.no. %s odometer for the month of %s' % (record.reg_no, str((request.now).strftime('%B %Y'))))
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'New Odometer record save.', _class='white'),_class='alert alert-success') 
    elif form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
    else: 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 

    rows = db(db.km_used.reg_no_id == form.vars.reg_no_id).select(orderby = db.km_used.given_month)
    r = 1
    row = len(rows)
    while (r < row):
        rows[r].update_record(consumed_mil = rows[r].current_mil - rows[r-1].current_mil)
        r +=1              
    return dict(form = form)
@auth.requires_membership('level_1_user')
def EditOdometerForm():
    db.km_used.consumed_mil.readable = False
    form = SQLFORM(db.km_used, request.args(0), deletable=True, showid=False, delete_label='Check to delete')
    if form.process().accepted:
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'created reg.no. %s odometer for the month of %s' % (record.reg_no, str((request.now).strftime('%B %Y'))))
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'New Odometer record save.', _class='white'),_class='alert alert-success') 
    elif form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
    else: 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 

    rows = db(db.km_used.reg_no_id == form.vars.reg_no_id).select(orderby = db.km_used.given_month)
    r = 1
    row = len(rows)
    while (r < row):
        rows[r].update_record(consumed_mil = rows[r].current_mil - rows[r-1].current_mil)
        r +=1              
    return dict(form = form)

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

# -----------  COMPANY/DIVISION VEHICLE CRUD ODOMETER ENDS HERE.        ------------- #                
# -----------  EXPIRATION NOTIFICATION STARTS HERE.        ------------- #                

def ExpirationNotification():
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return locals()

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def RoadPermitNotification():
    today = datetime.date.today()
    rows = db(db.vehicle).select(orderby = db.vehicle.exp_date)
    r = 0
    row = len(rows)
    while (r < row):
        rows[r].update_record(datetoalert = rows[r].exp_date - datetime.timedelta(days = 7))
        r += 1
    query = db.vehicle.datetoalert <= today
    query |= db.vehicle.exp_date <= today

    head = THEAD(TR(TH('#'),TH('Company'),TH('Code'),TH('Reg.No.'),TH('Brand'),TH('Model'),TH('RPEx Date'),TH('Purpose'),TH(_class='sorting_disabled')))
    v = []
    for r in db(query).select(db.vehicle.ALL, orderby = db.vehicle.exp_date):      
        edit = A(SPAN(_class = 'fa fa-pencil bigger-130'), _title="Update", _href=URL("default","edit_VehicleProfileForm", args=r.id,  extension=False), _class="blue")
        prin = A(SPAN(_class = 'fa fa-print bigger-130'), _title="Print",_target='blank', _href=URL("Reports","VehicleProfileReport", args=r.id,  extension=False), _class="blue")        
        btn_lnks = DIV(prin, edit, _class="hidden-sm hidden-xs action-buttons")
        v.append(TR(TD(),TD(r.company_id.company),TD(r.vehicle_code),TD(r.reg_no),TD(r.vehicle_name_id.vehicle_name),TD(r.model),TD(r.exp_date),TD(r.purpose.purpose),TD(btn_lnks)))    
    body = TBODY(*v)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def InsPolicyNotification():
    today = datetime.date.today()
    rows = db(db.insurance_policy).select(orderby = db.insurance_policy.period_covered)
    r = 0
    row = len(rows)
    while (r < row):
        rows[r].update_record(datetoalert = rows[r].period_covered - datetime.timedelta(days = 45))
        r += 1
    query = db.insurance_policy.status_id == 1
    query &= db.insurance_policy.datetoalert <= today
    head = THEAD(TR(TH('#'),TH('Company'),TH('Insurance Company'),TH('Policy No.'),TH('From Date'),TH('To Date'),TH('Amount'),TH('Status'),TH(_class='sorting_disabled')))
    i = []
    for r in db(query).select(db.insurance_policy.ALL, orderby = db.insurance_policy.period_covered):
        edit = A(SPAN(_class = 'fa fa-pencil bigger-130'), _title="Update", _href=URL("default","edit_InsurancePolicyForm", args=r.id,  extension=False), _class="blue")
        prin = A(SPAN(_class = 'fa fa-print bigger-130'), _title="Print", _target='blank', _href=URL("Reports","InsurancePolicyReport", args=r.id,  extension=False), _class="blue")        
        btn_lnks = DIV(prin, edit, _class="hidden-sm hidden-xs action-buttons")        
        i.append(TR(TD(),TD(r.company_id.company),TD(r.insurance_company_id.name),TD(r.policy_no),TD(r.from_period_covered),TD(r.period_covered),TD(locale.format('%.2F',r.amount, grouping = True)),TD(r.status_id.status),TD(btn_lnks)))
    body = TBODY(i)
    table = TABLE([head, body],_width='100%', _class='table table-striped table-bordered table-hover')
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DriverNotification():
    today = datetime.date.today()
    rows = db(db.driver).select(orderby = db.driver.expiry_date)
    r = 0
    row = len(rows)
    while (r < row):
        rows[r].update_record(alertdate = rows[r].expiry_date - datetime.timedelta(days = 45))
        r +=1
    query = db.driver.alertdate <= today
    query |= db.driver.expiry_date <= today

    head = THEAD(TR(TH('#'),TH('Emp. No.'),TH('Driver Name'),TH('Position'),TH('License No.'),TH('Exp. Date'),TH('Contact No.'),TH(_class='sorting_disabled')))
    d = []
    for r in db(query).select(db.driver.ALL, orderby = db.driver.expiry_date):
        edit = A(SPAN(_class = 'fa fa-pencil bigger-130'), _title="Update", _href=URL("default","edit_DriverForm", args=r.id,  extension=False), _class="blue")
        prin = A(SPAN(_class = 'fa fa-print bigger-130'), _title="Print", _target='blank' ,_href=URL("Reports","DriverProfileReport", args=r.id,  extension=False), _class="blue")        
        btn_lnks = DIV(prin, edit, _class="hidden-sm hidden-xs action-buttons")
        d.append(TR(TD(),TD(r.employee_number),TD(r.driver_name),TD(r.position_id.name),TD(r.driver_id),TD(r.expiry_date),TD(r.contact_no),TD(btn_lnks)))
    body = TBODY(d)
    table = TABLE([head, body], _width = "100%", _class='table table-striped table-bordered table-hover')    
    return dict(table = table)
# -----------  EXPIRATION NOTIFICATION ENDS HERE.        ------------- #                

# -----------  COMPANY/DIVISION VEHICLE CRUD PHOTOS STARTS HERE.        ------------- #

@auth.requires_membership("level_1_user") 
def edit_PhotosForm():
    #form = SQLFORM(db.repair_history, request.args(0), deletable=True, showid=False, delete_label='Check to delete:')    
    record = db.v_photos(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.v_photos, record, upload=URL('download'),showid = False)    
    form.process(detect_record_change=True)
    if form.record_changed:
        #rec_id = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        #db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'updated reg.no. %s photo\'s.' % (rec_id.reg_no))
        response.flash = form_warning      
    elif form.accepted:  
        rec_id = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'updated reg.no. %s photo\'s.' % (rec_id.reg_no))
        response.flash = form_success
    elif form.errors:
        response.flash = form_error
    else: 
        response.flash = form_info
    return dict(form = form)

@auth.requires_membership("level_1_user") 
def PhotosForm():
    form = SQLFORM(db.v_photos)
    if form.process().accepted:
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'created reg.no. %s photo\'s.' % (record.reg_no))
        response.flash = form_success      
    elif form.errors:
        response.flash = form_error
    else: 
        response.flash = form_info

    row = []
    query = db().select(db.v_photos.ALL,orderby = db.v_photos.reg_no_id)
    head = THEAD(TR(TH('#'),TH('Reg.No.'),TH('RP'),TH('FT'),TH('RR'),TH('LF'),TH('RT'),TH(_class='sorting_disabled')))
    for n in query:
        prin = A(SPAN(_class = 'fa fa-print bigger-130 blue'), _title="Print",_target='blank', _href=URL("#", args=n.id))
        edit = A(SPAN(_class = 'fa fa-pencil bigger-130 blue'), _title="Edit", _href=URL("default","edit_PhotosForm", args=n.id ))
        dele = A(SPAN(_class = 'fa fa-trash bigger-130 blue'), _name='btndel',_title="Delete", callback=URL(args=n.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(n.id)})
        btn_lnks = DIV(prin, edit, dele, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(n.reg_no_id.reg_no),            
            TD(A(SPAN(_class='ace-icon fa fa-drivers-license'), _title='Road Permit', _href = URL('default', 'download', args= n.road_permit), **{'_data-rel':'colorbox'}) if n.road_permit else "",_class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _title='Front Side Photo', _href = URL('default', 'download', args= n.photo),**{'_data-rel':'colorbox'}) if n.photo else "",_class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _title='Rear Side Photo', _href = URL('default', 'download', args= n.photo2), **{'_data-rel':'colorbox'}) if n.photo2 else "",_class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _title='Left Side Photo', _href = URL('default', 'download', args= n.photo3),**{'_data-rel':'colorbox'}) if n.photo3 else "",_class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _title='Right Side Photo', _href = URL('default', 'download', args= n.photo4), **{'_data-rel':'colorbox'}) if n.photo4 else "",_class='ace-thumbnails clearfix'),
            TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')

    return dict(form = form, table = table)


@auth.requires_membership("level_1_user")
def FleetPhoto():
    ctr = 0
    row = []
    query = db().select(db.v_photos.ALL,orderby = db.v_photos.reg_no_id)
    head = THEAD(TR(TH('#'),TH('Reg.No.'),TH('RP'),TH('FT'),TH('RR'),TH('LF'),TH('RT'),TH(_class='sorting_disabled')))
    for n in query:
        prin = A(SPAN(_class = 'fa fa-print bigger-130 blue'), _title="Print",_target='blank', _href=URL("Mileage","VehicleMileageReport", args=n.id))
        edit = A(SPAN(_class = 'fa fa-pencil bigger-130 blue'), _title="Edit", _href=URL("default","edit_PhotosForm", args=n.id ))
        dele = A(SPAN(_class = 'fa fa-trash bigger-130 blue'), _name='btndel',_title="Delete", callback=URL( args=n.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(n.id)})
        btn_lnks = DIV(_class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(n.reg_no_id.reg_no),            
            TD(A(SPAN(_class='ace-icon fa fa-drivers-license'), _title='Road Permit', _href = URL('default', 'download', args= n.road_permit), **{'_data-rel':'colorbox'}) if n.road_permit else "",_class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _title='Front Side Photo', _href = URL('default', 'download', args= n.photo),**{'_data-rel':'colorbox'}) if n.photo else "",_class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _title='Rear Side Photo', _href = URL('default', 'download', args= n.photo2), **{'_data-rel':'colorbox'}) if n.photo2 else "",_class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _title='Left Side Photo', _href = URL('default', 'download', args= n.photo3),**{'_data-rel':'colorbox'}) if n.photo3 else "",_class='ace-thumbnails clearfix'),
            TD(A(SPAN(_class='ace-icon fa fa-car'), _title='Right Side Photo', _href = URL('default', 'download', args= n.photo4), **{'_data-rel':'colorbox'}) if n.photo4 else "",_class='ace-thumbnails clearfix'),
            TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    return dict(table=table)



def deletePhoto():
    pho = db(db.v_photos.id == request.args(1)).select(db.v_photos.ALL).first()
    fre = db(db.vehicle.id == pho.reg_no_id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'deleted reg.no. %s photo\'s' %(fre.reg_no))
    db(db.v_photos.id == request.args(1)).delete()
    

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
def InsuranceForm():
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict()

@auth.requires_membership("level_1_user") 
def InsurancePolicyForm():
    db.insurance_policy.id.readable = False
    form = SQLFORM(db.insurance_policy)
    if form.process().accepted:
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name,auth.user.last_name), action = 'created insurance policy no %s' % (form.vars.policy_no))
        response.flash = form_success
    elif form.errors:
        response.flash = form_error
    else:
        response.flash = form_info    
    return dict(form = form)    

@auth.requires_membership("level_1_user") 
def edit_InsurancePolicyForm():
    rec_id = db.insurance_policy(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.insurance_policy, rec_id, showid = False)
    form.process(detect_record_change = True)
    if form.record_changed:
        response.flash = form_warning
    elif form.accepted:
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name,auth.user.last_name), 
            action = 'updated insurance policy no. %s' % (request.vars.policy_no))
        response.flash = form_success
    elif form.errors:
        response.flash = form_error
    else:
        response.flash = form_info
    return dict(form = form)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def InsurancePolicy():
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict()

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def ActiveInsurancePolicy():
    row = []    
    head = THEAD(TR(TH('#'),TH('Company'),TH('Insurance Company'),TH('Policy No.'),TH('From Date'),TH('To Date'),TH('Amount'),TH('Status'),TH(_class='sorting_disabled')))
    for a in db(db.insurance_policy.status_id == 1).select(db.insurance_policy.ALL):
        pr_v = A(I(_class = 'fa fa-print bigger-130 blue'), _title="Print", _target='blank',_href=URL("Reports","IPFleetReport", args=a.id, extension=False))
        in_v = A(I(_class = 'fa fa-car bigger-130 blue'), _title='Fleets', _href=URL('default','InsuredFleet', args = a.id, extension = False))
        edit = A(I(_class = 'fa fa-pencil bigger-130 blue'), _title="Edit", _href=URL("default","edit_InsurancePolicyForm", args=a.id, extension=False))
        btn_lnks = DIV(pr_v, in_v, edit, _class="hidden-sm hidden-xs action-buttons")        
        row.append(TR(TD(),TD(a.company_id.company),TD(a.insurance_company_id.name),TD(a.policy_no),TD(a.from_period_covered),
            TD(a.period_covered),TD(locale.format('%.2F',a.amount, grouping = True)),TD(a.status_id.status),TD(btn_lnks)))
    body = TBODY(*row)
    active_table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    return dict(active_table=active_table)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def NonActiveInsurancePolicy():
    row = []    
    head = THEAD(TR(TH('#'),TH('Company'),TH('Insurance Company'),TH('Policy No.'),TH('From Date'),TH('To Date'),TH('Amount'),TH('Status'),TH(_class='sorting_disabled')))
    for a in db(db.insurance_policy.status_id == 2).select(db.insurance_policy.ALL):
        pr_v = A(I(_class = 'fa fa-print bigger-130 blue'), _title="Print",_target='blank', _href=URL("Reports","IPFleetReport", args=a.id, extension=False))
        in_v = A(I(_class = 'fa fa-car bigger-130 blue'), _title='Fleets', _href=URL('default','InsuredFleet', args = a.id, extension = False))
        edit = A(I(_class = 'fa fa-pencil bigger-130 blue'), _title="Edit", _href=URL("default","edit_InsurancePolicyForm", args=a.id, extension=False))
        btn_lnks = DIV(pr_v, in_v, edit, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(a.company_id.company),TD(a.insurance_company_id.name),TD(a.policy_no),TD(a.from_period_covered),
            TD(a.period_covered),TD(locale.format('%.2F',a.amount, grouping = True)),TD(a.status_id.status),TD(btn_lnks)))
    body = TBODY(*row)
    nonactive_table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    return dict(nonactive_table=nonactive_table)    
    
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def InsuredFleet():
    row = []
    head = THEAD(TR(TH('#'),TH('Reg.No'),TH('Passenger Covered'),TH('Amount Insured'),TH('Excess'),TH('Amount'),TH(_class='sorting_disabled')))
    for d in db(db.insured_vehicles.policy_no_id == request.args(0)).select(db.insured_vehicles.ALL):
        prin = A(SPAN(_class = 'fa fa-print bigger-130 blue'), _title="Print",_target='blank', _href=URL("Reports","InsuredVehiclesReport", args=d.id))
        edit = A(SPAN(_class = 'fa fa-pencil bigger-130 blue'), _title="Edit", _href=URL("default","edit_InsuredVehiclesForm", args=d.id ))
        dele = A(SPAN(_class = 'fa fa-trash bigger-130 blue'), _name='btndel',_title="Delete", callback=URL( args=d.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(d.id)})
        btn_lnks = DIV(prin, edit, dele, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(d.reg_no_id.reg_no),TD(d.passenger_covered),TD(locale.format('%.2F',d.amount_insured, grouping=True)),TD(d.excess),TD(locale.format('%.2F',d.amount, grouping = True)),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info')     
    return dict(table=table)

def insured_fleet_delete():
    ins = db(db.insured_vehicles.id == request.args(1)).select(db.insured_vehicles.ALL).first()
    fle = db(db.vehicle.id == ins.reg_no_id).select(db.vehicle.ALL).first()    
    pol = db(db.insurance_policy.id == ins.policy_no_id).select(db.insurance_policy.ALL).first()
    db.activities.insert(log_date = request.now, person = '%s %s' %(auth.user.first_name, auth.user.last_name), action = 'delete reg.no. %s insurance with license no. %s' % (fle.reg_no, pol.policy_no))
    db(db.insured_vehicles.id == request.args(1)).delete()

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
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = "created reg.no. %s insured vehicle with policy no. %s" % (record.reg_no, policy.policy_no))       
        response.flash = form_success
    elif form.errors:
        response.flash = form_error
    else:
        response.flash = form_info
    return dict(form = form)

@auth.requires_membership("level_1_user") 
def edit_InsuredVehiclesForm():
    rec_id = db.insured_vehicles(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.insured_vehicles, rec_id, showid = False)
    form.process(detect_record_change = True)
    if form.record_changed:
        response.flash = form_warning
    elif form.accepted:
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name,auth.user.last_name), action = 'updated insurance policy no %s' % (form.vars.policy_no))
        response.flash = form_success
    elif form.errors:
        response.flash = form_error
    else:
        response.flash = form_info
    return dict(form = form)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def InsurancePolicy_():
    ctr = 0
    row = []
    det_row = []
    active_query = db(db.insurance_policy.status_id == 1).select(db.insurance_policy.ALL)
    det_head = THEAD(TR(TH('Reg.No'),TH('Passenger Covered'),TH('Amount Insured'),TH('Excess'),TH('Amount')))
    head = THEAD(TR(TH('#'),TH('Company'),TH('Insurance Company'),TH('Policy No.'),TH('From Date'),TH('To Date'),TH('Amount'),TH('Status'),TH()))
    for a in active_query:
        #<div id="some_btn"><a class="btn btn-success btn-mini" data-target="#some_modal" data-toggle="modal"><i class="icon-search icon-white"></i>    
        #links =[lambda row: A(SPAN(_class = 'icon icon-print'), _target = '_blank', _title = "Print", _href = URL('Reports', 'DriverReport', args=row.id),
        #            _onclick="MyWindow=window.open = 'URL('Reports', 'DriverReport', args = row.id)' ")]

        #lambda row: A(SPAN(_class = 'icon icon-file'), **{'_title':'Insurance Detail', '_data-target':'#InsDetails', '_data-toggle':'modal', '_href':URL("default","VehicleInsDetail", args = row.id)}),
        pr_v = A(SPAN(_class = 'glyphicon glyphicon-print'), _title="Print", _href=URL("default","InsuranceForm", args=a.id),_class='btn btn-default btn-sm')
        #dele = A(SPAN(_class = 'glyphicon glyphicon-trash'), _title="Delete", callback=URL("PhotosDelete", args=n.id),_class='delete btn btn-default btn-sm', _id='rem') vars=dict(id=row.id, **{'data-target':'cart'}
        in_v = A(SPAN(_class = 'glyphicon glyphicon-road'), _type='button', _role='button', _title='Vehicles', _onclick="jQuery('.slider').slideToggle()", callback=URL('InsDetails',vars=dict(id=a.id)),_class='in_v btn btn-default btn-sm')
        edit = A(SPAN(_class = 'glyphicon glyphicon-pencil'), _title="Edit", _href="#",_class='btn btn-default btn-sm')
        #dele = A(SPAN(_class = 'glyphicon glyphicon-trash'), _title="Delete", callback=URL("PhotosDelete", args=a.id),_class='btn btn-default btn-sm')
        row.append(TR(TD(),TD(a.company_id.company),TD(a.insurance_company_id.name),TD(a.policy_no),TD(a.from_period_covered),TD(a.period_covered),TD(locale.format('%.2F',a.amount, grouping = True)),TD(a.status_id.status),TD(in_v, ' ', edit)))
        for d in db(db.insured_vehicles.policy_no_id == a.id).select(db.insured_vehicles.ALL):
            det_row.append(TR(TD(d.reg_no_id.reg_no),TD(d.passenger_covered),TD(d.amount_insured),TD(d.excess),TD(locale.format('%.2F',d.amount, grouping = True))))
            det_body = TBODY(*det_row)
            det_act_table = TABLE(*[det_head, det_row])
    body = TBODY(*row)
    active_table = TABLE(*[head, body], _class='table table-hover table-striped table-bordered table-condensed')
    
    n_row = []
    non_active_query = db(db.insurance_policy.status_id == 2).select(db.insurance_policy.ALL)   
    for n in non_active_query:
        edit = A(SPAN(_class = 'glyphicon glyphicon-pencil'), _title="Edit", _href=URL("default","InsuranceForm", args=n.id),_class='btn btn-default btn-sm')
        dele = A(SPAN(_class = 'glyphicon glyphicon-trash'), _title="Delete", callback=URL("PhotosDelete", args=n.id),_class='btn btn-default btn-sm')
        n_row.append(TR(TD(),TD(n.company_id.company),TD(n.insurance_company_id.name),TD(n.policy_no),TD(n.from_period_covered),TD(n.period_covered),TD(locale.format('%.2F',n.amount, grouping=True)),TD(n.status_id.status),TD(edit)))
    n_body = TBODY(*n_row)
    non_active_table = TABLE(*[head, n_body], _width='100%',_class='table table-hover table-striped table-bordered table-condensed')

    detail_row = []
    detail_query = db(db.insured_vehicles.policy_no_id == request.args(0)).select(db.insured_vehicles.ALL)
    detail_head = THEAD(TR(TH('#'),TH('Reg.No'),TH('Passenger Covered'),TH('Amount Insured'),TH('Excess'),TH('Amount'),TH()))
    for d in detail_query:
        detail_row.append(TR(TD(),TD(d.reg_no_id.reg_no),TD(d.passenger_covered),TD(d.amount_insured),TD(d.excess),TD(locale.format('%.2F',d.amount, grouping = True)),TD()))
    detail_body = TBODY(*detail_row)
    detail_table = TABLE(*[detail_head, detail_body], _width='90%', _align='right')
    return dict(policy_no=0, active_table=active_table, non_active_table=non_active_table, detail_table=detail_table, det_act_table=det_act_table)

# -----------  COMPANY/DIVISION VEHICLE CRUD INSURANCE POLICY ENDS HERE.    ------------- #                    


# -----------  COMPANY/DIVISION DRIVER CRUD STARTS HERE.    ------------- #


@auth.requires_membership('level_1_user')
def edit_DriverForm():
    rec_id = db.driver(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.driver, rec_id, showid=False)
    form.process(detect_record_change = True)
    if form.record_changed:
        response.flash = form_warning
    elif form.accepted:
        db.activities.insert(log_date = request.now,person = '%s %s' % (auth.user.first_name, auth.user.last_name),action = 'updated %s driver profile.' % (form.vars.driver_name))        
        response.flash = form_success
    elif form.errors:
        response.flash = form_error
    else:
        response.flash = form_info
    return dict(form = form)

@auth.requires_membership('level_1_user')
def DriverForm():
    form = SQLFORM(db.driver, request.args(0), showid=False)
    if form.process().accepted:
        db.activities.insert(log_date = request.now,person = '%s %s' % (auth.user.first_name, auth.user.last_name),action = 'created %s driver profile.' % (form.vars.driver_name))
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Driver record save.', _class='white'),_class='alert alert-success') 
    elif form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
    else: 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Kindly fill the form', _class='white'),_class='alert alert-info')     
    return dict(form = form)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Driver():      
    row = []
    head = THEAD(TR(TH('#'),TH('Emp.#'),TH('Name'),TH('Position'),TH('Department'),TH('Contact #'),TH('License'),TH(_class='sorting_disabled')))
    for d in db(db.driver).select(db.driver.ALL):
        #view = A(SPAN(_class = 'fa fa-search bigger-110 blue'), _tabindex='0', _role='button', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Driver Info','_data-content': dri_info(d.id)})
        prin = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _title="Print",_target='blank', _href=URL("Reports","DriverProfileReport", args=d.id))
        edit = A(SPAN(_class = 'fa fa-pencil bigger-110 blue'), _title="Edit", _href=URL("default","edit_DriverForm", args=d.id ))
        dele = A(SPAN(_class = 'fa fa-trash bigger-110 blue'), _name='btndel',_title="Delete", callback=URL( args=d.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(d.id)})
        btn_lnks = DIV( prin, edit, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(d.employee_number),TD(d.driver_name),TD(d.position_id.name),TD(d.department_id.name),TD(d.contact_no),TD(A(SPAN(_class='ace-icon fa fa-drivers-license blue'), _title='Driver License',_href = URL('default', 'download', args= d.driver_license),**{'_data-rel':'colorbox'}) if d.driver_license else "", _class='ace-thumbnails clearfix'),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info')     
    return dict(table = table)

def dri_info(z = request.args(0)):
    for x in db(db.driver.id == z).select():
        i = TABLE(*[
            TR(TD('Emp.No.: '),TD(x.employee_number, _style = 'text-align: right' )),
            TR(TD('Name: '),TD(x.driver_name, _style = 'text-align: right')), 
            TR(TD('Position:'),TD(x.position_id.name, _style = 'text-align: right')),
            TR(TD('Company:'),TD(x.company_id.company, _style = 'text-align: right')),
            TR(TD('Division:'),TD(x.division_id.division, _style = 'text-align: right')),
            TR(TD('Department:'),TD(x.department_id.name, _style = 'text-align: right')),
            TR(TD('Contact No.:'),TD(x.contact_no, _style = 'text-align: right')),
            TR(TD('License No:'),TD(x.driver_id, _style = 'text-align: right')),
            TR(TD('Expiration:'),TD(x.expiry_date, _style = 'text-align: right')),
            TR(TD('Category:'),TD(x.license_category_id, _style = 'text-align: right'))])
    table = str(XML(i, sanitize=False))
    return table

# -----------  COMPANY/DIVISION DRIVER CRUD ENDS HERE.      ------------- #
# -----------  EXPIRATION NOTIFICATION STARTS HERE.    ------------- #
@auth.requires_membership('level_1_user')
def ExpNotification():  #[Hand over form]
    return locals()
# -----------  EXPIRATION NOTIFICATION ENDS HERE.    ------------- #


# -----------  COMPANY/DIVISION VEHICLE CRUD HAND-OVER STARTS HERE.    ------------- #

@auth.requires_membership('level_1_user')
def HandOverForm():  #[Hand over form]
    form = SQLFORM(db.vehicles_hand_over, request.args(0))
    if form.process().accepted: 
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = "created reg.no. %s hand-over." % (record.reg_no))
        response.flash = form_success   
    elif form.errors:
        response.flash = form_error
    else:
        response.flash = form_info 
    return dict(form = form)


@auth.requires_membership('level_1_user')
def edit_HandOverForm():
    rec_id = db.vehicles_hand_over(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.vehicles_hand_over, rec_id, showid=False)
    form.process(detect_record_change = True)
    if form.record_changed:
        response.flash = form_warning
    elif form.accepted:
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now,person = '%s %s' % (auth.user.first_name, auth.user.last_name),action = 'updated reg.no. %s hand-over.' % (record.reg_no))        
        response.flash = form_success
    elif form.errors:
        response.flash = form_error
    else:
        response.flash = form_info
    return dict(form = form)
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def HandOver(): #[Hand over grid]
    row = []
    head = THEAD(TR(TH('#'),TH('Date & Time'),TH('Reg.No.'),TH('F/Driver'),TH('T/Driver'),TH('Mileage'),TH(_class='sorting_disabled')))
    for h in db(db.vehicles_hand_over).select(db.vehicles_hand_over.ALL):
        view = A(SPAN(_class = 'fa fa-search bigger-110 blue'), _tabindex='0', _role='button', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Hand-Over Info','_data-content': han_info(h.id)})
        prin = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _title="Print",_target='blank', _href=URL("Reports","HandOverReport", args=h.id))
        edit = A(SPAN(_class = 'fa fa-pencil bigger-110 blue'), _title="Edit", _href=URL("default","edit_HandOverForm", args=h.id ))
        dele = A(SPAN(_class = 'fa fa-trash bigger-110 blue'), _name='btndel',_title="Delete", callback=URL( args=h.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(h.id)})
        btn_lnks = DIV(view, prin, edit,  _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(h.date_and_time),TD(h.reg_no_id.reg_no),TD(h.from_driver_id.driver_name),TD(h.to_driver_id.driver_name),TD(h.mileage),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(table=table)

def han_info(z = request.args(0)):
    for x in db(db.vehicles_hand_over.id == z).select():
        i = TABLE(*[
            TR(TD('Reg.No.: '),TD(x.reg_no_id.reg_no, _style = 'text-align: right' )),
            TR(TD('Date & Time: '),TD(x.date_and_time, _style = 'text-align: right' )), 
            TR(TD('From Dept.:'),TD(x.from_department_id.name, _style = 'text-align: right')),
            TR(TD('To Dept.:'),TD(x.to_department_id.name, _style = 'text-align: right')),
            TR(TD('From Driver:'),TD(x.from_driver_id.driver_name, _style = 'text-align: right')),
            TR(TD('To Driver:'),TD(x.to_driver_id.driver_name, _style = 'text-align: right')),
            TR(TD('Mileage:'),TD(x.mileage, _style = 'text-align: right')),
            TR(TD('Accessories:'),TD(x.vehicles_acc, _style = 'text-align: right')),
            TR(TD('Remarks:'),TD(x.remarks, _style = 'text-align: right'))])
    table = str(XML(i, sanitize=False))
    return table


# -----------  COMPANY/DIVISION VEHICLE CRUD HAND-OVER ENDS HERE.    ------------- #                    

def FormDownload(): #[Vehicle form download]
    import os
    fullpath = os.path.join(request.folder,'uploads', 'VehicleForm.pdf')
    response.stream(os.path.join(request.folder, fullpath))


# -----------  DEPARTMENT CONTROLLER CRUD ENDS HERE.    ------------- #                    

def Profile():
    form = auth.profile()
    for input in form.elements('input', _class='string'):
        input['_class'] = 'string form-control'
    return dict(form=form)

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
    response.flash = 'error'
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


