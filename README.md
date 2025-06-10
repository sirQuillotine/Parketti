# Parketti

## Sovelluksen toiminnot
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tanssitapahtumia.
- Käyttäjä näkee sovellukseen lisätyt tapahtumat.
- Käyttäjä pystyy etsimään tapahtumia hakusanalla.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja käyttäjän lisäämistä tapahtumista ja osallistumisista.
- Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun tanssilajin mukaan.
- Käyttäjä pystyy ilmoittaa osallistuvansa tapahtumaan.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```

##Suuren tietomäärän käsittely

Tietokanta täytettiin seed.py tiedoston mukaisella tavalla. Sivutus tekee etusivun lataamisesta sujuvaa. Käyttäjäsivu kuitenkin hidastelee, koska tietokannasta haetaan käyttäjänimeä vastaavat tapahtumat sekä osallistumiset.

```
CREATE INDEX idx_event_participants ON event_participants (event_id);
CREATE INDEX idx_username ON events (username);
CREATE INDEX idx_username_part ON event_participants (username);
```
Käyttäjäsivun latausnopeus ennen indeksöintiä oli noin 0,22 sekuntia. Indesöinnin jälkeen latausnopeus oli 0,8 sekuntia. Etusivuun indeksöinti vaikutti sivutuksen jälkeen enää alle millisekuntin verran.