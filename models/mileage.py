rows = db(db.km_used.reg_no_id == db.vehicle(request.args(0))).select(orderby = db.km_used.given_month)
r = 1
row = len(rows)
while (r < row):
    rows[r].update_record(consumed_mil = rows[r].current_mil - rows[r-1].current_mil)
    r +=1
