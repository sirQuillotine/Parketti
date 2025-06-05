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
