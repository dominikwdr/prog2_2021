from flask import Flask
from flask import render_template

app = Flask("Hello World!")


@app.route("/")
def index():
    return render_template('index.html', name="Dominik")

@app.route("/input-expenses")
def input():
    return render_template('input_expenses.html', name="Dominik")


@app.route("/test")
def test():
    return "done!"

@app.route("/done")
def done():
    return "abgeschickt!"


if __name__ == "__main__":
    app.run(debug=True, port=5000)