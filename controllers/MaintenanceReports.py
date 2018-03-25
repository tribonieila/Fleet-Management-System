from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas

MaxWidth_Content = 530
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']

tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.8*inch, leftMargin=30, rightMargin=30)#, showBoundary=1)
logo_path = request.folder + 'static/images/kds-logo.jpg'
row = []

I = Image(logo_path)
I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
I.drawWidth = 1.25*inch
I.hAlign='RIGHT'
darwish = Paragraph('''<font size=14><b>Darwish Group </b><font color="gray">|</font></font> <font size=9 color="gray"> Fleet Management System</font>''',styles["BodyText"])

import time
from datetime import date
today = date.today()
###########

def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header
    header = Table([['',I],[darwish,''],['Maintenance Expenses Report','']], colWidths=[445,90])
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
form_info = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Choose category and enter date range.', _class='white'),_class='alert alert-info') 
form_warning = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-exclamation-triangle smaller-130'),B(' Warning: '), 'Other user has changed record before you did', _class='white'),_class='alert alert-warning') 

@auth.requires_login()
def MaintenanceReport():
    query = db.repair_history.id == request.args(0)
    query &= db.vehicle.id == db.repair_history.reg_no_id
    vehicle_info = db(db.vehicle.id == request.args(0)).select(db.vehicle.ALL)
    for f in db(query).select(db.vehicle.ALL, db.repair_history.ALL):
        fle_data = [['Fleet Specification','','','Company Info',''],
        ['Code:',f.vehicle.vehicle_code,'','Company:',f.vehicle.company_id.company],
        ['Reg.No.:',f.vehicle.reg_no,'','Division:',f.vehicle.division_id.division],
        ['Manufacturer:',f.vehicle.vehicle_name_id.vehicle_name,'','Department:',f.vehicle.department.name],
        ['Model:', f.vehicle.model,'', 'Owner:', f.vehicle.owner.name],
        ['','','','',''],
        ['Expenses','','','',''],
        ['Date:',f.repair_history.invoice_date,'','Labour:',locale.format('%.2F',f.repair_history.regular_maintenance or 0, grouping = True)],
        ['Invoice #:',f.repair_history.invoice_number,'','Spare Parts:',locale.format('%.2F',f.repair_history.spare_parts or 0, grouping = True)],
        ['Date Begin:',f.repair_history.date_time_in,'','Statutory Expense:',locale.format('%.2F', f.repair_history.statutory_expenses or 0, grouping = True)],
        ['Date End:',f.repair_history.date_time_out,'','Accident Repair:',locale.format('%.2F', f.repair_history.accident_repair or 0, grouping = True)],
        ['Duration:',T('%s %%{day}',abs(f.repair_history.date_time_out - f.repair_history.date_time_in).days), '','TOTAL AMOUNT:',locale.format('%.2F',f.repair_history.total_amount or 0, grouping = True)],
        ['Mileage:',locale.format('%d',f.repair_history.mileage or 0, grouping = True),'','',''],
        ['Details:',Paragraph(str(f.repair_history.details), styles["BodyText"]),'','','']]
        
        pro_tbl = Table(fle_data, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
        pro_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),
            ('LINEBELOW',(1,7),(1,13),0.50, colors.Color(0, 0, 0, 0.2)),
            ('LINEBELOW',(4,7),(4,11),0.50, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
            ('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),
            ('BACKGROUND',(0,6),(4,6),colors.Color(0, 0, 0, 0.3)),
            ('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3)),
            ('ALIGN',(4,7),(4,11),'RIGHT')]))        
        row.append(pro_tbl)
        #('ALIGN',(0,0),(0,0),'RIGHT')
        doc.build(row, onFirstPage = _header_footer, onLaterPages = _header_footer)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response['Content-Disposition'] = "attachement; filename=ProfileReport.pdf"
        response.headers['Content-Type'] = 'application/pdf'
        return pdf_data

  
