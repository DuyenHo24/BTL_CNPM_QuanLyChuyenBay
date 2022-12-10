from flask import render_template, request

from saleapp import app, dao


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)