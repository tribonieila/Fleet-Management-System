def create_v_record(form):
    db.activities.insert(log_date = request.now,
    person = '%s %s' %(auth.user.first_name, auth.user.last_name),
    action = 'created company vehicle with reg.no. %s' %(form.vars.reg_no))

def create_vm_record(form):
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name), 
        action = 'created maintenance expenses with invoice number %s' % (form.vars.invoice_number),
        log_code = 1,
        focal_person = auth.user.id)

def create_vp_record(form):
    record = db(form.vars.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now,
    	person = '%s %s' % (auth.user.first_name, auth.user.last_name),
    	action = 'created reg.no. %s image.' % (record.reg_no))
    redirect(URL('upload_photos'))

def create_av_record(form):
	db.activities.insert(log_date = request.now,
		person = '%s %s' % (auth.user.first_name, auth.user.last_name),
		action = 'Created vehicle ads')
	redirect(URL('Advertisement'))

def create_ads_record(form):
	db.activities.insert(log_date = request.now,
		person = '%s %s' % (auth.user.first_name, auth.user.last_name),
		action = 'created advertisement vehicle with license no. %s' % (request.vars.license_no))
	redirect(URL('Advertisement'))

def create_ip_record(form):
	db.activities.insert(log_date = request.now,
        person = auth.user.first_name + ' ' + auth.user.last_name,
        action = 'Created insurance policy no %s' % (request.vars.policy_no))
	redirect(URL('InsurancePolicy'))

def create_iv_record(form):
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = "Created insured vehicle with policy no. %s" % (form.vars.policy_no_id))
    redirect(URL('InsuredVehiclesForm'))

def create_d_record(form):
    db.activities.insert(log_date = request.now,
    	person = '%s %s' % (auth.user.first_name, auth.user.last_name),
		action = 'Created %s driver profile.' % (form.vars.driver_name))
    redirect(URL('Driver'))

def create_ho_record(form):
    db.activities.insert(log_date = request.now, 
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
    	action = 'Created hand-over.')
    redirect(URL('HandOver'))