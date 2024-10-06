import mydb
inprogress_id={'Pizza': 2.0, 'Chole Bhature': 3.0, 'Mango Lassi': 1.0, 'Pav Bhaji': 2.0}
new=100
for food_item, quantity in inprogress_id.items():
    rcode=mydb.insert_order_item(
        food_item,
        quantity,
        new
    )