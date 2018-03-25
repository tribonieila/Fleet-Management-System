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

#from reportlab.pdfbase import pdfdoc

#pdfdoc.PDFCatalog.OpenAction = '<</S/JavaScript/JS(this.print\({bUI:true,bSilent:false,bShrinkToFit:true}\);)>>'

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


###########

def _title(title):
    title = 'Title'
    return str(title)

def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Vehicle Summary Report'
    header = Table([['',I],[darwish,''],['Fleet Mileage Report','']], colWidths=[None,90])
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

@auth.requires_login()
def VehicleMileageReport():
    query = db(db.km_used.id == request.args(0)).select(db.vehicle.ALL, db.km_used.ALL, left=db.km_used.on(db.km_used.reg_no_id == db.vehicle.id))
    for n in query:
        c_info = [['Fleet Specification','','','Company Info',''],
        ['Code:',n.vehicle.vehicle_code,'','Company:',n.vehicle.company_id.company],
        ['Reg.No.:',n.vehicle.reg_no,'','Division:',n.vehicle.division_id.division],
        ['Manufacturer',n.vehicle.vehicle_name_id.vehicle_name,'','Department:',n.vehicle.department.name],
        ['Model',n.vehicle.model,'','Owner:',n.vehicle.owner.name],
        ['','','','',''],
        ['Odometer','','','',''],
        ['Given Month',n.km_used.given_month.strftime('%Y, %B'),'','',''],
        ['Given Odometer', locale.format('%d',n.km_used.current_mil or 0, grouping = True),'','','']]

    com_tbl=Table(c_info, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
    com_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW',(1,7),(1,8),0.50, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),9),
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

@auth.requires_login()
def FleetMileageReport():
    query = db.km_used.reg_no_id == request.args(0)
    query &= db.km_used.given_month >= request.args(1)
    query &= db.km_used.given_month <= request.args(2)
    
    total_mileage = db.km_used.consumed_mil.sum().coalesce_zero()
    total_mileage = db(query).select(total_mileage).first()[total_mileage]

    for f in db(db.vehicle.id == request.args(0)).select(db.vehicle.ALL):
        rows = [['Fleet Specification','','','Company Info',''],
        ['Code:',f.vehicle_code,'','Company:',f.company_id.company],
        ['Reg.No.:',f.reg_no,'','Division:',f.division_id.division],
        ['Manufacturer',f.vehicle_name_id.vehicle_name,'','Department:',f.department.name],
        ['Model',f.model,'','Owner:',f.owner.name]]

    m_data = [['#','Month','Mileage','Diff.Odometer']]
    ctr = 0
    for m in db(query).select(db.km_used.ALL, orderby = ~db.km_used.given_month):
        ctr += 1
        m_data.append([ctr, m.given_month.strftime('%Y - %B'),str(locale.format('%d', m.current_mil or 0, grouping = True)) + ' km.',str(locale.format('%d', m.consumed_mil or 0, grouping = True)) + ' km.'])
    m_data.append(['Duration Period: ' + request.args(1) + ' - ' + request.args(2),'','TOTAL MILEAGE:',str(locale.format('%.d', total_mileage or 0, grouping = True)) + ' km.'])   


    fle_tbl = Table(rows, colWidths=[100,140,50,100,140], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
    fle_tbl.setStyle(TableStyle([('LINEBELOW',(1,1),(1,4),0.50, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW',(1,7),(1,8),0.50, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('BOX',(3,0),(4,4),0.3,colors.Color(0, 0, 0, 0.3)),
        ('BACKGROUND',(0,0),(1,0),colors.Color(0, 0, 0, 0.3)),
        ('BACKGROUND',(3,0),(4,0),colors.Color(0, 0, 0, 0.3))]))

    m_tbl = Table(m_data, colWidths=[25,168,168,170], rowHeights=None, splitByRow=1, repeatRows=0, repeatCols=0)
    m_tbl.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1),9),
        ('GRID',(0,0),(-1,-2),0.5, colors.Color(0, 0, 0, 0.2)),('ALIGN',(2,-1),(2,-1),'RIGHT'),
        ('TOPPADDING',(0,-1),(3,-1), 10),('FONTSIZE',(2,-1),(3,-1),11),('TEXTCOLOR',(3,-1),(3,-1),colors.red),
        ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.3))]))
        
    row.append(fle_tbl)
    row.append(Spacer(1,0.3*cm))             
    row.append(m_tbl)
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data 
