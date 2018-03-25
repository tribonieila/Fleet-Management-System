export = {'xml':False, 'html':False, 'csv_with_hidden_cols':False,
          'csv':False, 'tsv_with_hidden_cols':False, 'json':False}


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def RoadPermitNotification():
    today = datetime.date.today()
    rows = db(db.vehicle).select(orderby = db.vehicle.exp_date)
    r = 0
    row = len(rows)
    while (r < row):
        rows[r].update_record(datetoalert = rows[r].exp_date - datetime.timedelta(days = 45))
        r += 1

    form = SQLFORM.factory(Field('company_id', requires = IS_IN_DB(db, db.company, '%(company)s'), label = 'Company'))
    img_report = FORM(INPUT(_align = 'right',_type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))
    if form.accepts(request):
        query = db.vehicle.company_id == request.vars.company_id
        query &= (db.vehicle.datetoalert <= today) | (db.vehicle.exp_date <= today)
        query = db(query).select(db.vehicle.ALL, orderby = db.vehicle.exp_date)
        head = THEAD(TR(TH('No.'),
            TH('Reg.No.'),
            TH('Vehicle Code'),           
            TH('RPEx Date'), 
            TH('Vehicle Name'),
            TH('Model'),
            TH('Department'),
            TH('Remarks'),_bgcolor = '#E0E0E0'))
        v = []
        n = 0
        for l in query:
            row = len(query)
            n += 1
            v.append(TR(TD(n),
                TD(l.reg_no, _align = 'right'),
                TD(l.vehicle_code, _align = 'right'),
                TD(l.exp_date, _align = 'right'),
                TD(l.vehicle_name_id.vehicle_name),
                TD(l.model),
                TD(l.department.name),
                TD(l.remarks)))    
        body = TBODY(v)
        table = TABLE([head, body], _align="center", _width="100%", _class = 'pure-table pure-table-vertical')

        return dict(form = form,  table = table, img_report = img_report)
    else: 
        return dict(form = form, table = 'Choose company', img_report = None)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def RodPerNotDiv():
    today = datetime.date.today()
    rows = db(db.vehicle).select(orderby = db.vehicle.exp_date)
    r = 0
    row = len(rows)
    while (r < row):
        rows[r].update_record(datetoalert = rows[r].exp_date - datetime.timedelta(days = 45))
        r += 1

    form = SQLFORM.factory(Field('division_id', requires = IS_IN_DB(db, db.division, '%(division)s'), label = 'Division'))
    img_report = FORM(INPUT(_align = 'right',_type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))
    if form.accepts(request):
        query = db.vehicle.division_id == request.vars.division_id
        query &= (db.vehicle.datetoalert <= today) | (db.vehicle.exp_date <= today)

        query = db(query).select(db.vehicle.ALL, orderby = db.vehicle.exp_date)
        head = THEAD(TR(TH('No.'),
            TH('Reg.No.'),
            TH('Vehicle Code'),           
            TH('RPEx Date'), 
            TH('Vehicle Name'),
            TH('Model'),
            TH('Department'),
            TH('Remarks'),_bgcolor = '#E0E0E0'))
        v = []
        n = 0
        for l in query:
            row = len(query)
            n += 1
            v.append(TR(TD(n),
                TD(l.reg_no, _align = 'right'),
                TD(l.vehicle_code, _align = 'right'),
                TD(l.exp_date, _align = 'right'),
                TD(l.vehicle_name_id.vehicle_name),
                TD(l.model),
                TD(l.department.name),
                TD(l.remarks)))     
        body = TBODY(v)
        table = TABLE([head, body], _align="center", _width="100%", _class = 'pure-table pure-table-vertical')

        return dict(form = form,  table = table, img_report = img_report)
    else: 
        return dict(form = form, table = 'Choose division', img_report = None)

