from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from db import db

import reviews
import users
import books

# Tämä funktio lataa etusivun
@app.route("/")
def index():
    return render_template("index.html")


# Tämä funktio lataa sisäänkirjautumis-sivun
@app.route("/login_page")
def login_page():
    return render_template("login.html")


# Tämä funktio tarkistaa annetun käyttäjätunnuksen ja salasanan.
# Jos käyttäjätunnusta ei löydy niin se lataa create_account.html-tiedoston
# jossa voi luoda uuden käyttäjätunnuksen.
# Jos salasana on oikein niin käyttäjä kirjaudutaan sisään.
# Jos salasana on väärin niin ladataan virheilmoitus.
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = users.login(username, password)

    if user == None:
        return render_template("create_account.html")
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            session["username"] = username
            users.start_session(users.get_id(session.get("username")))
            return render_template("index.html")
        else:
            # Tämä pitää korvaa virheilmoituksella index.html-tiedoston omalla virheilmoituksella
            return render_template("login.html", message="Väärä käyttäjätunnus tai salasana")


# Tämä funktio kirjauttaa käyttäjän ulos
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


# Tämä funktio vastaa uuden käyttäjätunnuksen luomisesta
@app.route("/create_account", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Vielä viimeinen tarkistus onko salasana oikean pituinen
        if len(password) < 4:
            return render_template("create_account.html", message="Salasanan tulee olla vähintään neljä merkkiä")

        if users.register(username, password):
            session["username"] = username
            users.start_session(users.get_id(session.get("username")))
            return render_template("index.html")
        else:
            return render_template("create_account.html")
    else:
        return render_template("create_account.html", message="Luo uusi käyttäjä")


# Tämä funkito poistaa profiileja ja niihin littyvät kommentit
@app.route("/delete_profile")
def delete_profile():
    if not users.delete_account(users.get_id(session.get("username"))):
        return render_template("error.html", message="Adminkäyttäjää ei voi poistaa!")

    del session["username"]
    return redirect("/")


# Tämä funktio lataa sisäänkirjautumis-sivun
@app.route("/profile")
def profile():
    user_id = users.get_id(session.get("username"))
    user_reviews = reviews.select_reviews_user_id(user_id)
    if not user_reviews:
        reviews_count = 0
        last_log = 0
    else:
        reviews_count = user_reviews[0][5]

    # Ladataan eri sivu jos käyttäjä on admin
    if users.privileges(users.get_id(session.get("username"))):
        return render_template("add_book.html", reviews=user_reviews, reviews_count=reviews_count)
    return render_template("profile.html", reviews=user_reviews, reviews_count=reviews_count, last_log=users.last_log(user_id))


# Tämä funktio vastaa hakutominaisuudesta
# Tähän tulee vielä lisätä haun tarkennus ja erikseen tiettyjen hakujen tekeminen
# esim sivumäärän mukaan ja arviointien mukaan
@app.route("/search", methods=["POST"])
def search():
    searchterm = request.form["searchterm"].lower()
    message = "Haukutulokset:"
    found_books = books.search_by(searchterm)

    # Luodaan uusi viesti jos haku ei tuota tulosta
    if not found_books:
        message = "Haullesi ei löytynyt tuloksia :("
    if session.get("username", None) != None and users.privileges(users.get_id(session.get("username"))):
        return render_template("delete_book.html", books=found_books, message="Hei admin, poista kirja tästä")
    return render_template("search_results.html", books=found_books, message=message)


# Tämä funktio vastaa arviointien hakemisesta niiden esittämisestä
# Tähän pitäisi lisätä useampi tapa hakea arviointeja pituuden ja arviointituloksen perusteella
@app.route("/display_reviews/<int:id>")
def display_reviews(id):
    return render_template("display_reviews.html", id=id, reviews=reviews.select_reviews(id), book=books.search_id(id))


# Tämä funktio vastaa arvioiniten lisäämisestä
@app.route("/add_review/<int:id>", methods=["POST", "GET"])
def add_review(id):
    review_text = request.form["review_text"]
    review_score = int(float(request.form["review_score"]))
    session_username = session.get("username")

    # Tarkistetaan vielä onko arvosana oikein
    if (review_score > 10) or (review_score < 1):
        return render_template("error.html", message="Virheellinen arvio")
    reviews.add_review(id, review_text, review_score, session_username)
    return render_template("display_reviews.html", id=id, reviews=reviews.select_reviews(id), book=books.search_id(id))


# Tämä funktio vastaa arvioiniten poistamisesta
@app.route("/delete_review/<int:id>", methods=["POST", "GET"])
def delete_review(id):
    reviews.delete_review(id)
    user_reviews = reviews.select_reviews_user_id(users.get_id(session.get("username")))
    # Tarkistetaan sisälsikö vastaus tuloksia
    if not user_reviews:
        return render_template("profile.html", reviews=user_reviews, reviews_count=0, last_log=users.last_log(id))
    else:
        return render_template("profile.html", reviews=user_reviews, reviews_count=user_reviews[0][5], last_log=users.last_log(id))


# Tämä funktio vastaa kirjojen lisäämisestä
@app.route("/add_book", methods=["POST", "GET"])
def add_book():
    if request.method == "GET":
        return render_template("add_book.html")
    else:
        name = request.form["name"]
        length = request.form["length"]
        publication_year = request.form["publication_year"]
        author = request.form["author"]

        # Tarkistetaan vielä onko käyttäjä admin
        if not users.privileges:
            return render_template("error.html", message="Sä et ole admin??")

        books.add_book(name, length, publication_year, author)
        return render_template("add_book.html", message="Lisätty")


# Tämä funktio vastaa kirjojen poistamisesta, tarkastetaan myös profiilin oikeudet
@app.route("/delete_book/<int:id>", methods=["GET"])
def delete_book(id):
    if users.privileges:
        books.delete_book(id)
        return render_template("index.html")
    return render_template("error.html", message="Sä et oo admin bro!")