    #expiration = check.period_covered + datetime.timedelta(weeks = 1)
import datetime
today = datetime.date.today()
query = db(db.insurance_policy).select(db.insurance_policy.period_covered,
                                           db.insurance_policy.insurance_company_id,
                                           orderby = db.insurance_policy.period_covered).first()
'''
Day30 = query.period_covered + datetime.timedelta(days = 30)
Day25 = query.period_covered + datetime.timedelta(days = 25)
Day20 = query.period_covered + datetime.timedelta(days = 20)
Day15 = query.period_covered + datetime.timedelta(days = 15)
Day10 = query.period_covered + datetime.timedelta(days = 10)
Day5  = query.period_covered + datetime.timedelta(days = 5)
Day1  = query.period_covered + datetime.timedelta(days = 1)
      
if Day30 == today:
    response.flash = str(query.insurance_company_id.name) + " is " + " 30 day's to expire."
elif Day25 == today:
    response.flash = str(query.insurance_company_id.name) + " is " + " 25 day's to expire."
elif Day10 == today:
    response.flash = str(query.insurance_company_id.name) + " is " + " 20 day's to expire."
elif Day15 == today:
    response.flash = str(query.insurance_company_id.name) + " is " + " 15 day's to expire."
elif Day10 == today:
    response.flash = str(query.insurance_company_id.name) + " is " + " 10 day's to expire."
elif Day5 == today:
    response.flash = str(query.insurance_company_id.name) + " is " + " 5 day's to expire."
elif Day1 == today:
    response.flash = str(query.insurance_company_id.name) + " is " + " 1 day to expire."
elif query.period_covered == today:
    response.flash = str(query.insurance_company_id.name) + " is expired."
elif query.period_covered <= today:
    ExDate = today - query.period_covered
    response.flash = str(query.insurance_company_id.name) + " is " + str(ExDate.days) + " day's expired."
else:
    response.flash = ''


v_query = db(db.vehicle).select(db.vehicle.reg_no, db.vehicle.exp_date, orderby = db.vehicle.exp_date).first()
VExp_30 = v_query.exp_date + datetime.timedelta(days = 30)
VExp_25 = v_query.exp_date + datetime.timedelta(days = 25)
VExp_20 = v_query.exp_date + datetime.timedelta(days = 20)
VExp_15 = v_query.exp_date + datetime.timedelta(days = 15)
VExp_10 = v_query.exp_date + datetime.timedelta(days = 10)
VExp_5  = v_query.exp_date + datetime.timedelta(days = 5)
VExp_1  = v_query.exp_date + datetime.timedelta(days = 1)

if VExp_30 == today:
    response.flash = "Reg.No. " + str(v_query.reg_no) + " is " + " 30 day's to expire."
elif Day25 == today:
    response.flash = "Reg.No. " + str(v_query.reg_no) + " is " + " 25 day's to expire."
elif Day20 == today:
    response.flash = "Reg.No. " + str(v_query.reg_no) + " is " + " 20 day's to expire."
elif Day15 == today:
    response.flash = "Reg.No. " + str(v_query.reg_no) + " is " + " 15 day's to expire."
elif Day10 == today:
    response.flash = "Reg.No. " + str(v_query.reg_no) + " is " + " 10 day's to expire."
elif Day1 == today:
    response.flash = "Reg.No. " + str(v_query.reg_no) + " is " + " 1 day to expire."
elif v_query.exp_date == today:
    response.flash = "Reg.No. " + str(v_query.reg_no) + " is expired."    
#elif v_query.exp_date <= today:
#    V_ExDate = today - v_query.exp_date
#    response.flash = "Reg.No. " + str(v_query.reg_no) + " is " + str(V_ExDate.days) + " day's expired."
else:
    response.flash = ''
 
ads_query = db(db.advertisement).select(db.advertisement.ALL, orderby = db.advertisement.expiry_date).first()
AExp_30 = ads_query.expiry_date + datetime.timedelta(days = 30)
AExp_25 = ads_query.expiry_date + datetime.timedelta(days = 25)
AExp_20 = ads_query.expiry_date + datetime.timedelta(days = 20)
AExp_15 = ads_query.expiry_date + datetime.timedelta(days = 15)
AExp_10 = ads_query.expiry_date + datetime.timedelta(days = 10)
AExp_5  = ads_query.expiry_date + datetime.timedelta(days = 5)
AExp_1  = ads_query.expiry_date + datetime.timedelta(days = 1)

if AExp_30 == today:
    response.flash = "Reg.No. " + str(ads_query.reg_no_id.reg_no) + " with ads is 30 day's to expire."
elif AExp_25 == today:
    response.flash = "Reg.No. " + str(ads_query.reg_no_id.reg_no) + " with ads is 25 day's to expire."
elif AExp_20 == today:
    response.flash = "Reg.No. " + str(ads_query.reg_no_id.reg_no) + " with ads is 20 day's to expire."
elif AExp_15 == today:
    response.flash = "Reg.No. " + str(ads_query.reg_no_id.reg_no) + " with ads is 15 day's to expire."
elif AExp_10 == today:
    response.flash = "Reg.No. " + str(ads_query.reg_no_id.reg_no) + " with ads is 10 day's to expire."
elif AExp_5 == today:
    response.flash = "Reg.No. " + str(ads_query.reg_no_id.reg_no) + " with ads is 5 day's to expire."
elif AExp_1 == today:
    response.flash = "Reg.No. " + str(ads_query.reg_no_id.reg_no) + " with ads is 1 day's to expire."
elif ads_query.expiry_date == today:
    response.flash = "Reg.No. " + str(ads_query.reg_no_id.reg_no) + " with ads is expired."    
elif ads_query.expiry_date <= today:
    A_ExDate = today - ads_query.expiry_date
    response.flash = "Reg.No. " + str(ads_query.reg_no_id.reg_no) + " is " + str(A_ExDate.days) + " day's expired."
else:
    response.flash = ''

'''   