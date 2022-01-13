import datetime
import json
from flask import Flask
from flask import request
from flask import render_template


app = Flask("XPENSE")


#Index-Seite
@app.route("/")
def index():
    r = open("data/expenses.json")
    expenses_data = json.load(r)
    w = open("data/income.json")
    income_data = json.load(w)

    print(expenses_data)
    expenses_categories = expenses_data["categories"]
    expenses_transactions = expenses_data["transactions"]

    income_categories = income_data["categories"]
    income_transactions = income_data["transactions"]

    with open('data/expenses.json', 'w') as f:
        json.dump(expenses_data, f, indent=4, separators=(',', ':'))
    with open('data/income.json', 'w') as f:
        json.dump(income_data, f, indent=4, separators=(',', ':'))

    return render_template('index.html', expenses_transactions=expenses_transactions,
                           expenses_categories=expenses_categories, income_transactions=income_transactions,
                           income_categories=income_categories)





#Input für Geldausgaben
@app.route("/input-expenses", methods=['GET', 'POST'])
def input_expenses():
    r = open("data/expenses.json")
    expenses_data = json.load(r)

    expenses_categories = expenses_data["categories"]
    expenses_transactions = expenses_data["transactions"]

    if request.method == 'POST':
        if "category_name" in request.form:
            category_name = request.form["category_name"]
            category_color = request.form["category_color"]

            expenses_categories[category_name] = {
                "name": category_name,
                "color": category_color
            }

        if "transaction_title" in request.form:
            datetime_now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            dt_obj = datetime.datetime.strptime(str(datetime_now), '%d.%m.%Y %H:%M:%S')
            datetime_now_ms = int(round(dt_obj.timestamp() * 1000))

            transaction_id = datetime_now_ms
            transaction_datetime = datetime_now
            transaction_title = request.form["transaction_title"]
            transaction_amount = request.form["transaction_amount"]
            transaction_category = request.form["transaction_category"]

            expenses_transactions[transaction_id] = {
                "title": transaction_title,
                "amount": transaction_amount,
                "category": transaction_category,
                "datetime": transaction_datetime
            }

    with open('data/expenses.json', 'w') as f:
        json.dump(expenses_data, f, indent=4, separators=(',', ':'))

    return render_template('input_expenses.html', expenses_transactions=expenses_transactions,
                           expenses_categories=expenses_categories)



#Input für Geldeinnahmen
@app.route("/input-income", methods=['GET', 'POST'])
def input_income():
    w = open("data/income.json")
    income_data = json.load(w)

    income_categories = income_data["categories"]
    income_transactions = income_data["transactions"]

    if request.method == 'POST':
        if "category_name" in request.form:
            category_name = request.form["category_name"]

            income_categories[category_name] = {
                "name": category_name
            }


        if "transaction_title" in request.form:
            datetime_now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            dt_obj = datetime.datetime.strptime(str(datetime_now), '%d.%m.%Y %H:%M:%S')
            datetime_now_ms = int(round(dt_obj.timestamp() * 1000))

            transaction_id = datetime_now_ms
            transaction_datetime = datetime_now
            transaction_title = request.form["transaction_title"]
            transaction_amount = request.form["transaction_amount"]
            transaction_category = request.form["transaction_category"]

            income_transactions[transaction_id] = {
                "title": transaction_title,
                "amount": transaction_amount,
                "category": transaction_category,
                "datetime": transaction_datetime
            }


        with open('data/income.json', 'w') as f:
            json.dump(income_data, f, indent=4, separators=(',', ':'))

    return render_template('input_income.html', income_transactions=income_transactions,
                           income_categories=income_categories)





if __name__ == "__main__":
    app.run(debug=True, port=5000)
