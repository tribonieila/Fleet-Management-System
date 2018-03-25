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

width=535

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

def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header
    header = Table([['',I],[darwish,''],['Fuel Expenses Report','']], colWidths=[445,90])
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

def btn_report():
    img_report = FORM(INPUT(_title = 'Print', _type = 'image',  _target = "_blank",_src=URL('static','images/print.png'), 
                            _onclick = "javascript:PrintContent()"))       
    chart_link = FORM(INPUT(**{'_title':'Graph', '_type':'image',  '_data-target':'.modal-large','_data-toggle':'modal', 
        '_src':URL('static','images/chart.png')}))   
    table = TABLE(*[TR(TD(),TD(img_report))], _align = 'right')
    return table

def ReportScript():
    return locals()

form_success = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Record shows.', _class='white'),_class='alert alert-success') 
form_error = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-warning smaller-130'),B(' Error: '), 'Errors in form, please check it out.', _class='white'),_class='alert alert-danger') 
form_info = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-info-circle smaller-130'),B(' Info: '), 'Choose category and enter date range.', _class='white'),_class='alert alert-info') 
form_warning = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-exclamation-triangle smaller-130'),B(' Warning: '), 'Other user has changed record before you did', _class='white'),_class='alert alert-warning') 
def HeadRpt():
    for info in db(db.vehicle.id == request.vars.reg_no_id).select(db.vehicle.ALL):

        table = TABLE(THEAD(TR(TH('Fleet Specification',_colspan='2',_width='40%',_class='tblhead'),TH(_width='10%'),TH('Company Info',_colspan='2',_width='40%',_class='tblhead lftborder topborder'))),
            TBODY(TR(TD('Code:'),TD(info.vehicle_code,_class='btmborder'),TD(''),TD('Company:', _class='lftborder'),TD(info.company_id.company,_class='rtborder')),
                TR(TD('Reg.No.:'),TD(info.reg_no,_class='btmborder'),TD(''),TD('Division:', _class='lftborder'),TD(info.division_id.division,_class='rtborder')),
                TR(TD('Manufacturer:'),TD(info.vehicle_name_id.vehicle_name,_class='btmborder'),TD(''),TD('Department:', _class='lftborder'),TD(info.department.name,_class='rtborder')),
                TR(TD('Model:'),TD(info.model,_class='btmborder'),TD(''),TD('Owner:', _class='lftborder btmborder'),TD(info.owner.name,_class='rtborder btmborder' ))),_class='border-collapse: collapse;',_width='100%')
    return table
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def FuelExpensesReport():
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
            sum_que = db.vehicle.id == db.fuel_expenses.reg_no_id
            sum_que &= db.fuel_expenses.date_expense >= form.vars.start_date
            sum_que &= db.fuel_expenses.date_expense <= form.vars.end_date

            total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
            grand_total = db(sum_que).select(total_amount).first()[total_amount]
                
            head = THEAD(TR(TH('Company'),TH('Division'),TH('Department'),TH('Amount'),TH('Amount'),TH('Total Amount')))
            row = []
            # company
            for c in db(sum_que).select(db.company.company, db.company.id, total_amount, orderby = db.company.company, groupby = db.company.id | db.company.company, join=(db.vehicle.on(db.vehicle.company_id == db.company.id))):
                row.append(TR(TD(c.company.company),TD(),TD(),TD(),TD(),TD(locale.format('%.2F', c[total_amount] or 0, grouping = True),_align='right')))
                # division 
                for d in db(sum_que & (db.vehicle.company_id == c.company.id)).select(db.division.division, db.division.id,  total_amount, orderby = db.division.division, groupby = db.division.division | db.division.id, join=(db.vehicle.on(db.division.id == db.vehicle.division_id))):      
                    row.append(TR(TD(),TD(d.division.division),TD(),TD(),TD(locale.format('%.2F', d[total_amount] or 0, grouping = True),_align='right'),TD()))

                    # department
                    for p in db(sum_que & (db.vehicle.division_id == d.division.id)).select(db.department.name, total_amount, orderby = db.department.name, groupby = db.department.name, join=(db.vehicle.on(db.department.id == db.vehicle.department))):
                        row.append(TR(TD(),TD(),TD(p.department.name),TD(locale.format('%.2F', p[total_amount] or 0, grouping = True),_align='right'),TD(),TD()))

            body = TBODY(*row)
            table = TABLE(*[head, body], _class='table table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(summary_pdf, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form = form, table = table)       

            
        elif request.vars.optionRadios == 'option2':
            reg_no_id_pdf = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print",_href=URL('_opt_2', args=[request.vars.reg_no_id, request.vars.start_date, request.vars.end_date]))
            reg_row = []
            reg_que = db.fuel_expenses.reg_no_id == request.vars.reg_no_id
            reg_que &= db.fuel_expenses.date_expense >= request.vars.start_date
            reg_que &= db.fuel_expenses.date_expense <= request.vars.end_date

            grand_total = db.fuel_expenses.amount.sum().coalesce_zero()
            grand_total = db(reg_que).select(grand_total).first()[grand_total]
                      
            head = THEAD(TR(TH('#'),TH('Date'),TH('Paid By'),TH('Station'),TH('Amount')))
            ctr = 0
            for r in db(reg_que).select(db.fuel_expenses.ALL, orderby = ~db.fuel_expenses.date_expense):
                ctr += 1
                reg_row.append(TR(TD(ctr),TD(r.date_expense),TD(r.paid_by),TD(r.station),TD(locale.format('%.2f', r.amount or 0, grouping = True),_align='right')))
            body = TBODY(*reg_row)
            table = HeadRpt()
            table += DIV(_class='space-2')
            table += DIV(_class='space-2')              
            table += TABLE(*[head, body],_class = 'table table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(reg_no_id_pdf, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 

            return dict(form=form, table = table)               
        elif request.vars.optionRadios == 'option3':
            company_pdf = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print",_href=URL('_opt_3', args=[request.vars.company_id, request.vars.start_date, request.vars.end_date]))
            com_row = []
            com_que = db.vehicle.company_id == request.vars.company_id
            com_que &= db.vehicle.id == db.fuel_expenses.reg_no_id
            com_que &= db.fuel_expenses.date_expense >= request.vars.start_date
            com_que &= db.fuel_expenses.date_expense <= request.vars.end_date 

            total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
            grand_total = db.fuel_expenses.amount.sum().coalesce_zero()
            grand_total = db(com_que).select(grand_total).first()[grand_total]
           
            head = THEAD(TR(TH('Division'),TH('Department'),TH('Reg.No.'),TH('Amount'),TH('Amount'),TH('Total Amount')))
            table = DIV('Period: ' + request.vars.start_date + ' - ' + request.vars.end_date)

            
            # division 
            for d in db(com_que & (db.vehicle.company_id == request.vars.company_id)).select(db.division.division, db.division.id,  total_amount, orderby = db.division.division, groupby = db.division.division | db.division.id, join=(db.vehicle.on(db.division.id == db.vehicle.division_id))):
                com_row.append(TR(TD(d.division.division),TD(),TD(),TD(),TD(),TD(locale.format('%.2F', d[total_amount] or 0, grouping = True),_align='right'))) 
            
                # department
                for p in db(com_que & (db.vehicle.division_id == d.division.id)).select(db.department.id, db.department.name, total_amount, orderby = db.department.name, groupby = db.department.id | db.department.name, join=(db.vehicle.on(db.department.id == db.vehicle.department))):
                    com_row.append(TR(TD(),TD(p.department.name),TD(),TD(),TD(locale.format('%.2F', p[total_amount] or 0, grouping = True),_align='right'),TD()))

                    # reg.no
                    for r in db(com_que & (db.vehicle.department == p.department.id)).select(db.vehicle.reg_no, total_amount, orderby=db.vehicle.reg_no, groupby=db.vehicle.reg_no, join=(db.vehicle.on(db.vehicle.id == db.fuel_expenses.reg_no_id))):
                        com_row.append(TR(TD(),TD(),TD(r.vehicle.reg_no), TD(locale.format('%.2F', r[total_amount] or 0, grouping = True),_align='right'),TD(),TD()))

            body = TBODY(*com_row)
            #table = HeadRpt()
            table = DIV(_class='space-2')
            table += DIV(_class='space-2')               
            table += TABLE(*[head, body],_class = 'table table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(company_pdf, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form=form,table=table)
        elif request.vars.optionRadios == 'option4':
            division_pdf = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print",_href=URL('_opt_4', args=[request.vars.division_id, request.vars.start_date, request.vars.end_date]))
            div_row = []
            div_que = db.vehicle.division_id == request.vars.division_id
            div_que &= db.vehicle.id == db.fuel_expenses.reg_no_id
            div_que &= db.fuel_expenses.date_expense >= request.vars.start_date
            div_que &= db.fuel_expenses.date_expense <= request.vars.end_date 

            total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
            grand_total = db.fuel_expenses.amount.sum().coalesce_zero()
            grand_total = db(div_que).select(grand_total).first()[grand_total]

            head = THEAD(TR(TH('Department'),TH('Reg.No.'),TH('Amount'),TH('Amount')))
            # department
            for p in db(div_que & (db.vehicle.division_id == request.vars.division_id)).select(db.department.id, db.department.name, total_amount, orderby = db.department.name, groupby = db.department.id | db.department.name, join=(db.vehicle.on(db.department.id == db.vehicle.department))):
                div_row.append(TR(TD(p.department.name),TD(),TD(),TD(locale.format('%.2F', p[total_amount] or 0, grouping = True))))

                # reg.no
                for r in db(div_que & (db.vehicle.department == p.department.id)).select(db.vehicle.reg_no, total_amount, orderby=db.vehicle.reg_no, groupby=db.vehicle.reg_no, join=(db.vehicle.on(db.vehicle.id == db.fuel_expenses.reg_no_id))):
                    div_row.append(TR(TD(),TD(r.vehicle.reg_no),TD(locale.format('%.2F', r[total_amount] or 0, grouping = True),TD())))
            
            body = TBODY(*div_row)
            table = DIV(_class='space-2')
            table += DIV(_class='space-2')               
            table += TABLE(*[head, body],_class = 'table table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(division_pdf, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form=form, table=table)

        elif request.vars.optionRadios == 'option5':
            department_pdf = A(SPAN(_class = 'fa fa-print bigger-110 blue'), _target='blank', _title="Print",_href=URL('_opt_5', args=[request.vars.department_id, request.vars.start_date, request.vars.end_date]))
            dep_row = []
            dep_que = db.vehicle.department == request.vars.department_id
            dep_que &= db.vehicle.id == db.fuel_expenses.reg_no_id
            dep_que &= db.fuel_expenses.date_expense >= request.vars.start_date
            dep_que &= db.fuel_expenses.date_expense <= request.vars.end_date 

            total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
            
            grand_total = db(dep_que).select(total_amount).first()[total_amount]

            head = THEAD(TR(TH('#'),TH('Reg.No.'),TH('Amount')))
            # reg.no
            ctr = 0
            for r in db(dep_que & (db.vehicle.department == request.vars.department_id)).select(db.vehicle.reg_no, total_amount, orderby=db.vehicle.reg_no, groupby=db.vehicle.reg_no, join=(db.vehicle.on(db.vehicle.id == db.fuel_expenses.reg_no_id))):
                ctr += 1
                dep_row.append(TR(TD(ctr),TD(r.vehicle.reg_no),TD(locale.format('%.2F', r[total_amount] or 0, grouping = True),_align='right')))

            body = TBODY(*dep_row)
            table = DIV(_class='space-2')
            table += DIV(_class='space-2')               
            table += TABLE(*[head, body],_class = 'table table-bordered')
            table += DIV(_class='hr hr8 hr-double hr-dotted')
            table += DIV(DIV('Duration Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,_class='col-sm-7 pull-left'),DIV(H4('GRAND TOTAL: ', SPAN(locale.format('%.2f',grand_total or 0, grouping=True), _class='red'),_class='pull-right'),_class='col-sm-5 pull-right'),_class='row')

            table = DIV(DIV(H4('Print Preview',_class='widget-title'),DIV(department_pdf, _class='widget-toolbar'),_class='widget-header'),DIV(DIV(DIV(table),_class='widget-main'),_class='widget-body'),_class='widget-box')

            response.flash = DIV(BUTTON(SPAN(_class='ace-icon fa fa-times'),_type='button', _class='close', **{'_data-dismiss':'alert'}),DIV(SPAN(_class='ace-icon fa fa-check smaller-130'),B(' Success: '), 'Below is the summary reports.', _class='white'),_class='alert alert-success') 
            return dict(form=form, table=table)      

    response.flash = form_info
    return dict(form = form, table = '')


def _opt_1():
    query = db.vehicle.id == db.fuel_expenses.reg_no_id
    query &= db.fuel_expenses.date_expense >=  request.args(0)
    query &= db.fuel_expenses.date_expense <= request.args(1)
    
    total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
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
    query &= db.fuel_expenses.reg_no_id == db.vehicle.id
    query &= db.fuel_expenses.date_expense >= request.args(1)
    query &= db.fuel_expenses.date_expense <= request.args(2)

    total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
    grand_total = db(query).select(total_amount).first()[total_amount]

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
    fle_query = db(query).select(db.fuel_expenses.ALL, orderby = ~db.fuel_expenses.date_expense)        
    ctr = 0
    #   head = THEAD(TR(TH('#'),TH('Date'),TH('Paid By'),TH('Station'),TH('Amount')))
    fle_data = [['#','Date','Paid By','Station','Amount']]
    for v in fle_query:
        ctr += 1
        #reg_row.append(TR(TD(ctr),TD(r.date_expense),TD(r.paid_by),TD(r.station),TD(locale.format('%.2f', r.amount or 0, grouping = True),_align='right')))
        fle_data.append([ctr,v.date_expense,v.paid_by,v.station,locale.format('%.2f',v.amount or 0, grouping=True)])
    fle_data.append(['Duration Period: ' + request.args(1) + ' - ' + request.args(2),'','','GRAND TOTAL:',locale.format('%.2F', grand_total or 0, grouping = True)])
    row.append(Spacer(1,0.3*cm))
    fle_tble=Table(fle_data, colWidths=[25,70,85,280,70])                                                              
    fle_tble.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),
        ('GRID',(0,0),(-1,-2),0.5, colors.Color(0, 0, 0, 0.2)),('ALIGN',(4,1),(-1,-1),'RIGHT'),('ALIGN',(3,-1),(-1,-1),'RIGHT'),('TOPPADDING',(0,-1),(4,-1), 10),
        ('FONTSIZE',(3,-1),(-1,-1),11),('TEXTCOLOR',(4,-1),(-1,-1),colors.red)]))
    #fle_tble.setStyle(TableStyle([('ALIGN',(4,1),(6,-1),'RIGHT'),('ALIGN',(4,-1),(5,-1),'RIGHT'),('TEXTCOLOR',(6,-1),(6,-1),colors.red),
    #    ('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),('FONTSIZE',(4,-1),(6,-1),11),
    #    ('GRID',(0,0),(-1,-2),0.5, colors.Color(0, 0, 0, 0.2)),('TOPPADDING',(0,-1),(6,-1), 10),
    #    ('SPAN',(0,-1),(3,-1)),('SPAN',(4,-1),(5,-1))]))
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
    query &= db.vehicle.id == db.fuel_expenses.reg_no_id
    query &= db.fuel_expenses.date_expense >=  request.args(1)
    query &= db.fuel_expenses.date_expense <= request.args(2)
    
    total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
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
    div_row = []
    div_que = db.vehicle.division_id == request.args(0)
    div_que &= db.vehicle.id == db.fuel_expenses.reg_no_id
    div_que &= db.fuel_expenses.date_expense >= request.args(1)
    div_que &= db.fuel_expenses.date_expense <= request.args(2)

    total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
    grand_total = db(div_que).select(total_amount).first()[total_amount]
    

    row_data = [['Department','Reg.No.','Amount','Total Amount']]

    for p in db(div_que).select(db.department.id, db.department.name, total_amount, orderby = db.department.name, groupby = db.department.name | db.department.id, join=(db.vehicle.on(db.department.id == db.vehicle.department))):
        row_data.append([p.department.name, '','',locale.format('%.2F',p[total_amount] or 0, grouping = True)])
        for r in db(div_que & (db.vehicle.department == p.department.id)).select(db.vehicle.reg_no, total_amount, orderby = db.vehicle.reg_no, groupby = db.vehicle.reg_no):
            row_data.append(['',r.vehicle.reg_no, locale.format('%.2F',r[total_amount] or 0, grouping = True),''])
    row_data.append(['Duration Period: ' + request.args(1) + ' - ' + request.args(2),'','GRAND TOTAL:',locale.format('%.2F', grand_total or 0, grouping = True)])   
    row = []
    que_tbl=Table(row_data, colWidths=[132,132,132,132], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)                                                              
    que_tbl.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1),9),
        ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),
        ('GRID',(0,0),(-1,-2),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN',(2,1),(3,-1),'RIGHT'),
        ('TOPPADDING',(0,-1),(3,-1), 10),
        #('SPAN',(0,-1),(3,-1)),
        #('SPAN',(3,-1),(4,-1)),
        ('TEXTCOLOR',(3,-1),(-1,-1),colors.red),
        ('FONTSIZE',(2,-1),(3,-1),11)]))        
    row.append(que_tbl)    
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data   


