from db import db
import users

# Tämä funktio hakee kirjan tietyn merkkijonon perusteella
def search_by(searchterm):
    sql = "SELECT id, name, length, COUNT(*) FROM books WHERE to_tsvector(name || ' ' || author) @@ to_tsquery(:searchterm) GROUP BY id"
    result = db.session.execute(sql, {"searchterm": searchterm})
    return result.fetchall()


# Tämä funktio vastaa arvioiden poistamisesta
def search_id(id):
    sql = "SELECT *, (SELECT SUM(score)/COUNT(*) FROM reviews WHERE book_id=:id) FROM books WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

def add_book(name, length, publication_year, author):
    sql = "INSERT INTO books (name, length, publication_year, author) VALUES (:name, :length, :publication_year, :author)"
    db.session.execute(sql, {"name": name, "length": length, "publication_year": publication_year, "author": author})
    db.session.commit()
    return True

def delete_book(id):
    sql = "DELETE FROM reviews WHERE book_id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()
    
    sql = "DELETE FROM books WHERE id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()  
    return True