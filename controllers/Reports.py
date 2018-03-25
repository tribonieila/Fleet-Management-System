from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.utils import ImageReader
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

#from reportlab.pdfbase import pdfdoc

#pdfdoc.PDFCatalog.OpenAction = '<</S/JavaScript/JS(this.print\({bUI:true,bSilent:false,bShrinkToFit:true}\);)>>'

styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']

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
    header = Table([['',I],[darwish,''],['Fleet Summary Report','']], colWidths=[None,90])
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

form_success = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Record shows.', _class='white'),_class='alert alert-success') 
form_error = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
form_info = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Kindly fill the form', _class='white'),_class='alert alert-info') 
form_warning = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-exclamation-triangle smaller-130'),B(' Warning: '), 'Other user has changed record before you did', _class='white'),_class='alert alert-warning') 


n = 0
import locale
export = {'xml':False, 'html':False, 'csv_with_hidden_cols':False,
          'csv':False, 'tsv_with_hidden_cols':False, 'json':False}

def btn_report():
    img_report = FORM(INPUT(_title = 'Print', _type = 'image',  _target = "_blank",_src=URL('static','images/print.png'), 
                            _onclick = "javascript:PrintContent()"))       
    chart_link = FORM(INPUT(**{'_title':'Graph', '_type':'image',  '_data-target':'.modal-large','_data-toggle':'modal', 
        '_src':URL('static','images/chart.png')}))   
    table = TABLE(*[TR(TD(),TD(img_report))], _align = 'right')
    return table

def HeadRpt():
    for info in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):

        table = TABLE(THEAD(TR(TH('Fleet Specification',_colspan='2',_width='40%',_class='tblhead'),TH(_width='10%'),TH('Company Info',_colspan='2',_width='40%',_class='tblhead lftborder topborder'))),
            TBODY(TR(TD('Code:'),TD(info.vehicle_code,_class='btmborder'),TD(''),TD('Company:', _class='lftborder'),TD(info.company_id.company,_class='rtborder')),
                TR(TD('Reg.No.:'),TD(info.reg_no,_class='btmborder'),TD(''),TD('Division:', _class='lftborder'),TD(info.division_id.division,_class='rtborder')),
                TR(TD('Manufacturer:'),TD(info.vehicle_name_id.vehicle_name,_class='btmborder'),TD(''),TD('Department:', _class='lftborder'),TD(info.department.name,_class='rtborder')),
                TR(TD('Model:'),TD(info.model,_class='btmborder'),TD(''),TD('Owner:', _class='lftborder btmborder'),TD(info.owner.name,_class='rtborder btmborder' ))),_class='border-collapse: collapse;',_width='100%')
    return table