@auth.requires_login()
def MaintenanceReport2():
    query = db(db.repair_history.id == request.args(0)).select(db.vehicle.ALL, db.repair_history.ALL, left=db.repair_history.on(db.repair_history.reg_no_id == db.vehicle.id))
    for c in query:
        c_info = [['Reg.No.', 'Company', 'Division', 'Department', 'Chassis No', 'Last Reading', 'Model'],       
        [c.vehicle.reg_no, c.vehicle.company_id.company, c.vehicle.division_id.division, c.vehicle.department.name, c.vehicle.chassis_no, 
        locale.format('%d',c.vehicle.mileage or 0, grouping = True), c.vehicle.model]]
    
        inv_tbl = [['Invoice', '', 'Duration', '', ''],['Invoice #', 'Date', 'Beginning', 'Ending', 'Duration'],
        [c.repair_history.invoice_number, c.repair_history.invoice_date, c.repair_history.date_time_in, c.repair_history.date_time_out,str(abs(c.repair_history.date_time_out-c.repair_history.date_time_in).days)+' days']]

        exp_tbl =[['Expenses','','','',''],
        ['Labour', 'Accident', 'Statutory', 'Spare Parts', 'Total Amount'],
        [locale.format('%.2F', c.repair_history.regular_maintenance, grouping=True), 
        locale.format('%.2F', c.repair_history.spare_parts, grouping = True),
        locale.format('%.2F', c.repair_history.statutory_expenses, grouping = True), 
        locale.format('%.2F', c.repair_history.accident_repair, grouping = True), 
        locale.format('%.2f', c.repair_history.total_amount, grouping = True)]]
        
        oth_tbl = [['Others','',''],
        ['Workshop','Mileage','Details'],
        [c.repair_history.workshop_done.workshop,locale.format('%d',c.repair_history.mileage, grouping=True),
        [Paragraph(c.repair_history.details, styles["BodyText"])]]]
        
    t=Table(c_info, colWidths=[50,70,100,100,100,70,40], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
    t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),0.50, colors.Color(0, 0, 0, 0.2)),('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(6,0),colors.Color(0, 0, 0, 0.3))]))
    row.append(t)

    row.append(Spacer(1,0.3*cm))             

    inv_tbl=Table(inv_tbl, colWidths=[130,100,100,100,100], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
    inv_tbl.setStyle(TableStyle([('GRID',(0,1),(4,2),0.5, colors.Color(0, 0, 0, 0.2)),('SPAN',(0,0),(1,0)),('SPAN',(2,0),(4,0)),('SPAN',(0,3),(4,3)),('SPAN',(0,6),(4,6)),('SPAN',(0,7),(1,7)),('SPAN',(3,7),(4,7)),('FONTSIZE',(0,0),(-1,-1),9),
        ('BACKGROUND',(0,1),(5,1),colors.Color(0, 0, 0, 0.2)),('TEXTCOLOR',(0,0),(4,0),colors.gray)]))
    row.append(inv_tbl)

    row.append(Spacer(1,0.3*cm))             
    exp_tbl=Table(exp_tbl, colWidths=[100,100,100,100,130], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
    exp_tbl.setStyle(TableStyle([('GRID',(0,1),(4,2),0.5, colors.Color(0, 0, 0, 0.2)),('SPAN',(0,0),(4,0)),('FONTSIZE',(0,0),(-1,-1),9),
        ('BACKGROUND',(0,1),(4,1),colors.Color(0, 0, 0, 0.2)),('TEXTCOLOR',(0,0),(0,0),colors.gray)]))
    row.append(exp_tbl)


    row.append(Spacer(1,0.3*cm))             
    oth_tbl=Table(oth_tbl, colWidths=[130,100,300], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
    oth_tbl.setStyle(TableStyle([('GRID',(0,1),(2,2),0.5, colors.Color(0, 0, 0, 0.2)),('SPAN',(0,0),(2,0)),('FONTSIZE',(0,0),(-1,-1),9),
        ('BACKGROUND',(0,1),(2,1),colors.Color(0, 0, 0, 0.2)),('TEXTCOLOR',(0,0),(0,0),colors.gray),('VALIGN',(0,2),(1,2),'TOP')]))
    row.append(oth_tbl)

    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data    


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_2_user') | auth.has_membership('level_3_user'))
def VehicleMaintenanceReport():

    form = SQLFORM.factory(
        Field('reg_no_id', widget = SQLFORM.widgets.autocomplete(request, db.vehicle.reg_no,
            id_field = db.vehicle.id, limitby = (0,10), min_length = 2), label = 'Reg.No.'),
        Field('start_date', 'date', requires = IS_DATE(), default = request.now),
        Field('end_date', 'date', requires = IS_DATE(), default = request.now))
    if form.accepts(request):
        query = db.repair_history.reg_no_id == request.vars.reg_no_id
        query &= db.repair_history.invoice_date >= request.vars.start_date
        query &= db.repair_history.invoice_date <= request.vars.end_date
        
        grand_total = db.repair_history.total_amount.sum().coalesce_zero()
        grand_total = db(query).select(grand_total).first()[grand_total]

        vehicle_info = db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL)
        
        for info in vehicle_info:
            i = TABLE(*[
                TR(TD(B('Vehicle Info.'), _colspan = '2', _style = 'background: #e0e0e0' )),
                TR(TD('Reg.No.:'), TD(info.reg_no)),
                TR(TD('Company:'), TD(str(info.company_id.company) + ' - ' +(info.division_id.division) + ' - '+(info.department.name)), _class = 'pure-table-odd'),
                TR(TD('Brand:'), TD(info.vehicle_name_id.vehicle_name)),
                TR(TD('Chassis No:'), TD(info.chassis_no), _class = 'pure-table-odd'), 
                TR(TD('Last Reading:'), TD(str(locale.format('%d', info.mileage or 0, grouping = True)) + ' km.')),
                TR(TD('Model:'), TD(info.model), _class = 'pure-table-odd')], 
                _border = '0', _align = 'center', _width = '100%',  _class = 'pure-table')    
               
        head = THEAD(TR(TH('No.'),TH('Invoice No.'), TH('Invoice Date'), TH('LA'), TH('SP'), 
            TH('SE'), TH('AR'), TH('Total Amount'), _bgcolor='#E0E0E0'))
        foot = THEAD(TR(TD(H4('Grand Total Amount: '), _colspan = '7', _align = 'right'), 
            TD(H4(str('QR ' + locale.format('%.2F', grand_total or 0, grouping = True))))))
        r = []
        ctr = 0
        veh_query = db(query).select(db.repair_history.ALL, orderby = ~db.repair_history.invoice_date)
        for q in veh_query:
            row = len(veh_query)
            ctr += 1
            r.append(TR(TD(ctr),TD(q.invoice_number), TD(q.invoice_date), TD(q.regular_maintenance), 
                TD(q.spare_parts), TD(q.statutory_expenses), TD(q.accident_repair),
                TD(locale.format('%.2F', q.total_amount or 0, grouping = True ), _align = 'right')))
            
        body = TBODY(*r)
        table = TABLE(*[head, body, foot], _align="center", _width="100%", _class = 'pure-table')
        veh_query = db(query).select(db.repair_history.ALL, orderby = db.repair_history.invoice_date)
        return dict(form = form,  i = i, table = table, grand_total = grand_total, veh_query = veh_query)
    else: 
        return dict(form = form, i = '', table = '',
                    grand_total = 0, veh_query = '')
    

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def CompanyMaintenanceReport():
    form = SQLFORM.factory(
        Field('company_id', requires = IS_IN_DB(db, db.company, '%(company)s', zero = 'Choose company'), label = 'Company'),
        Field('start_date', 'date', requires = IS_DATE(), default = request.now, label = 'Start Date'),
        Field('end_date', 'date', requires = IS_DATE(), default = request.now, label = 'End Date'))
    if form.accepts(request):
        query = db.vehicle.company_id == form.vars.company_id
        query &= db.vehicle.id == db.repair_history.reg_no_id
        query &= db.repair_history.invoice_date >= request.vars.start_date
        query &= db.repair_history.invoice_date <= request.vars.end_date
        
        grand_total = db.repair_history.total_amount.sum().coalesce_zero()
        grand_total = db(query).select(grand_total).first()[grand_total]
        i = ''
        for c in db(db.vehicle.company_id == form.vars.company_id).select(db.vehicle.ALL):
            i = TABLE(*[TR(TD(B('Company Info'), _colspan = '2'), _bgcolor = '#E0E0E0'),
                TR(TD('Company:'), TD(c.company_id.company)), 
                TR(TD('Start Date:'), TD(form.vars.start_date)), 
                TR(TD('End Date:'),TD(form.vars.end_date))], _border = '0', _align = 'center', 
                _width = '100%',  _class = 'pure-table')       
           
        head = THEAD(TR(TH('No.'),TH('Reg.No.'), TH('Labour'), TH('Spart Parts'), TH('Statutory Exp.'), TH('Accident Rep.'),
            TH('Total Amount'), _bgcolor='#E0E0E0'))

        foot = THEAD(TR(TD(H4('Grand Total Amount: '), _colspan = '6', _align = 'right'), 
            TD(H4(str('QR ' + locale.format('%.2F', grand_total or 0, grouping = True))))))

        r = []
        ctr = 0
        c_query = db(query).select(db.repair_history.reg_no_id, 'sum(repair_history.regular_maintenance)', 'sum(repair_history.spare_parts)',
            'sum(repair_history.statutory_expenses)', 'sum(repair_history.accident_repair)', 'sum(repair_history.total_amount)',
            groupby = db.repair_history.reg_no_id, orderby = db.repair_history.reg_no_id)
        for q in c_query: 
            ctr += 1
            r.append(TR(TD(ctr),TD(q.repair_history.reg_no_id.reg_no), 
                TD(locale.format('%.2F', q._extra['sum(repair_history.regular_maintenance)'] or 0, grouping = True)),
                TD(locale.format('%.2F',q._extra['sum(repair_history.spare_parts)'] or 0, grouping = True)), 
                TD(locale.format('%.2F',q._extra['sum(repair_history.statutory_expenses)'] or 0, grouping = True)),
                TD(locale.format('%.2F',q._extra['sum(repair_history.accident_repair)'] or 0, grouping = True)), 
                TD(locale.format('%.2F',q._extra['sum(repair_history.total_amount)'] or 0, grouping = True))))
        body = TBODY(*r)
        
        table = TABLE(*[head, body, foot], _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, i=i, table = table, grand_total = grand_total, c_query = c_query)
    else:
        return dict(form = form, i= '', table = '', c_query = '', grand_total = 0)    

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DivisionMaintenanceReport():
    form = SQLFORM.factory(
        Field('division', requires = IS_IN_DB(db, db.division, '%(division)s', zero = 'Choose division'), label = 'Division'),
        Field('start_date', 'date', requires = IS_DATE(), label = 'Start Date', default = request.now),
        Field('end_date', 'date', requires = IS_DATE(), label = 'End Date', default = request.now))
    
    if form.accepts(request):
        query = db.vehicle.division_id == request.vars.division
        query &= db.vehicle.id == db.repair_history.reg_no_id
        query &= db.repair_history.invoice_date >= request.vars.start_date
        query &= db.repair_history.invoice_date <= request.vars.end_date
        
        grand_total = db.repair_history.total_amount.sum().coalesce_zero()
        grand_total = db(query).select(grand_total).first()[grand_total]        

        division_info = db(db.vehicle.division_id == request.vars.division).select(db.vehicle.ALL)
        for c in db(db.vehicle.division_id == request.vars.division).select(db.vehicle.ALL):
            i = TABLE(*[TR(TD(B('Company Info'), _colspan = '2'), _bgcolor = '#E0E0E0'),
                TR(TD('Company:'), TD(str(c.company_id.company) + ' - ' + (c.division_id.division))), 
                TR(TD('Start Date:'), TD(form.vars.start_date)), 
                TR(TD('End Date:'),TD(form.vars.end_date))], _border = '0', _align = 'center', 
                _width = '100%',  _class = 'pure-table')    

           
        head = THEAD(TR(TH('No.'),TH('Reg.No.'), TH('Labour'), TH('Spart Parts'), 
            TH('Statutory Exp.'), TH('Accident Rep.'), TH('Total Amount'),_bgcolor='#E0E0E0'))
        foot = THEAD(TR(TD(H4('Grand Total Amount: '), _colspan = '6', _align = 'right'), 
            TD(H4(str('QR ' + locale.format('%.2F', grand_total or 0, grouping = True))))))
        r = []
        ctr = 0
        d_query = db(query).select(db.repair_history.reg_no_id, 'sum(repair_history.regular_maintenance)', 'sum(repair_history.spare_parts)',
            'sum(repair_history.statutory_expenses)', 'sum(repair_history.accident_repair)', 'sum(repair_history.total_amount)',
            groupby = db.repair_history.reg_no_id, orderby = db.repair_history.reg_no_id)
        for q in d_query: 
            ctr += 1
            r.append(TR(TD(ctr),TD(q.repair_history.reg_no_id.reg_no), 
                TD(locale.format('%.2F', q._extra['sum(repair_history.regular_maintenance)'] or 0, grouping = True)),
                TD(locale.format('%.2F',q._extra['sum(repair_history.spare_parts)'] or 0, grouping = True)), 
                TD(locale.format('%.2F',q._extra['sum(repair_history.statutory_expenses)'] or 0, grouping = True)),
                TD(locale.format('%.2F',q._extra['sum(repair_history.accident_repair)'] or 0, grouping = True)), 
                TD(locale.format('%.2F',q._extra['sum(repair_history.total_amount)'] or 0, grouping = True))))       
        body = TBODY(*r)
        table = TABLE(*[head, body, foot], _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, i= i, table = table, grand_total = grand_total, d_query = d_query)
    else:
        return dict(form = form, i= '', table = '', grand_total = 0, d_query = '')    

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DepartmentMaintenanceReport():
    form = SQLFORM.factory(
        Field('department', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose department'), label = 'Department'),
        Field('start_date', 'date', requires = IS_DATE(), default = request.now),
        Field('end_date', 'date', requires = IS_DATE(), default = request.now))  

    if form.accepts(request):       
        query = db.vehicle.department == request.vars.department
        query &= db.vehicle.id == db.fuel_expenses.reg_no_id
        query &= db.repair_history.invoice_date >= request.vars.start_date
        query &= db.repair_history.invoice_date <= request.vars.end_date

        grand_total = db.repair_history.total_amount.sum().coalesce_zero()
        grand_total = db(query).select(grand_total).first()[grand_total]   

        for c in db(db.vehicle.department == request.vars.department).select(db.vehicle.ALL):
            i = TABLE(*[TR(TD(B('Company Info'), _colspan = '2'), _bgcolor = '#E0E0E0'),
                TR(TD('Company:'), TD(str(c.company_id.company) + ' - ' + (c.division_id.division) + ' - ' + (c.department.name))), 
                TR(TD('Start Date:'), TD(form.vars.start_date)), 
                TR(TD('End Date:'),TD(form.vars.end_date))], _border = '0', _align = 'center', 
                _width = '100%',  _class = 'pure-table')    
        
        head = THEAD(TR(TH('No.'),TH('Reg.No.'), TH('Labour'), TH('Spart Parts'), 
            TH('Statutory Exp.'), TH('Accident Rep.'), TH('Total Amount'), _bgcolor='#E0E0E0'))
        
        r = []
        ctr = 0
        d_query = db(query).select(db.repair_history.reg_no_id, 'sum(repair_history.regular_maintenance)', 'sum(repair_history.spare_parts)',
            'sum(repair_history.statutory_expenses)', 'sum(repair_history.accident_repair)', 'sum(repair_history.total_amount)',
            groupby = db.repair_history.reg_no_id, orderby = ~db.repair_history.reg_no_id)
        for q in d_query: 
            ctr += 1 
            r.append(TR(TD(ctr),TD(q.repair_history.reg_no_id.reg_no),
                TD(locale.format('%.2F', q._extra['sum(repair_history.regular_maintenance)'] or 0, grouping = True), _align = 'right'),
                TD(locale.format('%.2F', q._extra['sum(repair_history.spare_parts)'] or 0, grouping = True), _align = 'right'),
                TD(locale.format('%.2F', q._extra['sum(repair_history.statutory_expenses)'] or 0, grouping = True), _align = 'right'),
                TD(locale.format('%.2F', q._extra['sum(repair_history.accident_repair)'] or 0, grouping = True), _align = 'right'),
                TD(locale.format('%.2F', q._extra['sum(repair_history.total_amount)'] or 0, grouping = True), _align = 'right')))        
        body = TBODY(*r)
        
        table = TABLE(*[head, body], _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, i=i, table = table,grand_total = grand_total, d_query = d_query)
    else:
        return dict(form = form, i= '', table = '', grand_total = 0, d_query = '')    

def HeadRpt():
    for info in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):

        table = TABLE(THEAD(TR(TH('Fleet Specification',_colspan='2',_width='40%',_class='tblhead'),TH(_width='10%'),TH('Company Info',_colspan='2',_width='40%',_class='tblhead lftborder topborder'))),
            TBODY(TR(TD('Code:'),TD(info.vehicle_code,_class='btmborder'),TD(''),TD('Company:', _class='lftborder'),TD(info.company_id.company,_class='rtborder')),
                TR(TD('Reg.No.:'),TD(info.reg_no,_class='btmborder'),TD(''),TD('Division:', _class='lftborder'),TD(info.division_id.division,_class='rtborder')),
                TR(TD('Manufacturer:'),TD(info.vehicle_name_id.vehicle_name,_class='btmborder'),TD(''),TD('Department:', _class='lftborder'),TD(info.department.name,_class='rtborder')),
                TR(TD('Model:'),TD(info.model,_class='btmborder'),TD(''),TD('Owner:', _class='lftborder btmborder'),TD(info.owner.name,_class='rtborder btmborder' ))),_class='border-collapse: collapse;',_width='100%')
    return table

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def RepairExpensesReport():
    table = ''
    rows = []
    form = FORM(DIV(
        DIV(LABEL(INPUT(_name='optionRadios',_class='ace', _type='radio', _id='opt_summary', _value='option1', _checked='true'),SPAN('Summary',_class='lbl')),_class='radio-inline'),
        DIV(LABEL(INPUT(_name='optionRadios',_class='ace', _type='radio', _id='opt_regno', _value='option2'),SPAN('Reg.No.',_class='lbl')),_class='radio-inline'),
        DIV(LABEL(INPUT(_name='optionRadios',_class='ace', _type='radio', _id='opt_company', _value='option3'),SPAN('Company',_class='lbl')),_class='radio-inline'),
        DIV(LABEL(INPUT(_name='optionRadios',_class='ace', _type='radio', _id='opt_division', _value='option4'),SPAN('Division',_class='lbl')),_class='radio-inline'),
        DIV(LABEL(INPUT(_name='optionRadios',_class='ace', _type='radio', _id='opt_department', _value='option5'),SPAN('Department',_class='lbl')),_class='radio-inline'),_class='control-group'),
        DIV(_class='space space-8'),
        DIV(DIV(DIV('Reg.No.',_class='input-group-addon'),SELECT(_name='reg_no_id', *[OPTION(r.reg_no, _value=r.id) for r in db().select(db.vehicle.ALL, orderby=db.vehicle.reg_no)],_class='form-control', widget=SQLFORM.widgets.options.widget),_class='input-group'),_class='form-group', _id='reg_no_id'),
        DIV(DIV(DIV('Company',_class='input-group-addon'),SELECT(_name='company_id',*[OPTION(c.company, _value=c.id) for c in db().select(db.company.ALL, orderby=db.company.company)], _class='form-control', widget=SQLFORM.widgets.options.widget),_class='input-group'),_class='form-group', _id='company_id'),
        DIV(DIV(DIV('Division',_class='input-group-addon'),SELECT(_name='division_id',*[OPTION(d.division, _value=d.id) for d in db().select(db.division.ALL, orderby=db.division.division)],_class='form-control', widget=SQLFORM.widgets.options.widget),_class='input-group'),_class='form-group', _id='division_id'),
        DIV(DIV(DIV('Department',_class='input-group-addon'),SELECT(_name='department_id',*[OPTION(p.name, _value=p.id) for p in db().select(db.department.ALL, orderby=db.department.name)],_class='form-control', widget=SQLFORM.widgets.options.widget),_class='input-group'),_class='form-group', _id='department_id'),
        DIV(INPUT(_id='start_date', _class='date form-control', _value=request.now.date(),_name='start_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),
            SPAN(SPAN(_class='fa fa-exchange'),_class='input-group-addon'),
            INPUT(_id='end_date', _class='date form-control', _value=request.now.date(),_name='end_date', widget=SQLFORM.widgets.date.widget,requires=IS_DATE()),
            _class='input-daterange input-group'),
        DIV(_class='space space-8'),
        INPUT(_type='submit', _value='submit', _class='btn btn-primary'))  
    if form.process().accepted:
        if request.vars.optionRadios == 'option1':
            summary_pdf = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print",_href=URL('_opt_1', args=[request.vars.start_date, request.vars.end_date]))
            query = db.vehicle.id == db.repair_history.reg_no_id
            query &= db.repair_history.invoice_date >=  request.vars.start_date
            query &= db.repair_history.invoice_date <= request.vars.end_date
            
            total_amount = db.repair_history.total_amount.sum().coalesce_zero()
            grand_total = db(query).select(total_amount).first()[total_amount]      
        
            head = THEAD(TR(TH('Company'),TH('Division'),TH('Department'),TH('Amount'),TH('Amount'),TH('Total Amount')))
            rows = []
            # for company
            for row in db(query).select(db.company.company, db.company.id, total_amount, orderby = db.company.company, groupby = db.company.id | db.company.company, join=(db.vehicle.on(db.vehicle.company_id == db.company.id))):
                rows.append(TR(TD(row.company.company),TD(),TD(),TD(),TD(),TD(locale.format('%.2F', row[total_amount] or 0, grouping = True),_align='right')))
                for row in db(query & (db.vehicle.company_id == row.company.id)).select(db.division.division, db.division.id,  total_amount, orderby = db.division.division, groupby = db.division.division | db.division.id, join=(db.vehicle.on(db.division.id == db.vehicle.division_id))):
                    rows.append(TR(TD(),TD(row.division.division),TD(),TD(),TD(locale.format('%.2F', row[total_amount] or 0, grouping = True),_align='right'),TD()))
                    for row in db(query & (db.vehicle.division_id == row.division.id)).select(db.department.name, total_amount, orderby = db.department.name, groupby = db.department.name, join=(db.vehicle.on(db.department.id == db.vehicle.department))):
                        rows.append(TR(TD(),TD(),TD(row.department.name),TD(locale.format('%.2F', row[total_amount] or 0, grouping = True),_align='right'),TD(),TD()))
            body = TBODY(*rows)
            table = TABLE(*[head, body], _class='table table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(summary_pdf, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)       
        
        elif request.vars.optionRadios == 'option2':
            reg_no_id_pdf = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print",_href=URL('_opt_2', args=[request.vars.reg_no_id, request.vars.start_date, request.vars.end_date]))
            query = db.repair_history.reg_no_id == request.vars.reg_no_id
            query &= db.repair_history.invoice_date >= request.vars.start_date
            query &= db.repair_history.invoice_date <= request.vars.end_date

            grand_total = db.repair_history.total_amount.sum().coalesce_zero()
            grand_total = db(query).select(grand_total).first()[grand_total]
        
            ctr = 0
            head = THEAD(TR(TH('#'),TH('Date'),TH('Invoice'),TH('Workshop'),TH('Duration'),TH('Mileage'),TH('Amount')))
            for row in db(query).select(db.repair_history.ALL, orderby = ~db.repair_history.invoice_date):
                ctr += 1
                rows.append(TR(TD(ctr),TD(row.invoice_date),TD(row.invoice_number),TD(row.workshop_done.workshop),TD(str(abs(row.date_time_out-row.date_time_in).days)+' days'),TD(locale.format('%d',row.mileage or 0, grouping = True)),TD(locale.format('%.2f',row.total_amount or 0, grouping = True),_style = 'text-align: right')))
            body = TBODY(*rows)
            table = HeadRpt()
            table += DIV(_class='space-2')
            table += DIV(_class='space-2')  
            table += TABLE(*[head, body], _class='table table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(reg_no_id_pdf, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)

        elif request.vars.optionRadios == 'option3':
            company_pdf = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print",_href=URL('_opt_3', args=[request.vars.company_id, request.vars.start_date, request.vars.end_date]))
            query = db.vehicle.company_id == request.vars.company_id
            query &= db.vehicle.id == db.repair_history.reg_no_id
            query &= db.repair_history.invoice_date >=  request.vars.start_date
            query &= db.repair_history.invoice_date <= request.vars.end_date
            
            total_amount = db.repair_history.total_amount.sum().coalesce_zero()
            grand_total = db(query).select(total_amount).first()[total_amount]      
        
            head = THEAD(TR(TH('Division'),TH('Department'),TH('Reg.No.'),TH('Amount'),TH('Amount'),TH('Total Amount')))
            rows = []
            # for company
            for row in db(query).select(db.division.division, db.division.id,  total_amount, orderby = db.division.division, groupby = db.division.division | db.division.id, join=(db.vehicle.on(db.division.id == db.vehicle.division_id))):
                rows.append(TR(TD(row.division.division),TD(),TD(),TD(),TD(),TD(locale.format('%.2F', row[total_amount] or 0, grouping = True),_align='right')))
                for row in db(query & (db.vehicle.division_id == row.division.id)).select(db.department.name, db.department.id, total_amount, orderby = db.department.name, groupby = db.department.name | db.department.id, join=(db.vehicle.on(db.department.id == db.vehicle.department))):
                    rows.append(TR(TD(),TD(row.department.name),TD(),TD(),TD(locale.format('%.2F', row[total_amount] or 0, grouping = True),_align='right'),TD()))
                    for row in db(query & (db.vehicle.department == row.department.id)).select(db.vehicle.reg_no, total_amount, groupby = db.vehicle.reg_no, orderby = db.vehicle.reg_no):
                         rows.append(TR(TD(),TD(),TD(row.vehicle.reg_no),TD(locale.format('%.2F',row[total_amount] or 0, grouping = True),_align=''),TD(),TD()))
            body = TBODY(*rows)
            table = TABLE(*[head, body], _class='table table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(company_pdf, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)                   

        
        elif request.vars.optionRadios == 'option4':
            division_pdf = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print",_href=URL('_opt_4', args=[request.vars.division_id, request.vars.start_date, request.vars.end_date]))
            query = db.vehicle.division_id == request.vars.division_id
            query &= db.vehicle.id == db.repair_history.reg_no_id
            query &= db.repair_history.invoice_date >=  request.vars.start_date
            query &= db.repair_history.invoice_date <= request.vars.end_date
            
            total_amount = db.repair_history.total_amount.sum().coalesce_zero()
            grand_total = db(query).select(total_amount).first()[total_amount]      
        
            head = THEAD(TR(TH('Department'),TH('Reg.No.'),TH('Amount'),TH('Total Amount')))
            rows = []
            # for company
            for row in db(query).select(db.department.id, db.department.name, total_amount, orderby = db.department.name, groupby = db.department.id | db.department.name, join=(db.vehicle.on(db.department.id == db.vehicle.department))):
                rows.append(TR(TD(row.department.name),TD(),TD(),TD(locale.format('%.2F', row[total_amount] or 0, grouping = True),_align='right')))
                for row in db(query & (db.vehicle.department == row.department.id)).select(db.vehicle.reg_no, total_amount, orderby = db.vehicle.reg_no, groupby = db.vehicle.reg_no):
                    rows.append(TR(TD(),TD(row.vehicle.reg_no),TD(locale.format('%.2F',row[total_amount] or 0, grouping = True),_align='right'),TD()))
            body = TBODY(*rows)
            table = TABLE(*[head, body], _class='table table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(division_pdf, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)   
        
        elif request.vars.optionRadios == 'option5':
            department_pdf = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print",_href=URL('_opt_5', args=[request.vars.department_id, request.vars.start_date, request.vars.end_date]))
            query = db.vehicle.department == request.vars.department_id
            query &= db.vehicle.id == db.repair_history.reg_no_id
            query &= db.repair_history.invoice_date >=  request.vars.start_date
            query &= db.repair_history.invoice_date <= request.vars.end_date
            
            total_amount = db.repair_history.total_amount.sum().coalesce_zero()
            grand_total = db(query).select(total_amount).first()[total_amount]      
        
            head = THEAD(TR(TH('#'),TH('Reg.No.'),TH('Amount')))
            rows = []
            # for company
            ctr = 0
            for row in db(query).select(db.vehicle.reg_no, total_amount, orderby = db.vehicle.reg_no, groupby = db.vehicle.reg_no):
                ctr += 1
                rows.append(TR(TD(ctr),TD(row.vehicle.reg_no),TD(locale.format('%.2F',row[total_amount] or 0, grouping = True),_align='right')))
            body = TBODY(*rows)
            table = TABLE(*[head, body], _class='table table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(department_pdf, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)   
        
        #else:
        #    response.flash = 'else'

    response.flash = form_info
    return dict(form=form, table = '')

def _opt_1():
    query = db.vehicle.id == db.repair_history.reg_no_id
    query &= db.repair_history.invoice_date >=  request.args(0)
    query &= db.repair_history.invoice_date <= request.args(1)
    
    total_amount = db.repair_history.total_amount.sum().coalesce_zero()
    grand_total = db(query).select(total_amount).first()[total_amount]       

    row_data = [['Company','Division','Department','Amount','Amount','Total Amount']]

    for q in db(query).select(db.company.company, db.company.id, total_amount, orderby = db.company.company, groupby = db.company.id | db.company.company, join=(db.vehicle.on(db.vehicle.company_id == db.company.id))):
        row_data.append([q.company.company,'','','','',locale.format('%.2F', q[total_amount] or 0, grouping = True)])
        for d in db(query & (db.vehicle.company_id == q.company.id)).select(db.division.division, db.division.id,  total_amount, orderby = db.division.division, groupby = db.division.division | db.division.id, join=(db.vehicle.on(db.division.id == db.vehicle.division_id))):
            row_data.append(['',d.division.division,'','',locale.format('%.2F', d[total_amount] or 0, grouping=True)])
            for p in db(query & (db.vehicle.division_id == d.division.id)).select(db.department.name, total_amount, orderby = db.department.name, groupby = db.department.name, join=(db.vehicle.on(db.department.id == db.vehicle.department))):
                row_data.append(['','', p.department.name, locale.format('%.2F',p[total_amount] or 0, grouping = True)])
    row_data.append(['Duration Period: ' + request.args(0) + ' - ' + request.args(1),'','','GRAND TOTAL:','',locale.format('%.2F', grand_total or 0, grouping = True)])   
    row = []
    que_tbl=Table(row_data, colWidths=[96,96,96,80,80,80], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)                                                              
    que_tbl.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),('GRID',(0,0),(-1,-2),0.5, colors.Color(0, 0, 0, 0.2)),('ALIGN',(3,1),(5,-1),'RIGHT'),('TOPPADDING',(0,-1),(5,-1), 10),('SPAN',(0,-1),(3,-1)),('SPAN',(3,-1),(4,-1)),('TEXTCOLOR',(5,-1),(5,-1),colors.red),('FONTSIZE',(3,-1),(5,-1),11)]))        
    row.append(que_tbl)    
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data   

  
def _opt_2():
    query = db.vehicle.id == request.args(0)
    query &= db.repair_history.reg_no_id == db.vehicle.id
    query &= db.repair_history.invoice_date >= request.args(1)
    query &= db.repair_history.invoice_date <= request.args(2)

    grand_total = db.repair_history.total_amount.sum().coalesce_zero()
    grand_total = db(query).select(grand_total).first()[grand_total]

    row=[]                     
    for f in db(query).select(db.vehicle.ALL):
        fle_data = [['Fleet Specification','','','Company Info',''],
        ['Code:',f.vehicle_code,'','Company:',f.company_id.company],
        ['Reg.No.:',f.reg_no,'','Division:',f.division_id.division],
        ['Manufacturer:',f.vehicle_name_id.vehicle_name,'','Department:',f.department.name],
        ['Model:', f.model,'', 'Owner:', f.owner.name]]
    fle_tbl = Table(fle_data, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
    fle_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),
        ('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3))]))
    row.append(fle_tbl)
    row.append(Spacer(1,0.3*cm))             
    fle_query = db(query).select(db.repair_history.ALL, orderby = ~db.repair_history.invoice_date)        
    ctr = 0
    fle_data = [['#','Date','Invoice','Workshop','Duration','Mileage','Total Amount']]
    for v in fle_query:
        ctr += 1
        fle_data.append([ctr,v.invoice_date,v.invoice_number,v.workshop_done.workshop,T('%s %%{day}',abs(v.date_time_out-v.date_time_in).days),locale.format('%d',v.mileage or 0, grouping=True),locale.format('%.2f',v.total_amount or 0, grouping=True)])
    fle_data.append(['Duration Period: ' + request.args(1) + ' - ' + request.args(2),'','','','GRAND TOTAL:','' , locale.format('%.2F', grand_total or 0, grouping = True)])
    row.append(Spacer(1,0.3*cm))
    fle_tble=Table(fle_data, colWidths=[25,70,85,140,70,70,70])                                                              
    fle_tble.setStyle(TableStyle([('ALIGN',(4,1),(6,-1),'RIGHT'),('ALIGN',(4,-1),(5,-1),'RIGHT'),('TEXTCOLOR',(6,-1),(6,-1),colors.red),
        ('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),('FONTSIZE',(4,-1),(6,-1),11),
        ('GRID',(0,0),(-1,-2),0.5, colors.Color(0, 0, 0, 0.2)),('TOPPADDING',(0,-1),(6,-1), 10),
        ('SPAN',(0,-1),(3,-1)),('SPAN',(4,-1),(5,-1))]))
    row.append(fle_tble)
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data   
    
def _opt_3():
    com_row = []
    ctr = 0
    query = db.vehicle.company_id == request.args(0)
    query &= db.vehicle.id == db.repair_history.reg_no_id
    query &= db.repair_history.invoice_date >=  request.args(1)
    query &= db.repair_history.invoice_date <= request.args(2)
    
    total_amount = db.repair_history.total_amount.sum().coalesce_zero()
    grand_total = db(query).select(total_amount).first()[total_amount]       

    row_data = [['Division','Department','Reg.No.','Amount','Amount','Total Amount']]

    #for q in db(query).select(db.company.company, db.company.id, total_amount, orderby = db.company.company, groupby = db.company.id | db.company.company, join=(db.vehicle.on(db.vehicle.company_id == db.company.id))):
    #    row_data.append([q.company.company,'','','','',locale.format('%.2F', q[total_amount] or 0, grouping = True)])
    for d in db(query).select(db.division.division, db.division.id,  total_amount, orderby = db.division.division, groupby = db.division.division | db.division.id, join=(db.vehicle.on(db.division.id == db.vehicle.division_id))):
        row_data.append([d.division.division,'','','','',locale.format('%.2F', d[total_amount] or 0, grouping=True)])
        for p in db(query & (db.vehicle.division_id == d.division.id)).select(db.department.id, db.department.name, total_amount, orderby = db.department.name, groupby = db.department.name | db.department.id, join=(db.vehicle.on(db.department.id == db.vehicle.department))):
            row_data.append(['', p.department.name, '','',locale.format('%.2F',p[total_amount] or 0, grouping = True),''])
            for r in db(query & (db.vehicle.department == p.department.id)).select(db.vehicle.reg_no, total_amount, orderby = db.vehicle.reg_no, groupby = db.vehicle.reg_no):
                row_data.append(['','',r.vehicle.reg_no, locale.format('%.2F',r[total_amount] or 0, grouping = True),'',''])
    row_data.append(['Duration Period: ' + request.args(1) + ' - ' + request.args(2),'','','GRAND TOTAL:','',locale.format('%.2F', grand_total or 0, grouping = True)])   
    row = []
    que_tbl=Table(row_data, colWidths=[96,96,96,80,80,80], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)                                                              
    que_tbl.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),('GRID',(0,0),(-1,-2),0.5, colors.Color(0, 0, 0, 0.2)),('ALIGN',(3,1),(5,-1),'RIGHT'),('TOPPADDING',(0,-1),(5,-1), 10),('SPAN',(0,-1),(3,-1)),('SPAN',(3,-1),(4,-1)),('TEXTCOLOR',(5,-1),(5,-1),colors.red),('FONTSIZE',(3,-1),(5,-1),11)]))        
    row.append(que_tbl)    
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data   

def _opt_4():
    ctr = 0
    query = db.vehicle.division_id == request.args(0)
    query &= db.vehicle.id == db.repair_history.reg_no_id
    query &= db.repair_history.invoice_date >=  request.args(1)
    query &= db.repair_history.invoice_date <= request.args(2)
    
    total_amount = db.repair_history.total_amount.sum().coalesce_zero()
    grand_total = db(query).select(total_amount).first()[total_amount]       

    row_data = [['Department','Reg.No.','Amount','Total Amount']]
    for p in db(query).select(db.department.id, db.department.name, total_amount, orderby = db.department.name, groupby = db.department.name | db.department.id, join=(db.vehicle.on(db.department.id == db.vehicle.department))):
        row_data.append([ p.department.name, '','',locale.format('%.2F',p[total_amount] or 0, grouping = True)])
        for r in db(query & (db.vehicle.department == p.department.id)).select(db.vehicle.reg_no, total_amount, orderby = db.vehicle.reg_no, groupby = db.vehicle.reg_no):
            row_data.append(['',r.vehicle.reg_no, locale.format('%.2F',r[total_amount] or 0, grouping = True),''])
    row_data.append(['Duration Period: ' + request.args(1) + ' - ' + request.args(2),'','GRAND TOTAL:',locale.format('%.2F', grand_total or 0, grouping = True)])   
    row = []
    que_tbl=Table(row_data, colWidths=[132,132,132,132], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)                                                              
    que_tbl.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1),9),
        ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),
        ('GRID',(0,0),(-1,-2),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN',(2,1),(3,-1),'RIGHT'),
        ('TOPPADDING',(0,-1),(3,-1), 10),
        #('SPAN',(0,-1),(1,-1)),
        ('TEXTCOLOR',(3,-1),(3,-1),colors.red),('FONTSIZE',(2,-1),(3,-1),11)]))        
    row.append(que_tbl)    
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data   

