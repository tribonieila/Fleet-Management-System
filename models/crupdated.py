def update_c_record(form):
    db.activities.insert(log_date = request.now,
        person = '%s %s' %(auth.user.first_name, auth.user.last_name),
        action = 'updated %s %s controller' %(form.vars.first_name, form.vars.last_name))
    return

def update_v_record(form): #[vehicle update]
    db.activities.insert(log_date = request.now,
        person = '%s %s' %(auth.user.first_name, auth.user.last_name),
        action = 'updated reg.no. %s company vehicle.' % form.vars.reg_no)
    return

def update_cv_record(form): #[cancelled vehicle update]
    db.activities.insert(log_date = request.now,
        person = '%s %s' %(auth.user.first_name, auth.user.last_name),
        action = 'updated reg.no. %s cancelled company vehicle.' % form.vars.reg_no)
    return 

def update_fe_record(form): #[fuel expenses update]
    record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now,
    	person = '%s %s' %(auth.user.first_name, auth.user.last_name),
    	action = 'updated reg.no. %s fuel expenses amounted QR %s' %(record.reg_no, locale.format('%.2f', form.vars.amount, grouping = True)))
    return 

def update_od_record(form): #[odemeter update]
    record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now, 
        person = '%s %s' % (auth.user.first_name,auth.user.last_name),
        action = 'updated reg.no. %s odometer for the month of %s' % (record.reg_no, str((request.now).strftime('%B %Y'))))
    return

def update_me_record(form): #[repair & maintenance expenses update]
    record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now,
    	person = '%s %s' % (auth.user.first_name, auth.user.last_name),
    	action = 'updated reg.no. %s maintenance expenses with invoice number %s' % (record.reg_no, form.vars.invoice_number))
    return 

def update_vp_record(form):
    record = db(request.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = "updated reg.no. %s photo's" % (record.reg_no))
    return 

def update_av_record(form):
    record = db(request.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    licens = db(request.vars.license_no_id == db.advertisement.id).select(db.advertisement.ALL).first()
    db.activities.insert(log_date = request.now,
		person = '%s %s' % (auth.user.first_name, auth.user.last_name),
		action = 'updated reg.no. %s vehicle ads with license no. %s' % (record.reg_no, licens.license_no))
    return

def update_ads_record(form):
	db.activities.insert(log_date = request.now,
		person = '%s %s' % (auth.user.first_name, auth.user.last_name),
		action = 'updated advertisement vehicle with license no. %s' % (request.vars.license_no))
	return

def update_ip_record(form):
    db.activities.insert(log_date = request.now,
    	person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = "updated insurance policy no. %s" % (request.vars.policy_no))
    return

def update_iv_record(form):
    record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = "updated reg.no. %s insured vehicle." %(record.reg_no))
    return

def update_d_record(form):
    db.activities.insert(log_date = request.now,
    	person = '%s %s' % (auth.user.first_name, auth.user.last_name),
		action = 'updated %s driver profile.' % (form.vars.driver_name))
    return

def update_ho_record(form):
    record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now, 
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
    	action = 'updated reg.no. %s hand-over.' %(record.reg_no))
    return