def _opt_5():
    
    
    dept_que = db.vehicle.department == request.args(0)
    dept_que &= db.vehicle.id == db.fuel_expenses.reg_no_id
    dept_que &= db.fuel_expenses.date_expense >= request.args(1)
    dept_que &= db.fuel_expenses.date_expense <= request.args(2)

    total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
    grand_total = db(dept_que).select(total_amount).first()[total_amount]
    

    row_data = [['#','Reg.No.','Amount']]
    ctr = 0
    for r in db(dept_que).select(db.vehicle.reg_no, total_amount, orderby = db.vehicle.reg_no, groupby = db.vehicle.reg_no):
        ctr += 1
        row_data.append([ctr,r.vehicle.reg_no, locale.format('%.2F',r[total_amount] or 0, grouping = True)])

    grand_total_data = [['Duration Period: ' + request.args(1) + ' - ' + request.args(2),'GRAND TOTAL:',locale.format('%.2F', grand_total or 0, grouping = True)]]

    row = []
    que_tbl=Table(row_data, colWidths=[25,252,252], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)                                                              
    grand_tbl=Table(grand_total_data, colWidths=[330,130,70], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)                                                              
    grand_tbl.setStyle(TableStyle([('ALIGN',(1,0),(2,0),'RIGHT'),('FONTSIZE',(1,0),(2,0),11),('FONTSIZE',(0,0),(0,0),9),('TEXTCOLOR',(2,0),(2,0),colors.red)]))
    que_tbl.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3)),('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),('ALIGN',(2,1),(2,-1),'RIGHT')]))
    row.append(que_tbl)    
    row.append(Spacer(1,0.3*cm))   
    row.append(grand_tbl)
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data   

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def CompanySummaryFuelReport():
    qc_length = 0
    form = SQLFORM.factory(
        Field('start_date', 'date', default = request.now, requires = IS_DATE(), label = 'Start Date'),
        Field('end_date', 'date', default = request.now, requires = IS_DATE(), label = 'End Date'))
    if form.accepts(request):        
        sum_que = db.vehicle.id == db.fuel_expenses.reg_no_id
        sum_que &= db.fuel_expenses.date_expense >= form.vars.start_date
        sum_que &= db.fuel_expenses.date_expense <= form.vars.end_date
      
        total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
        grand_total = db(sum_que).select(total_amount).first()[total_amount]
       
        #foot = THEAD(TR(TD(H4('Grand Total Amount: '), _colspan = '5', _align = 'right'), TD(H4(str('QR ' + locale.format('%.2F', grand_total or 0, grouping = True))))))

        sum_dat = [['Period: ' + request.vars.start_date + ' - ' + request.vars.end_date,'','','','',''],
        ['Company', 'Division','Department', 'Amount','Amount','Total Amount']]

        for c in db(sum_que).select(db.vehicle.company_id, total_amount, orderby = ~db.vehicle.company_id, groupby = db.vehicle.company_id):
            sum_dat.append([c.vehicle.company_id.company,'','','','',locale.format('%.2F', c[total_amount] or 0, grouping = True)]) 
            
            ###### SUB-DIVISION ########
            for d in db((sum_que) & (db.vehicle.company_id == c.vehicle.company_id)).select(db.vehicle.division_id,  total_amount, orderby = ~db.vehicle.division_id, groupby = db.vehicle.division_id):      
                sum_dat.append(['',d.vehicle.division_id.division,'','',locale.format('%.2F', d[total_amount] or 0, grouping = True)]) 
            
                ######### SUB-DEPARTMENT ###########
                for p in db((sum_que) & (db.vehicle.division_id == d.vehicle.division_id)).select(db.vehicle.department, total_amount, orderby = ~db.vehicle.department, groupby = db.vehicle.department):
                    sum_dat.append(['','', p.vehicle.department.name, locale.format('%.2F', y[total_amount] or 0, grouping = True)])
                    #print y.vehicle.department.name
        '''
        q_division = db(sum_que).select(db.vehicle.division_id,  total_amount, orderby = ~db.vehicle.division_id, groupby = db.vehicle.division_id )            
        q_department = db(sum_que).select(db.vehicle.department, total_amount, orderby = ~db.vehicle.department, groupby = db.vehicle.department)
        qd_length = len(q_division)
        qdt_length = len(q_department)        
        body = TBODY(*f)
        table = TABLE(*[head, body, foot],_align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, i=i, table = table, grand_total = grand_total, qc_length = qc_length, qd_length = qd_length, qdt_length = qdt_length,
                        q_company = q_company, total_amount = total_amount, q_division = q_division, q_department = q_department)
    else:
        return dict(form = form, i= '', table = '', qc_length = '', q_company = '', qd_length = '', qdt_length = '',
                    grand_total = 0, total_amount = 0, q_division = '', q_department = '')
        '''
    return dict(form=form)
@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DivisionSummaryFuelReport():
    form = SQLFORM.factory(
        Field('start_date', 'date', requires = IS_DATE(), label = 'Start Date'),
        Field('end_date', 'date', requires = IS_DATE(), label = 'End Date'))
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))   
    if form.accepts(request):   
        start_date = request.now.strptime(request.vars.start_date, '%Y-%m-%d')
        end_date = request.now.strptime(request.vars.end_date, '%Y-%m-%d')
        
        query = db.vehicle.id == db.fuel_expenses.reg_no_id
        query &= db.fuel_expenses.date_expense >= start_date
        query &= db.fuel_expenses.date_expense <= end_date
        
        total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
        
        grand_total = db(query).select(total_amount).first()[total_amount]
        i = TABLE(*[THEAD(TR(TD(B('Start Date:')), TD(B('End Date:'))),_bgcolor='#E0E0E0'),
            TR(TD(form.vars.start_date),TD(form.vars.end_date))],
            _border = '0', _align = 'center', _width = '100%',  _class = 'pure-table')
            
        head = THEAD(TR(TH('Division'), TH('Total Amount'),_bgcolor='#E0E0E0'))
                        
        f = []
        for f_rep in db(query).select(db.vehicle.division_id, total_amount, orderby = ~db.vehicle.division_id, groupby = db.vehicle.division_id):
            f.append(TR(TD(f_rep.vehicle.division_id.division), 
                        TD(locale.format('%.2F', f_rep[total_amount] or 0, grouping = True))))

        body = TBODY(*f)
        table = TABLE(*[head, body], _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, i=i, table = table, grand_total = grand_total,
                        img_report = img_report)
    else:
        return dict(form = form, i= '', table = 'Enter Start date & End date',
                    grand_total = 0, img_report = None)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DepartmentSummaryFuelReport():
    form = SQLFORM.factory(
        Field('start_date', 'date', requires = IS_DATE(), label = 'Start Date'),
        Field('end_date', 'date', requires = IS_DATE(), label = 'End Date'))
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))   
    if form.accepts(request):           

        query = db.vehicle.id == db.fuel_expenses.reg_no_id
        query &= db.fuel_expenses.date_expense >= form.vars.start_date
        query &= db.fuel_expenses.date_expense <= form.vars.end_date
        
        total_amount = db.fuel_expenses.amount.sum().coalesce_zero()
        grand_total = db(query).select(total_amount).first()[total_amount]

        i = TABLE(*[THEAD(TR(TD(B('Start Date:')), TD(B('End Date:'))),_bgcolor='#E0E0E0'),
            TR(TD(form.vars.start_date),TD(form.vars.end_date))],
            _border = '0', _align = 'center', _width = '100%',  _class = 'pure-table')
            
        head = THEAD(TR(TH('Department'), TH('Total Amount'),_bgcolor='#E0E0E0'))
                        
        f = []
        for f_rep in db(query).select(db.vehicle.department, total_amount, orderby = ~db.vehicle.department,
            groupby = db.vehicle.department):
            f.append(TR(TD(f_rep.vehicle.department.name, _width = '50%'), 
                        TD(locale.format('%.2F', f_rep[total_amount] or 0, grouping = True), _align = 'right', _width = '20%')))

        body = TBODY(*f)
        table = TABLE(*[head, body], _align="center", _width="100%", _class = 'pure-table')

        return dict(form = form, i=i, table = table, grand_total = grand_total,
                        img_report = img_report)
    else:
        return dict(form = form, i= '', table = 'Enter Start date & End date', grand_total = 0, img_report = None)

