import random
import sqlite3

print("Seeding database...")
db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM events")
db.execute("DELETE FROM event_participants")

user_count = 1000
event_count = 10**5
participant_count = 100



content = '''Tanssi on taide- ja urheilumuoto, jossa ihminen liikuttaa vartaloaan, yleensä rytmikkäästi musiikin mukaan, tuottaakseen esteettisiä elämyksiä, huvitellakseen, sosiaalisena toimintana tai ilmaistakseen tanssillaan jotain. Tanssia voi nähdä myös uskonnollisissa ja muissa hengellisissä tilaisuuksissa. Toisaalta eräät uskonnolliset ryhmät suhtautuvat tanssiin torjuvasti ja pitävät sitä syntinä.

Tanssi voi olla joko ennakolta määrättyjen askelkuvioiden noudattamista taikka vapaata liikkumista, usein musiikin tahtiin. Askelkuviot liittyvät usein perinteisiin tansseihin kuten valssi, foxtrot ja poloneesi. Tanssi voi olla myös taiteellinen esitys, jolloin sillä on usein ennalta määrätty koreografia. Tanssiesitys voi myös perustua joko osin tai kokonaan improvisaatioon. Tanssin elementtejä käytetään myös poikkitaiteellisesti muun muassa teatterin, sirkustaiteen kuin erilaisten performanssienkin yhteydessä. Tanssia voidaan harrastaa pareittain, yksin, tai ryhmässä.'''


for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])
    
print("Users added!")

for i in range(1, event_count + 1):
    db.execute("INSERT INTO events (title, content, start_time, username) VALUES (?, ?, ?, ?)",
               ["event" + str(i), content, "2023-10-01", "user" + str(random.randint(1, user_count))])
    if i % 1000 == 0:
        print(f"Events added: {i}")
    for j in range(1, participant_count + 1):
        db.execute("INSERT INTO event_participants (event_id, username) VALUES (?, ?)", [i, "user" + str(random.randint(1, user_count))])



db.commit()
db.close()

print("Database seeded succesfully!")