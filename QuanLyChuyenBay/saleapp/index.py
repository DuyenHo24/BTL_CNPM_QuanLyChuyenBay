from flask import render_template, request

from saleapp import app, dao, admin


@app.route("/")
def index():

    tb_id = request.args.get('tuyen_bay_id')
    kw = request.args.get('keyword')
    chuyenbay = dao.load_chuyenbay(tb_id, kw)
    return render_template('index.html', chuyen_bay=chuyenbay)

@app.route("/chuyen_bay/<int:chuyen_bay_id>")
def details(chuyen_bay_id):
    cb = dao.get_chuyenbay_by_id(chuyen_bay_id)
    return render_template('details.html', chuyenbay=cb) #chuyenbay sd bên details.html


@app.context_processor
def common_attr():
    tuyenbay = dao.load_tuyenbay()

    return {
        'tuyenbay': tuyenbay,
    }


if __name__ == "__main__":
    app.run(debug=True)