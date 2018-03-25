def RprtHdr():
    styles = getSampleStyleSheet()
    tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
    doc = SimpleDocTemplate(tmpfilename,pagesize=letter, topMargin=30, leftMargin=30, rightMargin=30)
    logo_path = request.folder + 'static/images/kds-logo.jpg'
    row = []
    
    I = Image(logo_path)
    I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
    I.drawWidth = 1.25*inch
    I.hAlign='RIGHT'
    #story.append(I)
    #story.append(Paragraph(escape("Darwish Group"),styles["Heading2"]))
    #story.append(Paragraph(escape("Fleet Management System"), styles["Heading2"]))
    #story.append(Paragraph(escape("Maintenance Expenses Report"),styles["Heading5"]))
    #story.append(Paragraph('My User Names', styles['RightAlign']))
    #story.append(Paragraph(escape("<b>Darwish Group</b>")))
    #styleSheet=styles(["Normal"])
    
    