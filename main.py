import datetime
import json
from flask import Flask
from flask import request
from flask import render_template


app = Flask("XPENSE")


#Index-Seite

@app.route("/")
def index():
    e = open("data/expenses.json")
    expenses_data = json.load(e)
    i = open("data/income.json")
    income_data = json.load(i)

    expenses_categories = expenses_data["categories"]
    expenses_transactions = expenses_data["transactions"]

    income_categories = income_data["categories"]
    income_transactions = income_data["transactions"]


    #Berechnungen

    number_expenses = len(expenses_data)
    total_expenses = float(0.00)
    average_expense = float(0.00)
    number_income = len(income_data)
    total_income = float(0.00)
    highest_expense = float(0.00)
    highest_income = float(0.00)

    if number_expenses > 0:

        for entry in expenses_transactions:
            total_expenses = total_expenses + float(str(expenses_transactions[entry]["amount"]))
            if float(str(expenses_transactions[entry]["amount"])) > highest_expense:
                highest_expense = float(str(expenses_transactions[entry]["amount"]))
        average_expense = round(total_expenses / number_expenses, 2)

    if number_income > 0:
        for entry in income_transactions:
            total_income += float(income_transactions[entry]["amount"])
            if float(str(income_transactions[entry]["amount"])) > highest_expense:
                highest_income = float(str(income_transactions[entry]["amount"]))

    statistics = {
        "Einnahmen total": total_income,
        "Ausgaben total": total_expenses,
        "Übriges Guthaben": total_income - total_expenses,
        "Höchste Ausgabe": highest_expense,
        "Höchste Einnahme": highest_income,
        "Durchschnittliche Ausgabe pro Transaktion": average_expense
    }


    with open('data/expenses.json', 'w') as f:
        json.dump(expenses_data, f, indent=4, separators=(',', ':'))
    with open('data/income.json', 'w') as f:
        json.dump(income_data, f, indent=4, separators=(',', ':'))

    return render_template('index.html', expenses_transactions=expenses_transactions,
                           expenses_categories=expenses_categories, income_transactions=income_transactions,
                           income_categories=income_categories, statistics=statistics)




#Input für Geldausgaben

@app.route("/input-expenses", methods=['GET', 'POST'])
def input_expenses():
    e = open("data/expenses.json")
    expenses_data = json.load(e)

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
    i = open("data/income.json")
    income_data = json.load(i)

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



#Rest Python

if __name__ == "__main__":
    app.run(debug=True, port=5000)