@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def RodPerNotDept():
    today = datetime.date.today()
    rows = db(db.vehicle).select(orderby = db.vehicle.exp_date)
    r = 0
    row = len(rows)
    while (r < row):
        rows[r].update_record(datetoalert = rows[r].exp_date - datetime.timedelta(days = 45))
        r += 1

    form = SQLFORM.factory(Field('department_id', requires = IS_IN_DB(db, db.department, '%(name)s'), label = 'Department'))
    img_report = FORM(INPUT(_align = 'right',_type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))
    if form.accepts(request):
        query = db.vehicle.department == request.vars.department_id
        query &= (db.vehicle.datetoalert <= today) | (db.vehicle.exp_date <= today)
        query = db(query).select(db.vehicle.ALL, orderby = db.vehicle.exp_date)
        head = THEAD(TR(TH('No.'),
            TH('Reg.No.'),
            TH('Vehicle Code'),           
            TH('RPEx Date'), 
            TH('Vehicle Name'),
            TH('Model'),
            TH('Department'),
            TH('Remarks'),_bgcolor = '#E0E0E0'))
        v = []
        n = 0
        for l in query:
            row = len(query)
            n += 1
            v.append(TR(TD(n),
                TD(l.reg_no, _align = 'right'),
                TD(l.vehicle_code, _align = 'right'),
                TD(l.exp_date, _align = 'right'),
                TD(l.vehicle_name_id.vehicle_name),
                TD(l.model),
                TD(l.department.name),
                TD(l.remarks)))   
        body = TBODY(v)
        table = TABLE([head, body], _align="center", _width="100%", _class = 'pure-table pure-table-vertical')

        return dict(form = form,  table = table, img_report = img_report)
    else: 
        return dict(form = form, table = 'Choose department', img_report = None)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def InsPolicyNotification():
    today = datetime.date.today()
    rows = db(db.insurance_policy).select(orderby = db.insurance_policy.period_covered)
    r = 0
    row = len(rows)
    while (r < row):
        rows[r].update_record(datetoalert = rows[r].period_covered - datetime.timedelta(days = 45))
        r += 1
    
    form = SQLFORM.factory(
        Field('insurance_id', requires = IS_IN_DB(db, db.vehicle_insurance, '%(name)s'), label = 'Insurance Policy'))
    img_report = FORM(INPUT(_align = 'right',  _type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))
    if form.accepts(request):

        query = db.insurance_policy.insurance_company_id == request.vars.insurance_id
        query &= (db.insurance_policy.datetoalert <= today) | (db.insurance_policy.period_covered <= today)
        query = db(query).select(db.insurance_policy.ALL, orderby = db.insurance_policy.period_covered)
        
        head = THEAD(TR(TH('No.'),
            TH('Insurance Company', _width = '50%'),
            TH('Policy', _width = '25%'),
            TH('Period Covered', _width = '25%'), _bgcolor = '#E0E0E0'))
        i = []
        n = 0
        for r in query:
            row = len(query)
            n += 1
            i.append(TR(TD(n),
                TD(r.insurance_company_id.name, _width = '50%'),
                TD(r.policy_no, _align = 'right', _width = '25%'),
                TD(r.period_covered, _align = 'right', _width = '25%')))
        body = TBODY(i)
        table = TABLE([head, body], _align = 'center', _width = '100%', _class = 'pure-table pure-table-vertical')
        return dict(form = form,  table = table, img_report = img_report)
    else: 
        return dict(form = form, table = '', img_report = None)


@auth.requires(lambda: auth.has_membership('level_1_user') | auth.has_membership('level_3_user'))
def DriverNotification():
    today = datetime.date.today()
    rows = db(db.driver).select(orderby = db.driver.expiry_date)
    r = 0
    row = len(rows)
    while (r < row):
        rows[r].update_record(alertdate = rows[r].expiry_date - datetime.timedelta(days = 45))
        r +=1

    form = SQLFORM.factory(
        Field('company_id', requires = IS_IN_DB(db, db.company, '%(company)s'), label = 'Company'))
    img_report = FORM(INPUT(_align = 'right',_type = 'image',  _target = "_blank",_src=URL('static','images/printButton.png'), 
                            _onclick = "javascript:PrintContent()"))
    if form.accepts(request):
        query = db.driver.company_id == request.vars.company_id
        query &= (db.driver.alertdate <= today) | (db.driver.expiry_date <= today)

        head = THEAD(TR(TH('Emp. No.', _align = 'center', _width = '10%'),
                        TH('Driver Name', _align = 'center',_width = '30%'),
                        TH('Position', _align = 'center',_width = '18%'),
                        TH('License No.', _align = 'center',_width = '15%'),
                        TH('Exp. Date', _align = 'center',_width = '12%'),
                        TH('Contact No.', _align = 'center',_width = '15%'), _bgcolor='#E0E0E0'))
        d = []
        for c in db(query).select(db.driver.ALL, orderby = db.driver.expiry_date):
            d.append(TR(TD(c.employee_number, _width = '10%', _align = 'right'),
                        TD(c.driver_name, _width = '30%'),
                        TD(c.position_id.name, _align = 'right', _width = '18%'),
                        TD(c.driver_id, _width = '15%'),
                        TD(c.expiry_date, _width = '12%'),
                        TD(c.contact_no, _align = 'right', _width = '15%')))
        body = TBODY(d)
        table = TABLE([head, body], _align="center", _width="100%", _class = 'pure-table pure-table-vertical')
        return dict(form = form,  table = table, img_report = img_report)
    else: 
        return dict(form = form, table = 'Choose drivers company', img_report = None)
