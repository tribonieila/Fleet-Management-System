def delete_c_record(table, record_id): #[cancelled vehicle]
    record = db(table[table._id.name] == record_id).select().first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted %s %s controller.' %(record.first_name, record.last_name))
    return 

def delete_cv_record(table, record_id): #[cancelled vehicle]
    record = db(table[table._id.name] == record_id).select().first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted reg.no. %s cancelled vehicle.' %(record.reg_no))
    return 

def delete_vp_record(table, record_id): #[photo's]
    record = db(table[table._id.name] == record_id).select().first()
    v_reco = db(record.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted reg.no. %s photo\'s' %(v_reco.reg_no))
    return
    
def delete_ads_record(table, record_id): # [advertising]
    record = db(table[table._id.name] == record_id).select().first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted vehicle ads with license no. %s ' % (record.license_no))
    return

def delete_av_record(table, record_id): # [advertise vehicle]
    record = db(table[table._id.name] == record_id).select().first()
    v_reco = db(record.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    vehi_a = db(record.license_no_id == db.advertisement.id).select(db.advertisement.ALL).first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted reg.no. %s vehicle ads with license no. %s' % (v_reco.reg_no, vehi_a.license_no))
    return

def delete_me_record(table, record_id): # [maintenance expenses]
    record = db(table[table._id.name] == record_id).select().first()
    v_reco = db(record.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted reg.no. %s maintenance expenses with invoice number %s' % (v_reco.reg_no, record.invoice_number))
    return

def delete_fe_record(table, record_id): # [fuel expenses]
    record = db(table[table._id.name] == record_id).select().first()
    v_reco = db(record.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted reg.no. %s fuel expenses dated %s' % (v_reco.reg_no, record.date_expense))
    return

def delete_od_record(table, record_id): # [odometer]
    record = db(table[table._id.name] == record_id).select().first()
    v_reco = db(record.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted reg.no. %s odometer for the month of %s' % (v_reco.reg_no, str((record.given_month).strftime('%B %Y'))))  
    return

def delete_ip_record(table, record_id): # [insurance policy]
    record = db(table[table._id.name] == record_id).select().first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted insurance policy number %s' % (record.policy_no))

def delete_iv_record(table, record_id): # [insured vehicle]
    record = db(table[table._id.name] == record_id).select().first()
    v_reco = db(record.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted reg.no. %s insured vehicle.' % (v_reco.reg_no))
    return

def delete_d_record(table, record_id): # [driver]
    record = db(table[table._id.name] == record_id).select().first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
        action = 'deleted %s company driver name' % (record.driver_name))
    return

def delete_ho_record(table, record_id): # [hand-over]
    record = db(table[table._id.name] == record_id).select().first()
    v_reco = db(record.reg_no_id == db.vehicle.id).select(db.vehicle.ALL).first()
    db.activities.insert(log_date = request.now,
        person = '%s %s' % (auth.user.first_name, auth.user.last_name),
		action = 'deleted reg.no. %s hand-over.' %(v_reco.reg_no))
    return
	