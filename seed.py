import random
import sqlite3

print("Seeding database...")
db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM events")
db.execute("DELETE FROM event_participants")
db.execute("DELETE FROM styles")
db.execute("DELETE FROM event_styles")

USER_COUNT = 1000
EVENT_COUNT = 10**3
PARTICIPANT_COUNT = 100

styles = ["foksi", "fusku", "valssi", "jive", "samba", "tango"]


LOREMIPSUM = """Tanssi on taide- ja urheilumuoto, jossa ihminen liikuttaa vartaloaan,
 yleensä rytmikkäästi musiikin mukaan, tuottaakseen esteettisiä elämyksiä,
   huvitellakseen, sosiaalisena toimintana tai ilmaistakseen tanssillaan jotain.
     Tanssia voi nähdä myös uskonnollisissa ja muissa hengellisissä tilaisuuksissa.
       Toisaalta eräät uskonnolliset ryhmät suhtautuvat tanssiin torjuvasti ja pitävät sitä syntinä.

Tanssi voi olla joko ennakolta määrättyjen askelkuvioiden noudattamista taikka vapaata liikkumista,
 usein musiikin tahtiin. Askelkuviot liittyvät usein perinteisiin tansseihin kuten valssi,
   foxtrot ja poloneesi. Tanssi voi olla myös taiteellinen esitys,
     jolloin sillä on usein ennalta määrätty koreografia.
       Tanssiesitys voi myös perustua joko osin tai kokonaan improvisaatioon.
         Tanssin elementtejä käytetään myös poikkitaiteellisesti muun muassa teatterin,
           sirkustaiteen kuin erilaisten performanssienkin yhteydessä.
             Tanssia voidaan harrastaa pareittain, yksin, tai ryhmässä."""

for style in styles:
    db.execute("INSERT INTO styles (style) VALUES (?)", [style])
print("Styles added!")

for i in range(1, USER_COUNT + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

print("Users added!")
styles = ["foksi", "fusku", "valssi", "jive", "samba", "tango"]

for i in range(1, EVENT_COUNT + 1):
    db.execute("INSERT INTO events (title, content, start_time, username) VALUES (?, ?, ?, ?)",
               ["event" + str(i), LOREMIPSUM, "2023-10-01",
                 "user" + str(random.randint(1, USER_COUNT))])
    for style in random.sample(styles, random.randint(1, len(styles))):
        db.execute("INSERT INTO event_styles (event_id, style) VALUES (?, ?)", [i, style])
    if i % 1000 == 0:
        print(f"Events added: {i}")
    for j in range(1, PARTICIPANT_COUNT + 1):
        db.execute("INSERT INTO event_participants (event_id, username) VALUES (?, ?)",
                    [i, "user" + str(random.randint(1, USER_COUNT))])

db.commit()
db.close()

print("Database seeded succesfully!")