def _opt_5():
    ctr = 0

    query = db.vehicle.department == request.args(0)
    query &= db.vehicle.id == db.repair_history.reg_no_id
    query &= db.repair_history.invoice_date >=  request.args(1)
    query &= db.repair_history.invoice_date <= request.args(2)
    
    total_amount = db.repair_history.total_amount.sum().coalesce_zero()
    grand_total = db(query).select(total_amount).first()[total_amount]       

    for f in db(query).select(db.vehicle.ALL):
        fle_data = [['Company Info',''],
        ['Company:',f.company_id.company],
        ['Division:',f.division_id.division],
        ['Department:',f.department.name]]
    fle_tbl = Table(fle_data, colWidths=[100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0, hAlign='RIGHT')
    fle_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,-1),0.50, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
        ('BOX',(0,0),(-1,-1),0.3,colors.Color(0, 0, 0, 0.3))]))
    

    row_data = [['#','Reg.No.','Total Amount']]
    for r in db(query).select(db.vehicle.reg_no, total_amount, orderby = db.vehicle.reg_no, groupby = db.vehicle.reg_no):
        ctr += 1
        row_data.append([ctr,r.vehicle.reg_no, locale.format('%.2F',r[total_amount] or 0, grouping = True)])
    row_data.append(['Duration Period: ' + request.args(1) + ' - ' + request.args(2)])#,'GRAND TOTAL:',locale.format('%.2F', grand_total or 0, grouping = True)])   
    
    que_tbl=Table(row_data, colWidths=[25,100,100], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0, hAlign='LEFT')  
    #TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')])                                                            
    que_tbl.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1),9),('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),
        ('GRID',(0,0),(-1,-2),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN',(2,1),(2,-1),'RIGHT'),('ALIGN',(1,-1),(2,-1),'RIGHT'),
        ('TOPPADDING',(0,-1),(2,-1), 10),
        #('SPAN',(0,-1),(1,-1)),
        ('TEXTCOLOR',(2,-1),(2,-1),colors.red),('FONTSIZE',(1,-1),(2,-1),11)]))        

    two_tbl = Table([[fle_tbl, que_tbl]])
    two_tbl.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    row.append(two_tbl)
    #row.append(que_tbl)    
    #row.append(fle_tbl)


    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data   

