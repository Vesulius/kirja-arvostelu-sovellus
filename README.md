# kirja-arvostelu-sovellus
**Tämä on Helsingin yliopiston Aineopintojen harjoitustyö: Tietokantasovellus (TKT 20011) kurssin harjoitustyö.**

Tavoitteena on ottaa inspiraatiota esimerkkinä olleesta ravintola-arviot sovelluksesta sekä Steam – videopelien jakelualustasta. Tarkoituksena on siis luoda sovellus, jossa käyttäjät voivat arviodia kirjoja sekä etsiä kirjoja muiden käyttäjien arvioiden perusteella. 

Eli käyttäjät voivat arvioida kirjoja numeroasteikolla sekä kirjottaa arvostelun. Tämän lisäksi käyttäjät voivat liittää kirjoihin tiettyjä tagejä, joita voidaan käyttää kirjojen hakuprosessissa. Näitä tägejä voisi olla eri genrejä kuten fantasia, kauhu tai muuta kuvausta kirjasta kuten klassikko tms.

Kirjoja pystyy sitten hakemaan kirjailian, kirjan nimen, kirjan saamien arvioitien sekä käyttäjien antamien tagien mukaan. Näitä eri hakumenetelmiä voi sitten yhdistellä. Esim. Stephen Kingin kauhu-genren kirjat arviointijärjestyksen mukaan.

Sovellukseen tehdään käyttäjätili jossa nimi ja salasana. Käyttäjiä on peruskäyttäjiä jotka voivat arvioida kirjoja ja ylläpitäjiä, jotka voivat myös lisää ja poistaa kirjoja. Peruskäyttäjät voivat poistaa omia arviostelujaan ja ylläpitäjät kaikkia arvosteluja.

Käytetyt tietokantataulut olisivat ainakin

    1. kirjat -taulu jossa nimi, id, kirjailija (tämä sarake saatetaan muuttaa omaksi tauluksi)
    2. käyttäjät -taulu jossa nimi, id, salasana
    3. nimeriset arviot -taulu jossa käyttäjien antamat numerot, kirjan id, arvostelijan id.
    4. Teksti arviot -taulu jossa käyttäjien kirjoittamat arvostelut, kirjan id, käyttäjän id
    5. tagit -taulu jossa käyttäjien antamat tägit, kirjan id, käyttäjän id
    
Muita mahdollisia ominaisuuksia

    1. Mahdollisuus kommentoida ja arvioida muiden kirjoittamia arviointeja
    2. Käyttäjien profiileille pisteytys arvioitujen kirjojen määrän perusteella
    3. Amazon -verkkosivun käyttämä systeemi jossa käyttäjien tekstiarvosteluista nostetaan avainsanat


---


## Välipalautus 2

Tämä palautus tuli hieman kiirellä joten osa sovelluksen ominaisuuksista on vielä välivaiheessa. Kuitenkin tämänhetkinen tilanne on pohja tulevia ominaisuuksia varten.

Sovelluksella voi:

	1. Luoda käyttäjä ja kirjautua sisään
	2. Hakea kirjoja kirjan tai kirjailijan nimen perusteella
	3. Lisää kommentti ja arvosana kirjaan

Koodissa itsessään on kommentoitu näiden ominaisuuksien puutteita.

Ohjelmaa voi testata luoamalla käyttäjätunnuksen sekä hakemalla kirjoja. Ainoat lisätyt kirjat ovat harry potter sarjaa.
Sivustolle pääsee osoitteesta https://tsoha-book-rewiew.herokuapp.com.


---


## Välipalautus 3

Tässä palautuksessa paranneltiin toimintoja ja selkeytettiin nettisivulla selaamista.

Uudet ominaisuudet ovat:

    1. Käyttäjillä on oma profiilisivu johon pääsee etusivun yläosan linkistä 'Käyttäjän session.username profiili'
    2. Profiilisivulla näkyy omat arviot ja niiden määrä. Tällä sivulla voi poistaa arvioita sekä profiili.
    3. Jos on kirjautunut admin-käyttäjänä, niin profiilisivulla voi myös lisää kirjoja
    4. Admin käyttäjänä voi myös poistaa kirjoja hakemalla niitä yleisestä hausta

Ohjelmaa voi testata luoamalla käyttäjätunnuksen sekä hakemalla kirjoja. Ainoat lisätyt kirjat ovat harry potter sarjaa.
Sivustolle pääsee osoitteesta https://tsoha-book-rewiew.herokuapp.com. 

Admin-profiilin käyttäjätunnus on 'harryfani2000' ja salasana 'harry2000'. Tätä käyttäjää ei pysty poistaa että kokeile vaan.


---


## Viimeinen palautus

Tässä palautuksessa viimeisteltiin sivun ulkonäköä ja paikattiin pieniä virheilmoituksa. Ulkoasua paranneltiin käyttämällä Bootstrap-kirjastoa
joka olikin jo käytössä etu- ja profiilisivulla. 

Ohjelmaa voi testata luoamalla käyttäjätunnuksen sekä hakemalla kirjoja. Ainoat lisätyt kirjat ovat harry potter sarjaa.
Sivustolle pääsee osoitteesta https://tsoha-book-rewiew.herokuapp.com. 

Admin-profiilin käyttäjätunnus on 'harryfani2000' ja salasana 'harry2000'. Tätä käyttäjää ei pysty poistaa että kokeile vaan.

