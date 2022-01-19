import datetime
import json
from flask import Flask
from flask import request
from flask import render_template


app = Flask("XPENSE")


#Index / Page "Dashboard"

@app.route("/")
def index():
    e = open("data/expenses.json") #Datenabfrage von Ausgabe-Daten
    expenses_data = json.load(e)
    i = open("data/income.json") #Datenabfrage von Einnahme-Daten
    income_data = json.load(i)

    #Unterteilung der Daten in Kategorien oder Transaktionen von Einnahmen/Ausgaben
    expenses_categories = expenses_data["categories"]
    expenses_transactions = expenses_data["transactions"]

    income_categories = income_data["categories"]
    income_transactions = income_data["transactions"]


    #Berechnungen für die Statistiken

    #Definierung von einzelnen Werten
    number_expenses = len(expenses_data) #Formatierungen in "length", um Durchschnitt an Ausgaben/Einnahme zu berechnen
    total_expenses = float(0.00) #Formatierungen in "float", da Geldbeträge auf 5 Rappen genau (also 2 Dezimalstellen)
    average_expense = float(0.00)
    number_income = len(income_data)
    total_income = float(0.00)
    highest_expense = float(0.00)
    highest_income = float(0.00)

    #Berechnungen Ausgaben
    if number_expenses > 0:
        for entry in expenses_transactions:
            total_expenses = total_expenses + float(expenses_transactions[entry]["amount"])
            if float(expenses_transactions[entry]["amount"]) > highest_expense:
                highest_expense = float(expenses_transactions[entry]["amount"])
        average_expense = round(total_expenses / number_expenses, 2)


    #Berechnugnen Einnahmen
    if number_income > 0:
        for entry in income_transactions:
            total_income += float(income_transactions[entry]["amount"])
            if float(income_transactions[entry]["amount"]) > highest_income:
                highest_income = float(income_transactions[entry]["amount"])



    #Ausgabe der Statistik-Werte für Übersicht
    statistics = {
        "Einnahmen total": total_income,
        "Ausgaben total": total_expenses,
        "Übriges Guthaben": total_income - total_expenses,
        "Höchste Ausgabe": highest_expense,
        "Höchste Einnahme": highest_income,
        "Durchschnittliche Ausgabe pro Transaktion": average_expense
    }

    return render_template('index.html', expenses_transactions=expenses_transactions,
                           expenses_categories=expenses_categories, income_transactions=income_transactions,
                           income_categories=income_categories, statistics=statistics)



#Input für Geldausgaben / Page "Ausgabe erfassen"

@app.route("/input-expenses", methods=['GET', 'POST'])
def input_expenses():
    e = open("data/expenses.json") #Datenabfrage der Ausgaben
    expenses_data = json.load(e)

    #Unterteilung der Daten in Kategorien oder Transaktionen von Ausgaben
    expenses_categories = expenses_data["categories"]
    expenses_transactions = expenses_data["transactions"]

    if request.method == 'POST':
        if "category_name" in request.form: #Abfrage, ob neuer Eintrag auf Page "Ausgabe erfassen" eine Kategorie ist
            if request.form["category_name"] != "": #Abfrage ob request.form Werte enthält
                category_name = request.form["category_name"] #Auswerten der Eingaben aus dem Formular (Name der Kategorie)
                category_color = request.form["category_color"] #Auswerten der Eingaben aus dem Formular (Farbe im HEX-Code)

                #Ausgabe der Ausgabenkategorien
                expenses_categories[category_name] = {
                    "name": category_name, #"categorie_name" doppelt, für einfachere Ausgabe und doch einheitliche Gliederung
                    "color": category_color #HEX-Code der Farbe, welche für Kategorie definiert werden muss
                }

        if "transaction_title" in request.form: #Abfrage, ob neuer Eintrag eine Transaktion ist
            if request.form["transaction_title"] != "": #Abfrage ob request.form Werte enthält
                #Erstellung einer individuellen ID pro Transaktion mittels Timestamp auf Millisekunde genau
                datetime_now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                dt_obj = datetime.datetime.strptime(str(datetime_now), '%d.%m.%Y %H:%M:%S')
                datetime_now_ms = int(round(dt_obj.timestamp() * 1000))
                #Quelle/Tipp zu dieser Methode: Felix (Freund)

                #Übersicht der einzelnen Daten aus request.form
                transaction_id = datetime_now_ms
                transaction_datetime = datetime_now
                transaction_title = request.form["transaction_title"]
                transaction_amount = request.form["transaction_amount"]
                transaction_category = request.form["transaction_category"]

                # Daten gegliedert für Dump in expenses.json
                expenses_transactions[transaction_id] = {
                    "title": transaction_title,
                    "amount": transaction_amount,
                    "category": transaction_category,
                    "datetime": transaction_datetime
                }

    #Dump Daten in expenses.json
    with open('data/expenses.json', 'w') as f:
        json.dump(expenses_data, f, indent=4, separators=(',', ':'))

    return render_template('input_expenses.html', expenses_transactions=expenses_transactions,
                           expenses_categories=expenses_categories)


#Input für Geldeinnahmen / Page "Einnahme erfassen"

@app.route("/input-income", methods=['GET', 'POST'])
def input_income():
    i = open("data/income.json") #Datenabfrage der Einnahmen
    income_data = json.load(i)

    #Unterteilung der Daten in Kategorien oder Transaktionen von Einnahmen
    income_categories = income_data["categories"]
    income_transactions = income_data["transactions"]

    if request.method == 'POST':
        if "category_name" in request.form: #Abfrage, ob neuer Eintrag eine Kategorie ist
            if request.form["category_name"] != "": #Abfrage ob request.form Werte enthält
                category_name = request.form["category_name"] #Auswerten der Eingaben aus dem Formular (Name der Kategorie)
                category_color = request.form["category_color"] #Auswerten der Eingaben aus dem Formular (Farbe im HEX-Format)

                #Ausgabe der Einnahmekategorien
                income_categories[category_name] = {
                    "name": category_name, #"categorie_name" doppelt, für einfachere Ausgabe und doch einheitliche Gliederung
                    "color": category_color #HEX-Code der Farbe, welche für Kategorie definiert werden muss
                }


        if "transaction_title" in request.form: #Abfrage, ob neuer Eintrag eine Transaktion ist
            if request.form["transaction_title"] != "": #Abfrage ob request.form Werte enthält
                # Erstellung einer individuellen ID pro Transaktion mittels Timestamp auf Millisekunde genau
                datetime_now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                dt_obj = datetime.datetime.strptime(str(datetime_now), '%d.%m.%Y %H:%M:%S')
                datetime_now_ms = int(round(dt_obj.timestamp() * 1000))
                #Quelle/Tipp zu dieser Methode: Felix (Freund)

                #Übersicht der einzelnen Daten aus request.form
                transaction_id = datetime_now_ms
                transaction_datetime = datetime_now
                transaction_title = request.form["transaction_title"]
                transaction_amount = request.form["transaction_amount"]
                transaction_category = request.form["transaction_category"]

                #Daten gegliedert für Dump in income.json
                income_transactions[transaction_id] = {
                    "title": transaction_title,
                    "amount": transaction_amount,
                    "category": transaction_category,
                    "datetime": transaction_datetime
                }

        # Dump Daten in income.json
        with open('data/income.json', 'w') as f:
            json.dump(income_data, f, indent=4, separators=(',', ':'))

    return render_template('input_income.html', income_transactions=income_transactions,
                           income_categories=income_categories)


if __name__ == "__main__":
    app.run(debug=True, port=5000)