def ord():
    com_que = db.vehicle.company_id == 54 #request.vars.company_id
    com_que &= db.vehicle.id == db.repair_history.reg_no_id
    com_que &= db.repair_history.invoice_date >= datetime.date(2015,6,11)
    com_que &= db.repair_history.invoice_date <= datetime.date(2016,6,11)
    #rows = db(db.person).select(join=db.thing.on(db.person.id == db.thing.owner_id))
    #query = db(db.vehicle.department.belongs(query)).select(db.vehicle.department)
    #query = db(com_que).select(db.vehicle.ALL)
    for c in db(com_que).select(db.vehicle.company_id, orderby=db.vehicle.company_id, groupby=db.vehicle.company_id):
        print c.company_id.company
        for d in db(com_que & (db.vehicle.company_id == c.company_id)).select(db.vehicle.division_id, orderby=db.vehicle.division_id, groupby=db.vehicle.division_id):
            print '          ' +  d.division_id.division
            #for p in db(com_que & (db.vehicle.division_id == d.division_id)).select(db.vehicle.department, orderby=db.vehicle.department, groupby=db.vehicle.department):
            for p in db(com_que & (db.vehicle.division_id == d.division_id)).select(db.vehicle.department, db.department.name, orderby=db.department.name, groupby=db.department.name | db.vehicle.department, join=(db.vehicle.on(db.department.id == db.vehicle.department))):
                print '                      '+p.department.name 
                query = db(com_que & (db.vehicle.department == p.vehicle.department)).select(db.vehicle.id, db.vehicle.reg_no, orderby=db.vehicle.id | db.vehicle.reg_no, groupby=db.vehicle.id | db.vehicle.reg_no, join=(db.repair_history.on(db.vehicle.id == db.repair_history.reg_no_id)))
                for r in query: #db(com_que & (db.vehicle.department == p.vehicle.department)).select(db.vehicle.reg_no, orderby=~db.vehicle.reg_no, groupby=db.vehicle.reg_no, join=(db.repair_history.on(db.vehicle.id == db.repair_history.reg_no_id))):
                    print '                                       '+ str(r.id) + ' - ' + r.reg_no
    return query
        #for d in db()
        #    return d.division_id.division

    
    #query = db(db.division.company_id.belongs(query)).select(db.division.division, orderby=db.division.division, groupby=db.division.division)
    #div_query = db(com_que)._select(db.vehicle.division_id)
    #query = db(db.department.division_id.belongs(query)).select(db.department.name, orderby=db.department.name)

    

