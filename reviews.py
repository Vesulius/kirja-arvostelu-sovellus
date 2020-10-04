from db import db
import users, books

# Tämä funktio vastaa arvioiniten lisäämisestä.
# Tähän pitää lisätä vielä useita ominaisuuksia kuten kirjottajan
# profiilin tallenus jolloin käyttäjä voi kirjoittaa vain yhden arvion per kirja
def add_review(book_id, review_text, review_score, session_username):
    sql = "INSERT INTO reviews (text,book_id,score, user_id) VALUES (:review_text,:book_id,:review_score, (SELECT id FROM users WHERE username = :session_username))"
    db.session.execute(sql, {"review_text": review_text,
                             "book_id": book_id, "review_score": review_score, "session_username": session_username})
    db.session.commit()
    return book_id


# Tämä funktio vastaa arvioiden poistamisesta
def delete_review(id):
    sql = "DELETE FROM reviews WHERE id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()
    return True


# Tämä funktio hakee tietystä kirjasta tehdyt arviot
def select_reviews(id):
    sql = "SELECT S.text, S.time, S.score, (SELECT username FROM users WHERE id=S.user_id) username FROM reviews S WHERE S.book_id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()


# Tämä funktio hakee titetyn käyttäjän kaikki arviot
def select_reviews_user_id(id):
    sql = "SELECT text, time, score, (SELECT name FROM books WHERE R.book_id=id), id, (SELECT COUNT(*) FROM reviews WHERE user_id=:id) FROM reviews R WHERE user_id=:id GROUP BY id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()