def CompanyInfo():
    i = 0   
    for info in db(db.vehicle.id == request.args(0)).select(db.vehicle.ALL):
        i = TABLE(*[TR(TD(B('Company Info'), _colspan = '2'), _bgcolor = '#E0E0E0'),
            TR(TD('Company:'), TD(c.company_id.company)), 
            TR(TD('Start Date:'), TD(form.vars.start_date)), 
            TR(TD('End Date:'),TD(form.vars.end_date))], 
            _border = '0', _align = 'center', _width = '100%',  _class = 'pure-table')            
    return dict(i = i) 

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def CompanyFuelExpensesReport():
    i = None
    ctr = 0
    r = []       
    form = SQLFORM.factory(
        Field('company_id', requires = IS_IN_DB(db, db.company, '%(company)s', zero = 'Choose company'), label = 'Company'),
        Field('start_date', 'date', default = request.now, requires = IS_DATE(), label = 'Start Date'),
        Field('end_date', 'date', default = request.now, requires = IS_DATE(), label = 'End Date'))
    if form.accepts(request):      
        query = db.vehicle.company_id == form.vars.company_id
        query &= db.vehicle.id == db.fuel_expenses.reg_no_id
        query &= db.fuel_expenses.date_expense >= form.vars.start_date
        query &= db.fuel_expenses.date_expense <= form.vars.end_date 

        grand_total = db.fuel_expenses.amount.sum().coalesce_zero()
        grand_total = db(query).select(grand_total).first()[grand_total]
        
        for c in db(db.vehicle.company_id == form.vars.company_id).select(db.vehicle.ALL):
            i = TABLE(*[TR(TD(B('Company Info'), _colspan = '2'), _bgcolor = '#E0E0E0'),
                TR(TD('Company:'), TD(c.company_id.company)), 
                TR(TD('Start Date:'), TD(form.vars.start_date)), 
                TR(TD('End Date:'),TD(form.vars.end_date))], _border = '0', _align = 'center', 
                _width = '100%',  _class = 'pure-table')            
        head = THEAD(TR(TH('No.'),TH('Reg.No.'), TH('Brand'), TH('Mileage'),TH('Model'), 
            TH('Total Amount'),_bgcolor='#E0E0E0'))       
        
        foot = THEAD(TR(TD(H4('Grand Total Amount: '), _colspan = '5', _align = 'right'), 
            TD(H4(str('QR ' + locale.format('%.2F', grand_total or 0, grouping = True))))))
        
        c_query = db(query).select(db.fuel_expenses.reg_no_id, db.vehicle.ALL, 'sum(fuel_expenses.amount)', 
            groupby = db.fuel_expenses.reg_no_id | db.vehicle.ALL, orderby = ~db.fuel_expenses.reg_no_id) 
        for q in c_query:
            row = len(c_query)
            ctr += 1
            r.append(TR(TD(ctr),TD(q.fuel_expenses.reg_no_id.reg_no), TD(q.vehicle.vehicle_name_id.vehicle_name), 
                TD(str(locale.format('%d', q.vehicle.mileage or 0, grouping = True)) + ' km.'), 
                TD(q.vehicle.model), TD(locale.format('%.2f', q._extra['sum(fuel_expenses.amount)'] or 0, grouping = True))))
        body = TBODY(*r)
        table = TABLE(*[head, body, foot], _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, i=i, table = table, c_query = c_query, grand_total = grand_total)
    else:
        return dict(form = form, i= '', table = '', c_query = '', grand_total = 0)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DivisionFuelExpensesReport():
    i = None
    ctr = 0
    r = []   
    form = SQLFORM.factory(
        Field('division_id', requires = IS_IN_DB(db, db.division, '%(division)s', zero = 'Choose division'), label = 'Division'),
        Field('start_date', 'date', default = request.now, requires = IS_DATE(), label = 'Start Date'),
        Field('end_date', 'date', default = request.now, requires = IS_DATE(), label = 'End Date'))
    if form.accepts(request):
        query = db.vehicle.division_id == form.vars.division_id
        query &= db.vehicle.id == db.fuel_expenses.reg_no_id
        query &= db.fuel_expenses.date_expense >= form.vars.start_date
        query &= db.fuel_expenses.date_expense <= form.vars.end_date
        
        grand_total = db.fuel_expenses.amount.sum().coalesce_zero()
        grand_total = db(query).select(grand_total).first()[grand_total]

        for c in db(db.vehicle.division_id == form.vars.division_id).select(db.vehicle.ALL):
            i = TABLE(*[TR(TD(B('Company Info'), _colspan = '2'), _bgcolor = '#E0E0E0'),
                TR(TD('Company:'), TD(c.company_id.company)), 
                TR(TD('Start Date:'), TD(form.vars.start_date)), 
                TR(TD('End Date:'),TD(form.vars.end_date))], _border = '0', _align = 'center', 
                _width = '100%',  _class = 'pure-table')            
        head = THEAD(TR(TH('No.'),TH('Reg.No.'), TH('Brand'), TH('Mileage'),TH('Model'), 
            TH('Total Amount'),_bgcolor='#E0E0E0'))       
        
        foot = THEAD(TR(TD(H4('Grand Total Amount: '), _colspan = '5', _align = 'right'), 
            TD(H4(str('QR ' + locale.format('%.2F', grand_total or 0, grouping = True))))))
        div_query = db(query).select(db.fuel_expenses.reg_no_id, db.vehicle.ALL, 'sum(fuel_expenses.amount)', 
            groupby = db.fuel_expenses.reg_no_id | db.vehicle.ALL, orderby = ~db.fuel_expenses.reg_no_id)
        for q in div_query:
            row = len(db(query).select(db.fuel_expenses.reg_no_id, groupby = db.fuel_expenses.reg_no_id))
            ctr += 1
            r.append(TR(TD(ctr),TD(q.fuel_expenses.reg_no_id.reg_no), TD(q.vehicle.vehicle_name_id.vehicle_name), 
                TD(str(locale.format('%d', q.vehicle.mileage or 0, grouping = True)) + ' km.'), 
                TD(q.vehicle.model), TD(locale.format('%.2f', q._extra['sum(fuel_expenses.amount)'] or 0, grouping = True))))
        body = TBODY(*r)
        table = TABLE(*[head, body, foot], _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, i=i, table = table, div_query = div_query, grand_total = grand_total)
    else:
        return dict(form = form, i= '', table = '', div_query = '', grand_total = 0)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DepartmentFuelExpensesReport():   
    i = None
    ctr = 0
    r = []  
    form = SQLFORM.factory(
        Field('department', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose department'), label = 'Department'),
        Field('start_date', 'date', default = request.now, requires = IS_DATE(), label = 'Start Date'),
        Field('end_date', 'date', default = request.now, requires = IS_DATE(), label = 'End Date'))
    if form.accepts(request):       
        query = db.vehicle.department == form.vars.department
        query &= db.vehicle.id == db.fuel_expenses.reg_no_id
        query &= db.fuel_expenses.date_expense >= form.vars.start_date
        query &= db.fuel_expenses.date_expense <= form.vars.end_date
        
        grand_total = db.fuel_expenses.amount.sum().coalesce_zero()
        grand_total = db(query).select(grand_total).first()[grand_total]

        d_query = db(db.vehicle.department == form.vars.department).select(db.vehicle.ALL) 
        for c in d_query:
            i = TABLE(*[TR(TD(B('Company Info'), _colspan = '2'), _bgcolor = '#E0E0E0'),
                TR(TD('Company:'), TD(c.company_id.company)), 
                TR(TD('Start Date:'), TD(form.vars.start_date)), 
                TR(TD('End Date:'),TD(form.vars.end_date))], _border = '0', _align = 'center', 
                _width = '100%',  _class = 'pure-table')            
        head = THEAD(TR(TH('No.'),TH('Reg.No.'), TH('Brand'), TH('Mileage'),TH('Model'), 
            TH('Total Amount'),_bgcolor='#E0E0E0'))       
        
        foot = THEAD(TR(TD(H4('Grand Total Amount: '), _colspan = '5', _align = 'right'), 
            TD(H4(str('QR ' + locale.format('%.2F', grand_total or 0, grouping = True))))))
        dept_query = db(query).select(db.fuel_expenses.reg_no_id, db.vehicle.ALL, 'sum(fuel_expenses.amount)', 
            groupby = db.fuel_expenses.reg_no_id | db.vehicle.ALL, orderby = ~db.fuel_expenses.reg_no_id)

        for q in dept_query:
            row = len(db(query).select(db.fuel_expenses.reg_no_id, groupby = db.fuel_expenses.reg_no_id))
            ctr += 1
            r.append(TR(TD(ctr),TD(q.fuel_expenses.reg_no_id.reg_no), TD(q.vehicle.vehicle_name_id.vehicle_name), 
                TD(str(locale.format('%d', q.vehicle.mileage or 0, grouping = True)) + ' km.'), 
                TD(q.vehicle.model), TD(locale.format('%.2f', q._extra['sum(fuel_expenses.amount)'] or 0, grouping = True))))
        body = TBODY(*r)
        table = TABLE(*[head, body, foot], _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, i=i, table = table, dept_query = dept_query, d_query = d_query, grand_total = grand_total, query = query)
    else:
        return dict(form = form, i= '', table = '', dept_query = '', d_query = '', grand_total = 0)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def VehicleFuelExpensesReport(): 
    form = SQLFORM.factory(
        Field('reg_no_id', label = 'Reg.No.', widget = SQLFORM.widgets.autocomplete(request, db.vehicle.reg_no,
            id_field = db.vehicle.id, limitby = (0,10), min_length=2)),
        Field('start_date', 'date', default = request.now, requires = IS_DATE(), label = 'Start Date'),
        Field('end_date', 'date', default = request.now, requires = IS_DATE(), label = 'End Date'))
    if form.accepts(request):      
        query = db.fuel_expenses.reg_no_id == form.vars.reg_no_id
        query &= db.fuel_expenses.date_expense >= form.vars.start_date
        query &= db.fuel_expenses.date_expense <= form.vars.end_date
        
        grand_total = db.fuel_expenses.amount.sum().coalesce_zero()
        grand_total = db(query).select(grand_total).first()[grand_total]

        vehicle_info = db(db.vehicle.id == form.vars.reg_no_id).select(db.vehicle.ALL)      
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

        head = THEAD(TR(TH('No.'),TH('Date'), TH('Amount'),TH('Paid by'),TH('Station'), _bgcolor='#E0E0E0'))
        foot = THEAD(TR(TD(H4('Grand Total Amount: '), _colspan = '4', _align = 'right'), TD(H4(str('QR ' + locale.format('%.2F', grand_total or 0, grouping = True))))))
        r = []
        ctr = 0
        v_query = db(query).select(db.fuel_expenses.ALL, orderby = ~db.fuel_expenses.date_expense)
        for q in v_query:
                row = len(db(query).select(db.fuel_expenses.ALL, orderby = ~db.fuel_expenses.date_expense))
                ctr +=1
                r.append(TR(TD(ctr), TD(q.date_expense), TD(locale.format('%.2f', q.amount or 0, grouping = True), 
                    _align = 'right'), TD(q.paid_by), TD(q.station)))
        body = TBODY(*r)
        table = TABLE(*[head, body, foot], _align="center", _width="100%", _class = 'pure-table')
        return dict(form = form, table = table, i = i, grand_total = grand_total, v_query = v_query)
    else:
        return dict(form = form, i = '', table ='', v_query = '', grand_total = 0)    

@auth.requires_login()
def FuelReport():    
    query = db(db.fuel_expenses.id == request.args(0)).select(db.vehicle.ALL, db.fuel_expenses.ALL, left=db.fuel_expenses.on(db.fuel_expenses.reg_no_id == db.vehicle.id))
    for n in query:
        c_info = [['Fleet Specification','','','Company Info',''],
        ['Code:',n.vehicle.vehicle_code,'','Company:',n.vehicle.company_id.company],
        ['Reg.No.:',n.vehicle.reg_no,'','Division:',n.vehicle.division_id.division],
        ['Manufacturer',n.vehicle.vehicle_name_id.vehicle_name,'','Department:',n.vehicle.department.name],
        ['Model',n.vehicle.model,'','Owner:',n.vehicle.owner.name],
        ['','','','',''],
        ['Expenses','','','',''],
        ['Date',n.fuel_expenses.date_expense,'','',''],
        ['Amount', locale.format('%.2F', n.fuel_expenses.amount or 0, grouping = True),'','',''],
        ['Paid by',n.fuel_expenses.paid_by,'','',''], 
        ['Station', Paragraph(str(n.fuel_expenses.station), styles["BodyText"]),'','',''], 
        ['Remarks', Paragraph(str(n.fuel_expenses.remarks), styles["BodyText"]),'','','']]

    com_tbl=Table(c_info, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
    com_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW',(1,7),(1,11),0.50, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('ALIGN',(1,8),(1,8),'RIGHT'),
        ('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3)),
        ('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
        ('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3)),
        ('BACKGROUND',(0,6),(1,6),colors.Color(0, 0, 0, 0.3))]))
    row.append(com_tbl)
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data 

def Modal():
    form = SQLFORM.factory(
        Field('department', requires = IS_IN_DB(db, db.department, '%(name)s', zero = 'Choose department'), label = 'Department'),
        Field('start_date', 'date', requires = IS_DATE()),
        Field('end_date', 'date', requires = IS_DATE()))    
    if form.accepts(request):
        response.flash = 'ok'
    return dict(form = form) 