def test():
    elements = []
    # Make heading for each column and start data list
    column1Heading = "COLUMN ONE HEADING"
    column2Heading = "COLUMN TWO HEADING"
    # Assemble data for each column using simple loop to append it into data list
    data = [[column1Heading,column2Heading]]
    for i in range(1,100):
        data.append([str(i),str(i)])

    tableThatSplitsOverPages = Table(data, [6 * cm, 6 * cm], repeatRows=1)
    tableThatSplitsOverPages.hAlign = 'LEFT'
    tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                           ('VALIGN',(0,0),(-1,-1),'TOP'),
                           ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
                           ('BOX',(0,0),(-1,-1),1,colors.black),
                           ('BOX',(0,0),(0,-1),1,colors.black)])
    tblStyle.add('BACKGROUND',(0,0),(1,0),colors.lightblue)
    tblStyle.add('BACKGROUND',(0,2),(1,2),colors.gray)
    tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
    tableThatSplitsOverPages.setStyle(tblStyle)
    elements.append(tableThatSplitsOverPages)

    doc.build(elements)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data 

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def CompanyMaintenanceSummaryReport():
    form = SQLFORM.factory(
        Field('start_date', 'date', default = request.now, requires = IS_DATE(), label = 'Start Date'),
        Field('end_date', 'date', default = request.now,  requires = IS_DATE(), label = 'End Date'))
    if form.accepts(request):
        query = db.vehicle.id == db.repair_history.reg_no_id
        query &= db.repair_history.invoice_date >= request.vars.start_date
        query &= db.repair_history.invoice_date <= request.vars.end_date

        total_amount = db.repair_history.total_amount.sum().coalesce_zero()
        grand_total = db(query).select(total_amount).first()[total_amount]

        i = TABLE(*[THEAD(TR(TH('Start Date:'), TH('End Date:'),_bgcolor = '#E0E0E0')),
            TR(TD(request.vars.start_date), TD(request.vars.end_date))], _align = 'center', _width = '100%', _class = 'pure-table')

        head = THEAD(TR(TH('Company'), TH('Division'), TH('Department'), TH('Amount'), TH('Amount'), TH('Total Amount'), _bgcolor = '#E0E0E0'))
        foot = THEAD(TR(TD(H4('Grand Total Amount: '), _colspan = '5', _align = 'right'), TD(H4(str('QR ' + locale.format('%.2F', grand_total or 0, grouping = True))))))
        row = []
        q_company = db(query).select(db.vehicle.company_id, total_amount, orderby = ~db.vehicle.company_id, groupby = db.vehicle.company_id)
        for c in q_company:
            row.append(TR(TD(c.vehicle.company_id.company), TD(), TD(), TD(), TD(),
                TD(locale.format('%.2F', c[total_amount] or 0, grouping = True), _align = 'right')))
            # Sub-Division
            q_division = db((query)&(db.vehicle.company_id == c.vehicle.company_id)).select(db.vehicle.division_id, total_amount, orderby = ~db.vehicle.division_id, groupby = db.vehicle.division_id)
            for d in q_division:
                row.append(TR(TD(), TD(d.vehicle.division_id.division), TD(),TD(),TD(locale.format('%.2F',d[total_amount] or 0, grouping = True)),TD()))
                # Sub-Department
                q_department = db((query)&(db.vehicle.division_id == d.vehicle.division_id)).select(db.vehicle.department, total_amount, orderby = ~db.vehicle.department, groupby = db.vehicle.department)
                for t in q_department:
                    row.append(TR(TD(), TD(), TD(t.vehicle.department.name), TD(locale.format('%.2F',t[total_amount] or 0, grouping = True)), TD(), TD()))

        body = TBODY(*row)
        table = TABLE(*[head, body, foot], _align="center", _width="100%", _class = 'pure-table')
        q_division = db(query).select(db.vehicle.division_id, total_amount, orderby = ~db.vehicle.division_id, groupby = db.vehicle.division_id)
        q_department = db(query).select(db.vehicle.department, total_amount, orderby = ~db.vehicle.department, groupby = db.vehicle.department)
        return dict(form = form, i = i, table = table, total_amount = total_amount, grand_total = grand_total, q_company = q_company, q_division =q_division, q_department = q_department)
    else:
        return dict(form = form, i = '', table = '', grand_total = 0, q_company='', q_division = '', q_department = '')


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DivisionMaintenanceSummaryReport():
    form = SQLFORM.factory(
        Field('start_date', 'date', requires = IS_DATE(), label = 'Start Date', default = request.now),
        Field('end_date', 'date', requires = IS_DATE(), label = 'End Date', default = request.now))
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
        _onclick = "javascript:PrintContent()"))
    if form.accepts(request):
        query = db.vehicle.id == db.repair_history.reg_no_id
        query &= db.repair_history.invoice_date >= form.vars.start_date
        query &= db.repair_history.invoice_date <= form.vars.end_date

        total_amount = db.repair_history.total_amount.sum().coalesce_zero()
        grand_total = db(query).select(total_amount).first()[total_amount]

        i = TABLE(*[THEAD(TR(TH('Start Date:'), TH('End Date:'), _bgcolor = '#E0E0E0')),
            TR(TD(form.vars.start_date), TD(form.vars.end_date))], _align = 'center', _width = '100%', _class = 'pure-table')

        head = THEAD(TR(TH('Division', _width = "50%"), TH('Total Amount', _width = "20%"), _bgcolor = '#E0E0E0'))

        m = []
        for m_rep in db(query).select(db.vehicle.division_id, total_amount, groupby = db.vehicle.division_id):
            m.append(TR(TD(m_rep.vehicle.division_id.division, _width = '50%'),
                        TD(locale.format('%.2F', m_rep[total_amount] or 0, grouping = True), _align = 'right', _width = '20%')))

        body = TBODY(*m)
        table = TABLE(*[head, body], _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, i = i, table = table, img_report = img_report, grand_total = grand_total)
    else:
        return dict(form = form, i = '', table = 'Enter Start date & End date', img_report = None, grand_total = 0)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DepartmentMaintenanceSummaryReport():
    form = SQLFORM.factory(
        Field('start_date', 'date', default = request.now, requires = IS_DATE(), label = 'Start Date'),
        Field('end_date', 'date', default = request.now, requires = IS_DATE(), label = 'End Date'))
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
        _onclick = "javascript:PrintContent()"))
    if form.accepts(request):
        query = db.vehicle.id == db.repair_history.reg_no_id
        query &= db.repair_history.invoice_date >= request.vars.start_date
        query &= db.repair_history.invoice_date <= request.vars.end_date

        total_amount = db.repair_history.total_amount.sum().coalesce_zero()
        grand_total = db(query).select(total_amount).first()[total_amount]

        i = TABLE(*[THEAD(TR(TH('Start Date:'), TH('End Date:'),_bgcolor = '#E0E0E0')), 
            TR(TD(request.vars.start_date), TD(request.vars.end_date))], _align = 'center', _width = '100%', _class = 'pure-table')

        head = THEAD(TR(TH('Department', _width = "50%"), TH('Total Amount', _width = "20%"), _bgcolor = '#E0E0E0'))

        m = []
        for m_rep in db(query).select(db.vehicle.department, total_amount, groupby = db.vehicle.department):
            m.append(TR(TD(m_rep.vehicle.department.name, _width = '50%'),
                        TD(locale.format('%.2F', m_rep[total_amount] or 0, grouping = True), _align = 'right', _width = '20%')))

        body = TBODY(*m )
        table = TABLE(*[head, body], _align="center", _width="100%", _class = 'pure-table')

        return dict(form = form, i = i, table = table, img_report = img_report, grand_total = grand_total)
    else:
        return dict(form = form, i = '', table = 'Enter Start date & End date', img_report = None, grand_total = 0)
