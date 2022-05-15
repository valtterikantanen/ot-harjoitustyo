## Viikko 3

* Käyttäjä voi rekisteröityä sekä kirjautua sisään ja ulos
* Luotu sovellukselle tekstikäyttöliittymä
* Lisätty sovelluslogiikasta huolehtiva BudgetService-luokka
* Lisätty käyttäjien tietojen tallentamisesta vastaava UserRepository-luokka
* Testattu, että rekisteröityminen sekä kirjautuminen sisään ja ulos toimivat

## Viikko 4

* Käyttäjä voi lisätä ja tarkastella tapahtumia
* Käyttäjä voi lisätä ja poistaa kategorioita
* Lisätty tapahtumien tietojen tallentamisesta vastaava TransactionRepository-luokka
* Lisätty kategorioiden tallentamisesta vastaava CategoryRepository-luokka
* Testattu, että tapahtumien ja kategorioiden lisääminen ja listaaminen toimivat

## Viikko 5

* Aloitettu graafisen käyttöliittymän rakentaminen
* Testi- ja tuotantotietokannat erotettu toisistaan
* Korjattu vika, jossa tietokanta tyhjeni uudelleenkäynnistyksen yhteydessä
* Testattu lisää mm. rekisteröitymistä ja kategorioiden poistamista

## Viikko 6

* Saatettu graafinen käyttöliittymä ajan tasalle, eli kaikki nykyiset toiminnot ovat käytössä graafisessa käyttöliittymässä
* Korjattu lukuisia bugeja mm. syötteiden validointiin ja rekisteröitymiseen liittyen
* Lisätty käyttöliittymään virheilmoitukset virheellisistä syötteistä
* Muokattu tietokantaa niin, että jokaisella käyttäjällä on omat kategoriansa, jolloin yhden käyttäjän lisäämät tai poistamat kategoriat eivät suoraan vaikuta muihin käyttäjiin
* Lisätty mahdollisuus muokata ja poistaa jo lisättyjä tapahtumia
* Testattu, että kategorioiden poisto sekä tapahtumien muokkaus ja poisto toimivat odotetulla tavalla

## Viikko 7

* Lisätty mahdollisuus suodattaa päänäkymässä näkyviä menoja ajankohdan tai kategorian mukaan
* Korjattu pieniä virheitä mm. uuden tapahtuman lisäämisessä
* Viimeistelty graafisen käyttöliittymän ulkoasua