@auth.requires_login()
def VehicleMileageReport():
    form = SQLFORM.factory(
        Field('reg_no_id', widget = SQLFORM.widgets.autocomplete(request, db.vehicle.reg_no,
            id_field = db.vehicle.id, limitby = (0,10), min_length = 2), label = 'Reg.No.'),
        Field('start_date', 'date', default = request.now),
        Field('end_date', 'date', default = request.now))
    for input in form.elements('input', _class='string'):
        input['_class'] = 'string form-control'

    for input in form.elements('input', _class='date'):
        input['_class'] = 'date form-control'    
    if form.accepts(request):
        reg_no_id_pdf = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print",_href=URL('Mileage','FleetMileageReport', args=[request.vars.reg_no_id, request.vars.start_date, request.vars.end_date]))
        rows = db(db.km_used.reg_no_id == request.vars.reg_no_id).select(orderby = db.km_used.given_month)
        r = 1
    	row = len(rows)
    	while (r < row):
        	rows[r].update_record(consumed_mil = rows[r].current_mil - rows[r-1].current_mil)
        	r +=1
        
        query = db.km_used.reg_no_id == request.vars.reg_no_id
        query &= db.km_used.given_month >= request.vars.start_date
        query &= db.km_used.given_month <= request.vars.end_date
        
        total_mileage = db.km_used.consumed_mil.sum().coalesce_zero()
        total_mileage = db(query).select(total_mileage).first()[total_mileage]

        head = THEAD(TR(TH('No.'),TH('Month'),TH('Mileage'),  TH('Diff. Odometer')))
        r = []
        v_mileage = db(query).select(db.km_used.ALL, orderby = ~db.km_used.given_month)
        ctr = 0
        for m in v_mileage:
            ctr += 1
            r.append(TR(TD(ctr),TD(m.given_month.strftime('%Y - %B')),TD(str(locale.format('%d', m.current_mil or 0, grouping = True)) + ' km.'),TD(str(locale.format('%d', m.consumed_mil or 0, grouping = True)) + ' km.')))
        body = TBODY(*r)
        table = HeadRpt()
        table += DIV(_class='space')
        table += TABLE(*[head, body], _class = 'table table-bordered')
        table += DIV(_class='hr hr8 hr-double hr-dotted')
        table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('TOTAL MILEAGE: ', SPAN(locale.format('%d',total_mileage or 0, grouping=True) + 'Km.' , _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')
        table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(reg_no_id_pdf, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')
        response.flash = form_success
        return dict(form = form, table = table,  v_mileage = v_mileage)
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Fill the reg.no. and date range form.', _class='white'),_class='alert alert-info') 
    
    return dict(form = form, table = '')

@auth.requires_login()
def CompanyMileageReport():
    form = SQLFORM.factory(
        Field('company_id', requires = IS_IN_DB(db, db.company, '%(company)s'), label = 'Company'),
        Field('start_date', 'date', requires = IS_DATE()),
        Field('end_date', 'date', requires = IS_DATE()))
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))
    if form.accepts(request):
        query = db.vehicle.company_id == request.vars.company_id
        query &= db.km_used.reg_no_id == db.vehicle.id
        query &= db.km_used.given_month >= request.vars.start_date
        query &= db.km_used.given_month <= request.vars.end_date
        
        #query = db(query).select(db.vehicle.company_id, db.km_used.reg_no_id, groupby = (db.km_used.reg_no_id, db.vehicle.company_id))
        #TABLE(*[TR(TD(item)) for item in [...]])
        #for qs in filter(lambda a: a != '', q.split(' ')):
        #    query = query | db.page.content.lower().like(qs.strip())
        #    rows = db(query).select()
        
        head = THEAD(TR(TD('Month', _width = '20%'), TD('Mileage', _width = '20%'), TD('Diff. Odometer', _width = '20%'), _bgcolor = '#E0E0E0'))
        
        q = db(query).select()
        r = []
        company = []
        for car in db(query).select(db.vehicle.ALL):
            company.append(TR(TD('Reg.No.:', _width = '13%'), TD(car.reg_no, _width = '30%')))#,
            for km in car.km_used.select():
                r.append(TR(TD(km.given_month,  _align = 'right', _width = '20%'),
                            TD(km.current_mil,  _align = 'right', _width = '20%'),
                            TD(km.consumed_mil, _align = 'right', _width = '20%')))
        body = TBODY(*r)
        company_table = TABLE(*[TBODY(*company)])
        table = TABLE(*[company, head, body],  _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, company_table = company_table, table = table, img_report = img_report)
    else:
        return dict(form = form, company_table = '', table = 'Type Reg.No., Start date & End date',
                    img_report = None)

@auth.requires_login()
def SummaryMaintenanceReport():
    form = SQLFORM.factory(
        Field('by_category', requires = IS_IN_SET(['Company','Division','Department'], zero='Choose one'),widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('start_date', 'date', default = request.now, widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),
        Field('end_date', 'date',  default = request.now, widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')))  
    if request.extenstion == 'pdf' or form.accepts(request):
        query = db.vehicle.id == db.repair_history.reg_no_id
        query &= db.repair_history.invoice_date >= request.vars.start_date
        query &= db.repair_history.invoice_date <= request.vars.end_date
       
        r_maint = db.repair_history.regular_maintenance.sum().coalesce_zero()
        s_parts = db.repair_history.spare_parts.sum().coalesce_zero()
        s_expen = db.repair_history.statutory_expenses.sum().coalesce_zero()
        a_repai = db.repair_history.accident_repair.sum().coalesce_zero()
        t_amoun = db.repair_history.total_amount.sum().coalesce_zero()

        grand_total = db(query).select(t_amoun).first()[t_amoun]

        row = []
        if request.vars.by_category == 'Company':
            cat_lbl = 'Company'
            for s in db(query).select(db.vehicle.company_id, r_maint, s_parts, s_expen, a_repai, t_amoun, orderby = ~db.vehicle.company_id, groupby=db.vehicle.company_id):
                row.append(TR(TD(s.vehicle.company_id.company),TD(locale.format('%.2F',s[r_maint] or 0, grouping = True),_align='right'),TD(locale.format('%.2F', s[s_parts] or 0, grouping = True),_align='right'),TD(locale.format('%.2F',s[s_expen] or 0, grouping = True),_align='right'),TD(locale.format('%.2F',s[a_repai] or 0, grouping = 0),_align='right'),TD(locale.format('%.2F',s[t_amoun] or 0, grouping = True),_align='right')))
        elif request.vars.by_category == 'Division':
            cat_lbl = 'Division'
            for s in db(query).select(db.vehicle.division_id, r_maint, s_parts, s_expen, a_repai, t_amoun, orderby = ~db.vehicle.division_id, groupby=db.vehicle.division_id):
                row.append(TR(TD(s.vehicle.division_id.division),TD(locale.format('%.2F',s[r_maint] or 0, grouping = True),_align='right'),TD(locale.format('%.2F', s[s_parts] or 0, grouping = True),_align='right'),TD(locale.format('%.2F',s[s_expen] or 0, grouping = True),_align='right'),TD(locale.format('%.2F',s[a_repai] or 0, grouping = 0),_align='right'),TD(locale.format('%.2F',s[t_amoun] or 0, grouping = True),_align='right')))
        elif request.vars.by_category == 'Department':
            cat_lbl = 'Deparment'
            for s in db(query).select(db.vehicle.department, r_maint, s_parts, s_expen, a_repai, t_amoun, orderby = ~db.vehicle.department, groupby=db.vehicle.department):
                row.append(TR(TD(s.vehicle.department.name),TD(locale.format('%.2F',s[r_maint] or 0, grouping = True),_align='right'),TD(locale.format('%.2F', s[s_parts] or 0, grouping = True),_align='right'),TD(locale.format('%.2F',s[s_expen] or 0, grouping = True),_align='right'),TD(locale.format('%.2F',s[a_repai] or 0, grouping = 0),_align='right'),TD(locale.format('%.2F',s[t_amoun] or 0, grouping = True),_align='right')))
        
        head = THEAD(TR(TH(cat_lbl),TH('Labour'),TH('Spart Parts'),TH('Statutory Exp.'),TH('Accident Rep.'),TH('Total Amount')))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class = 'table table-striped table-bordered')
        table += DIV(H4('Grand Total: ',locale.format('%.2F', grand_total or 0, grouping = True)))
        return dict(form=form, table=table)
        
    else:
        return dict(form = form, table = 'table')

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

@auth.requires_login()
def DivisionCostPerYear():
    query = (db.vehicle.division_id == auth.user.division_id)
    form = FORM(DIV(
        DIV(DIV(DIV('Reg.No.',_class='input-group-addon'),SELECT(_name='reg_no_id', *[OPTION(r.reg_no, _value=r.id) for r in db().select(db.vehicle.ALL, orderby=db.vehicle.reg_no)],_class='form-control', widget=SQLFORM.widgets.options.widget),_class='input-group'),_class='form-group', _id='reg_no_id'),
        DIV(DIV(DIV('Date Range:',_class='input-group-addon'),INPUT(_id='start_date', _class='date form-control', _value=request.now.date(),_name='start_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),
            SPAN(SPAN(_class='fa fa-exchange'),_class='input-group-addon'),
            INPUT(_id='end_date', _class='date form-control', _value=request.now.date(),_name='end_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),_class='input-daterange input-group'),_class='form-group'),
        DIV(_class='space space-8'),
        INPUT(_type='submit', _value='submit', _class='btn btn-primary')))
    pdf_link = FORM(INPUT(_type='image', _value = 'Print', _title = 'Print',  _src = URL('static','images/1475070815_print_16.png'), _width="24", _height="24", _style="margin-top:8px;"),     hidden = dict(reg_no_id = request.vars.reg_no_id,start_date = request.vars.start_date,end_date = request.vars.end_date), _action = 'DivisionCostPerYear.pdf', _target = '_blank')
    if request.extension == 'pdf' or form.process().accepted:
        que_fleet = db.vehicle.id == request.vars.reg_no_id

        que_driv = db.vehicles_hand_over.reg_no_id == request.vars.reg_no_id
        
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
@auth.requires_login()
def VehicleMaintenanceReport():
    fields = []
    db.repair_history.invoice_date.represent = lambda x, row: x.strftime("%d, %B %Y")
    form = SQLFORM.factory(
        Field('reg_no_id', 'reference vehicle', requires = IS_IN_DB(db, db.vehicle, '%(reg_no)s', zero = 'Choose Reg.No.'), 
            represent = lambda id, r: db.vehicle(id).reg_no, label = 'Reg.No.', widget = SQLFORM.widgets.autocomplete(request, db.vehicle.reg_no, 
            id_field = db.vehicle.id, limitby = (0,10), min_length = 2)), 
        Field('start_date', 'date', default = request.now, label = 'Start Date', widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),
        Field('end_date', 'date',  default = request.now, label = 'End Date',
            widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),style='form-contorl')  
    #pdf_link = A(SPAN(_class='ace-icon fa fa-print'), _title='print', 
    #    _hidden = dict(reg_no_id = request.vars.reg_no_id, start_date = request.vars.start_date, end_date = request.vars.end_date), 
    #    _target='_blank', _action='VehicleMaintenanceReport.pdf',_href='#')

    
    pdf_link = FORM(INPUT(_align = 'right', _type='image', _value = 'Print', _title = 'Print', _src = URL('images', 'printButton.png')),
                    hidden = dict(reg_no_id = request.vars.reg_no_id,
                                  start_date = request.vars.start_date,
                                  end_date = request.vars.end_date),
                    _action = 'VehicleMaintenanceReport.pdf', _target = '_blank')
    
    empty_table = DIV(H3(SPAN(_class='ace-icon fa fa-info smaller-90'),'Info',_class='header blue lighter smaller'),DIV(SPAN(_class='ace-icon fa fa-hand-o-right'),' Enter Reg.No. & Date Range',_class='grey bigger-110'),_class='col-xs-12')
    if request.extension == 'pdf' or form.accepts(request):
        
        query = db.repair_history.reg_no_id == request.vars.reg_no_id
        query &= db.repair_history.invoice_date >= request.vars.start_date
        query &= db.repair_history.invoice_date <= request.vars.end_date       
        vehicle_info = db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL)
        
        for info in vehicle_info:
            i = DIV(DIV(DIV(DIV(B('Fleet Info'),_class='col-xs-11 label label-lg label-info arrowed-in arrowed-right'),_class='row'),DIV(UL(LI(SPAN(_class='ace-icon fa fa-caret-right blue'),'Reg.No.: ',B(info.reg_no,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right blue'),'Category: ',B(info.category_id.category,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right blue'),'Model: ',B(info.model,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right blue'),'Last Reading: ',B(locale.format('%d', info.mileage or 0, grouping = True),_class='red')),_class='list-unstyled spaced')),_class='col-sm-6'),
                DIV(DIV(DIV(B('Company Info'),_class='col-xs-11 label label-lg label-success arrowed-in arrowed-right'),_class='row'),DIV(UL(LI(SPAN(_class='ace-icon fa fa-caret-right green'),'Company: ',B(info.company_id.company,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right green'),'Division: ',B(info.division_id.division,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right green'),'Department: ',B(info.department.name,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right green'),'Owner: ',B(info.owner.name,_class='red')),_class='list-unstyled spaced')),_class='col-sm-6'))

        grand_total = db.repair_history.total_amount.sum().coalesce_zero()
        grand_total = db(query).select(grand_total).first()[grand_total]

        head = THEAD(TR(TH('#'),TH('Invoice Date'),TH('Invoice No.'),TH('Workshop Done'),TH('Mileage'),TH('Amount'),TH('Details')))
        row = []
        ctr = 0
        for q in db(query).select(db.repair_history.ALL, orderby = ~db.repair_history.invoice_date):            
            ctr += 1
            row.append(TR(TD(ctr),TD(q.invoice_date),TD(q.invoice_number),TD(q.workshop_done.workshop), TD(locale.format('%d', q.mileage or 0, grouping = True),_align = "right"),TD(locale.format('%.2F', q.total_amount or 0, grouping = True ),_align="right"),TD(q.details)))
        body = TBODY(*row)
        #table = DIV(H3('Fleet Maintenance Report', _class='widget-title grey lighter'),DIV(A(SPAN(_class='ace-icon fa fa-print'),_href='#'),_class='widget-toolbar hidden-480'),_class='widget-header widget-header-large')
        table = DIV(H3('Fleet Maintenance Report', _class='widget-title grey lighter'),DIV(_class = 'widget-toolbar hidden-480'),_class='widget-header widget-header-large')
        table += DIV(_class='hr hr8 hr-single hr-dotted')
        table += i
        table += TABLE(*[head, body],  _align="center", _width="100%", _class = 'table table-striped table-bordered')
        table += DIV(_class='hr hr8 hr-double hr-dotted')
        table += DIV(DIV(H4('Total Amount: ', SPAN(locale.format('%.2F',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')
    
        if request.extension == 'pdf':
            ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'

            row.append(Paragraph(ptext, styles["Normal"]))
 
            doc.build(row)#, onFirstPage=_header_footer, onLaterPages=_header_footer)
            pdf_data = open(tmpfilename,"rb").read()
            os.unlink(tmpfilename)
            
            #response['Content-Disposition'] = "inline; filename= tmpfilename"
            #response.headers['Content-Disposition'] = "attachment; filename=SummaryReport.pdf"
            
            response.headers['Content-Type']='application/pdf'       
            return pdf_data 
        else:
            return dict(form=form, table=table, pdf_link=pdf_link)
            #return dict(form = form,  i = i, table = table, grand_total = grand_total,
            #            pdf_link = pdf_link)
    else: 
        return dict(form = form, i = '', table = empty_table, grand_total = 0, pdf_link = None)


@auth.requires_login()
def CompanyMaintenanceReport():
    form = SQLFORM.factory(
        Field('company', requires = IS_IN_DB(db, db.company, '%(company)s', zero='Choose company'),widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('start_date', 'date', default = request.now,widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')),
        Field('end_date', 'date', default=request.now, widget = lambda field, value: SQLFORM.widgets.date.widget(field, value, _class='date form-control')))
    pdf_link = FORM(INPUT(_align = 'right', _type = 'image', _value = 'Print', _title='Print', _src = URL('images', 'printButton.png')),
                    hidden = dict(company = request.vars.company,
                                  start_date = request.vars.start_date,
                                  end_date = request.vars.end_date),
                    _action = 'CompanyMaintenanceReport.pdf', _target = '_blank')

    if request.extension == 'pdf' or form.accepts(request):
        #start_date = request.vars.start_date
        #end_date = request.vars.end_date
        
        query = db.vehicle.company_id == request.vars.company
        query &= db.vehicle.id == db.repair_history.reg_no_id
        query &= db.repair_history.invoice_date >= request.vars.start_date
        query &= db.repair_history.invoice_date <= request.vars.end_date
        
        r_maint = db.repair_history.regular_maintenance.sum().coalesce_zero()
        s_parts = db.repair_history.spare_parts.sum().coalesce_zero()
        s_expen = db.repair_history.statutory_expenses.sum().coalesce_zero()
        a_repai = db.repair_history.accident_repair.sum().coalesce_zero()
        t_amoun = db.repair_history.total_amount.sum().coalesce_zero()

        t_maint = db(query).select(r_maint).first()[r_maint]
        t_parts = db(query).select(s_parts).first()[s_parts]
        t_expen = db(query).select(s_expen).first()[s_expen]
        t_repai = db(query).select(a_repai).first()[a_repai]
        total_a = db(query).select(t_amoun).first()[t_amoun]

        #company_info = db(db.vehicle.company_id == request.vars.company).select(db.vehicle.ALL)
        #for c_info in company_info:
        #    i = TABLE(*[TR(TD('Company:', _width = '13%'), TD(c_info.company_id.company, _width = '30%'))])
                        #TR(TD('Start Date:', _width = '13%'), TD((request.vars.start_date).strftime('%d, %B %Y'), _width = '30%')),
                        #TR(TD('End Date:', _width = '13%'), TD((request.vars.end_date).strftime('%d, %B %Y'), _width = '30%'))])
            
        head = THEAD(TR(TH('Reg.No.'),TH('Labour'),TH('Spart Parts'),TH('Statutory Exp.'),TH('Accident Rep.'),TH('Total Amount')))
        r = []
        for q in db(query).select(db.repair_history.reg_no_id, r_maint, s_parts,s_expen,a_repai,t_amoun,orderby = db.repair_history.reg_no_id, groupby = db.repair_history.reg_no_id): #db.vehicle.department, orderby = db.vehicle.department,
            r.append(TR(TD(q.repair_history.reg_no_id.reg_no),
                TD(locale.format('%.2F', q[r_maint] or 0, grouping = True), _align = 'right'),
                TD(locale.format('%.2F', q[s_parts] or 0, grouping = True), _align = 'right'),
                TD(locale.format('%.2F', q[s_expen] or 0, grouping = True), _align = 'right'),
                TD(locale.format('%.2F', q[a_repai] or 0, grouping = True), _align = 'right'),
                TD(locale.format('%.2F', q[t_amoun] or 0, grouping = True), _align = 'right')))
            
        body = TBODY(*r)
        
        table = TABLE(*[head, body], _class = 'table table-striped table-bordered')
        
        if request.extension == 'pdf':
            ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'

            row.append(Paragraph(ptext, styles["Normal"]))

            doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
            pdf_data = open(tmpfilename,"rb").read()
            os.unlink(tmpfilename)
            
            #response['Content-Disposition'] = "inline; filename= tmpfilename"
            #response.headers['Content-Disposition'] = "attachment; filename=SummaryReport.pdf"
            
            response.headers['Content-Type']='application/pdf'       
            return pdf_data            
            '''
            pdf = MyFPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 13)
            pdf.multi_cell(0, 8,'Company Maintenance Report', 0,'C')
            pdf.write_html(str(XML(i, sanitize = False)))
            pdf.write_html(str(XML(table, sanitize = False)))
            response.headers['Content-Type']='application/pdf'
            return pdf.output(dest = 'S')
            '''
            
        else:
            return dict(form = form, i='i', table = table, total_amount = '',
                        pdf_link = pdf_link, )
    else:
        return dict(form = form, i= '', table = 'Select company, Start date & End date',
                    total_amount = '', pdf_link = None, grand_total = '')    


@auth.requires_login()
def DepartmentMaintenanceReport():
    form = SQLFORM.factory(
        Field('department', requires = IS_IN_DB(db, db.department, '%(name)s'), label = 'Department'),
        Field('start_date', 'date', default=request.now),
        Field('end_date', 'date', default=request.now))  
    pdf_link = FORM(INPUT(_align = 'right', _type = 'image', _value = 'Print', _title='Print', 
        _src = URL('images', 'printButton.png')),
                    hidden = dict(department = request.vars.department,
                                  start_date = request.vars.start_date,
                                  end_date = request.vars.end_date),
                    _action = 'DepartmentMaintenanceReport.pdf', _target = '_blank')
    if request.extension == 'pdf' or form.accepts(request):
        start_date = request.vars.start_date
        end_date = request.vars.end_date
        
        query = db.vehicle.department == request.vars.department
        query &= db.vehicle.id == db.fuel_expenses.reg_no_id
        query &= db.fuel_expenses.date_expense >= start_date
        query &= db.fuel_expenses.date_expense <= end_date
        
        total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
        total_amount = db(query).select(total_amount).first()[total_amount]

        for c_info in db(db.vehicle.department == request.vars.department).select(db.vehicle.ALL):
            i = TABLE(*[TR(TD('Company:', _width = '13%'), TD(c_info.company_id.company, _width = '30%')),
                        TR(TD('Department:', _width = '13%'), TD(c_info.department.name, _width = '30%')),
                        TR(TD('Start Date:', _width = '13%'), TD(request.vars.start_date)),
                        TR(TD('End Date:', _width = '13%'), TD(request.vars.end_date))])
            
        
        head = THEAD(TR(TH('Reg.No.', _width = '20%'), TH('Date', _width = '20%'),
                        TH('Amount', _width = '20%'), _bgcolor='#E0E0E0'))
        
        r = []
        for q in db(query).select(db.fuel_expenses.ALL, orderby = ~db.fuel_expenses.date_expense | ~db.fuel_expenses.reg_no_id ):
            r.append(TR(TD(q.reg_no_id.reg_no, _align = 'right'),
                        TD(q.date_expense, _align = 'center'),
                        TD(locale.format('%.2F', q.amount or 0, grouping = True), _align = 'right')))
        
        body = TBODY(*r)
        table = TABLE(*[head, body],  _align="center", _width="100%", _class = 'pure-table')
        
        if request.extension == 'pdf':
            ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'

            row.append(Paragraph(ptext, styles["Normal"]))

            doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
            pdf_data = open(tmpfilename,"rb").read()
            os.unlink(tmpfilename)
            
            #response['Content-Disposition'] = "inline; filename= tmpfilename"
            #response.headers['Content-Disposition'] = "attachment; filename=SummaryReport.pdf"
            
            response.headers['Content-Type']='application/pdf'       
            return pdf_data   
        else:
            return dict(form =form, i = i, table = table, total_amount = total_amount,
                        pdf_link = pdf_link)
    else:
        return dict(form = form, i = '', table = 'Select Department, Start date & End date',
                    total_amount = 0, pdf_link = None )  

def mileage():
    reg_no_id = 75
    start = datetime.date(2012, 5, 29)
    end = datetime.datetime.now()

    f = db.fuel_expenses.reg_no_id == reg_no_id
    f &= db.fuel_expenses.date_expense >= start
    f &= db.fuel_expenses.date_expense <= end

    k = db.km_used.reg_no_id == reg_no_id
    k &= db.km_used.given_month >= start
    k &= db.km_used.given_month <= end

    query = db(k).select()
    cost_km = None
    try:
        fuel = db.fuel_expenses.amount.sum().coalesce_zero()
      
        fuel_expenses = db(f).select(fuel).first()[fuel]

        km = db.km_used.consumed_mil.sum().coalesce_zero()
        total_km = db(k).select(km).first()[km]
        cost_km = fuel_expenses / total_km

    except Exception, e:           
        response.flash = 'zero'


    
    return cost_km

@auth.requires_login()
def VehicleSummaryReport():

    form = SQLFORM.factory(
        Field('reg_no_id',  widget = SQLFORM.widgets.autocomplete(request, db.vehicle.reg_no, id_field = db.vehicle.id, limitby = (0,10),min_length=2)),
        Field('start_date', 'date', default = request.now),
        Field('end_date', 'date', default = request.now))
    
    for input in form.elements('input', _class='string'):
        input['_class'] = 'string form-control'

    for input in form.elements('input', _class='date'):
        input['_class'] = 'date form-control'
    if form.process().accepted:

        query = db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL)#db.repair_history.ALL, left=db.repair_history.on(db.repair_history.reg_no_id == db.vehicle.id))

        f = db.fuel_expenses.reg_no_id == request.vars.reg_no_id
        f &= db.fuel_expenses.date_expense >= request.vars.start_date
        f &= db.fuel_expenses.date_expense <= request.vars.end_date
      
        r = db.repair_history.reg_no_id == request.vars.reg_no_id
        r &= db.repair_history.invoice_date >= request.vars.start_date
        r &= db.repair_history.invoice_date <= request.vars.end_date

        n = db.insured_vehicles.reg_no_id == request.vars.reg_no_id
        n &= db.insured_vehicles.policy_no_id == db.insurance_policy.id
        n &= db.insurance_policy.status_id == 1

        a = db.ads_vehicle.reg_no_id == request.vars.reg_no_id
        a &= db.ads_vehicle.license_no_id == db.advertisement.id
        a &= db.advertisement.status_id == 1

        k = db.km_used.reg_no_id == request.vars.reg_no_id
        k &= db.km_used.given_month >= request.vars.start_date
        k &= db.km_used.given_month <= request.vars.end_date

        try:
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
            repr = db.repair_history.total_amount.sum().coalesce_zero()
        
            r_mai = db(r).select(r_mai).first()[r_mai]
            a_rep = db(r).select(a_rep).first()[a_rep]
            s_exp = db(r).select(s_exp).first()[s_exp]
            s_parts = db(r).select(s_parts).first()[s_parts]
            repair_expenses = db(r).select(repr).first()[repr]
        
            cost_km = fuel_expenses / total_km
            main_exp = s_parts + r_mai + a_rep
            grand_total = fuel_expenses + repair_expenses + ads_exp + ins_expenses
        
            total_run_cost = grand_total / total_km

        except Exception, e:
            total_run_cost = float('0')#redirect(URL('Reports','Empty'))
            #response.flash = DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Warning: '),'No mileage entered between date range.',_class='white')
            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Warning: '), 'No mileage entered between date range.', _class='white'),_class='alert alert-warning') 
            return dict(form = form, table = '')
        else:
            table = DIV(H3('Fleet Maintenance Report', _class='widget-title grey lighter'),DIV(_class = 'widget-toolbar hidden-480'),_class='widget-header widget-header-large')
            table += DIV(_class='hr hr8 hr-single hr-dotted')

            for info in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):
                table += DIV(DIV(DIV(DIV(B('Fleet Info'),_class='col-xs-11 label label-lg label-info arrowed-in arrowed-right'),_class='row'),DIV(UL(LI(SPAN(_class='ace-icon fa fa-caret-right blue'),'Reg.No.: ',B(info.reg_no,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right blue'),'Category: ',B(info.category_id.category,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right blue'),'Model: ',B(info.model,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right blue'),'Last Reading: ',B(locale.format('%d', info.mileage or 0, grouping = True),_class='red')),_class='list-unstyled spaced')),_class='col-sm-6'),
                    DIV(DIV(DIV(B('Company Info'),_class='col-xs-11 label label-lg label-success arrowed-in arrowed-right'),_class='row'),DIV(UL(LI(SPAN(_class='ace-icon fa fa-caret-right green'),'Company: ',B(info.company_id.company,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right green'),'Division: ',B(info.division_id.division,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right green'),'Department: ',B(info.department.name,_class='red')),LI(SPAN(_class='ace-icon fa fa-caret-right green'),'Owner: ',B(info.owner.name,_class='red')),_class='list-unstyled spaced')),_class='col-sm-6'))
            
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
            response.flash = form_success
            return dict(form = form, table = table)
        finally:            
            if request.extension == 'pdf':
                for c in query:
                    c_info = [['Reg.No.', 'Company', 'Division', 'Department', 'Chassis No', 'Last Reading', 'Model'],       
                    [c.reg_no, c.company_id.company, c.division_id.division, c.department.name, c.chassis_no, 
                    locale.format('%d',c.mileage or 0, grouping = True), c.model]]        

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

                com_tbl=Table(c_info, colWidths=[50,70,100,100,100,70,40], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
                com_tbl.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(6,0),colors.Color(0, 0, 0, 0.3))]))
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
                
                response['Content-Disposition'] = "inline; filename= tmpfilename"
                #response.headers['Content-Disposition'] = "attachment; filename=SummaryReport.pdf"
                
                response.headers['Content-Type']='application/pdf'       
                return pdf_data            
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Enter Reg.No. & Date Range', _class='white'),_class='alert alert-info') 
    return dict(form = form, table = '')    


@auth.requires_login()
def VehicleProfileReport():
    for f in db(db.vehicle.id == request.args(0)).select(db.vehicle.ALL):
        data = [['Fleet Specification','','','Company Info',''],
        ['Code:',f.vehicle_code,'','Company:',f.company_id.company],
        ['Reg.No.:',f.reg_no,'','Division:',f.division_id.division],
        ['Manufacturer:',f.vehicle_name_id.vehicle_name,'','Department:',f.department.name],
        ['Model:', f.model,'', 'Owner:', f.owner.name],
        ['Chassis No.:',f.chassis_no,'','',''],
        ['Mileage:',f.mileage,'','',''],
        ['Car Type:',f.plate_type,'','',''],
        ['Cylinder CNT:',f.cylinder_count,'','',''],
        ['Transmission:',f.transmission,'','',''],
        ['Tyre Size:',f.tyre_size,'','',''],
        ['Category:',f.category_id.category,'','',''],
        ['','','','',''],
        ['Others Info','','','Date and Value Info',''],
        ['Plate Type:',f.plate_type,'','Invoice:',f.invoice],
        ['External Color Code:',f.ext_color_code,'','Expiration Date:',f.exp_date],
        ['Accessories:',f.accessories,'','1st Reg. Date:',f.reg_date],
        ['Purpose:',f.purpose.purpose,'','Value Purchase.:',f.value_purchase],
        ['Status:',f.status_id.status,'','Date of Sale:',f.date_of_sale],
        ['Remarks:',f.remarks,'','Depreciation Value:',f.depreciation_value]]
        pro_tbl = Table(data, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
        pro_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,11),0.50, colors.Color(0, 0, 0, 0.2)),
            ('LINEBELOW',(1,14),(1,19),0.50, colors.Color(0, 0, 0, 0.2)),
            ('LINEBELOW',(4,14),(4,19),0.50, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
            ('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),
            ('BACKGROUND',(0,13),(1,13),colors.Color(0, 0, 0, 0.3)),
            ('BACKGROUND',(3,13),(4,13),colors.Color(0, 0, 0, 0.3)),
            ('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3))]))

        row.append(pro_tbl)
        doc.build(row, onFirstPage = _header_footer, onLaterPages = _header_footer)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response['Content-Disposition'] = "attachement; filename=ProfileReport.pdf"
        response.headers['Content-Type'] = 'application/pdf'
        return pdf_data


################  GROUP/DIVISION VEHICLE REPORTS #################

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def HOReport():
    
    total_amount = 0
    

    form = SQLFORM.factory(
        Field('reg_no_id',  widget = SQLFORM.widgets.autocomplete(request, db.vehicle.reg_no, id_field = db.vehicle.id, limitby = (0,10),min_length=2)),
        Field('driver_id',  widget = SQLFORM.widgets.autocomplete(request, db.driver.driver_name, id_field = db.driver.id, limitby = (0,10),min_length=2)),
        Field('start_date', 'date', default = request.now),
        Field('end_date', 'date', default = request.now))
    
    for input in form.elements('input', _class='string'):
        input['_class'] = 'string form-control'

    for input in form.elements('input', _class='date'):
        input['_class'] = 'date form-control'

    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))   
    
    if form.accepts(request):
        query = db.vehicles_hand_over.reg_no_id == request.vars.reg_no_id#)  | (db.driver.driver_name == request.vars.driver_id)
        query |= db.vehicles_hand_over.from_driver_id == request.vars.driver_id
        query &= db.vehicles_hand_over.date_and_time >= request.vars.start_date
        query &= db.vehicles_hand_over.date_and_time <= request.vars.end_date      

        for info in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):
            i = TABLE(*[THEAD(TR(TH('Reg.No.:'), TH('Company:'),TH('Division:'),TH('Department:'),TH('Chassis No:'), TH('Last Reading:'),TH('Model:'), _bgcolor='#E0E0E0')),
                TR(TD(info.reg_no), TD(info.company_id.company), TD(info.division_id.division), TD(info.department.name),
                TD(info.chassis_no),TD(str(info.mileage) + ' Km.'), TD(info.model))], _border = '0', _align = 'center', _width = '100%', _class = 'pure-table')

        head = THEAD(TR(TH('Date'), TH('Reg.No.'),TH('From Dept.'), TH('To Dept.'), TH('From Driver'), TH('To Driver'), TH('Mileage'),
                        TH('Remarks')))
        r = []
        for q in db(query).select(db.vehicles_hand_over.ALL):
            r.append(TR(TD(q.date_and_time.date()), TD(q.reg_no_id.reg_no),TD(q.from_department_id.name), TD(q.to_department_id.name), TD(q.from_driver_id.driver_name),
                        TD(q.to_driver_id.driver_name), TD(q.mileage), TD(q.remarks)))
        body = TBODY(*r)
        table = TABLE(*[head, body], _class = 'table table-striped table-bordered')
        return dict(form = form, table = table, i=None, img_report= None)    

    else:
        return dict(form = form,i = '', table ='Type Reg.No., Start date & End date', img_report= None)    

    if form2.accepts(request):
        query = db.vehicles_hand_over.reg_no_id == request.vars.reg_no_id
        #query = db.vehicles_hand_over.driver_name
        query &= db.vehicles_hand_over.date_and_time >= request.vars.start_date
        query &= db.vehicles_hand_over.date_and_time <= request.vars.end_date      

        for info in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):
            i = TABLE(*[THEAD(TR(TH('Reg.No.:'), TH('Company:'),TH('Division:'),TH('Department:'),TH('Chassis No:'), TH('Last Reading:'),TH('Model:'), _bgcolor='#E0E0E0')),
                TR(TD(info.reg_no), TD(info.company_id.company), TD(info.division_id.division), TD(info.department.name),
                TD(info.chassis_no),TD(str(info.mileage) + ' Km.'), TD(info.model))], _border = '0', _align = 'center', _width = '100%', _class = 'pure-table')

        head = THEAD(TR(TH('Date'), TH('From Company'), TH('To Company'), TH('From Driver'), TH('To Driver'), TH('Mileage'),
                        TH('Remarks'),_bgcolor='#E0E0E0'))
        r = []
        for q in db(query).select(db.vehicles_hand_over.ALL):
            r.append(TR(TD(q.date_and_time), TD(q.from_department_id.name), TD(q.to_department_id.name), TD(q.from_driver_id.driver_name),
                        TD(q.to_driver_id.driver_name), TD(q.mileage), TD(q.remarks,_width = "21%")))
        body = TBODY(*r)
        table = TABLE(*[head, body], _border = '0', _align="center", _width="100%", _class = 'pure-table')
        return dict(form1 = form1,form= form, table = table, i=None, img_report= None)    

    else:
        return dict(form1 = form1, form = form,i = '', table ='Type Reg.No., Start date & End date', img_report= None)    

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def RegNoHandoverReport():
    total_amount = 0
    db.fuel_expenses.date_expense.represent = lambda x, row: x.strftime("%d, %B %Y")
    form = SQLFORM.factory(
        Field('reg_no_id', label = 'Reg.No.',
              widget = SQLFORM.widgets.autocomplete(request, db.vehicle.reg_no, id_field = db.vehicle.id, limitby = (0,10),min_length=2)),
        Field('start_date', 'date', requires = IS_DATE(), default = request.now, label = 'Start Date'),
        Field('end_date', 'date', requires = IS_DATE(), default = request.now, label = 'End Date'),formstyle='bootstrap3_inline')
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))   
    
    if form.accepts(request):
        query = db.vehicles_hand_over.reg_no_id == request.vars.reg_no_id
        query &= db.vehicles_hand_over.date_and_time >= request.vars.start_date
        query &= db.vehicles_hand_over.date_and_time <= request.vars.end_date      

        for info in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):
            i = TABLE(*[THEAD(TR(TH('Reg.No.:'), TH('Company:'),TH('Division:'),TH('Department:'),TH('Chassis No:'), TH('Last Reading:'),TH('Model:'), _bgcolor='#E0E0E0')),
                TR(TD(info.reg_no), TD(info.company_id.company), TD(info.division_id.division), TD(info.department.name),
                TD(info.chassis_no),TD(str(info.mileage) + ' Km.'), TD(info.model))], _border = '0', _align = 'center', _width = '100%', _class = 'pure-table')

        head = THEAD(TR(TH('Date'), TH('From Company'), TH('To Company'), TH('From Driver'), TH('To Driver'), TH('Mileage'),
                        TH('Remarks'),_bgcolor='#E0E0E0'))
        r = []
        for q in db(query).select(db.vehicles_hand_over.ALL):
            r.append(TR(TD(q.date_and_time), TD(q.from_department_id.name), TD(q.to_department_id.name), TD(q.from_driver_id.driver_name),
                        TD(q.to_driver_id.driver_name), TD(q.mileage), TD(q.remarks,_width = "21%")))
        body = TBODY(*r)
        table = TABLE(*[head, body], _border = '0', _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, table = table, i=i, img_report= img_report)    
    else:
        return dict(form = form, i = '', table ='Type Reg.No., Start date & End date', img_report= None)    

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DriverHandoverReport():
    form = SQLFORM.factory(
        Field('from_driver_id', label = "Driver's Name", requires = IS_IN_DB(db, db.driver, '%(driver_name)s', zero = 'Choose driver\'s name')),
        Field('start_date', 'date', requires = IS_DATE(), default = request.now, label = 'Start Date'),
        Field('end_date', 'date', requires = IS_DATE(), default = request.now, label = 'End Date'))
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))    
    if form.accepts(request):
        query = db.vehicles_hand_over.from_driver_id == request.vars.from_driver_id
        query &= db.vehicles_hand_over.date_and_time >= request.vars.start_date
        query &= db.vehicles_hand_over.date_and_time <= request.vars.end_date      

        for info in db(db.driver.id == request.vars.from_driver_id).select(db.driver.ALL):
            i = TABLE(*[THEAD(TR(TH('Employee Number:'), TH("Drivers Name:"),TH('Company:'),TH('Division:'),TH('Department:'),
                TH('Position:'),TH('License No.:'),_bgcolor='#E0E0E0')),
                TR(TD(info.employee_number), TD(info.driver_name), TD(info.company_id.company), TD(info.division_id.division), 
                    TD(info.department_id.name), TD(info.position_id.name), TD(info.driver_id))], _border = '0', _align = 'center', 
            _width = '100%', _class = 'pure-table')

        head = THEAD(TR(TH('Date'), TH('Reg.No.'), TH('Mileage'), TH('Remarks'),_bgcolor='#E0E0E0'))
        r = []
        for q in db(query).select(db.vehicles_hand_over.ALL, orderby= db.vehicles_hand_over.date_and_time):
            r.append(TR(TD(q.date_and_time), TD(q.reg_no_id.reg_no), TD(q.mileage), TD(q.remarks)))
        body = TBODY(*r)
        table = TABLE(*[head, body], _border = '0', _align="center", _width="100%", _class = 'pure-table')

        return dict(form = form, i = i, table = table, img_report= img_report)    
    else:
        return dict(form = form, i = '', table ='Select driver\'s name, Start date & End date', img_report= None)   


def HandOverReport():
    han_que = db(db.vehicles_hand_over.id == request.args(0)).select(db.vehicles_hand_over.ALL)
    fir_que = db(db.vehicles_hand_over.id == request.args(0)).select(db.vehicles_hand_over.ALL).first()
    fle_que = db(db.vehicle.id == fir_que.reg_no_id).select(db.vehicle.ALL)

    for c in fle_que:
        c_info = [['Fleet Specification','','','Company Info',''],['Code:',c.vehicle_code,'','Company:',c.company_id.company],['Reg.No.:',c.reg_no,'','Division:',c.division_id.division],['Manufacturer:',c.vehicle_name_id.vehicle_name,'','Department:',c.department.name],['Model:', c.model,'', 'Owner:', c.owner.name]]   
        com_tbl=Table(c_info, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
        com_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3))]))

    for h in han_que:
        h_data = [['Details',''],
        ['Date',h.date_and_time],
        ['From Dept:',h.from_department_id.name],
        ['To Dept:',h.to_department_id.name],
        ['From Driver:',h.from_driver_id.driver_name],
        ['To Driver:',h.to_driver_id.driver_name],
        ['Mileage:',h.mileage],
        ['Accessories:',Paragraph(str(', '.join(h.vehicles_acc)), styles["BodyText"])],
        ['Remarks:',Paragraph(h.remarks, styles["BodyText"])]]
        han_tbl=Table(h_data, colWidths=[100,430], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)#,  hAlign='LEFT')
        han_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,-1),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3))]))

    for s in han_que:
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
@auth.requires_login()
def HandOverReport2():

    query = db.vehicles_hand_over.id  == request.args(0)
    query &= db.vehicle.id == db.vehicles_hand_over.reg_no_id

    photo = db.vehicles_hand_over.id == request.args(0)
    photo &= db.v_photos.reg_no_id == db.vehicles_hand_over.reg_no_id

    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/print.png'), 
                            _onclick = "javascript:PrintContent()"))    
    try:

        for info in db(query).select(db.vehicle.ALL):
            i = TABLE(*[
                TR(TD(B('Company Info.'), _colspan = '2', _style = 'background: #e0e0e0' )),
                TR(TD('Reg.No.:'), TD(info.reg_no)),
                TR(TD('Company:'), TD(info.company_id.company), _class = 'pure-table-odd'),
                TR(TD('Division'), TD(info.division_id.division)),
                TR(TD('Department:'), TD(info.department.name), _class = 'pure-table-odd'),
                TR(TD('Chassis No:'), TD(info.chassis_no)), 
                TR(TD('Last Reading:'), TD(info.mileage), _class = 'pure-table-odd'),
                TR(TD('Model:'), TD(info.model))], 
                _border = '0', _align = 'center', _width = '100%',  _class = 'pure-table')

        for d in db(db.vehicles_hand_over.id == request.args(0)).select(db.vehicles_hand_over.ALL):
            row1 = TABLE(*[
                TR(TD(B('Hand-Over Details'), _colspan = '2', _style = 'background: #e0e0e0')),
                TR(TD('Date & Time', _width = '60%'), TD(d.date_and_time, _width = '40%')),
                TR(TD('Mileage:'), TD(d.mileage))],
                _border = '0', _align = 'center', _width = '100%', _class = 'pure-table pure-table-horizontal')

            row2 = TABLE(*[
                TR(TD(B('Department'), _colspan = '2', _style = 'background: #e0e0e0')),
                TR(TD('From Department:', _width = '60%'), TD(d.from_department_id.name, _width = '40%')), 
                TR(TD('To Department:'), TD(d.to_department_id.name))],
                _border = '0', _align = 'center', _width = '100%', _class = 'pure-table pure-table-horizontal')
            
            row3 = TABLE(*[
                TR(TD(B('Driver'), _colspan = '2', _style = 'background: #e0e0e0')),
                TR(TD('From Driver:', _width = '60%'), TD(d.from_driver_id.driver_name, _width = '40%')), 
                TR(TD('To Driver:'), TD(d.to_driver_id.driver_name))],
                _border = '0', _align = 'center', _width = '100%', _class = 'pure-table pure-table-horizontal')    
            #DIV(', '.join(row.test))
            row4 = TABLE(*[
                TR(TD(B('Others'), _colspan = '2', _style = 'background: #e0e0e0')),                
                TR(TD('Accessories:', _width = '60%'), TD(DIV(', '.join(d.vehicles_acc)), _width = '40%')),
                TR(TD('Remarks:'), TD(d.remarks), _colspan = '3')], 
                _border = '0', _align = 'center', _width = '100%', _class = 'pure-table pure-table-horizontal')

        img_table = None
        for row in db(photo).select(db.v_photos.ALL):
            img_table = TABLE(*[
                THEAD(TR(TH('Road Permit:', _colspan = '2'), _bgcolor='#E0E0E0')),
                TR(TD(IMG(_src = URL('default', 'download', args = row.road_permit), _width = '100%', _height = '100%', _align = 'center'))),
                THEAD(TR(TH('Photos', _colspan = '2'), _bgcolor='#E0E0E0')),
                TR(TD(IMG(_src = URL('default', 'download', args = row.photo), _width = '420', _height = '300', _align = 'center'), _width = '50%'), 
                    TD(IMG(_src = URL('default', 'download', args = row.photo2), _width = '420', _height = '300', _align = 'center'), _width = '50%'))],
                _align = 'center', _width = '100%', _class = 'pure-table')
        
        for sign in db(db.vehicles_hand_over.id == request.args(0)).select(db.vehicles_hand_over.ALL):
            sign_table = TABLE(*[
                TR(TD(B(sign.from_driver_id.driver_name), _width = "30%", _align = "center"),
                    TD(B(sign.to_driver_id.driver_name), _width = "30%", _align = "center"),
                    TD("" ,_width = "30%", _align = "center")),
                TR(TD("Driver Signature:", _width = "30%", _align = "center"),
                    TD("Driver Signature:", _width = "30%", _align = "center"),
                    TD("Checked and verified by", _width = "30%", _align = "center"))],
                _border = '0', _align = 'center', _width = '100%')

        return dict(i = i, row1 = row1, row2 = row2, row3 = row3, row4 = row4, sign_table = sign_table,
            img_table = img_table, img_report = img_report)            
    except:
        redirect(URL('Reports', 'Empty')) 

def Conflict():
    return locals()

@auth.requires_login()
def HandOverReportx():
    try:
        row_id = request.args(0)
    
        for info in db(db.vehicles_hand_over.id == row_id).select(db.vehicles_hand_over.ALL):
            x = TABLE([TR(TD('Reg.No.:', _width = '20%'), TD(info.reg_no_id.reg_no, _width = '30%')),
                       TR(TD('Date and Time:', _width = '20%'), TD((info.date_and_time).strftime('%d, %B %Y %I:%M:%S %p'), _width = '30%')),
                       TR(TD('From Company:', _width = '20%'), TD(info.from_company_id.company, _width = '30%')),
                       TR(TD('To Company:', _width = '20%'), TD(info.to_company_id.company, _width = '30%')),
                       TR(TD('From Driver:', _width = '20%'), TD(info.from_driver_id.driver_name, _width = '30%')),
                       TR(TD('To Driver:', _width = '20%'), TD(info.to_driver_id.driver_name, _width = '30%')),
                       TR(TD('Mileage:', _width = '20%'), TD(info.mileage, _width = '30%')),
                       TR(TD('Vehicle Accessories:', _width = '20%'), TD(info.vehicles_acc, _width = '30%')),
                       TR(TD('Remarks:', _width = '20%'),TD(info.remarks, _width = '30%'))],
                _border = '0', _align = 'center', _width = '100%')

        for sign in db(db.vehicles_hand_over.id == row_id).select(db.vehicles_hand_over.ALL):
            sign_table = TABLE([TR(TD(sign.from_driver_id.driver_name, _width = "30%", _align = "center"),
                                   TD(sign.to_driver_id.driver_name, _width = "30%", _align = "center"),
                                   TD("" ,_width = "30%", _align = "center")),
                                TR(TD("From Driver Signature:", _width = "30%", _align = "center"),
                                   TD("To Driver Signature:", _width = "30%", _align = "center"),
                                   TD("Checked and verified by", _width = "30%", _align = "center"))],
                _border = '0', _align = 'center', _width = '100%')
    
        photo = db.v_photos.reg_no_id == db.vehicles_hand_over.reg_no_id
        row = db(photo).select(db.v_photos.ALL).first() #db.v_photos.id, db.v_photos.road_permit, db.v_photos.photo, db.v_photos.photo2).first()
        reg = db.v_photos[int(row)].road_permit
        fp  = db.v_photos[int(row)].photo
        rp  = db.v_photos[int(row)].photo2

        if reg:
            source = os.path.join(request.folder, 'uploads', reg)
            reg_img = IMG(_src = source, _width = '200', _height = '130')
        else:
            reg_img = None

        if fp:
            source = os.path.join(request.folder, 'uploads', fp)
            front_img = IMG(_src = source, _width = '200', _height = '130')
        else:
            front_img = None

        if rp:
            source = os.path.join(request.folder, 'uploads', rp)
            rear_img = IMG(_src = source, _width = '200', _height = '130')
        else:
            rear_img = None
            
        img_table = 0
        for i in db(db.v_photos.reg_no_id == db.vehicles_hand_over.reg_no_id).select(db.v_photos.ALL):
            img_table = TABLE(*[TR(TD(front_img, _width = '300'), TD(rear_img, _width = '300')),
                                TR(TD(reg_img, _width = '300'))],
                              _border = '5', _align = 'center', _width = '100%')
    
        pdf=MyFPDF()       
        pdf.add_page()
        pdf.set_font('Arial', 'B', 13)
        pdf.multi_cell(0, 8,'Hand-Over Report', 0,'C')
        pdf.write_html(str(XML(x, sanitize = False)))
        pdf.write_html(str(XML(img_table, sanitize = False)))
        pdf.write_html(str(XML(sign_table, sanitize = False)))
        response.headers['Content-Type']='application/pdf'
        return pdf.output(dest='S')
    except:
        license = redirect(URL('Reports', 'Empty')) 
        #raise HTTP(400,"sorry guy's, still in progress.")
        #return 'alert("This is a Javascript document, it is not supposed to run!");'
        #raise HTTP(400)

@auth.requires_login()
def Photos():
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))      
    for info in db(db.vehicle.id == request.args(0)).select(db.vehicle.ALL):
        i = TABLE(*[THEAD(TR(TH('Reg.No.:'), TH('Company:'),TH('Division:'),TH('Department:'),
            TH('Chassis No:'), TH('Last Reading:'),TH('Model:'), _bgcolor='#E0E0E0')),
        TR(TD(info.reg_no), TD(info.company_id.company), TD(info.division_id.division), 
            TD(info.department.name), TD(info.chassis_no),TD(str(locale.format('%d', info.mileage or 0, grouping = True)) + ' Km.'), 
            TD(info.model))], _border = '0', _align = 'center', _width = '100%', _class = 'pure-table')
    p = None
    for row in db(db.v_photos.reg_no_id == request.args(0)).select(db.v_photos.ALL):
        p = TABLE(*[THEAD(TR(TH('Road Permit:', _colspan = '2'))),
            TR(TD(IMG(_src = URL('default', 'download', args = row.road_permit)if row.road_permit else "", _width = '100%', _height = '100%', _align = 'center'))),
            THEAD(TR(TH('Photos', _colspan = '2'))),
            TR(TD(IMG(_src = URL('default', 'download', args = row.photo), _width = '450', _height = '300', _align = 'center')if row.photo else "", _width = '50%'), 
                TD(IMG(_src = URL('default', 'download', args = row.photo2), _width = '450', _height = '300', _align = 'center')if row.photo2 else "", _width = '50%')),
            TR(TD(IMG(_src = URL('default', 'download', args = row.photo3), _width = '450', _height = '300', _align = 'center')if row.photo3 else "", _width = '50%'), 
                TD(IMG(_src = URL('default', 'download', args = row.photo4), _width = '450', _height = '300', _align = 'center')if row.photo4 else "", _width = '50%'))],
            _align = 'center', _width = '100%', _class = 'table')
    return dict(i = i, img_report = img_report, p = p)




#@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
@auth.requires_login()
def VehicleProfileReport2(): 
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _src=URL('static','images/print.png'), 
                            _onclick = "javascript:PrintContent()"))  
    img_logo = IMG(_src=URL('static', 'images/header_report.png'))
    #img_logo = IMG(_src='http://example.com/image.png',_alt='test')

    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _src=URL('static','images/print.png'), 
                            _onclick = "javascript:PrintContent()"))  

    profile = db(db.vehicle.id == request.args(0)).select(db.vehicle.ALL)
                            
    for q in db(db.vehicle.id == request.args(0)).select(db.vehicle.ALL):
        c_info = TABLE(*[THEAD(TR(TH('Company Info', _colspan = '4')),
            TR(TH('Company'),TH('Division'),TH('Department'),TH('Owner'))),
            TBODY(TR(TD(q.company_id.company),TD(q.division_id.division),TD(q.department.name),TD(q.owner.name))),
            ], _class='table table-bordered',_id='company_info')
        

        v_info = TABLE(*[THEAD(TR(TH("Vehicle Info", _colspan = '6')),
            TR(TH("Vehicle Code:"),TH("Reg.No.:"),TH("Manufacturer:"),TH("Model:"),TH("Chassis No.:"),TH("Mileage:"))),
            TBODY(TR(TD(q.vehicle_code),TD(q.reg_no),TD(q.vehicle_name_id.vehicle_name),TD(q.model),TD(q.chassis_no),TD(q.mileage)), 
            TR(TH("Car Type:"),TH("Cylinder CNT:"),TH("Transmission:"),TH("Tyre Size:"),TH("Category:",_colspan='2')),
            TR(TD(q.car_type or None),TD(q.cylinder_count or None),TD(q.transmission),TD(q.tyre_size),TD(q.category_id.category,_colspan='2')))],
            _class = 'table table-bordered')
                    
        dv_info = TABLE(*[THEAD(TR(TH("Date and Value Info", _colspan = '3')),
            TR(TH("Invoice:"),TH("Exp. Date:"),TH("1st Reg. Date:"))),
            TBODY(TR(TD(q.invoice or None),TD(q.exp_date),TD(q.reg_date)), 
            TR(TH("Value PUR.:"),TH("Date of Sale:"),TH("Dep. Value:")),
            TR(TD(q.value_purchase),TD(q.date_of_sale),TD(q.depreciation_value)))],
            _class = 'table table-bordered')

        o_info = TABLE(*[THEAD(TR(TH("Others Info", _colspan = '3')),
            TR(TH("Plate Type:"),TH("Ext. Color CD:"),TH("Accessories:"))),
            TBODY(TR(TD(q.plate_type or None),TD(q.ext_color_code or None),TD(q.accessories or None)),
            TR(TH("Purpose:"),TH("Status:"),TH("Remarks:")),
            TR(TD(q.purpose.purpose),TD(q.status_id.status),TD(q.remarks)))],
            _class = 'table table-bordered')
        
    
    for row in db(db.v_photos.reg_no_id == request.args(0)).select(db.v_photos.ALL):
        p = TABLE(*[THEAD(TR(TH('Image'))),
            TBODY(TR(TD(IMG(_src=URL('default','download', args = row.photo),_class='img-thumbnail'))))],
            _class='table')
        #p = TABLE(*[THEAD(TR(TH('Road Permit:',_colspan='2'))),
            #TBODY(TR(TD(IMG(_src = URL('default', 'download', args = row.road_permit) if row.road_permit else "", _onerror="this.style.display='none'"),_colspan='2')),
            #TR(TH('Vehicle Photos:',_colspan='2')),
            #TBODY(TR(TD(IMG(_src = URL('default', 'download', args = row.photo),_onerror="this.style.display='none'",_class="img-thumbnail")), 
            #TD(IMG(_src = URL('default', 'download', args = row.photo2),_onerror="this.style.display='none'",_class="img-thumbnail"))))],
            #TR(TD(IMG(_src = URL('default', 'download', args = row.photo3),_onerror="this.style.display='none'",_class="img-thumbnail")), 
            #TD(IMG(_src = URL('default', 'download', args = row.photo4),_onerror="this.style.display='none'",_class="img-thumbnail"))))],
            #_align = 'center', _width = '100%', _class = 'table table-bordered', _id='company_info')

    return dict(c_info = c_info, v_info = v_info, dv_info = dv_info, o_info = o_info, 
        p = p, img_report = img_report, img_logo = img_logo, profile = profile)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def InsuredVehiclesReport():

    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))  

    row_id = request.args(0)
    for ip in db(db.insurance_policy.id == request.args(0)).select(db.insurance_policy.ALL):
        ip_report = TABLE(*[THEAD(TR(TD(B("Company:")), TD(B("Insurance Company:")),TD(B("Policy Covered:")), TD(B("Policy No.:")),TD(B("Amount:"))),_bgcolor='#E0E0E0'),
            TR(TD(ip.company_id.company), TD(ip.insurance_company_id.name),TD(ip.period_covered),TD(ip.policy_no),
                TD(locale.format('%.2F', ip.amount or 0, grouping = True)))], _border = '0', _align = 'left', _width = '100%', _class = 'pure-table')
    
    head = THEAD(TR(TH('No.'),TH('Reg.No.', _width = '18%'), TH('Passenger Covered', _width = '18%'), TH('Amount Insured', _width = '18%'),
        TH('Excess', _width = '18%'),TH('Amount', _width = '28%')),_bgcolor='#E0E0E0')
    r = []
    n = 0
    query = db(db.insured_vehicles.policy_no_id == row_id).select(db.insured_vehicles.ALL, orderby = ~db.insured_vehicles.reg_no_id)
    for iv in query:
        row = len(query)
        n += 1        
        r.append(TR(TD(str(n)+'.'),TD(iv.reg_no_id.reg_no, _align = 'right'), TD(iv.passenger_covered, _align = 'right'),
            TD(locale.format('%.2F', iv.amount_insured or 0, grouping = True), _align = 'right'), 
            TD(locale.format('%.2F',iv.excess or 0, grouping = True), _align = 'right'), TD(locale.format('%.2F', iv.amount or 0, grouping = True), _align = 'right')))
    
    grand_total = db.insured_vehicles.amount.sum().coalesce_zero()
    grand_total = db(db.insured_vehicles.policy_no_id == row_id).select(grand_total).first()[grand_total]
    
    body = TBODY(*r)
    i_vehicle = TABLE(*[head, body], _border = '0', _align="center", _width="100%", _class = 'pure-table')

    return dict(ip_report = ip_report, i_vehicle = i_vehicle, img_report = img_report, grand_total = grand_total)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DriverProfileReport():
    import urllib
    import StringIO
    import PIL.Image
    for x in db(db.driver.id == request.args(0)).select(db.driver.ALL):
        #lic_path = request.folder + x.driver_license
        #lic_path = ImageReader(IMG(_src = URL('default','download', args = x.driver_license)))
        #lic_path = os.path.join(request.folder, URL=('default','download'), x.driver_license)
        #imagen_logo = Image(os.path.realpath(logo),width=400,height=100)
        #lic_path = os.path.realpath(URL=('default','download',args = x.driver_license))
        #image_file = urllib.urlopen(URL('default','uploads', args = x.driver_license))
        #image_string = StringIO.StringIO(image_file.read())
        #logo = PIL.Image.open(image_string)
        #img_path = URL('default','download', args = x.driver_license)
        #_file = request.folder + URL('default','download', args = x.driver_license)
        image_file = os.path.join(request.folder, 'uploads')
        #print image_file
        category_id = db(db.authorized_vehicle_category.id.belongs(x.license_category_id)).select(db.authorized_vehicle_category.name)
        data = [['Driver Profile','','','Company Info',''],
        ['Emp. No.:',x.employee_number,'','Company:',x.company_id.company],
        ['Name:',x.driver_name,'','Division:',x.division_id.division],
        ['Position:',x.position_id.name,'','Department:',x.department_id.name],
        ['Licenses No.:',x.driver_id,'','',''],
        ['Expiration Date:',x.expiry_date,'','',''],
        ['Category:',(', '.join(x.name for x in category_id)),'','',''], 
        ['Contact No.:',x.contact_no,'','','']]
        #['License Picture:', Image(image_file),'','','']] #os.path.join(request.folder, 'uploads')
        dta_tbl = Table(data, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
        dta_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,-1),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),
            ('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
            ('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),
            ('BOX',(3,0),(4,3),0.3,colors.Color(0, 0, 0, 0.3))]))
        row.append(dta_tbl)
        doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'
        return pdf_data

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DriverReport():
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))       
    for row in db(db.driver.id == request.args(0)).select(db.driver.ALL):
        category_id = db(db.authorized_vehicle_category.id.belongs(row.license_category_id)).select(db.authorized_vehicle_category.name)
        i = TABLE(*[TR(TD(B('Company:')),TD(row.company_id.company),TD(B('Division:')), TD(row.division_id.division)),
            TR(TD(B('Department:')), TD(row.department_id.name), TD(B('Employee No.:')),TD(row.employee_number)),
            TR(TD(B('Driver Name:')), TD(row.driver_name), TD(B('License No.:')), TD(row.driver_id)),
            TR(TD(B('Position:')), TD(row.position_id.name), TD(B('Expiration Date:')), TD(row.expiry_date)),
            TR(TD(B('Category:')), TD(', '.join(r.name for r in category_id)), TD(B('Contact No.:')), TD(row.contact_no)),
            TR(TD(B('Image:'), _colspan = '4'), _bgcolor = '#f2f2f2'),
            TR(TD(IMG(_src = URL('default','download', args = row.driver_license), _width = '40%', _height = '40%', _align = 'center'), 
                _colspan = '4'))], _align = 'center', _width = '100%', _border = '0', _class = 'pure-table pure-table-horizontal')
	return dict(i = i, img_report = img_report)

