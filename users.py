from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

# Tämä funktio hakee salasanan käyttäjänimen perusteella
def login(username, password):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


# Tämä funktio hakee profiilin id:n käyttäjänimen perusteella
def get_id(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return int(result.fetchone()[0])


# Tämä funktio lisää uuden profiilin tietokantaan
def register(username, password):
    hash_value = generate_password_hash(password)

    # Tarkistetaan onko käyttäjänimi otettu
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    if result.fetchone():
        return False

    # Lisätään uusi käyttäjä tietokantaan
    sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()
    start_session(get_id(username))
    return True

# Tämä funktio hakee käyttäjän viimeisen kirjautumisen
def last_log(id):
    sql = "SELECT log FROM user_logs WHERE user_id=:id ORDER BY log LIMIT 1 OFFSET 1"
    result = db.session.execute(sql, {"id": id})
    if not result:
        return False
    return result.fetchone()[0]

# Tämä funktio poistaa profiilin sekä kaikki siihen liittyvät kommentit
def delete_account(id):
    if privileges(id):
        return False
    sql = "DELETE FROM reviews WHERE user_id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()

    sql = "DELETE FROM user_logs WHERE user_id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()
    
    sql = "DELETE FROM users WHERE id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()  
    return True


# Tämä funktio kertoo onko tietty käyttäjä admin 
def privileges(id):
    if not session.get("username"):
        return False
    sql = "SELECT privileges FROM users WHERE id=:id AND privileges=0"
    result = db.session.execute(sql, {"id": id})
    if result.fetchone():
        return True
    return False


# Tämä funktio kirjaa ylös kirjautumiset
def start_session(id):
    sql = "INSERT INTO user_logs (user_id, log) VALUES (:user_id, NOW())"
    db.session.execute(sql, {"user_id": id})
    db.session.commit()