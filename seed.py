import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM events")
db.execute("DELETE FROM event_participants")

user_count = 1000
event_count = 10**5
participant_count = 1000

print("1")

content = '''Tanssi on taide- ja urheilumuoto, jossa ihminen liikuttaa vartaloaan, yleensä rytmikkäästi musiikin mukaan, tuottaakseen esteettisiä elämyksiä, huvitellakseen, sosiaalisena toimintana tai ilmaistakseen tanssillaan jotain. Tanssia voi nähdä myös uskonnollisissa ja muissa hengellisissä tilaisuuksissa. Toisaalta eräät uskonnolliset ryhmät suhtautuvat tanssiin torjuvasti ja pitävät sitä syntinä.

Tanssi voi olla joko ennakolta määrättyjen askelkuvioiden noudattamista taikka vapaata liikkumista, usein musiikin tahtiin. Askelkuviot liittyvät usein perinteisiin tansseihin kuten valssi, foxtrot ja poloneesi. Tanssi voi olla myös taiteellinen esitys, jolloin sillä on usein ennalta määrätty koreografia. Tanssiesitys voi myös perustua joko osin tai kokonaan improvisaatioon. Tanssin elementtejä käytetään myös poikkitaiteellisesti muun muassa teatterin, sirkustaiteen kuin erilaisten performanssienkin yhteydessä. Tanssia voidaan harrastaa pareittain, yksin, tai ryhmässä.

Tanssin määritelmään vaikuttavat sosiaaliset, kulttuuriset, esteettiset ja moraaliset määritelmät ja rajat. Tanssina voidaan pitää niin kuviokelluntaa kuin kamppailulajien harrastajien kata-liikesarjoja. Amerikkalainen antropologi Judith Lynne Hanna määrittelee tanssin olevan "ihmisen käyttäytymistä, joka tanssijan näkökulmasta koostuu merkityksellisistä, harkitusti rytmitetyistä ja kulttuurin muokkaamista sanattomien ruumiinliikkeiden jaksoista, jotka poikkeavat tavallisista liiketoiminnoista siinä, että liikkumiseen on sisäinen ja esteettinen tarve".[1]

Eläimillä tanssi voi olla osa pariutumisrituaalia, mehiläiset ovat tunnettuja tanssistaan, jolla kertovat muille pesän mehiläisille mistä löytyy mettä. Kurkien soidintanssi on erityisen komeaa katsottavaa. Tanssiksi voidaan myös kutsua esimerkiksi tuulen aikaansaamaa liikettä puiden lehdissä ja muissa kasveissa. Tällöin liikkeestä käytetään ilmaisua kuvaannollisesti. Tiettyjä musiikkityylejä kutsutaan erityisesti tanssimusiikiksi.'''




db.commit()
db.close()