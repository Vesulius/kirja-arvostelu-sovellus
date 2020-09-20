from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

# Kuten koodista näkee tämä projekti lähti hieman kiireellä päälle.
# Aikataulun takia kaikki python koodi on vain yhdessä tiedostossa.
# Sivuston perusominaisuudet ovat kuitenkin jokseen kohdillaan.


# Tämä funktio lataa etusivun
@app.route("/")
def index():
    return render_template("index.html")


# Tämä funktio tarkistaa annetun käyttäjätunnuksen ja salasanan.
# Jos käyttäjätunnusta ei löydy niin se lataa create_account.html-tiedoston
# jossa voi luoda uuden käyttäjätunnuksen.
# Jos salasana on oikein niin käyttäjä kirjaudutaan sisään.
# Jos salasana on väärin niin ladataan virheilmoitus.
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user == None:
        return render_template("create_account.html")
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            session["username"] = username
            return render_template("index.html")
        else:
            # Tämä pitää korvaa virheilmoituksella index.html-tiedoston omalla virheilmoituksella
            return "Väärä käyttäjätunnus tai salasana"


# Tämä funktio vastaa uuden käyttäjätunnuksen luomisesta.
# Tähän tulisi lisätä vielä kyky tarkistaa uniikki käyttäjätunnus
@app.route("/create_account", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hash_value = generate_password_hash(password)

        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()

        session["username"] = username
        return render_template("index.html")
    else:
        return render_template("create_account.html")


# Tämä funktio vastaa hakutominaisuudesta.
# Tähän tulee vielä lisätä haun tarkennus ja erikseen tiettyjen hakujen tekeminen
# esim sivumäärän mukaan ja arviointien mukaan.
@app.route("/search", methods=["POST"])
def search():
    searchterm = request.form["searchterm"].lower()

    sql = "SELECT id, name, lenght FROM books WHERE to_tsvector(name || ' ' || author) @@ to_tsquery(:searchterm)"
    result = db.session.execute(sql, {"searchterm": searchterm})
    books = result.fetchall()

    if books == None:
        return "Ei tuloksia"
    return render_template("search_results.html", books=books)


# Tämä funktio vastaa arviointien hakemisesta niiden esittämisestä.
# Tähän pitäisi lisätä useampi tapa hakea arviointeja pituuden ja arviointituloksen perusteella
@app.route("/display_rewiews/<int:id>")
def display_rewiews(id):
    sql = "SELECT text, time, score FROM rewiews WHERE book_id=:id"
    result = db.session.execute(sql, {"id": id})
    rewiews = result.fetchall()

    sql = "SELECT name, lenght, author, id FROM books WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    book = result.fetchall()

    return render_template("display_rewiews.html", id=id, rewiews=rewiews, book=book)


# Tämä funktio vastaa arvioiniten lisäämisestä.
# Tähän pitää lisätä vielä useita ominaisuuksia kuten kirjottajan
# profiilin tallenus jolloin käyttäjä voi kirjoittaa vain yhden arvion per kirja
# Lisäksi virhelliset arvosanat voivat aiheuttaa oikean error viestin
@app.route("/add_rewiew/<int:id>", methods=["POST", "GET"])
def add_rewiew(id):

    rewiew_text = request.form["rewiew_text"]
    rewiew_score = int(float(request.form["rewiew_score"]))

    if (rewiew_score > 10) or (rewiew_score < 1):
        # Tähän parempi virheviesti
        return "Virheellinen arvosana"

    sql = "INSERT INTO rewiews (text,book_id,score) VALUES (:rewiew_text,:book_id,:rewiew_score)"
    db.session.execute(sql, {"rewiew_text": rewiew_text,
                             "book_id": id, "rewiew_score": rewiew_score})
    db.session.commit()


    return "Arviointi vastaanotettu"


# Tämä funktio kirjauttaa käyttäjän ulos
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
