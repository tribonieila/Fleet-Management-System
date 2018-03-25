from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas

import datetime
import time
#from reportlab.pdfbase import pdfdoc

#pdfdoc.PDFCatalog.OpenAction = '<</S/JavaScript/JS(this.print\({bUI:true,bSilent:false,bShrinkToFit:true}\);)>>'

styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']

styles.add(ParagraphStyle(name='Table Top Black Back', fontName ='Helvetica',fontSize=14, leading=16,backColor = colors.black, textColor=colors.white, alignment=TA_LEFT))
styles.add(ParagraphStyle(name='Wrap', fontSize=9, wordWrap='LTR', firstLineIndent = 0,alignment = TA_LEFT))

#styleN = styles["BodyText"]


tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.8*inch, leftMargin=30, rightMargin=30)#, showBoundary=1)
logo_path = request.folder + 'static/images/image003.jpg'
row = []

I = Image(logo_path)
I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
I.drawWidth = 1.25*inch
I.hAlign='RIGHT'
darwish = Paragraph('''<font size=14><b>Darwish Group </b><font color="gray">|</font></font> <font size=9 color="gray"> Fleet Management System</font>''',styles["BodyText"])


###########

def _title(title):
    title = 'Title'
    return str(title)

def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Vehicle Summary Report'
    header = Table([['',I],[darwish,''],['Division Summary Report','']], colWidths=[None,90])
    header.setStyle(TableStyle([('SPAN',(1,0),(1,1)),('SPAN',(0,2),(1,2)),('ALIGN',(0,0),(0,0),'RIGHT'),('LINEBELOW',(0,1),(1, 1),0.25, colors.gray),('BOTTOMPADDING',(0,0),(0, 1),10),('TOPPADDING',(0,2),(1,2),6)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .7 * inch)


    # Footer
    import time
    from datetime import date
    today = date.today()
    footer = Table([[today.strftime("%A %d. %B %Y")]], colWidths=[535])
    footer.setStyle(TableStyle([('TEXTCOLOR',(0,0),(0,0), colors.gray),('FONTSIZE',(0,0),(0,0),8),('ALIGN',(0,0),(0,0),'RIGHT'),('LINEABOVE',(0,0),(0,0),0.25, colors.gray)]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .7 * inch)

    # Release the canvas
    canvas.restoreState()

###########

def test():
    #query = db.vehicle.division_id == 19
    query = db.repair_history.reg_no_id == 19
    table = db(query).select(db.repair_history.ALL)

    return dict(table = table)

@auth.requires_membership('level_2_user')
def Dashboard():
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Welcome '), 'to our latest Fleet Management System.', _class='white'),_class='alert alert-success') 
    return dict()

def Statistics():
    from datetime import date, datetime, timedelta
    import calendar
    begin = date(2014, 1,1)
    end = date(2014, 12,31)
    f = db.vehicle.division_id == auth.user.division_id
    f &= db.fuel_expenses.reg_no_id == db.vehicle.id
    f &= db.fuel_expenses.date_expense >= date(date.today().year, 1, 1)
    f &= db.fuel_expenses.date_expense <= request.now

    r = db.vehicle.division_id == auth.user.division_id
    r &= db.repair_history.reg_no_id == db.vehicle.id
    r &= db.repair_history.invoice_date >= date(date.today().year, 1, 1)
    r &= db.repair_history.invoice_date <= request.now

    k = db.vehicle.division_id == auth.user.division_id
    k &= db.km_used.reg_no_id == db.vehicle.id
    k &= db.km_used.given_month >= date(date.today().year, 1, 1)
    k &= db.km_used.given_month <= request.now

    n = db.vehicle.division_id == auth.user.division_id 
    n &= db.insured_vehicles.reg_no_id == db.vehicle.id
    n &= db.insured_vehicles.policy_no_id == db.insurance_policy.id
    n &= db.insurance_policy.status_id == 1    

    a = db.vehicle.division_id == auth.user.division_id 
    a &= db.ads_vehicle.reg_no_id == db.vehicle.id
    a &= db.ads_vehicle.license_no_id == db.advertisement.id
    a &= db.advertisement.status_id == 1

    # annual ads expenses
    ads = db.ads_vehicle.amount.sum().coalesce_zero()
    ads_exp = db(a).select(ads).first()[ads]

    # annual insurance expenses
    ins = db.insured_vehicles.amount.sum().coalesce_zero()
    ins_expenses = db(n).select(ins).first()[ins]

    # monthly repair expenses
    r_mai = db.repair_history.regular_maintenance.sum().coalesce_zero()
    a_rep = db.repair_history.accident_repair.sum().coalesce_zero()
    s_exp = db.repair_history.statutory_expenses.sum().coalesce_zero()
    s_parts = db.repair_history.spare_parts.sum().coalesce_zero()
    repr = db.repair_history.total_amount.sum().coalesce_zero()

    r_mai = db(r).select(r_mai).first()[r_mai]
    a_rep = db(r).select(a_rep).first()[a_rep]
    s_exp = db(r).select(s_exp).first()[s_exp]
    s_parts = db(r).select(s_parts).first()[s_parts]
    repair_expenses = db(r).select(repr).first()[repr]

    main_exp = s_parts + r_mai + a_rep

    rep_exp = db.repair_history.total_amount.sum().coalesce_zero()
    rep_que = db(r).select(db.repair_history.invoice_date.month(),rep_exp, orderby=db.repair_history.invoice_date.month(), groupby = db.repair_history.invoice_date.month())    
    rep_tot = db(r).select(rep_exp).first()[rep_exp]

    # monthly fuel expenses
    fuel_exp = db.fuel_expenses.amount.sum().coalesce_zero()
    ful_que = db(f).select(db.fuel_expenses.date_expense.month(),fuel_exp, orderby=db.fuel_expenses.date_expense.month(), groupby = db.fuel_expenses.date_expense.month())
    ful_exp = db(f).select(fuel_exp).first()[fuel_exp]

    # monthly average mileage
    div_fle = db((db.vehicle.status_id == 3) & (db.vehicle.division_id == auth.user.division_id)).count()
    km = db.km_used.consumed_mil.sum().coalesce_zero()
    tot_mil = db(k).select(km).first()[km]
    mil_que = db(k).select(db.km_used.given_month.month(), km, orderby=db.km_used.given_month.month(), groupby=db.km_used.given_month.month())
    #mil_que = db(k).select(db.km_used.ALL, orderby = db.km_used.given_month | db.km_used.reg_no_id)


    # current grand total
    cur_tot = ful_exp + rep_tot + ads_exp + ins_expenses

    # annual total cost/km
    # current total run per cost
    if tot_mil != 0:
        ann_cos = ful_exp / tot_mil
        cos_run = cur_tot / tot_mil
    else:
        ann_cos = float('0')
        cos_run = float('0')    

    row = []
    head = THEAD(TR(TH('MONTH'),TH('AVERAGE MILEAGE')))
    for e in mil_que:
        row.append(TR(TD(calendar.month_name[e[db.km_used.given_month.month()]]),TD(locale.format('%d',e[km] or 0, grouping = True))))
        #row.append(TR(TD(e.reg_no_id.reg_no),TD(e.given_month),TD(e.current_mil)))
    body = TBODY(*row)
    table = TABLE(*[head,body], _class='table')

    return dict(main_exp=main_exp,cos_run = cos_run, cur_tot = cur_tot, ads_exp=ads_exp,ful_exp=ful_exp,
        ins_expenses = ins_expenses, ann_cos= ann_cos,table = table,mil_que=mil_que, rep_que = rep_que, 
        ful_que = ful_que, div_fle = div_fle, s_exp = s_exp)
    

def Fleet():
    active = db((db.vehicle.status_id == 3) & (db.vehicle.division_id == auth.user.division_id)).count()
    non_active = db((db.vehicle.status_id == 2) & (db.vehicle.division_id == auth.user.division_id)).count()
    cancelled = db((db.vehicle.status_id == 1) & (db.vehicle.division_id == auth.user.division_id)).count()
    regno_exp = db((db.vehicle.status_id == 3)&(db.vehicle.exp_date <= request.now) & (db.vehicle.division_id == auth.user.division_id)).count()
    licno_exp = db((db.driver.expiry_date <= request.now) & (db.driver.division_id == auth.user.division_id)).count()
    insur_exp = db((db.insurance_policy.status_id == 1) & (db.insurance_policy.period_covered <= request.now) & (db.insured_vehicles.policy_no_id == db.insurance_policy.id)&(db.insured_vehicles.reg_no_id == db.vehicle.id)&(db.vehicle.division_id == auth.user.division_id)).count()
    total = active + non_active + cancelled

    count_fleet = DIV('Active: ', active)
    count_fleet += DIV('Non-Active: ', non_active)
    count_fleet += DIV('Cancelled: ', cancelled)
    count_fleet += DIV('Expired Reg.No.: ', regno_exp)
    count_fleet += DIV('Expired Driver Lic.No.: ', licno_exp)
    count_fleet += DIV('Expired Insurance Policy: ', insur_exp)

    fleet = DIV(
    DIV(DIV(SPAN(_class='ace-icon fa fa-car'),_class='infobox-icon'),DIV(SPAN(active, _class='infobox-data-number'),DIV('Running',_class='infobox-content'),_class='infobox-data'),DIV(locale.format('%.2F', (active / float(total) * 100), grouping = True) +'%',_class='stat stat-important'),_class='infobox infobox-green'),
    DIV(DIV(SPAN(_class='ace-icon fa fa-car'),_class='infobox-icon'),DIV(SPAN(non_active, _class='infobox-data-number'),DIV('Non-Running',_class='infobox-content'),_class='infobox-data'),DIV(locale.format('%.2F', (non_active / float(total) * 100) or 0, grouping = True)+'%',_class='stat stat-success'),_class='infobox infobox-orange'),
    DIV(DIV(SPAN(_class='ace-icon fa fa-car'),_class='infobox-icon'),DIV(SPAN(cancelled, _class='infobox-data-number'),DIV('Cancelled',_class='infobox-content'),_class='infobox-data'),DIV(locale.format('%.2F', (cancelled / float(total) * 100) or 0, grouping = True)+'%',_class='stat stat-success'),_class='infobox infobox-red'),
    DIV(DIV(SPAN(_class='ace-icon fa fa-hourglass-end'),_class='infobox-icon'),DIV(SPAN(regno_exp, _class='infobox-data-number'),DIV('Expired Reg.No.',_class='infobox-content'),_class='infobox-data'),_class='infobox infobox-blue'),
    DIV(DIV(SPAN(_class='ace-icon fa fa-credit-card'),_class='infobox-icon'),DIV(SPAN(licno_exp, _class='infobox-data-number'),DIV('Exp. Driver Lic.No.',_class='infobox-content'),_class='infobox-data'),_class='infobox infobox-orange2'),
    DIV(DIV(SPAN(_class='ace-icon fa fa-heartbeat'),_class='infobox-icon'),DIV(SPAN(insur_exp, _class='infobox-data-number'),DIV('Exp. Insurance Policy',_class='infobox-content'),_class='infobox-data'),_class='infobox infobox-blue2'))   
    return fleet    

def FuelBoard():
    from datetime import date,datetime, timedelta      
    import calendar
    f = db.vehicle.division_id == auth.user.division_id
    f &= db.fuel_expenses.reg_no_id == db.vehicle.id
    f &= db.fuel_expenses.date_expense >= date(date.today().year, 1, 1)
    f &= db.fuel_expenses.date_expense <= request.now

    fuel_exp = db.fuel_expenses.amount.sum().coalesce_zero()
    total_exp = db(f).select(fuel_exp).first()[fuel_exp]

    query = db(f).select(db.fuel_expenses.date_expense.month(),fuel_exp, orderby=db.fuel_expenses.date_expense.month(), groupby = db.fuel_expenses.date_expense.month())
    row = []
    head = THEAD(TR(TH('Date'),TH('Amount')))

    for e in query:
        row.append(TR(TD(calendar.month_name[e[db.fuel_expenses.date_expense.month()]]),TD(locale.format('%.2F',e[fuel_exp] or 0, grouping = True))))
    body = TBODY(*row)
    table = TABLE(*[head,body], _class='table')
    return dict(query=query)


@auth.requires_membership('level_2_user')
def Fleets():
    
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    row = []
    ctr = 0
    head = THEAD(TR(TH(_class='sorting_disabled'),TH('Code'),TH('Reg.No.'),TH('Brand'),TH('Model'),TH('Mileage'),TH('Transmission'),TH('Color'),TH('Category'),TH('RPEX Date'),TH(_class='sorting_disabled')))
    for f in db(db.vehicle.division_id == auth.user.division_id).select(db.vehicle.ALL):
        btn_view = A(SPAN(_class = 'fa fa-info-circle bigger-130 popover-info'), _class='blue',_tabindex='0', _role='button', 
            **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Fleet Info','_data-content': view_info(f.id)})
        btn_print = A(SPAN(_class = 'fa fa-print bigger-130'), _title="Print", _target='blank', _href=URL('Reports','VehicleProfileReport', args = f.id),_class="blue ")        
        btn_lnks = DIV(btn_view, btn_print, _class="hidden-sm hidden-xs action-buttons")
        if f.status_id == 1: # cancelled vehicles
            row.append(TR(TD(A(SPAN(_class='fa fa-flag red bigger-130 tooltip-error', _title='', _role='button', **{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Cancelled Fleet'}))),TD(f.vehicle_code),TD(f.reg_no),TD(f.vehicle_name_id.vehicle_name),TD(f.model),TD(f.mileage),TD(f.transmission),TD(f.ext_color_code),TD(f.category_id.category),TD(f.exp_date),TD(btn_lnks)))
        elif (f.exp_date <= datetime.date.today()): # reg.no. expired 
            row.append(TR(TD(A(SPAN(_class='fa fa-flag orange bigger-130 tooltip-warning',_title='', _role='button', **{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Expired Reg.No.'}))),TD(f.vehicle_code),TD(f.reg_no),TD(f.vehicle_name_id.vehicle_name),TD(f.model),TD(f.mileage),TD(f.transmission),TD(f.ext_color_code),TD(f.category_id.category),TD(f.exp_date),TD(btn_lnks)))
        elif (db.insurance_policy.status_id == 1) & (db.insured_vehicles.policy_no_id == db.insurance_policy.id) & (db.insured_vehicles.reg_no_id == f.id): # insurance vehicles
            row.append(TR(TD(A(SPAN(_class='fa fa-flag blue bigger-130 tooltip-info' ,_title='', _role='button',**{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Expired Fleet Insurance'}))),TD(f.vehicle_code),TD(f.reg_no),TD(f.vehicle_name_id.vehicle_name),TD(f.model),TD(f.mileage),TD(f.transmission),TD(f.ext_color_code),TD(f.category_id.category),TD(f.exp_date),TD(btn_lnks)))
        else: # good status vehicles
            row.append(TR(TD(A(SPAN(_class='fa fa-flag green bigger-130 tooltip-success'),_title='', _role='button',**{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Good Fleet Status'})),TD(f.vehicle_code),TD(f.reg_no),TD(f.vehicle_name_id.vehicle_name),TD(f.model),TD(f.mileage),TD(f.transmission),TD(f.ext_color_code),TD(f.category_id.category),TD(f.exp_date),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')  
    table += DIV(IMG(_class='fa fa-flag red bigger-90'))  
    return dict(table = table) 


@auth.requires_membership('level_2_user')
def LoadFleet():
    row = []
    ctr = 0
    head = THEAD(TR(TH(),TH('Code'),TH('Reg.No.'),TH('Brand'),TH('Model'),TH('Mileage'),TH('Transmission'),TH('Color'),TH('Category'),TH('RPEX Date'),TH(_class='sorting_disabled')))
    for f in db(db.vehicle.division_id == auth.user.division_id).select(db.vehicle.ALL):
        btn_view = A(SPAN(_class = 'fa fa-info-circle bigger-130 popover-info'), _class='blue',_tabindex='0', _role='button', 
            **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Fleet Info','_data-content': view_info(f.id)})
        btn_print = A(SPAN(_class = 'fa fa-print bigger-130'), _title="Print", _target='blank', _href=URL('Reports','VehicleProfileReport', args = f.id),_class="blue ")        
        btn_lnks = DIV(btn_view, btn_print, _class="hidden-sm hidden-xs action-buttons")
        if f.status_id == 1: # cancelled vehicles
            row.append(TR(TD(A(SPAN(_class='fa fa-flag red bigger-130 tooltip-error', _title='', _role='button',
                **{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Cancelled Fleet'}))),TD(f.vehicle_code),TD(f.reg_no),TD(f.vehicle_name_id.vehicle_name),TD(f.model),TD(f.mileage),TD(f.transmission),TD(f.ext_color_code),TD(f.category_id.category),TD(f.exp_date),TD(btn_lnks)))
        elif (f.datetoalert <= datetime.date.today()) | (f.exp_date <= datetime.date.today()): # reg.no. expired 
            row.append(TR(TD(A(SPAN(_class='fa fa-flag orange bigger-130 tooltip-warning',_title='', _role='button',
                **{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Expired Reg.No.'}))),TD(f.vehicle_code),TD(f.reg_no),TD(f.vehicle_name_id.vehicle_name),TD(f.model),TD(f.mileage),TD(f.transmission),TD(f.ext_color_code),TD(f.category_id.category),TD(f.exp_date),TD(btn_lnks)))
        elif (db.insurance_policy.status_id == 1) & (db.insurance_policy.datetoalert <= datetime.date.today()) & (db.insured_vehicles.policy_no_id == db.insurance_policy.id) & (db.insured_vehicles.reg_no_id == f.id): # insurance vehicles
            row.append(TR(TD(A(SPAN(_class='fa fa-flag blue bigger-130 tooltip-info' ,_title='', _role='button',
                **{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Expired Fleet Insurance'}))),TD(f.vehicle_code),TD(f.reg_no),TD(f.vehicle_name_id.vehicle_name),TD(f.model),TD(f.mileage),TD(f.transmission),TD(f.ext_color_code),TD(f.category_id.category),TD(f.exp_date),TD(btn_lnks)))
        else: # good status vehicles
            row.append(TR(TD(A(SPAN(_class='fa fa-flag green bigger-130 tooltip-success'),_title='', _role='button',
                **{'_data-rel':'tooltip', '_data-placement':'right', '_data-original-title':'Good Fleet Status'})),TD(f.vehicle_code),TD(f.reg_no),TD(f.vehicle_name_id.vehicle_name),TD(f.model),TD(f.mileage),TD(f.transmission),TD(f.ext_color_code),TD(f.category_id.category),TD(f.exp_date),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')    
    
    return dict(table = table) 


def view_info(z = request.args(0)):
    for x in db(db.vehicle.id == z).select():
        i = TABLE(*[
            TR(TD('Company: '), TD(x.company_id.company)),
            TR(TD('Division: '), TD(x.division_id.division)),
            TR(TD('Department: '), TD(x.department.name)),
            TR(TD('Owner: '), TD(x.owner.name)),
            TR(TD('Chassis No.: '), TD(x.chassis_no)),
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


@auth.requires_membership('level_2_user') 
def Maintenance():
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict()

@auth.requires_membership('level_2_user') 
def MaintenanceExpensesForm():
    db.repair_history.regular_maintenance.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')
    db.repair_history.spare_parts.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')
    db.repair_history.statutory_expenses.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')
    db.repair_history.accident_repair.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')
    db.repair_history.total_amount.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')
    links = [lambda row: A(SPAN(_class = 'icon icon-print'), _title="Print", _target = "_blank", _href=URL("MaintenanceReports","MaintenanceReport", args = row.id))]
    query = (db.vehicle.division_id == auth.user.division_id)
    form = SQLFORM.factory(
        Field('reg_no_id', requires = IS_IN_DB(db(query), db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.'),widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('invoice_number', label = 'Invoice #', requires = (IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'repair_history.invoice_number',
            error_message = 'invoice no. already exist!')),widget = lambda field, value: SQLFORM.widgets.string.widget(field, value, _class='form-control')),
        Field('invoice_date', 'date', default = request.now, widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),
        Field('workshop_done', requires = IS_IN_DB(db, db.workshop_done, '%(workshop)s', zero = 'Choose workshop done'), widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('date_time_in', 'date', default = request.now,widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),
        Field('date_time_out', 'date', default = request.now,widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),
        Field('mileage', 'integer', default = 0,widget = lambda field, value: SQLFORM.widgets.integer.widget(field, value, _class='form-control')), 
        Field('regular_maintenance','decimal(10,2)',default = 00.00, comment = 'Service, Oil/Filter Change', widget = lambda field, value: SQLFORM.widgets.double.widget(field, value, _class='form-control')),
        Field('spare_parts', 'decimal(10,2)', default = 00.00, widget = lambda field, value: SQLFORM.widgets.double.widget(field, value, _class='form-control')),                
        Field('statutory_expenses','decimal(10,2)',default = 00.00, comment = 'Insurance, Road Permit Renewal, Advertisement License',widget = lambda field, value: SQLFORM.widgets.double.widget(field, value, _class='form-control')),
        Field('accident_repair','decimal(10,2)',default = 00.00,widget = lambda field, value: SQLFORM.widgets.double.widget(field, value, _class='form-control')),       
        Field('details', requires = IS_UPPER(),widget = lambda field, value: SQLFORM.widgets.string.widget(field, value, _class='form-control')))#,
        #Field('printys', 'boolean', default = True))
    if form.process().accepted:            
        db.repair_history.insert(reg_no_id = form.vars.reg_no_id,
            invoice_number = form.vars.invoice_number,
            invoice_date = form.vars.invoice_date,
            workshop_done = form.vars.workshop_done,
            date_time_in = form.vars.date_time_in,
            date_time_out = form.vars.date_time_out,
            mileage = form.vars.mileage,
            regular_maintenance = form.vars.regular_maintenance,
            spare_parts = form.vars.spare_parts,
            statutory_expenses = form.vars.statutory_expenses,
            accident_repair = form.vars.accident_repair,
            details = form.vars.details)
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = 'created reg.no. %s maintenance expenses with invoice number %s' % (record.reg_no, form.vars.invoice_number))       
        response.js =  "$('#tblME').get(0).reload()" 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'New maintenance expenses record save.', _class='white'),_class='alert alert-success') 

    elif form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 

    else: response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(form=form)


@auth.requires_membership('level_2_user') 
def MaintenanceExpenses():
    row = []
    query = db.vehicle.status_id != 1
    query &= db.vehicle.division_id == auth.user.division_id
    query &= db.repair_history.reg_no_id == db.vehicle.id

    head = THEAD(TR(TH('#'),TH('Date'),TH('Invoice'),TH('Reg.No.'),TH('Workshop'),TH('Duration'),TH('Mileage'),TH('Amount'),TH(_class='sorting_disabled')))

    for n in db(query).select(db.repair_history.ALL):
        pr_v = A(SPAN(_class = 'fa fa-print bigger-130'), _title="Print",_target='blank', _href=URL("MaintenanceReports","MaintenanceReport", args=n.id), _class="blue")
        btn_view = A(SPAN(_class = 'fa fa-info-circle bigger-130 popover-info'), _class='blue',_tabindex='0', _role='button', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Maintenance Info','_data-content': main_info(n.id)})

        btn_lnks = DIV(btn_view, pr_v, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(n.invoice_date),TD(n.invoice_number),TD(n.reg_no_id.reg_no),TD(n.workshop_done.workshop),
            #TD(T('%s %%{day}',abs(n.date_time_out - n.date_time_in ).days)),TD(locale.format('%d',n.mileage or 0, grouping = True)),
            TD(n.no_days_time),TD(locale.format('%d',n.mileage or 0, grouping = True)),
            TD(locale.format('%.2F',n.total_amount or 0, grouping=True),_style = 'text-align: right'),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _id='tblME', _class='table table-striped table-bordered table-hover')
    
    #response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Success: '), 'Data record save.', _class='white'),_class='alert alert-info') 
    return dict(table = table)

def main_info(z = request.args(0)):
    for x in db(db.repair_history.id == z).select():
        i = TABLE(*[
            TR(TD('Start Date: '),TD(x.date_time_in)),
            TR(TD('End Date: '),TD(x.date_time_out)), #str(abs(f.repair_history.date_time_out - f.repair_history.date_time_in).days)
            #T("You have %s %%{book}", symbols=10)

            TR(TD('Duration: '),TD(x.no_days_time)),
            TR(TD('LAB: '),TD(locale.format('%.2F',x.regular_maintenance or 0, grouping = True), _style = 'text-align: right')),
            TR(TD('SP: '),TD(locale.format('%.2F', x.spare_parts or 0, grouping = True), _style = 'text-align: right')),
            TR(TD('SE:'),TD(locale.format('%.2F', x.statutory_expenses or 0, grouping = True ), _style = 'text-align: right')),
            TR(TD('AR:'),TD(locale.format('%.2F',x.accident_repair or 0, grouping = True), _style = 'text-align: right')),
            TR(TD('Amount:'),TD(locale.format('%.2F',x.total_amount or 0, grouping = True), _style = 'text-align: right')),
            TR(TD('Details:'),TD(x.details))])
    table = str(XML(i, sanitize=False))
    return table

@auth.requires_membership('level_2_user')
def FuelExpenses():
    query = db.vehicle.status_id != 1            
    query &= db.vehicle.division_id == auth.user.division_id
    query &= db.fuel_expenses.reg_no_id == db.vehicle.id
    row = []
    head = THEAD(TR(TH('#'),TH('Date'),TH('Reg.No.'),TH('Amount'),TH('Paid By'),TH('Station'),TH('Remarks'),TH(_class='sorting_disabled')))
    for f in db(query).select(db.fuel_expenses.ALL):
        pr_v = A(SPAN(_class = 'fa fa-print bigger-130'), _title="Print", _target='blank', _href=URL("FuelReports","FuelReport", args=f.id),_class="blue")
        vi_v = A(SPAN(_class = 'fa fa-search bigger-130'), _title='View', _href="#", _class='green')
        btn_lnks = DIV(pr_v, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(f.date_expense),TD(f.reg_no_id.reg_no),TD(f.amount),TD(f.paid_by),TD(f.station),TD(f.remarks or 'None'),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _id='tblFE', _class='table table-striped table-bordered table-hover')
    return dict(table = table)





@auth.requires_membership('level_2_user')
def FuelExpensesBatchForm():   
    form = FORM(DIV(LABEL('Paid By: ',_class='col-sm-2'),SELECT('Cash','Credit','Fuel Card', _type='text', _id='paid_by', _name='paid_by',_placeholder='Paid By' ,_class='col-sx-10')),
        DIV(_class='space space-8'),
        DIV(LABEL('Station: ',_class='col-sm-2'),INPUT(_type='text', _id='station',_name='station', _placeholder='Station')),DIV(_class='space space-8'),
        TABLE(THEAD(TR(TH('#'),TH('Date'),TH('Reg.No.'),TH('Amount'),TH('Remarks'),TH(),TH())),
        TBODY(TR(TD(SPAN(_id='sheepItForm_label', _name = 'ctr')),
            TD(INPUT(_class='date col-xs-10 col-sm-10', _value=request.now.date(), _id='date_expense', _name="date_expense")),
            TD(SELECT(_class='col-xs-10 col-sm-10', _id='reg_no_id', _name='reg_no_id', *[OPTION(r.reg_no, _value=r.id) for r in db(db.vehicle.division_id == auth.user.division_id).select(db.vehicle.ALL, orderby=db.vehicle.reg_no)])),
            TD(INPUT(_class='col-xs-10 col-sm-10', _id='amount', _value=00.00, _name='amount')),
            TD(INPUT(_class='col-xs-10 col-sm-15', _id='remarks',_type='text', _name='remarks')),
            TD(INPUT(_id='counter',_type='hidden', _name='counter')),
            TD(A(SPAN(_class='ace-icon fa fa-remove bigger-110 icon-only'),_class='btn btn-danger btn-xs', _id='sheepItForm_remove_current', _name = 'sheepItForm_remove_current')),_id="sheepItForm_template"),TR(TD('No Entry Field',_colspan='6'),_id="sheepItForm_noforms_template"),_id="sheepItForm"),
        TFOOT(TR(TD(DIV(
            DIV(A(SPAN(' Add',_class='ace-icon fa fa-plus-circle bigger-120'),_class='btn btn-success btn-xs'), _id='sheepItForm_add'),
            DIV(A(SPAN(' Remove',_class='ace-icon fa fa-minus-circle bigger-120'),_class='btn btn-danger btn-xs'),_id='sheepItForm_remove_last'),
            DIV(A(SPAN(' Remove All', _class='ace-icon fa fa-remove bigger-120'),_class='btn btn-danger btn-xs'),_id='sheepItForm_remove_all'),_id='sheepItForm_controls'),_colspan='7'))),_class='table table-striped'),
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



@auth.requires_membership('level_2_user') 
def MaintenanceExpensesCopy():
    db.repair_history.regular_maintenance.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')
    db.repair_history.spare_parts.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')
    db.repair_history.statutory_expenses.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')
    db.repair_history.accident_repair.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')
    db.repair_history.total_amount.represent = lambda value, row: DIV(locale.format('%.2F', value or 0, grouping = True), _style = 'text-align: right')
    links = [lambda row: A(SPAN(_class = 'icon icon-print'), _title="Print", _target = "_blank", _href=URL("MaintenanceReports","MaintenanceReport", args = row.id))]
    query = (db.vehicle.division_id == auth.user.division_id)
    form = SQLFORM.factory(
        Field('reg_no_id', requires = IS_IN_DB(db(query), db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.'),widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('invoice_number', label = 'Invoice #', requires = (IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'repair_history.invoice_number',
            error_message = 'invoice no. already exist!')),widget = lambda field, value: SQLFORM.widgets.string.widget(field, value, _class='form-control')),
        Field('invoice_date', 'date', default = request.now, widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),
        Field('workshop_done', requires = IS_IN_DB(db, db.workshop_done, '%(workshop)s', zero = 'Choose workshop done'), widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('date_time_in', 'date', default = request.now,widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),
        Field('date_time_out', 'date', default = request.now,widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),
        Field('mileage', 'integer', default = 0,widget = lambda field, value: SQLFORM.widgets.integer.widget(field, value, _class='form-control')), 
        Field('regular_maintenance','decimal(10,2)',default = 00.00, comment = 'Service, Oil/Filter Change', widget = lambda field, value: SQLFORM.widgets.double.widget(field, value, _class='form-control')),
        Field('spare_parts', 'decimal(10,2)', default = 00.00, widget = lambda field, value: SQLFORM.widgets.double.widget(field, value, _class='form-control')),                
        Field('statutory_expenses','decimal(10,2)',default = 00.00, comment = 'Insurance, Road Permit Renewal, Advertisement License',widget = lambda field, value: SQLFORM.widgets.double.widget(field, value, _class='form-control')),
        Field('accident_repair','decimal(10,2)',default = 00.00,widget = lambda field, value: SQLFORM.widgets.double.widget(field, value, _class='form-control')),       
        Field('details', requires = IS_UPPER(),widget = lambda field, value: SQLFORM.widgets.string.widget(field, value, _class='form-control')),
        Field('printys', 'boolean', default = True, label =  'Print after submit?'))
    if form.process().accepted:       
        db.repair_history.insert(reg_no_id = form.vars.reg_no_id,
            invoice_number = form.vars.invoice_number,
            invoice_date = form.vars.invoice_date,
            workshop_done = form.vars.workshop_done,
            date_time_in = form.vars.date_time_in,
            date_time_out = form.vars.date_time_out,
            mileage = form.vars.mileage,
            regular_maintenance = form.vars.regular_maintenance,
            spare_parts = form.vars.spare_parts,
            statutory_expenses = form.vars.statutory_expenses,
            accident_repair = form.vars.accident_repair,
            details = form.vars.details)
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = 'created reg.no. %s maintenance expenses with invoice number %s' % (record.reg_no, form.vars.invoice_number),
            log_code=1,
            focal_person = auth.user.id)       
        response.flash = 'Record Inserted'  
    if form.vars.printys:
        if form.vars.reg_no_id == '':
            response.flash = 'Fill the empty fields!'
        else:
            record = db(db.repair_history.reg_no_id == form.vars.reg_no_id).select(db.repair_history.ALL).last()
            redirect(URL(r = request, c = "MaintenanceReports", f = "MaintenanceReport", args = record.id))
    query = db.vehicle.status_id != 1
    query &= db.vehicle.division_id == auth.user.division_id
    query &= db.repair_history.reg_no_id == db.vehicle.id
    query &= db.repair_history.reg_no_id == request.args(0)

    fields = [db.repair_history.reg_no_id, db.repair_history.invoice_date, db.repair_history.invoice_number, 
    db.repair_history.workshop_done, db.repair_history.mileage, db.repair_history.regular_maintenance, 
    db.repair_history.spare_parts, db.repair_history.statutory_expenses, db.repair_history.accident_repair, 
    db.repair_history.total_amount, db.repair_history.details]    

    if request.args(0):
        query = db.vehicle.status_id != 1
        query &= db.vehicle.division_id == auth.user.division_id
        query &= db.repair_history.reg_no_id == db.vehicle.id
        query &= db.repair_history.reg_no_id == request.args(0)

        row = []
        head = THEAD(TR(TH('#'),TH('Date'),TH('Invoice'),TH('Reg.No.'),TH('Workshop'),TH('Duration'),TH('Mileage'),TH('Lab'),TH('SP'),
            TH('SE'),TH('AR'),TH('Amount')))

        for n in db(query).select(db.repair_history.ALL):
            row.append(TR(TD(),TD(n.invoice_date),TD(n.invoice_number),TD(n.reg_no_id.reg_no),TD(n.workshop_done.workshop),TD(str(abs(n.date_time_out-n.date_time_in).days)+' days'),TD(locale.format('%d',n.mileage or 0, grouping = True)),
                TD(n.regular_maintenance),TD(n.spare_parts),TD(n.statutory_expenses),TD(n.accident_repair),TD(n.total_amount)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
        return dict(table = table, form=form)

        
    else:
        row = []

        query = db.vehicle.status_id != 1
        query &= db.vehicle.division_id == auth.user.division_id
        query &= db.repair_history.reg_no_id == db.vehicle.id

        head = THEAD(TR(TH('#'),TH('Date'),TH('Invoice'),TH('Reg.No.'),TH('Workshop'),TH('Duration'),TH('Mileage'),TH('Lab'),TH('SP'),
            TH('SE'),TH('AR'),TH('Amount')))

        for n in db(query).select(db.repair_history.ALL):
            row.append(TR(TD(),TD(n.invoice_date),TD(n.invoice_number),TD(n.reg_no_id.reg_no),TD(n.workshop_done.workshop),TD(str(abs(n.date_time_out-n.date_time_in).days)+' days'),TD(locale.format('%d',n.mileage or 0, grouping = True)),
                TD(n.regular_maintenance),TD(n.spare_parts),TD(n.statutory_expenses),TD(n.accident_repair),TD(n.total_amount)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
        return dict(table = table, form=form)



@auth.requires_membership('level_2_user')
def Fuel():
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict()

@auth.requires_membership('level_2_user')
def FuelExpensesForm():
    query = db.vehicle.division_id == auth.user.division_id
    form = SQLFORM.factory(
        Field('reg_no_id', requires = IS_IN_DB(db(query), db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.'),widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('date_expense', 'date', default = request.now, widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),
        Field('amount', 'decimal(10,2)', default = 00.00, widget = lambda field, value: SQLFORM.widgets.double.widget(field, value, _class='form-control')),
        Field('paid_by', requires = IS_IN_SET(['Cash','Credit','Fuel Card'], zero = 'Choose paid by'),widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('station', requires = IS_UPPER(),widget = lambda field, value: SQLFORM.widgets.string.widget(field, value, _class='form-control')),
        Field('remarks', requires = IS_UPPER(),widget = lambda field, value: SQLFORM.widgets.string.widget(field, value, _class='form-control')),
        Field('printys', 'boolean', default = True))
    if form.process().accepted:       
        db.fuel_expenses.insert(reg_no_id = form.vars.reg_no_id, date_expense = form.vars.date_expense,            
            amount = form.vars.amount, paid_by = form.vars.paid_by,
            station = form.vars.station, remarks = form.vars.remarks)
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = 'created reg.no. %s fuel expenses amounted QR %s' % (record.reg_no, 
                str(locale.format('%.2f', form.vars.amount, grouping = True))))       
        response.js =  "$('#tblFE').get(0).reload()" 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'New fuel expenses record save.', _class='white'),_class='alert alert-success') 

    elif form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 

    else: response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(form = form)

@auth.requires_membership('level_2_user')
def Mileage():
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict()

@auth.requires_membership('level_2_user')
def MileageForm():
    query = (db.vehicle.division_id == auth.user.division_id)
    form = SQLFORM.factory(
        Field('reg_no_id', requires = IS_IN_DB(db(query), db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.'), widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('given_month','date', default = request.now, widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),
        Field('current_mil', 'integer', requires = (IS_NOT_EMPTY(), IS_INT_IN_RANGE(1, 1000000)), widget = lambda field, value: SQLFORM.widgets.integer.widget(field, value, _class='form-control'))) 
    if form.process().accepted:  
        db.km_used.insert(reg_no_id = form.vars.reg_no_id, given_month = request.vars.given_month, current_mil = request.vars.current_mil)

        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now, person = '%s %s' % (auth.user.first_name, auth.user.last_name), action = 'created reg.no. %s odometer for the month of %s' % (record.reg_no, str((request.now).strftime('%B %Y'))))
        record.update_record(mileage = form.vars.current_mil)
        rows = db(db.km_used.reg_no_id == form.vars.reg_no_id).select(orderby = db.km_used.given_month)
        
        r = 1
        row = len(rows)
        while (r < row):
            rows[r].update_record(consumed_mil = rows[r].current_mil - rows[r-1].current_mil)
            r +=1

        response.js =  "$('#tblM').get(0).reload()"             
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'New mileage record save.', _class='white'),_class='alert alert-success') 

    elif form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 

    else: 
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 

    return dict(form = form)


@auth.requires_membership('level_2_user')
def MileageTable():

    query = db.vehicle.status_id != 1            
    query &= db.vehicle.division_id == auth.user.division_id
    query &= db.km_used.reg_no_id == db.vehicle.id
    head = THEAD(TR(TH('#'),TH('Month'),TH('Reg.No.'),TH('Odometer'),TH(_class='sorting_disabled')))
    row = []
    for o in db(query).select(db.km_used.ALL):
        pr_v = A(SPAN(_class = 'fa fa-print bigger-130'), _title="Print", _target="blank", _href=URL("Mileage","VehicleMileageReport", args=o.id),_class="blue")
        vi_v = A(SPAN(_class = 'fa fa-search bigger-130'), _title='View', _href="#", _class='green')
        btn_lnks = DIV(pr_v, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(o.given_month.strftime('%B, %Y')),TD(o.reg_no_id.reg_no),TD(locale.format('%d',o.current_mil or 0, grouping = True)),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _id='tblM',_class='table table-striped table-bordered table-hover')
    return dict(table = table)

@auth.requires_membership('level_2_user')
def HandOver():
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict()


@auth.requires_membership('level_2_user')
def HandOverForm():
    vehicles_accessories = IS_IN_SET(['Original Keys', 'Original Road Permit','Pertol Card', 'Spare Tyre', 'Tools (jack)'], multiple = True)
    query = (db.vehicle.division_id == auth.user.division_id)
    q_driver = (db.driver.division_id == auth.user.division_id)
    dep_id = (db.department.division_id == auth.user.division_id)
    db.vehicles_hand_over.id.readable = False 
    form = SQLFORM.factory(
        Field('reg_no_id', requires = IS_IN_DB(db(query), db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.'), widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('date_and_time', 'datetime', default=request.now, widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')), 
        Field('from_department_id', requires = IS_IN_DB(db(dep_id), db.department, '%(name)s', zero = 'Choose department'), widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('to_department_id', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose department'), widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('from_driver_id', requires = IS_IN_DB(db(q_driver), db.driver, '%(driver_name)s', zero = 'Choose driver'), widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('to_driver_id', requires = IS_IN_DB(db, db.driver, '%(driver_name)s', zero = 'Choose driver'), widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('mileage', default = 0, widget = lambda field, value: SQLFORM.widgets.integer.widget(field, value, _class='form-control')),
        #Field('vehicles_acc',  requires = vehicles_accessories, widget = lambda field, value: SQLFORM.widgets.multiple.widget(field, value, _id = 'form-field-select-4', _class = 'chosen-select form-control tag-input-style')),
        Field('vehicles_acc', 'list:string', requires = vehicles_accessories, widget = SQLFORM.widgets.checkboxes.widget),
        Field('remarks',requires = IS_UPPER(), widget = lambda field, value: SQLFORM.widgets.string.widget(field, value, _class='form-control')))
    if form.process().accepted:  
        db.vehicles_hand_over.insert(
            reg_no_id = form.vars.reg_no_id,
            date_and_time = form.vars.date_and_time,
            from_department_id = form.vars.from_department_id,
            to_department_id = form.vars.to_department_id,
            from_driver_id = form.vars.from_driver_id,
            to_driver_id = form.vars.to_driver_id,
            mileage = form.vars.mileage,
            vehicles_acc = form.vars.vehicles_acc,
            remarks = form.vars.remarks)
        record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name), 
            action = 'created reg.no. %s hand-over' % (record.reg_no))
        response.js =  "$('#tblHO').get(0).reload()"             
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'New hand-over record save.', _class='white'),_class='alert alert-success') 
    elif form.errors:
        response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 

    else: response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest Company Fleet', _class='white'),_class='alert alert-info') 
    return dict(form = form)

  
@auth.requires_membership('level_2_user')
def HandOverTable():
    query = db.vehicle.status_id != 1            
    query &= db.vehicle.division_id == auth.user.division_id
    query &= db.vehicles_hand_over.reg_no_id == db.vehicle.id

    row = []

    head = THEAD(TR(TH('#'),TH('Reg.No.'),TH('Date'), TH('F/Driver'),TH('T/Driver'),TH('Mileage'),TH(_class='sorting_disabled')))
    for h in db(query).select(db.vehicles_hand_over.ALL):
        pr_v = A(SPAN(_class = 'fa fa-print bigger-130'), _title="Print",_target='blank', _href=URL("Company","HandOverReport", args=h.reg_no_id), _class="blue")
        btn_view = A(SPAN(_class = 'fa fa-info-circle bigger-130 popover-info'), _class='blue',_tabindex='0', _role='button', 
            **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus', '_data-html':'true','_data-original-title':'<i class="ace-icon fa fa-info-circle blue"></i> Hand-Over Info','_data-content': hand_info(h.id)})
        btn_lnks = DIV(btn_view,pr_v, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(),TD(h.date_and_time.date()), TD(h.reg_no_id.reg_no),
            TD(h.from_driver_id.driver_name),TD(h.to_driver_id.driver_name),
            TD(h.mileage),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body],_id='tblHO', _class='table table-striped table-bordered table-hover')

    return dict( table = table)    

def hand_info(z = request.args(0)):
    for x in db(db.vehicles_hand_over.id == z).select():
        i = TABLE(*[
            TR(TD('From Dept.:'),TD(x.from_department_id.name)),
            TR(TD('To Dept.:'),TD(x.to_department_id.name)),
            TR(TD('Accessories: '), TD(str(', '.join(x.vehicles_acc)))), #str(', '.join(h.vehicles_acc
            TR(TD('Remarks.:'),TD(x.remarks))])
    table = str(XML(i, sanitize=False))
    return table

@auth.requires_membership('level_2_user')
def HandOverReport():
    for c in db(db.vehicle.id == request.args(0)).select(db.vehicle.ALL):
        c_info = [['Fleet Specification','','','Company Info',''],['Code:',c.vehicle_code,'','Company:',c.company_id.company],['Reg.No.:',c.reg_no,'','Division:',c.division_id.division],['Manufacturer:',c.vehicle_name_id.vehicle_name,'','Department:',c.department.name],['Model:', c.model,'', 'Owner:', c.owner.name]]   
        com_tbl=Table(c_info, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
        com_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3))]))

    for h in db(db.vehicles_hand_over.reg_no_id == request.args(0)).select(db.vehicles_hand_over.ALL):
        h_data = [['Details','','',''],
        ['Date',h.date_and_time,'',''],
        ['From Dept:',h.from_department_id.name,'',''],
        ['To Dept:',h.to_department_id.name,'',''],
        ['From Driver:',h.from_driver_id.driver_name,'',''],
        ['To Driver:',h.to_driver_id.driver_name,'',''],
        ['Mileage:',h.mileage,'',''],
        #['Details:',Paragraph(str(f.repair_history.details), styles["BodyText"]),'','','']]
        ['Accessories:',Paragraph(str(', '.join(h.vehicles_acc)), styles["BodyText"]),'',''],
        ['Remarks:',Paragraph(h.remarks, styles["BodyText"]),'','']]
        han_tbl=Table(h_data, colWidths=[100,190,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)#,  hAlign='LEFT')
        han_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,-1),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3))]))

    for s in db(db.vehicles_hand_over.reg_no_id == request.args(0)).select(db.vehicles_hand_over.ALL):
        s_data = [[s.from_driver_id.driver_name,'',s.to_driver_id.driver_name,'',''],['Signature','','Signature','','Checked and verified by']]
        sin_tbl=Table(s_data, colWidths=[150,30,150,30,150], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0,  hAlign='CENTER')
        sin_tbl.setStyle(TableStyle([('LINEBELOW',(0,0),(0,0),0.50, colors.Color(0, 0, 0, 0.2)),('ALIGNMENT',(0,0),(-1,-1),'CENTER'),
            ('LINEBELOW',(2,0),(2,0),0.50, colors.Color(0, 0, 0, 0.2)),('LINEBELOW',(4,0),(4,0),0.50, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),9)]))


        row.append(com_tbl)
        row.append(Spacer(1,.7*cm))  
        row.append(han_tbl)
        row.append(Spacer(1,.9*inch))  
        row.append(sin_tbl)
        
        doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'
        return pdf_data      


##############################################################################
#########                     R E P O R T                   ##################
##############################################################################

@auth.requires_membership('level_2_user')
def Summary(): 
    return dict()

def HeadRpt():
    for info in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):

        table = TABLE(THEAD(TR(TH('Fleet Specification',_colspan='2',_width='40%',_class='tblhead'),TH(_width='10%'),TH('Company Info',_colspan='2',_width='40%',_class='tblhead lftborder topborder'))),
            TBODY(TR(TD('Code:'),TD(info.vehicle_code,_class='btmborder'),TD(''),TD('Company:', _class='lftborder'),TD(info.company_id.company,_class='rtborder')),
                TR(TD('Reg.No.:'),TD(info.reg_no,_class='btmborder'),TD(''),TD('Division:', _class='lftborder'),TD(info.division_id.division,_class='rtborder')),
                TR(TD('Manufacturer:'),TD(info.vehicle_name_id.vehicle_name,_class='btmborder'),TD(''),TD('Department:', _class='lftborder'),TD(info.department.name,_class='rtborder')),
                TR(TD('Model:'),TD(info.model,_class='btmborder'),TD(''),TD('Owner:', _class='lftborder btmborder'),TD(info.owner.name,_class='rtborder btmborder' ))),_class='border-collapse: collapse;',_width='100%')
    return table



@auth.requires_membership('level_2_user')
def VehicleSummaryReport(): 
    query = (db.vehicle.division_id == auth.user.division_id)
    form = FORM(DIV(
        DIV(DIV(DIV('Reg.No.',_class='input-group-addon'),SELECT(_name='reg_no_id', *[OPTION(r.reg_no, _value=r.id) for r in db(query).select(db.vehicle.ALL, orderby=db.vehicle.reg_no)],_class='form-control', widget=SQLFORM.widgets.options.widget),_class='input-group'),_class='form-group', _id='reg_no_id'),
        DIV(DIV(DIV('Date Range:',_class='input-group-addon'),INPUT(_id='start_date', _class='date form-control', _value=request.now.date(),_name='start_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),
            SPAN(SPAN(_class='fa fa-exchange'),_class='input-group-addon'),
            INPUT(_id='end_date', _class='date form-control', _value=request.now.date(),_name='end_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),_class='input-daterange input-group'),_class='form-group'),
        DIV(_class='space space-8'),INPUT(_type='submit', _value='submit', _class='btn btn-primary')))
    
    pdf_link = FORM(INPUT(_type='image', _title = 'Print',  _src = URL('static','images/1475070815_print_16.png'), _width="24", _height="24", _style="margin-top:8px;"), 
        hidden = dict(reg_no_id = request.vars.reg_no_id,start_date = request.vars.start_date,end_date = request.vars.end_date), _action = 'VehicleSummaryReport.pdf', _target = '_blank')

    if request.extension == 'pdf' or form.process().accepted:
        query = db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL)
        f = db.fuel_expenses.reg_no_id == request.vars.reg_no_id
        f &= db.fuel_expenses.date_expense >= request.vars.start_date
        f &= db.fuel_expenses.date_expense <= request.vars.end_date
        
        r = db.repair_history.reg_no_id == request.vars.reg_no_id
        r &= db.repair_history.invoice_date >= request.vars.start_date
        r &= db.repair_history.invoice_date <= request.vars.end_date
        
        k = db.km_used.reg_no_id == request.vars.reg_no_id
        k &= db.km_used.given_month >= request.vars.start_date
        k &= db.km_used.given_month <= request.vars.end_date

        n = db.insured_vehicles.reg_no_id == request.vars.reg_no_id
        n &= db.insured_vehicles.policy_no_id == db.insurance_policy.id
        n &= db.insurance_policy.status_id == 1
        n &= db.insurance_policy.from_period_covered >= request.vars.start_date
        n &= db.insurance_policy.from_period_covered <= request.vars.end_date

        a = db.ads_vehicle.reg_no_id == request.vars.reg_no_id
        a &= db.ads_vehicle.license_no_id == db.advertisement.id
        a &= db.advertisement.status_id == 1
        a &= db.advertisement.from_expiry_date >= request.vars.start_date
        a &= db.advertisement.from_expiry_date <= request.vars.end_date

        vehicle_info = db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL)
        try:

            cost_km = main_exp = total_run_cost = grand_total =0
            ins = db.insured_vehicles.amount.sum().coalesce_zero()
            ins_expenses = db(n).select(ins).first()[ins]

            ads = db.ads_vehicle.amount.sum().coalesce_zero()
            ads_exp = db(a).select(ads).first()[ads]

            fuel = db.fuel_expenses.amount.sum().coalesce_zero()
          
            fuel_expenses = db(f).select(fuel).first()[fuel]
           
            km = db.km_used.consumed_mil.sum().coalesce_zero()
            total_km = db(k).select(km).first()[km]
            
        
            r_mai = db.repair_history.regular_maintenance.sum().coalesce_zero()
            a_rep = db.repair_history.accident_repair.sum().coalesce_zero()
            s_exp = db.repair_history.statutory_expenses.sum().coalesce_zero()
            s_parts = db.repair_history.spare_parts.sum().coalesce_zero()
            repair = db.repair_history.total_amount.sum().coalesce_zero()
        
            r_mai = db(r).select(r_mai).first()[r_mai]
            a_rep = db(r).select(a_rep).first()[a_rep]
            s_exp = db(r).select(s_exp).first()[s_exp]
            s_parts = db(r).select(s_parts).first()[s_parts]
            repair_expenses = db(r).select(repair).first()[repair]
        
            
            cost_km = fuel_expenses / total_km
            main_exp = s_parts + r_mai + a_rep
            grand_total = fuel_expenses + repair_expenses + ads_exp + ins_expenses
        
            total_run_cost = grand_total / total_km            

        except Exception, e:           
            total_run_cost = float('0')
            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Warning: '), 'No mileage entered between date range.', _class='white'),_class='alert alert-warning') 
            return dict(form = form, table = '')
        
        else:
            table = HeadRpt()
            table += DIV(_class='hr hr8 hr-single hr-dotted')        

            for d in query:
                table += TABLE(TR(TD('Mileage:',_colspan='4')),
                    TR(TD(),TD('Total Mileage For The Period: '),TD(locale.format('%d',total_km or 0, grouping = True),_align='right'),TD()),
                    TR(TD('Fuel Expenses:',_colspan='4')),
                    TR(TD(),TD('Total Amount:'),TD(),TD(locale.format('%.2f', fuel_expenses or 0, grouping = True),_align='right')),
                    TR(TD(),TD('Fuel cost/km. expenses'),TD(locale.format('%.2f', cost_km or 0, grouping = True),_align='right'),TD()),
                    TR(TD('Repair & Maintenance Expenses',_colspan='4')),
                    TR(TD(),TD('Parts'),TD(locale.format('%.2f', s_parts or 0, grouping = True),_align='right'),TD()),
                    TR(TD(),TD('Labour'),TD(locale.format('%.2f', r_mai or 0, grouping = True),_align='right'),TD()),
                    TR(TD(),TD('Accident Repair'),TD(locale.format('%.2f', a_rep or 0, grouping = True),_align='right'),TD()),
                    TR(TD(),TD('Total Amount'),TD(),TD(locale.format('%.2f', main_exp or 0, grouping = True),_align='right')),
                    TR(TD(),TD('Total Statutory Expenses'),TD(),TD(locale.format('%.2f', s_exp or 0, grouping = True),_align='right')),
                    TR(TD('Insurance Expenses',_colspan='4')),
                    TR(TD(),TD('Total Amount'),TD(),TD(locale.format('%.2f', ins_expenses or 0, grouping = True),_align='right')),
                    TR(TD('Advertisement Expenses',_colspan='4')),
                    TR(TD(),TD('Total Amount'),TD(),TD(locale.format('%.2f', ads_exp or 0, grouping = True),_align='right')),
                    TR(TD('Running Cost Expenses',_colspan='4')),
                    TR(TD(),TD('Total running cost/km expenses.'),TD(locale.format('%.2f', total_run_cost or 0, grouping = True),_align='right'),TD()),
                    TR(TD(H4('GRAND TOTAL'),_colspan='3'),TD(H4(locale.format('%.2f', grand_total or 0, grouping = True)),_align='right')),_class='table table-bordered', _width='50%')
                table = DIV(DIV(H4('Print Preview',_class='widget-title'),
                    DIV(pdf_link, _class='widget-toolbar'),_class='widget-header'),                        
                    DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),
                    _class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)
        finally:            

            if request.extension == 'pdf':
                for c in query:
                    c_info = [['Fleet Specification','','','Company Info',''],
                    ['Code:',c.vehicle_code,'','Company:',c.company_id.company],
                    ['Reg.No.:',c.reg_no,'','Division:',c.division_id.division],
                    ['Manufacturer:',c.vehicle_name_id.vehicle_name,'','Department:',c.department.name],
                    ['Model:', c.model,'', 'Owner:', c.owner.name]]

                    smr = [['Duration: ' + request.vars.start_date + ' - '+request.vars.end_date,'','',''],
                    ['Mileage','','',''],
                    ['','Total mileage for the period',locale.format('%d', total_km or 0, grouping=True),''],
                    ['Fuel Expenses','','',''],
                    ['','Total Amount','',locale.format('%.2f', fuel_expenses or 0, grouping = True)],
                    ['','Fuel cost/km. expenses',locale.format('%.2f', cost_km or 0, grouping = True),''],
                    ['Repair & Maintenance Expenses','','',''],
                    ['','Parts',locale.format('%.2f', s_parts or 0, grouping = True),''],
                    ['','Labour',locale.format('%.2f', r_mai or 0, grouping = True),''],
                    ['','Accident Repair',locale.format('%.2f', a_rep or 0, grouping = True),''],
                    ['','Total Amount','',locale.format('%.2f', main_exp or 0, grouping = True)],
                    ['','Total Statutory Expenses','',locale.format('%.2f', s_exp or 0, grouping = True)],
                    ['Insurance Expenses','','',''],
                    ['','Total Amount','',locale.format('%.2f', ins_expenses or 0, grouping = True)],
                    ['Advertisement Expenses','','',''],
                    ['','Total Amount','',locale.format('%.2f', ads_exp or 0, grouping = True)],
                    ['Running Cost Expenses','','',''],
                    ['','Total running cost/km expenses.',locale.format('%.2f', total_run_cost or 0, grouping = True),''],
                    ['GRAND TOTAL','','',locale.format('%.2f', grand_total or 0, grouping = True)]]

                com_tbl=Table(c_info, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
                com_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),
                    ('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
                    ('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),
                    ('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3))]))
                row.append(com_tbl)

                row.append(Spacer(1,.7*cm))  
                
                smr_tbl=Table(smr, colWidths=[40,290,100,100], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
                smr_tbl.setStyle(TableStyle([('TEXTCOLOR',(0,0),(0,16),colors.gray),('BOX',(0,1),(-1,-1),0.7,colors.Color(0, 0, 0, 0.3)),#('GRID',(0,0),(-1,-1),0.7,colors.Color(0, 0, 0, 0.3)),
                ('SPAN',(0,0),(3,0)),('TOPPADDING',(0,0),(0,3),10),
                ('SPAN',(0,1),(3,1)),('TOPPADDING',(0,1),(3,1),10),
                ('SPAN',(0,3),(3,3)),('TOPPADDING',(0,3),(3,3),10),
                ('SPAN',(0,6),(3,6)),('TOPPADDING',(0,6),(3,6),10),
                ('SPAN',(0,12),(3,12)),('TOPPADDING',(0,12),(3,12),10),
                ('SPAN',(0,14),(3,14)),('TOPPADDING',(0,14),(3,14),10),
                ('SPAN',(0,16),(3,16)),('TOPPADDING',(0,16),(3,16),10),('BOTTOMPADDING',(0,17),(3,17),10),
                ('SPAN',(0,18),(2,18)),('TOPPADDING',(0,18),(3,18),5),('BOTTOMPADDING',(0,18),(3,18),5),('ALIGN',(2,1),(3,18),'RIGHT'),('RIGHTPADDING',(2,1),(3,18),40),
                ('FONTSIZE',(0,0),(-1,-1),9),('FONTSIZE',(0,18),(3,18),10),('BACKGROUND',(0,18),(3,18),colors.Color(0, 0, 0, 0.3))]))#,('TEXTCOLOR',(0,0),(4,0),colors.gray),('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,1),(4,1),colors.Color(0, 0, 0, 0.2))]))
                row.append(smr_tbl)

                doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
                pdf_data = open(tmpfilename,"rb").read()
                os.unlink(tmpfilename)
                response.headers['Content-Type']='application/pdf'
                response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Enter Reg.No. & Date Range', _class='white'),_class='alert alert-info') 
                return pdf_data            
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Enter Reg.No. & Date Range', _class='white'),_class='alert alert-info') 
    return dict(form = form, table = '')    

def DivHeadRpt():
    
    fle_hand = db(db.vehicles_hand_over.reg_no_id == request.vars.reg_no_id).select(db.vehicles_hand_over.ALL, orderby = ~db.vehicles_hand_over.date_and_time).first()

    if fle_hand == None:
        fle_hand_dri = 'None'
        driver_license_expiration = 'None'
        driver_license_no = 'None'
        
    else:
        fle_hand_dri = fle_hand.to_driver_id.driver_name
        dri_info = db(db.driver.id == fle_hand.to_driver_id).select(db.driver.ALL).first()
        driver_license_expiration = dri_info.expiry_date
        driver_license_no = dri_info.driver_id

    for info in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):
        table = TABLE(THEAD(TR(TH('Fleet Specification',_colspan='2',_class='tblhead'),TH(_width='5%'),TH('Company Info',_colspan='2',_class='tblhead lftborder topborder'))),
            TBODY(TR(TD('Code:'),TD(info.vehicle_code,_class='btmborder'),TD(''),TD('Company:', _class='lftborder'),TD(info.company_id.company,_class='rtborder')),
                TR(TD('Reg.No.:'),TD(info.reg_no,_class='btmborder'),TD(''),TD('Division:', _class='lftborder'),TD(info.division_id.division,_class='rtborder')),
                TR(TD('Manufacturer:'),TD(info.vehicle_name_id.vehicle_name,_class='btmborder'),TD(''),TD('Department:', _class='lftborder'),TD(info.department.name,_class='rtborder')),
                TR(TD('Model:'),TD(info.model,_class='btmborder'),TD(''),TD('Owner:', _class='lftborder btmborder'),TD(info.owner.name,_class='rtborder btmborder' )),
                TR(TD('Mileage:'),TD(info.mileage,_class='btmborder'),TD(),TD(),TD()),
                TR(TD('Category:'),TD(info.category_id.category,_class='btmborder'),TD(),TH('Driver Info', _colspan='2',_class='tblhead'),TH()),
                TR(TD('Road Permit:'),TD(info.exp_date,_class='btmborder'),TD(),TD('Driver Name:'),TD(fle_hand_dri,_class='btmborder')),
                TR(TD('Date Purchase:'),TD(info.date_of_sale,_class='btmborder'),TD(),TD('License Expiration:'),TD(driver_license_expiration, _class='btmborder')),
                TR(TD('Fleet Cost:'),TD(info.value_purchase,_class='btmborder'),TD(),TD('Driver License:'),TD(driver_license_no,_class='btmborder')),
                TR(TD('Status:'),TD(info.status_id.status,_class='btmborder'),TD(),TD(),TD())),_class='border-collapse: collapse;',_width='100%')
    
    return table

@auth.requires_membership('level_2_user')
def DivisionCostPerYear():
    query = (db.vehicle.division_id == auth.user.division_id)
    form = FORM(DIV(
        DIV(DIV(DIV('Reg.No.',_class='input-group-addon'),SELECT(_name='reg_no_id', *[OPTION(r.reg_no, _value=r.id) for r in db(query).select(db.vehicle.ALL, orderby=db.vehicle.reg_no)],_class='form-control', widget=SQLFORM.widgets.options.widget),_class='input-group'),_class='form-group', _id='reg_no_id'),
        DIV(DIV(DIV('Date Range:',_class='input-group-addon'),INPUT(_id='start_date', _class='date form-control', _value=request.now.date(),_name='start_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),
            SPAN(SPAN(_class='fa fa-exchange'),_class='input-group-addon'),
            INPUT(_id='end_date', _class='date form-control', _value=request.now.date(),_name='end_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),_class='input-daterange input-group'),_class='form-group'),
        DIV(_class='space space-8'),
        INPUT(_type='submit', _value='submit', _class='btn btn-primary')))
    pdf_link = FORM(INPUT(_type='image', _value = 'Print', _title = 'Print',  _src = URL('static','images/1475070815_print_16.png'), _width="24", _height="24", _style="margin-top:8px;"),     hidden = dict(reg_no_id = request.vars.reg_no_id,start_date = request.vars.start_date,end_date = request.vars.end_date), _action = 'DivisionCostPerYear.pdf', _target = '_blank')
    if request.extension == 'pdf' or form.process().accepted:
        que_fleet = db.vehicle.id == request.vars.reg_no_id
        que_fleet &= db.vehicles_hand_over.reg_no_id == request.vars.reg_no_id
        
        que_cost = db.repair_history.reg_no_id == request.vars.reg_no_id
        que_cost &= db.repair_history.invoice_date >= request.vars.start_date
        que_cost &= db.repair_history.invoice_date <= request.vars.end_date        
        
        yearly_total = db.repair_history.total_amount.sum().coalesce_zero()
        grand_total = db(que_cost).select(yearly_total).first()[yearly_total]      


        fle_hand = db(db.vehicles_hand_over.reg_no_id == request.vars.reg_no_id).select(db.vehicles_hand_over.ALL, orderby = ~db.vehicles_hand_over.date_and_time).first()

        if fle_hand == None:
            fle_hand_dri = 'None'
            driver_license_expiration = 'None'
            driver_license_no = 'None'
            
        else:
            fle_hand_dri = fle_hand.to_driver_id.driver_name
            dri_info = db(db.driver.id == fle_hand.to_driver_id).select(db.driver.ALL).first()
            driver_license_expiration = dri_info.expiry_date
            driver_license_no = dri_info.driver_id

        if grand_total == 0:
            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Warning: '), 'Empty maintenance expenses entered between date range.', _class='white'),_class='alert alert-warning') 
            return dict(form = form , table = '')
        
        elif request.extension == 'pdf':
            row = []


            for c in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):
                c_info = [['Fleet Specification','','','Company Info',''],
                ['Code:',c.vehicle_code,'','Company:',c.company_id.company],
                ['Reg.No.:',c.reg_no,'','Division:',c.division_id.division],
                ['Manufacturer:',c.vehicle_name_id.vehicle_name,'','Department:',c.department.name],
                ['Model:', c.model,'', 'Owner:', c.owner.name],
                ['Mileage:', c.mileage,'', '', ''],
                ['Category:', c.category_id.category, '','Driver Info', ''],
                ['Road Permit:', c.exp_date,'', 'Driver Name:', fle_hand_dri],
                ['Date Purchase:', c.date_of_sale,'', 'License Expiration:', driver_license_expiration],
                ['Fleet Cost:', c.value_purchase, '','Driver License:', driver_license_no],
                ['Status:', c.status_id.status, '', '','']]

            com_tbl=Table(c_info, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            com_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,-1),0.50, colors.Color(0, 0, 0, 0.2)),('LINEBELOW',(4,7),(4,-2),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),
                ('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
                ('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),
                ('BACKGROUND',(3,6),(4,6),colors.Color(0, 0, 0, 0.3)),
                ('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3))]))
            row.append(com_tbl)
            row.append(Spacer(1,.7*cm)) 
            ctr = 0
            q_info = [['Year','Amount']]
            for q in db(que_cost).select(db.repair_history.invoice_date.year(), yearly_total, orderby=~db.repair_history.invoice_date.year(), groupby = db.repair_history.invoice_date.year(), distinct = True):
                q_info.append([q[db.repair_history.invoice_date.year()],locale.format('%.2F',q[yearly_total] or 0, grouping = True)])
            
            q_tbl=Table(q_info, colWidths=[100,430], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            q_tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.7,colors.Color(0, 0, 0, 0.3)),
                ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),
                ('ALIGN',(1,1),(1,-1),'RIGHT'),
                ('ALIGN',(0,0),(1,0),'CENTER'),('ALIGN',(0,0),(0,-1),'CENTER'),
                ('FONTSIZE',(0,0),(1,-1),9)]))
            row.append(q_tbl) 

            row.append(Spacer(1,.7*cm)) 
            g_info = [['Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,'GRAND TOTAL: ', locale.format('%.2F',grand_total or 0, grouping = True)]]
            g_tbl=Table(g_info, colWidths=[330,100,100], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            g_tbl.setStyle(TableStyle([
                ('LINEABOVE', (0,0), (-1,0), 0.7,colors.Color(0, 0, 0, 0.3)),
                ('FONTSIZE',(0,0),(1,0),8),
                ('FONTSIZE',(1,0),(2,0),12),
                ('ALIGN',(2,0),(2,0),'RIGHT')]))
            row.append(g_tbl) 

            row.append(Spacer(1,.7*cm)) 
            q_img = [['Front','Rear']]
            for i in db(db.v_photos.reg_no_id == request.vars.reg_no_id).select(db.v_photos.ALL):
                front_img = os.path.join(request.folder,'uploads', i.photo)
                rear_img = os.path.join(request.folder,'uploads', i.photo2)
                
                if not os.path.exists(front_img):
                    front_img = 'None'
                else:
                    front_img = Image(front_img, width = 250, height = 170)
                if not os.path.exists(rear_img):
                    rear_img = 'None'
                else:
                    rear_img = Image(rear_img or None,width=250,height=170)
                q_img.append([front_img, rear_img])
            q_tbl=Table(q_img, colWidths=[265,265], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)

            row.append(q_tbl)

            doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
            pdf_data = open(tmpfilename,"rb").read()
            os.unlink(tmpfilename)
            response.headers['Content-Type']='application/pdf'                
            return pdf_data            
        else:
            head = THEAD(TR(TH('Year'),TH('Amount')))
            foot = THEAD(TR(TD(H4('Grand Total Amount: '), _align = 'right'),TD(H4(str('QR ' + locale.format('%.2F', grand_total, grouping = True))))))
            row = []        
            for q in db(que_cost).select(db.repair_history.invoice_date.year(), yearly_total, orderby=~db.repair_history.invoice_date.year(), groupby = db.repair_history.invoice_date.year(), distinct = True):
                row.append(TR(TD(q[db.repair_history.invoice_date.year()]),TD(locale.format('%.2F',q[yearly_total] or 0, grouping = True),_align='right')))
            body = TBODY(*row)
            table = DivHeadRpt()
            table += DIV(_class='space-2')
            table += DIV(_class='space-2')
            table += TABLE(*[head, body], _class='table table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            for p in db(db.v_photos.reg_no_id == request.vars.reg_no_id).select(db.v_photos.ALL):
                table += TABLE(TR(TD('Front'),TD('Rear')),TR(TD(IMG(_src = URL('default','download', args = p.photo), _width='300', _height='190', _align='center'),_width='50%'),TD(IMG(_src = URL('default','download', args = p.photo2), _width='300', _height='190', _align='center'),_width='50%')),_width='100%')
            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(pdf_link, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)            
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Please choose Reg.No. & enter date range', _class='white'),_class='alert alert-info') 
    return dict(form = form, table = '')  

@auth.requires_membership('level_2_user')
def DivisionMaintenanceReport():
    
    query = (db.vehicle.division_id == auth.user.division_id)
    form = FORM(DIV(
        DIV(DIV(DIV('Reg.No.',_class='input-group-addon'),SELECT(_name='reg_no_id', *[OPTION(r.reg_no, _value=r.id) for r in db(query).select(db.vehicle.ALL, orderby=db.vehicle.reg_no)],_class='form-control', widget=SQLFORM.widgets.options.widget),_class='input-group'),_class='form-group', _id='reg_no_id'),
        DIV(DIV(DIV('Date Range:',_class='input-group-addon'),INPUT(_id='start_date', _class='date form-control', _value=request.now.date(),_name='start_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),
            SPAN(SPAN(_class='fa fa-exchange'),_class='input-group-addon'),
            INPUT(_id='end_date', _class='date form-control', _value=request.now.date(),_name='end_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),_class='input-daterange input-group'),_class='form-group'),
        DIV(_class='space space-8'),
        INPUT(_type='submit', _value='submit', _class='btn btn-primary')))
    pdf_link = FORM(INPUT(_type='image', _value = 'Print', _title = 'Print',  _src = URL('static','images/1475070815_print_16.png'), _width="24", _height="24", _style="margin-top:8px;"),     hidden = dict(reg_no_id = request.vars.reg_no_id,start_date = request.vars.start_date,end_date = request.vars.end_date), _action = 'DivisionMaintenanceReport.pdf', _target = '_blank')
    if request.extension == 'pdf' or form.process().accepted:
        query = db.repair_history.reg_no_id == request.vars.reg_no_id
        query &= db.repair_history.invoice_date >= request.vars.start_date
        query &= db.repair_history.invoice_date <= request.vars.end_date
        
        grand_total = db.repair_history.total_amount.sum().coalesce_zero()
        grand_total = db(query).select(grand_total).first()[grand_total]

        if grand_total == 0:
            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Warning: '), 'Empty maintenance expenses entered between date range.', _class='white'),_class='alert alert-warning') 
            return dict(form = form , table = '')
        
        elif request.extension == 'pdf':
            row = []
            for c in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):
                c_info = [['Fleet Specification','','','Company Info',''],
                ['Code:',c.vehicle_code,'','Company:',c.company_id.company],
                ['Reg.No.:',c.reg_no,'','Division:',c.division_id.division],
                ['Manufacturer:',c.vehicle_name_id.vehicle_name,'','Department:',c.department.name],
                ['Model:', c.model,'', 'Owner:', c.owner.name]]

            com_tbl=Table(c_info, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            com_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),
                ('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
                ('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),
                ('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3))]))
            row.append(com_tbl)
            row.append(Spacer(1,.7*cm)) 
            ctr = 0
            q_info = [['#','Date', 'Invoice','Workshop', 'Mileage', 'Amount']]
            for q in db(query).select(db.repair_history.ALL, orderby=~db.repair_history.invoice_date):
                ctr += 1
                q_info.append([ctr, q.invoice_date, q.invoice_number, q.workshop_done.workshop, locale.format('%d',q.mileage or 0, grouping = True), locale.format('%.2F', q.total_amount, grouping = True )])
            
            q_tbl=Table(q_info, colWidths=[20,80,100,150,80,100], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            q_tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.7,colors.Color(0, 0, 0, 0.3)),
                ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),
                ('ALIGN',(5,1),(5,-1),'RIGHT'),
                ('ALIGN',(0,0),(5,0),'CENTER'),
                ('FONTSIZE',(0,0),(5,-1),9),]))
            row.append(q_tbl) 

            row.append(Spacer(1,.7*cm)) 
            g_info = [['Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,'GRAND TOTAL: ', locale.format('%.2F',grand_total or 0, grouping = True)]]
            g_tbl=Table(g_info, colWidths=[330,100,100], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            g_tbl.setStyle(TableStyle([
                ('LINEABOVE', (0,0), (-1,0), 0.7,colors.Color(0, 0, 0, 0.3)),
                ('FONTSIZE',(0,0),(1,0),8),
                ('FONTSIZE',(1,0),(2,0),12),
                ('ALIGN',(2,0),(2,0),'RIGHT')]))
            row.append(g_tbl) 

            doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
            pdf_data = open(tmpfilename,"rb").read()
            os.unlink(tmpfilename)
            response.headers['Content-Type']='application/pdf'                
            return pdf_data            
        else:
            head = THEAD(TR(TH('#'),TH('Date'),TH('Invoice #'),TH('Workshop'),TH('Mileage'),TH('Amount')))
            foot = THEAD(TR(TD(H4('Grand Total Amount: '), _colspan = '7', _align = 'right'), 
                TD(H4(str('QR ' + locale.format('%.2F', grand_total, grouping = True))))))
            
            row = []        
            ctr = 0
            for q in db(query).select(db.repair_history.ALL, orderby=~db.repair_history.invoice_date):
                ctr += 1
                row.append(TR(TD(ctr),TD(q.invoice_date),TD(q.invoice_number),TD(q.workshop_done.workshop),TD(locale.format('%d',q.mileage or 0, grouping = True)),TD(locale.format('%.2F', q.total_amount, grouping = True ), _align = 'right')))            
            body = TBODY(*row)
            table = HeadRpt()
            table += DIV(_class='space-2')
            table += DIV(_class='space-2')
            table += TABLE(*[head, body], _class='table table-striped table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(pdf_link, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)            
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Please choose Reg.No. & enter date range', _class='white'),_class='alert alert-info') 
    return dict(form = form, table = '')    

@auth.requires_login()
def DivisionFuelReport():
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Enter Reg.No. & Date Range', _class='white'),_class='alert alert-info') 
    query = (db.vehicle.division_id == auth.user.division_id)
    form = FORM(DIV(
        DIV(DIV(DIV('Reg.No.',_class='input-group-addon'),SELECT(_name='reg_no_id', *[OPTION(r.reg_no, _value=r.id) for r in db(query).select(db.vehicle.ALL, orderby=db.vehicle.reg_no)],_class='form-control', widget=SQLFORM.widgets.options.widget),_class='input-group'),_class='form-group', _id='reg_no_id'),
        DIV(DIV(DIV('Date Range:',_class='input-group-addon'),INPUT(_id='start_date', _class='date form-control', _value=request.now.date(),_name='start_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),
            SPAN(SPAN(_class='fa fa-exchange'),_class='input-group-addon'),
            INPUT(_id='end_date', _class='date form-control', _value=request.now.date(),_name='end_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),_class='input-daterange input-group'),_class='form-group'),
        DIV(_class='space space-8'),
        INPUT(_type='submit', _value='submit', _class='btn btn-primary')))
    pdf_link = FORM(INPUT(_type='image', _value = 'Print', _title = 'Print',  _src = URL('static','images/1475070815_print_16.png'), _width="24", _height="24", _style="margin-top:8px;"),     hidden = dict(reg_no_id = request.vars.reg_no_id,start_date = request.vars.start_date,end_date = request.vars.end_date), _action = 'DivisionFuelReport.pdf', _target = '_blank')
    if request.extension == 'pdf' or form.process().accepted:
        query = db.fuel_expenses.reg_no_id == request.vars.reg_no_id
        query &= db.fuel_expenses.date_expense >= request.vars.start_date
        query &= db.fuel_expenses.date_expense <= request.vars.end_date
        
        grand_total = db.fuel_expenses.amount.sum().coalesce_zero()
        grand_total = db(query).select(grand_total).first()[grand_total]
        
        if grand_total == 0:
            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Warning: '), 'Empty fuel expenses entered between date range.', _class='white'),_class='alert alert-warning') 
            return dict(form = form , table = '')
        
        elif request.extension == 'pdf':
            row = []
            for c in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):
                c_info = [['Fleet Specification','','','Company Info',''],
                ['Code:',c.vehicle_code,'','Company:',c.company_id.company],
                ['Reg.No.:',c.reg_no,'','Division:',c.division_id.division],
                ['Manufacturer:',c.vehicle_name_id.vehicle_name,'','Department:',c.department.name],
                ['Model:', c.model,'', 'Owner:', c.owner.name]]

            com_tbl=Table(c_info, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            com_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),
                ('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
                ('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),
                ('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3))]))
            row.append(com_tbl)
            row.append(Spacer(1,.7*cm)) 
            
            ctr = 0
            
            q_info = [['#','Date', 'Amount','Paid by', 'Station']]
            for q in db(query).select(db.fuel_expenses.ALL, orderby = ~db.fuel_expenses.date_expense):
                ctr += 1
                #ctr),TD(q.date_expense),TD(locale.format('%.2F', q.amount or 0, grouping = True),_align = 'right'),TD(q.paid_by), TD(q.station)))
                q_info.append([ctr, q.date_expense, locale.format('%.2F', q.amount or 0, grouping = True), q.paid_by, q.station])
            
            
            q_tbl=Table(q_info, colWidths=[25,80,100,100,225], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            q_tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.7,colors.Color(0, 0, 0, 0.3)),
                ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),
                ('ALIGN',(2,1),(2,-1),'RIGHT'),
                ('FONTSIZE',(0,0),(-1,-1),9),
                ('ALIGN',(0,0),(-1,0),'CENTER')]))
            row.append(q_tbl)            

            row.append(Spacer(1,.7*cm)) 
            g_info = [['Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,'GRAND TOTAL: ', locale.format('%.2F',grand_total or 0, grouping = True)]]
            g_tbl=Table(g_info, colWidths=[330,100,100], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            g_tbl.setStyle(TableStyle([
                ('LINEABOVE', (0,0), (-1,0), 0.7,colors.Color(0, 0, 0, 0.3)),
                ('FONTSIZE',(0,0),(1,0),8),
                ('FONTSIZE',(1,0),(2,0),12),
                ('ALIGN',(2,0),(2,0),'RIGHT')]))
            row.append(g_tbl) 

            doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
            pdf_data = open(tmpfilename,"rb").read()
            os.unlink(tmpfilename)
            response.headers['Content-Type']='application/pdf'                
            return pdf_data            
        else:

            head = THEAD(TR(TH('No.'),TH('Date'),TH('Amount'),TH('Paid by'),TH('Station'), _bgcolor='#E0E0E0'))
            foot = THEAD(TR(TD(H4('Grand Total Amount: '), _colspan = '4', _align = 'right'), 
                TD(H4(str('QR ' + locale.format('%.2F', grand_total, grouping = True))))))

            r = []
            ctr = 0
            veh_query = db(query).select(db.fuel_expenses.ALL, orderby = ~db.fuel_expenses.date_expense)
            for q in veh_query:
                ctr += 1
                r.append(TR(TD(ctr),TD(q.date_expense),TD(locale.format('%.2F', q.amount or 0, grouping = True),_align = 'right'),TD(q.paid_by), TD(q.station)))
            body = TBODY(*r)
            table = HeadRpt()
            table += DIV(_class='space-2')
            table += DIV(_class='space-2')            
            table += TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')
            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(pdf_link, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)    
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Please choose Reg.No. & enter date range', _class='white'),_class='alert alert-info') 
    return dict(form = form, table = '')    

@auth.requires_membership('level_2_user')
def DivisionMileageReport():
    query = (db.vehicle.division_id == auth.user.division_id)
    form = FORM(DIV(
        DIV(DIV(DIV('Reg.No.',_class='input-group-addon'),SELECT(_name='reg_no_id', *[OPTION(r.reg_no, _value=r.id) for r in db(query).select(db.vehicle.ALL, orderby=db.vehicle.reg_no)],_class='form-control', widget=SQLFORM.widgets.options.widget),_class='input-group'),_class='form-group', _id='reg_no_id'),
        DIV(DIV(DIV('Date Range:',_class='input-group-addon'),INPUT(_id='start_date', _class='date form-control', _value=request.now.date(),_name='start_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),
            SPAN(SPAN(_class='fa fa-exchange'),_class='input-group-addon'),
            INPUT(_id='end_date', _class='date form-control', _value=request.now.date(),_name='end_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),_class='input-daterange input-group'),_class='form-group'),
        DIV(_class='space space-8'),
        INPUT(_type='submit', _value='submit', _class='btn btn-primary')))
    pdf_link = FORM(INPUT(_type='image', _value = 'Print', _title = 'Print',  _src = URL('static','images/1475070815_print_16.png'), _width="24", _height="24", _style="margin-top:8px;"),     hidden = dict(reg_no_id = request.vars.reg_no_id,start_date = request.vars.start_date,end_date = request.vars.end_date), _action = 'DivisionMileageReport.pdf', _target = '_blank')
    if request.extension == 'pdf' or form.process().accepted:
        rows = db(db.km_used.reg_no_id == request.vars.reg_no_id).select(orderby = db.km_used.given_month)
        r = 1
        row = len(rows)
        while (r < row):
            rows[r].update_record(consumed_mil = rows[r].current_mil - rows[r-1].current_mil)
            r +=1
        
        query = db.km_used.reg_no_id == request.vars.reg_no_id
        query &= db.km_used.given_month >= request.vars.start_date
        query &= db.km_used.given_month <= request.vars.end_date
        
        v_mileage = db(query).select(db.km_used.ALL, orderby = ~db.km_used.given_month)
        if len(v_mileage) <= 0:
            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Warning: '), 'Empty mileage entered between date range.', _class='white'),_class='alert alert-warning') 
            return dict(form = form, table = '')
        elif request.extension == 'pdf':
            row = []
            for c in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):
                c_info = [['Fleet Specification','','','Company Info',''],
                ['Code:',c.vehicle_code,'','Company:',c.company_id.company],
                ['Reg.No.:',c.reg_no,'','Division:',c.division_id.division],
                ['Manufacturer:',c.vehicle_name_id.vehicle_name,'','Department:',c.department.name],
                ['Model:', c.model,'', 'Owner:', c.owner.name]]

            com_tbl=Table(c_info, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            com_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),
                ('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
                ('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),
                ('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3))]))
            row.append(com_tbl)
            row.append(Spacer(1,.7*cm)) 
            
            ctr = 0
            
            q_info = [['#','Month', 'Mileage','Diff. Odometer']]
            for q in v_mileage:
                ctr += 1
                q_info.append([ctr, q.given_month.strftime("%Y - %B"), 
                    str(locale.format('%d', q.current_mil, grouping = True)) + ' km.',
                    str(locale.format('%d', q.consumed_mil, grouping = True)) + ' km.'])
            
            
            q_tbl=Table(q_info, colWidths=[25,168,168,170], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            q_tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.7,colors.Color(0, 0, 0, 0.3)),
                ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),
                ('ALIGN',(2,1),(3,-1),'RIGHT'),
                ('FONTSIZE',(0,0),(-1,-1),9),
                ('ALIGN',(0,0),(-1,0),'CENTER')]))
            row.append(q_tbl)            

            row.append(Spacer(1,.7*cm)) 
            g_info = [['Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date]]
            g_tbl=Table(g_info, colWidths=[530], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            g_tbl.setStyle(TableStyle([
                ('LINEABOVE', (0,0), (0,0), 0.7,colors.Color(0, 0, 0, 0.3)),
                ('FONTSIZE',(0,0),(0,0),8)]))
            row.append(g_tbl) 

            doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
            pdf_data = open(tmpfilename,"rb").read()
            os.unlink(tmpfilename)
            response.headers['Content-Type']='application/pdf'                
            return pdf_data                    
        else:
            head = THEAD(TR(TH('No.'),TH('Month'),TH('Mileage'), TH('Diff. Odometer')))
            r = []
            ctr = 0            
            for m in v_mileage:
                ctr += 1
                r.append(TR(TD(ctr), TD(m.given_month.strftime("%Y - %B")),
                            TD(str(locale.format('%d', m.current_mil, grouping = True)) + ' km.', _align = 'right'),
                            TD(str(locale.format('%d', m.consumed_mil, grouping = True)) + ' km.', _align = 'right')))
            body = TBODY(*r)
            table = HeadRpt()
            table += DIV(_class='space-2')
            table += DIV(_class='space-2')            
            table += TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
            table += DIV(_class='hr hr8 hr-double hr-dotted')

            v_mileage = db(query).select(db.km_used.ALL, orderby = db.km_used.given_month)
            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(pdf_link, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')
            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)    
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Please choose Reg.No. & enter date range', _class='white'),_class='alert alert-info') 
    return dict(form = form,table ='')         

@auth.requires_membership('level_2_user')
def DivisionHandOverReport():
    query = (db.vehicle.division_id == auth.user.division_id)
    form = FORM(DIV(
        DIV(DIV(DIV('Reg.No.',_class='input-group-addon'),SELECT(_name='reg_no_id', *[OPTION(r.reg_no, _value=r.id) for r in db(query).select(db.vehicle.ALL, orderby=db.vehicle.reg_no)],_class='form-control', widget=SQLFORM.widgets.options.widget),_class='input-group'),_class='form-group', _id='reg_no_id'),
        DIV(DIV(DIV('Date Range:',_class='input-group-addon'),INPUT(_id='start_date', _class='date form-control', _value=request.now.date(),_name='start_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),
            SPAN(SPAN(_class='fa fa-exchange'),_class='input-group-addon'),
            INPUT(_id='end_date', _class='date form-control', _value=request.now.date(),_name='end_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),_class='input-daterange input-group'),_class='form-group'),
        DIV(_class='space space-8'),
        INPUT(_type='submit', _value='submit', _class='btn btn-primary')))
    pdf_link = FORM(INPUT(_type='image', _value = 'Print', _title = 'Print',  _src = URL('static','images/1475070815_print_16.png'), _width="24", _height="24", _style="margin-top:8px;"),     hidden = dict(reg_no_id = request.vars.reg_no_id,start_date = request.vars.start_date,end_date = request.vars.end_date), _action = 'DivisionHandOverReport.pdf', _target = '_blank')
    if request.extension == 'pdf' or form.process().accepted:

        query = db.vehicles_hand_over.reg_no_id == request.vars.reg_no_id
        query &= db.vehicles_hand_over.date_and_time >= request.vars.start_date
        query &= db.vehicles_hand_over.date_and_time <= request.vars.end_date      

        query = db(query).select(db.vehicles_hand_over.ALL)

        if len(query) <= 0:
            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Warning: '), 'Empty hand-over entered between date range.', _class='white'),_class='alert alert-warning') 
            return dict(form = form, table = '')
        elif request.extension == 'pdf':
            row = []
            for c in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):
                c_info = [['Fleet Specification','','','Company Info',''],
                ['Code:',c.vehicle_code,'','Company:',c.company_id.company],
                ['Reg.No.:',c.reg_no,'','Division:',c.division_id.division],
                ['Manufacturer:',c.vehicle_name_id.vehicle_name,'','Department:',c.department.name],
                ['Model:', c.model,'', 'Owner:', c.owner.name]]

            com_tbl=Table(c_info, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            com_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),
                ('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
                ('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),
                ('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3))]))
            row.append(com_tbl)
            row.append(Spacer(1,.7*cm)) 
            
            ctr = 0

            q_info = [['#','Date', 'From Dept.','To Dept.','From Driver', 'To Driver', 'Mileage']]
            for q in query:
                ctr += 1
                q_info.append([ctr, q.date_and_time.date(),Paragraph(q.from_department_id.name, styles['Wrap']),
                    Paragraph(q.to_department_id.name, styles["Wrap"]),Paragraph(q.from_driver_id.driver_name, styles['Wrap']),
                    Paragraph(q.to_driver_id.driver_name, styles['Wrap']), q.mileage])                        
            q_tbl=Table(q_info, colWidths=[25,65,75,75,120,120,50], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            q_tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.7,colors.Color(0, 0, 0, 0.3)),
                ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),
                ('ALIGN',(2,1),(3,-1),'RIGHT'),
                ('FONTSIZE',(0,0),(-1,-1),9),
                ('ALIGN',(0,0),(-1,0),'CENTER')]))
            row.append(q_tbl)            

            row.append(Spacer(1,.7*cm)) 
            g_info = [['Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date]]
            g_tbl=Table(g_info, colWidths=[530], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
            g_tbl.setStyle(TableStyle([
                ('LINEABOVE', (0,0), (0,0), 0.7,colors.Color(0, 0, 0, 0.3)),
                ('FONTSIZE',(0,0),(0,0),8)]))
            row.append(g_tbl) 
            
            doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
            pdf_data = open(tmpfilename,"rb").read()
            os.unlink(tmpfilename)
            response.headers['Content-Type']='application/pdf'                
            return pdf_data             
        else:            
            head = THEAD(TR(TH('No.'),TH('Date'), TH('From Dept.'), TH('To Dept.'), TH('From Driver'),TH('To Driver'), TH('Mileage')))
            r = []
            ctr = 0
            
            for q in query:
                ctr +=1
                r.append(TR(TD(ctr),TD(q.date_and_time.date()), TD(q.from_department_id.name), TD(q.to_department_id.name),
                    TD(q.from_driver_id.driver_name), TD(q.to_driver_id.driver_name), TD(q.mileage)))
            body = TBODY(*r)
            table = HeadRpt()
            table += DIV(_class='space-2')
            table += DIV(_class='space-2')            
            table += TABLE(*[head, body], _class = 'table table-striped table-bordered table-hover')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),_class='row')
            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(pdf_link, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')
            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Please choose Reg.No. & enter date range', _class='white'),_class='alert alert-info') 
    return dict(form = form,table ='')         

####################################################################
####################################################################
####################################################################