def opps():
    return locals()
def Empty():
    return locals()

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Load_Activity():  
    row = []
    head = THEAD(TR(TH('Focal Person'),TH('Action Done'),TH('Log Date')))
    for a in db().select(db.activities.person, db.activities.action, db.activities.log_date, orderby=~db.activities.log_date):
        row.append(TR(TD(a.person),TD(a.action),TD(a.log_date)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _id='table', _class='table table-striped')

    return dict(table = table)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def Activity():    
    response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Latest activities', _class='white'),_class='alert alert-info') 
    return dict()
    

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def AdvertisementReport():
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))    
    row_id = request.args(0)
    ip_report = 0
    for ip in db(db.advertisement.id == row_id).select(db.advertisement.ALL):
        ip_report = TABLE(*[THEAD(TR(TD(B("Ads:")), TD(B("Logo:")),TD(B("License No.:")), TD(B("Expiry Date:")),TD(B("Amount:")))),
            TR(TD(ip.ads), TD(ip.logo),TD(ip.license_no),TD(ip.expiry_date),TD(locale.format('%.2F', ip.amount or 0, grouping = True), _align = 'right', _width ='20%'))], _border = '0', _align = 'center', _width = '100%', _class = 'pure-table')
    
    head = THEAD(TR(TH('No.:', _width = '1%'),TH('Reg.No.', _width = '15%'), TH('Amount', _width = '20%'), _bgcolor = '#E0E0E0'))
    r = []
    n = 0
    query = db(db.ads_vehicle.license_no_id == row_id).select(db.ads_vehicle.ALL, orderby = db.ads_vehicle.reg_no_id)
    for iv in query:
        row = len(query)
        n += 1
        r.append(TR(TD(str(n)+'.'),TD(iv.reg_no_id.reg_no, _align = 'left', _width = '15%'), TD(locale.format('%.2F', iv.amount or 0, grouping = True), _align = 'right', _width ='20%')))
    
    
    grand_total = db.ads_vehicle.amount.sum().coalesce_zero()
    grand_total = db(db.ads_vehicle.license_no_id == row_id).select(grand_total).first()[grand_total]

    
    body = TBODY(*r)
    i_vehicle = TABLE(*[head, body], _align = 'center', _width = '100%', _class = 'pure-table')
    return dict(ip_report = ip_report, i_vehicle = i_vehicle, grand_total = grand_total, img_report = img_report)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def VehiclesReport():
    row = []
    query = db().select(db.vehicle.ALL)
    
    head = THEAD(TR(TH('#'),TH('Company'),TH('Division'),TH('Department'),TH('Owner'),TH('Code'),TH('Reg.No.'),TH('Brand'),
        TH('Model'),TH('RPEx Date'),TH('Category'),TH('Status')))
    
    for c in query:       
        row.append(TR(TD(),TD(c.company_id.company),TD(c.division_id.division),TD(c.department.name),
            TD(c.owner.name),TD(c.vehicle_code),TD(c.reg_no),TD(c.vehicle_name_id.vehicle_name),
            TD(c.model),TD(c.exp_date),TD(c.category_id.category),TD(c.status_id.status)))
    body = TBODY(*row)
    table = TABLE(*[head,body], _class='table')
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def VehiclesReportx():
    form = SQLFORM.factory(
        Field('company_id', 'reference company',requires = IS_IN_DB(db, db.company, '%(company)s', zero = 'Choose company'),
            represent = lambda id, r: db.company(id).company, widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('order_by', requires = IS_IN_SET({'A':'Division','B':'Department','C':'Owner','D':'Veh.CD.','E':'Reg.No.','F':'Brand','G':'Model','H':'RPEx Date','I':'Category'},zero='Choose in order'),widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control'))) 
    if form.accepts(request):
        if request.vars.order_by == 'A':
            order = ~db.vehicle.division_id
        elif form.vars.order_by == 'B':
            order = ~db.vehicle.department
        elif request.vars.order_by == 'C':
            order = ~db.vehicle.owner
        elif request.vars.order_by == 'D':
            order = ~db.vehicle.vehicle_code
        elif request.vars.order_by == 'E':
            order = ~db.vehicle.reg_no
        elif request.vars.order_by == 'F':
            order = ~db.vehicle.vehicle_name_id
        elif request.vars.order_by == 'G':
            order = ~db.vehicle.model
        elif request.vars.order_by == 'H':       
            order = ~db.vehicle.exp_date
        elif request.vars.order_by == 'I':       
            order = ~db.vehicle.category_id
        else:
            order = ~db.vehicle.company_id
        ctr = 0
        query = db.vehicle.company_id == request.vars.company_id
        query &= db.vehicle.status_id != 1
        query = db(query).select(db.vehicle.ALL, orderby = order | ~db.vehicle.status_id)
        
        com_data = [['#','Company','Division','Department','Owner','Code','Reg.No.','Brand','Model','RPEx Date', 'Category','Status']]
        for c in query:       
            ctr += 1
            #[Paragraph(c.repair_history.details, styles["BodyText"])
            com_data.append([ctr, c.company_id.company,c.division_id.division,c.department.name,c.owner.name,c.vehicle_code,c.reg_no,
                c.vehicle_name_id.vehicle_name,c.model,c.exp_date,c.category_id.category,c.status_id.status])
        
        row.append(Spacer(1,0.3*cm))             
        com_tbl=Table(com_data, colWidths=[25,50,80,100,None,None,None,None,None,None,None,None,None])
        com_tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9)]))
        row.append(com_tbl)
        doc.pagesize = landscape(A4) 
        doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'
        return pdf_data  
        
    #else:
    #    return dict(form=form)

    frm_division = SQLFORM.factory(
        Field('division_id', requires = IS_IN_DB(db, db.division, '%(division)s', zero = 'Choose division'),widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('order_by', requires = IS_IN_SET({'A':'Department','B':'Owner','C':'Veh.CD.','D':'Reg.No.','E':'Brand','F':'Model','G':'RPEx Date','H':'Category'},zero='Choose in order'),widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')))    
    if frm_division.accepts(request):
        
        if frm_division.vars.order_by == 'A':
            order = db.vehicle.department
        elif frm_division.vars.order_by == 'B':
            order = db.vehicle.owner
        elif frm_division.vars.order_by == 'C':
            order = db.vehicle.vehicle_code
        elif frm_division.vars.order_by == 'D':
            order = db.vehicle.reg_no
        elif frm_division.vars.order_by == 'E':
            order = db.vehicle.vehicle_name_id
        elif frm_division.vars.order_by == 'F':
            order = db.vehicle.model
        elif frm_division.vars.order_by == 'G':
            order = db.vehicle.exp_date
        elif frm_division.vars.order_by == 'H':       
            order = db.vehicle.category_id            
        else:
            order = db.vehicle.company_id

        query = db.vehicle.division_id == frm_division.vars.division_id
        query &= db.vehicle.status_id != 1
        query = db(query).select(db.vehicle.ALL, orderby = ~db.vehicle.status_id | order )     
        ctr = 0
        div_data = [['#','Company','Division','Department','Owner','Code','Reg.No.','Brand','Model','RPEx Date', 'Category','Status']]
        for c in query:       
            ctr += 1
            #[Paragraph(c.repair_history.details, styles["BodyText"])
            div_data.append([ctr, c.company_id.company,c.division_id.division,c.department.name,c.owner.name,c.vehicle_code,c.reg_no,
                c.vehicle_name_id.vehicle_name,c.model,c.exp_date,c.category_id.category,c.status_id.status])
        
        row.append(Spacer(1,0.3*cm))             
        div_tbl=Table(div_data, colWidths=[25,50,80,100,None,None,None,None,None,None,None,None,None])
        div_tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9)]))
        row.append(div_tbl)
        doc.pagesize = landscape(A4) 
        doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'
        return pdf_data 

    frm_dep = SQLFORM.factory(
        Field('department_id', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose department'),widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')),
        Field('order_by', requires = IS_IN_SET({'A':'Owner','B':'Veh.CD.','C':'Reg.No.','D':'Brand','E':'Model','F':'RPEx Date','G':'Category'},zero='Choose in order'),widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')))
    if frm_dep.accepts(request):
        if frm_dep.vars.order_by == 'A':
            order = db.vehicle.owner
        elif frm_dep.vars.order_by == 'B':
            order = db.vehicle.vehicle_code
        elif frm_dep.vars.order_by == 'C':
            order = db.vehicle.reg_no
        elif frm_dep.vars.order_by == 'D':
            order = db.vehicle.vehicle_name_id
        elif frm_dep.vars.order_by == 'E':
            order = db.vehicle.model
        elif frm_dep.vars.order_by == 'F':
            order = db.vehicle.exp_date
        elif frm_dep.vars.order_by == 'G':       
            order = db.vehicle.category_id            
        else:
            order = db.vehicle.company_id

        query = db.vehicle.department == request.vars.department_id
        query &= db.vehicle.status_id != 1
        query = db(query).select(db.vehicle.ALL, orderby = ~db.vehicle.status_id | order )
        ctr = 0
        dep_data = [['#','Company','Division','Department','Owner','Code','Reg.No.','Brand','Model','RPEx Date', 'Category','Status']]
        for c in query:       
            ctr += 1
            #[Paragraph(c.repair_history.details, styles["BodyText"])
            dep_data.append([ctr, c.company_id.company,c.division_id.division,c.department.name,c.owner.name,c.vehicle_code,c.reg_no,
                c.vehicle_name_id.vehicle_name,c.model,c.exp_date,c.category_id.category,c.status_id.status])
        
        row.append(Spacer(1,0.3*cm))             
        dep_tbl=Table(dep_data, colWidths=[25,50,80,100,None,None,None,None,None,None,None,None,None])
        dep_tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9)]))
        row.append(dep_tbl)
        doc.pagesize = landscape(A4) 
        doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'
        return pdf_data 

    return dict(form=form, frm_division=frm_division, frm_dep=frm_dep)

             

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DepartmentVehiclesReport():   
    frm_dep = SQLFORM.factory(
        Field('department_id', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose department'), label = 'Department'),
        Field('order_by', requires = IS_IN_SET({
            'A':'Owner',
            'B':'Veh.CD.',
            'C':'Reg.No.',
            'D':'Brand', 
            'E':'Model',
            'F':'RPEx Date', 
            'G':'Category'}, 
            zero='Choose in order')))
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))    
    
    if frm_dep.accepts(request):
        
        head = THEAD(TR(TH('No.'),TH('Owner'),TH('VEH.CD.'),TH('Reg.No.'),TH('Brand'),TH('Model'),TH('RPEx Date'), 
            TH('Category'), TH('Status'), _bgcolor='#E0E0E0'))
        r = []
        if frm_dep.vars.order_by == 'A':
            order = db.vehicle.owner
        elif frm_dep.vars.order_by == 'B':
            order = db.vehicle.vehicle_code
        elif frm_dep.vars.order_by == 'C':
            order = db.vehicle.reg_no
        elif frm_dep.vars.order_by == 'D':
            order = db.vehicle.vehicle_name_id
        elif frm_dep.vars.order_by == 'E':
            order = db.vehicle.model
        elif frm_dep.vars.order_by == 'F':
            order = db.vehicle.exp_date
        elif frm_dep.vars.order_by == 'G':       
            order = db.vehicle.category_id            
        else:
            order = db.vehicle.company_id

        query = db.vehicle.department == frm_dep.vars.department_id
        query &= db.vehicle.status_id != 1
        query = db(query).select(db.vehicle.ALL, orderby = ~db.vehicle.status_id | order )
        n = 0
        for q in query: 
            row = len(query)
            n += 1
            r.append(TR(TD(n),
                        TD(q.owner.name),
                        TD(q.vehicle_code),
                        TD(q.reg_no),
                        TD(q.vehicle_name_id.vehicle_name),
                        TD(q.model),
                        TD(q.exp_date),
                        TD(q.category_id.category),
                        TD(q.status_id.status)))
        
        body = TBODY(*r)
        
        table = TABLE(*[head, body],  _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, table = table, img_report = img_report)
    else:
        return dict(form = form, table = '', img_report = None)                    

