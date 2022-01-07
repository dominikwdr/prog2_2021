from flask import Flask
from flask import render_template
import json

app = Flask("Hello World!")


@app.route("/")
def index():
    return render_template('index.html', name="Dominik")

@app.route("/input-expenses")
def input():
    return render_template('input_expenses.html', name="Dominik")


#expense-data aus json
def load_expenses_json(json_path):
    try:
        with open(json_path) as open_file:
            expenses = json.load(open_file)
    except FileNotFoundError:
        expenses = {}

    return expenses

if __name__ == "__main__":
    app.run(debug=True, port=5000)