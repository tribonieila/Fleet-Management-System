
#########################################################################
# -----------           ADMINISTRATOR ACCOUNT     ------------- #
#########################################################################                    

@auth.requires_membership('tribo_ng_datu')
def tagagamit_tribo():
    db.auth_user.username.writable = True
    db.auth_user.password.writable =True
    #db.auth_user.username.readable = True
    #db.auth_user.password.readable =True
    db.auth_user.division_id.writable = True
    db.auth_user.division_id.readable = True

    grid = SQLFORM.grid(db.auth_user, user_signature=False, csv = False,
        create = True, searchable = True, showbuttontext = False, links = '')
    return dict(grid = grid)    	

@auth.requires_membership('tribo_ng_datu')
def pangkat_tribo():
    db.auth_user.username.writable = True
    db.auth_user.password.writable =True
    db.auth_user.division_id.writable = True
    db.auth_user.division_id.readable = True

    grid = SQLFORM.grid(db.auth_group, user_signature=False, csv = False,
        create = True, searchable = True,  showbuttontext = False, links = '')
    return dict(grid = grid)  

@auth.requires_membership('tribo_ng_datu')
def kasapi_tribo():
    db.auth_user.username.writable = True
    db.auth_user.password.writable =True
    db.auth_user.division_id.writable = True
    db.auth_user.division_id.readable = True

    grid = SQLFORM.grid(db.auth_membership, user_signature=False, csv = False,
        create = True, searchable = True, showbuttontext = False, links = '')
    return dict(grid = grid)  

@auth.requires_membership('tribo_ng_datu')
def Controller():
    db.auth_user.id.readable = False
    form = SQLFORM(db.auth_user, deletable = False).process()
    if form.accepted:
        response.flash = 'Controller created.'
        db.activities.insert(log_date = request.now,
            person = '%s %s' % (auth.user.first_name, auth.user.last_name),
            action = 'created %s %s controller.' % (form.vars.first_name, form.vars.last_name))                      
    links=[lambda row: A('Print', _title="Print", _target="_blank",
                         _href=URL("Reports","HandOverReport", args = row.id))]
    grid = SQLFORM.grid(db.auth_user.id != 6, user_signature=False, csv = False,
        create = False, searchable = False, details = False, ondelete = delete_c_record,
        showbuttontext = False, editable = auth.has_membership('level_1_user'),
        deletable = auth.has_membership('level_1_user'), onupdate = update_c_record)
    if request.args(0) == 'edit':
        response.view = 'default/Controller.html'
        grid = grid.update_form
        form = ''    
    return dict(form = form, grid = grid)  

def rep_tribo():

    #table = SQLTABLE(rows, headers=headers, extracolums=extracolums)
    headers = {'auth_user.first_name':'First Name',
    'auth_user.last_name':'Last Name',
    'auth_user.division_id':'Division',
    'auth_user.department_id':'Department',
    'auth_user.email':'Email',
    'auth_user.po_box':'PO Box',
    'auth_user.mobile_no':'Mobile No.',
    'auth_user.office_no':'Office No.',
    'auth_user.fax_no':'Fax No.' }
    rows = db(db.auth_user).select(db.auth_user.first_name, db.auth_user.last_name,
        db.auth_user.division_id,  db.auth_user.department_id, db.auth_user.email,
        db.auth_user.po_box, db.auth_user.mobile_no, db.auth_user.office_no, db.auth_user.fax_no)
    table = SQLTABLE(rows, headers = headers, _class = 'pure-table')
    return dict(table = table)

@auth.requires_membership('tribo_ng_datu')
def ulat_tribo():
    img_report = FORM(INPUT(_align = 'right', _type = 'image',  _target = "_blank",
        _src=URL('static','images/printButton.png'), _onclick = "javascript:PrintContent()"))    
       
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