##########   With Advertisement ############
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def WAdsCompanyReport():
    form = SQLFORM.factory(
        Field('company_id', requires = IS_IN_DB(db, db.company, '%(company)s', zero = 'Choose company'), label = 'Company'))
    if form.accepts(request):
        
        head = THEAD(TR(TH('No.'),TH('Company'),TH('Division'), TH('Department'), TH('Owner'), 
            TH('VEH.CD.'),TH('Reg.No.'),TH('Brand'),TH('Model'),TH('RPEx Date'), TH('Category'),TH('Status'), _bgcolor='#E0E0E0'))
        r = []
        w_ads = db.vehicle.id == db.ads_vehicle.reg_no_id
        query = db.vehicle.company_id == form.vars.company_id
        query = db((db.vehicle.id.belongs(w_ads))&query).select(db.vehicle.ALL, orderby = db.vehicle.division_id)
        n = 0
        for q in query: 
            row = len(query)
            n += 1
            r.append(TR(TD(n),TD(q.company_id.company),TD(q.division_id.division),TD(q.department.name),TD(q.owner.name),TD(q.vehicle_code),TD(q.reg_no),TD(q.vehicle_name_id.vehicle_name),
                TD(q.model), TD(q.exp_date), TD(q.category_id.category), TD(q.status_id.status)))      
        body = TBODY(*r)
        table = TABLE(*[head, body],  _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, table = table)
    else:
        return dict(form = form, table = '')            

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def WAdsDivisionReport():
    form = SQLFORM.factory(
        Field('division_id', requires = IS_IN_DB(db, db.division, '%(division)s', zero = 'Choose division'), label = 'Division'))
    if form.accepts(request):
        
        head = THEAD(TR(TH('No.'),TH('Company'), TH('Division'), TH('Department'), TH('Owner'), 
            TH('VEH.CD.'),TH('Reg.No.'),TH('Brand'),TH('Model'),TH('RPEx Date'), TH('Category'),TH('Status'), _bgcolor='#E0E0E0'))
        r = []
        w_ads = db.vehicle.id == db.ads_vehicle.reg_no_id
        query = db.vehicle.division_id == form.vars.division_id
        query = db((db.vehicle.id.belongs(w_ads))&query).select(db.vehicle.ALL, orderby = db.vehicle.division_id)
        n = 0
        for q in query: 
            row = len(query)
            n += 1
            r.append(TR(TD(n),TD(q.company_id.company),TD(q.division_id.division), TD(q.department.name),TD(q.owner.name),TD(q.vehicle_code),TD(q.reg_no),TD(q.vehicle_name_id.vehicle_name),
                TD(q.model), TD(q.exp_date), TD(q.category_id.category), TD(q.status_id.status)))      
        body = TBODY(*r)
        table = TABLE(*[head, body],  _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, table = table)
    else:
        return dict(form = form, table = '')         

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def WAdsDepartmentReport():
    form = SQLFORM.factory(
        Field('department_id', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose department'), label = 'Department'))
    if form.accepts(request):
        
        head = THEAD(TR(TH('No.'),TH('Company'), TH('Division'), TH('Department'), TH('Owner'), 
            TH('VEH.CD.'),TH('Reg.No.'),TH('Brand'),TH('Model'),TH('RPEx Date'), TH('Category'),TH('Status'), _bgcolor='#E0E0E0'))
        r = []
        w_ads = db.vehicle.id == db.ads_vehicle.reg_no_id
        query = db.vehicle.department == form.vars.department_id
        query = db((db.vehicle.id.belongs(w_ads))&query).select(db.vehicle.ALL, orderby = db.vehicle.department)
        n = 0
        for q in query: 
            row = len(query)
            n += 1
            r.append(TR(TD(n),TD(q.company_id.company),TD(q.division_id.division),TD(q.department.name),TD(q.owner.name),TD(q.vehicle_code),TD(q.reg_no),TD(q.vehicle_name_id.vehicle_name),
                TD(q.model), TD(q.exp_date), TD(q.category_id.category), TD(q.status_id.status)))      
        body = TBODY(*r)
        table = TABLE(*[head, body],  _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, table = table)
    else:
        return dict(form = form, table = '')        

##########   With Advertisement ############        

##########   Without Advertisement ############
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def WOAdsCompanyReport():
    form = SQLFORM.factory(
        Field('company_id', requires = IS_IN_DB(db, db.company, '%(company)s', zero = 'Choose company'), label = 'Company'))
    if form.accepts(request):
        
        head = THEAD(TR(TH('No.'),TH('Company'),TH('Division'), TH('Department'), TH('Owner'), 
            TH('VEH.CD.'),TH('Reg.No.'),TH('Brand'),TH('Model'),TH('RPEx Date'), TH('Category'),TH('Status'), _bgcolor='#E0E0E0'))
        r = []
        w_ads = db.vehicle.id == db.ads_vehicle.reg_no_id
        query = db.vehicle.company_id == form.vars.company_id
        query = db(~(db.vehicle.id.belongs(w_ads))&query).select(db.vehicle.ALL, orderby = db.vehicle.division_id)
        n = 0
        for q in query: 
            row = len(query)
            n += 1
            r.append(TR(TD(n),TD(q.company_id.company),TD(q.division_id.division),TD(q.department.name),TD(q.owner.name),TD(q.vehicle_code),TD(q.reg_no),TD(q.vehicle_name_id.vehicle_name),
                TD(q.model), TD(q.exp_date), TD(q.category_id.category), TD(q.status_id.status)))      
        body = TBODY(*r)
        table = TABLE(*[head, body],  _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, table = table)
    else:
        return dict(form = form, table = '')            

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def WOAdsDivisionReport():
    form = SQLFORM.factory(
        Field('division_id', requires = IS_IN_DB(db, db.division, '%(division)s', zero = 'Choose division'), label = 'Division'))
    if form.accepts(request):
        
        head = THEAD(TR(TH('No.'),TH('Company'), TH('Division'), TH('Department'), TH('Owner'), 
            TH('VEH.CD.'),TH('Reg.No.'),TH('Brand'),TH('Model'),TH('RPEx Date'), TH('Category'),TH('Status'), _bgcolor='#E0E0E0'))
        r = []
        w_ads = db.vehicle.id == db.ads_vehicle.reg_no_id
        query = db.vehicle.division_id == form.vars.division_id
        query = db(~(db.vehicle.id.belongs(w_ads))&query).select(db.vehicle.ALL, orderby = db.vehicle.division_id)
        n = 0
        for q in query: 
            row = len(query)
            n += 1
            r.append(TR(TD(n),TD(q.company_id.company),TD(q.division_id.division), TD(q.department.name),TD(q.owner.name),TD(q.vehicle_code),TD(q.reg_no),TD(q.vehicle_name_id.vehicle_name),
                TD(q.model), TD(q.exp_date), TD(q.category_id.category), TD(q.status_id.status)))      
        body = TBODY(*r)
        table = TABLE(*[head, body],  _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, table = table)
    else:
        return dict(form = form, table = '')         

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def WOAdsDepartmentReport():
    form = SQLFORM.factory(
        Field('department_id', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose department'), label = 'Department'))
    if form.accepts(request):
        
        head = THEAD(TR(TH('No.'),TH('Company'), TH('Division'), TH('Department'), TH('Owner'), 
            TH('VEH.CD.'),TH('Reg.No.'),TH('Brand'),TH('Model'),TH('RPEx Date'), TH('Category'),TH('Status'), _bgcolor='#E0E0E0'))
        r = []
        w_ads = db.vehicle.id == db.ads_vehicle.reg_no_id
        query = db.vehicle.department == form.vars.department_id
        query = db(~(db.vehicle.id.belongs(w_ads))&query).select(db.vehicle.ALL, orderby = db.vehicle.department)
        n = 0
        for q in query: 
            row = len(query)
            n += 1
            r.append(TR(TD(n),TD(q.company_id.company),TD(q.division_id.division),TD(q.department.name),TD(q.owner.name),TD(q.vehicle_code),TD(q.reg_no),TD(q.vehicle_name_id.vehicle_name),
                TD(q.model), TD(q.exp_date), TD(q.category_id.category), TD(q.status_id.status)))      
        body = TBODY(*r)
        table = TABLE(*[head, body],  _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, table = table)
    else:
        return dict(form = form, table = '')        

##########   Without Advertisement ############        