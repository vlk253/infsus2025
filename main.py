from flask import Flask,request,make_response,jsonify, render_template, redirect, url_for
from pony import orm
from datetime import date, time
from collections import defaultdict
from datetime import datetime


app = Flask(__name__)

db = orm.Database()

class Termin(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    datum = orm.Required(date)
    pocetak = orm.Required(time)
    kraj = orm.Required(time)
    vrsta_treninga = orm.Required(str)
    kapacitet = orm.Required(int)
    popunjenost = orm.Required(int)

db.bind(provider='sqlite', filename='eteretana.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

def formatiraj_datum(datum):
    return datum.strftime('%d-%m-%Y') if datum else None

def formatiraj_vrijeme(vrijeme):
    if isinstance(vrijeme, str):
        return vrijeme  # već je string
    return vrijeme.strftime('%H:%M') if vrijeme else None


def add_termin(json_request):
    try:
        vrsta_treninga = json_request['vrsta_treninga']
        kapacitet = int(json_request['kapacitet'])
        popunjenost = int(json_request['popunjenost'])
        datum = datetime.strptime(json_request['datum'], '%Y-%m-%d').date()
        pocetak = datetime.strptime(json_request['pocetak'], '%H:%M').time()
        kraj = datetime.strptime(json_request['kraj'], '%H:%M').time()
        with orm.db_session:
            Termin(datum=datum, pocetak=pocetak, kraj=kraj,
                   vrsta_treninga=vrsta_treninga,
                   kapacitet=kapacitet, popunjenost=popunjenost)
            return {'response': 'Success'}
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

def get_termini():
    try:
        with orm.db_session:
            db_querry = orm.select(x for x in Termin)[:]
            results_list = []
            for r in db_querry:
                results_list.append(r.to_dict())
            response = {"response": "Success", "data": results_list}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

def get_termin_by_id(termin_id):
    try:
        with orm.db_session:
            result = Termin[termin_id].to_dict()
            result['datum'] = formatiraj_datum(result['datum'])
            response = {"response": "Success", "data": result}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


def patch_termin(termin_id, json_request):
    try:
        with orm.db_session:
            termin = Termin[termin_id]
            if 'datum' in json_request:
                termin.datum = datetime.strptime(json_request['datum'], '%d-%m-%Y').date()
            if 'pocetak' in json_request:
                termin.pocetak = datetime.strptime(json_request['pocetak'], '%H:%M').time()
            if 'kraj' in json_request:
                termin.kraj = datetime.strptime(json_request['kraj'], '%H:%M').time()
            if 'vrsta_treninga' in json_request:
                termin.vrsta_treninga = json_request['vrsta_treninga']
            if 'kapacitet' in json_request:
                termin.kapacitet = int(json_request['kapacitet'])
            if 'popunjenost' in json_request:
                termin.popunjenost = int(json_request['popunjenost'])
            return {"response": "Success"}
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

def put_termin(termin_id, json_request):
    try:
        with orm.db_session:
            termin = Termin[termin_id]
            termin.datum = datetime.strptime(json_request['datum'], '%d-%m-%Y').date()
            termin.pocetak = datetime.strptime(json_request['pocetak'], '%H:%M').time()
            termin.kraj = datetime.strptime(json_request['kraj'], '%H:%M').time()
            termin.vrsta_treninga = json_request['vrsta_treninga']
            termin.kapacitet = int(json_request['kapacitet'])
            termin.popunjenost = int(json_request['popunjenost'])
            return {"response": "Success"}
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

def delete_termin(termin_id):
    try:
        with orm.db_session:
            to_delete = Termin[termin_id]
            to_delete.delete()
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}

##################################################################
@app.route("/dodaj/termin", methods=["POST", "GET"])
def dodaj_termin():
    if request.method == "POST":
        try:
            if request.is_json:
                json_request = request.get_json()
            else:
                json_request = {key: (None if value == "" else value) for key, value in request.form.items()}
        except Exception as e:
            response = {"response": str(e)}
            return make_response(jsonify(response), 400)

        response = add_termin(json_request)

        if response["response"] == "Success":
            # Vrati JSON ako je JSON zahtjev
            if request.is_json:
                return make_response(jsonify(response), 200)
            return make_response(render_template("dodaj.html"), 200)
        return make_response(jsonify(response), 400)
    return make_response(render_template("dodaj.html"), 200)



@app.route("/vrati/termine", methods=["GET"])
def vrati_termine():
    if request.args and 'id' in request.args:
        termin_id = int(request.args.get("id"))
        response = get_termin_by_id(termin_id)
        if response["response"] == "Success":
            return make_response(render_template("vrati.html", data=[response["data"]]), 200)
        return make_response(jsonify(response), 400)
    response = get_termini()
    if response["response"] == "Success":
        return make_response(render_template("vrati.html", data=response["data"]), 200)
    return make_response(jsonify(response), 400)

@app.route("/vrati/termini/vizualizacija", methods=["GET"])
@orm.db_session
def vizualizacija():
    try:
        termini = orm.select(t for t in Termin)[:]
        dan_broj = defaultdict(int)
        for t in termini:
            dan = t.datum
            dan_broj[dan] += 1
        sorted_dan_broj = dict(sorted(dan_broj.items()))
        x_axis = [d.strftime("%d. %b") for d in sorted_dan_broj.keys()]
        y_axis = list(sorted_dan_broj.values())
        response = {"response": "Success"}
        if response["response"] == "Success":
            return make_response(render_template("vizualizacija.html", y_axis=y_axis, x_axis=x_axis), 200)
        return make_response(jsonify(response), 400)

    except Exception as e:
        error_response = {"response": "Error", "error_message": str(e)}
        return make_response(jsonify(error_response), 500)

@app.route("/termin/<int:termin_id>", methods=["DELETE"])
def obrisi_termin(termin_id):
    response = delete_termin(termin_id)
    if response["response"] == "Success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)

@app.route("/termin/<int:termin_id>", methods=["PATCH"])
def patch_termin():
    try:
        json_request = request.json
    except Exception as e:
        return make_response(jsonify(response), 400)
    if request.args:
        termin_id = int(request.args.get("id"))
        response = patch_termin(termin_id, json_request)
        if response["response"] == "Success":
            return make_response(jsonify(response), 200)
        return make_response(jsonify(response), 400)
    response = {"response": "Query string missing"}
    return make_response(jsonify(response), 400)

@app.route("/termin/<int:termin_id>", methods=["PUT"])
def zamijeni_termin(termin_id):
    try:
        json_request = request.json
        response = put_termin(termin_id, json_request)
        if response["response"] == "Success":
            return make_response(jsonify(response), 200)
        return make_response(jsonify(response), 400)
    except Exception as e:
        return make_response(jsonify({"response": str(e)}), 400)

@app.route("/izmjeni/<int:termin_id>", methods=["GET", "POST"])
def izmjeni_termin(termin_id):
    with orm.db_session:
        termin = Termin.get(id=termin_id)
        if not termin:
            return make_response("Termin nije pronađen", 404)
        if request.method == "POST":
            termin.vrsta_treninga = request.form["vrsta_treninga"]
            termin.datum = datetime.strptime(request.form["datum"], "%Y-%m-%d").date()
            termin.pocetak = datetime.strptime(request.form["pocetak"], "%H:%M:%S").time()
            termin.kraj = datetime.strptime(request.form["kraj"], "%H:%M:%S").time()
            termin.kapacitet = int(request.form["kapacitet"])
            termin.popunjenost = int(request.form["popunjenost"])
            return redirect(url_for("vrati_termine"))

        termin_data = {
            "vrsta_treninga": termin.vrsta_treninga,
            "datum": termin.datum.strftime("%Y-%m-%d") if hasattr(termin.datum, "strftime") else termin.datum,
            "pocetak": termin.pocetak.strftime("%H:%M:%S") if hasattr(termin.pocetak, "strftime") else termin.pocetak,
            "kraj": termin.kraj.strftime("%H:%M:%S") if hasattr(termin.kraj, "strftime") else termin.kraj,
            "kapacitet": termin.kapacitet,
            "popunjenost": termin.popunjenost,
        }

        return render_template("izmjeni_termin.html", termin=termin_data)

@app.route("/", methods=["GET"])
def home():
    return make_response(render_template("index.html"), 200)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
