# Vaatimusmäärittely

## Sovelluksen tarkoitus
Tavoitteena on luoda sovellus, jonka avulla käyttäjä voi seurata henkilökohtaista talouttaan. Seuranta tapahtuu pitämällä kirjaa tuloista ja menoista sekä tarkastelemalla kirjattuja tapahtumia joko tekstimuodossa tai graafisesti. Sovellukseen voi rekisteröityä useita käyttäjiä, jotka voivat seurata omia tapahtumiaan.

## Käyttäjät
Alussa sovelluksessa on vain yksi käyttäjätyyppi eli tavallinen käyttäjä. Tulevaisuudessa sovellukseen voi tulla mahdollisuus lisätä myös pääkäyttäjiä, joilla on laajemmat oikeudet.

## Toteutetut toiminnot

### Ennen kirjautumista

* Käyttäjä voi luoda järjestelmään uuden käyttäjätunnuksen
    * Käyttäjätunnus ei saa olla entuudestaan käytössä. Kirjautumista varten rekisteröitymisen yhteydessä tulee myös asettaa salasana.
* Jos käyttäjällä on olemassa oleva käyttäjätunnus, hän voi kirjautua sisään. Jos käyttäjätunnus ja salasana ovat oikein, kirjautuminen onnistuu. Muussa tapauksessa ohjelma antaa virheilmoituksen.

### Kirjautumisen jälkeen

Kirjautunut käyttäjä voi:

* lisätä uuden tapahtuman
    * Tapahtumaan liittyy tapahtumapäivä, tyyppi (meno vai tulo), summa, kategoria ja kuvaus.
* listata tapahtumat
    * Käyttäjä voi listata kaikki lisäämänsä tapahtumat.
* lisätä ja poistaa kategorioita
    * Kategorioiden tarkoitus on auttaa tapahtumien ryhmittelyssä. Sovelluksessa on valmiina ennalta asetettuja kategorioita (esim. *asuminen*, *ruoka ja päivittäistavarat*, *ajoneuvot ja liikenne*). Käyttäjä kuitenkin pystyy poistamaan sekä valmiita että itse luotuja kategorioita.
* kirjautua ulos.

## Tulevat toiminnot

Kirjautunut käyttäjä voi:

* poistaa tai muokata tapahtumia
    * Käyttäjä voi valita haluamansa tapahtuman ja muokata haluamiaan tietoja. Tapahtuman voi myös poistaa kokonaan. Vahinkojen minimoimiseksi käyttäjältä varmistetaan vielä ennen lopullista poistoa, haluaako hän todella poistaa tapahtuman.
* rajata tarkasteltavien tapahtumien määrää
    * Käyttäjä voi valita tietyn ajanjakson tai kategorian, johon kuuluvia tapahtumia hän haluaa tarkastella.
* tarkastella tapahtumia graafisesti
    * Listauksen lisäksi käyttäjä voi tarkastella tapahtumia myös graafisesti. Kuten listauksessa, hän voi tarkastella kaikkia tapahtumia tai jollakin kriteerillä valita osan niistä.

## Jatkokehitysideoita
Aikataulun salliessa sovellusta voidaan täydentää lisäämällä mm. seuraavia toimintoja:

* Pääkäyttäjän lisääminen
* Käyttäjätunnuksen tai salasanan vaihtaminen
* Useiden erillisten budjettien luominen samalle käyttäjälle