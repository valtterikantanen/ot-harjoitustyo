# Vaatimusmäärittely

## Sovelluksen tarkoitus

Tavoitteena on luoda sovellus, jonka avulla käyttäjä voi seurata henkilökohtaista talouttaan. Seuranta tapahtuu pitämällä kirjaa tuloista ja menoista sekä tarkastelemalla kirjattuja tapahtumia joko tekstimuodossa tai graafisesti. Sovellukseen voi rekisteröityä useita käyttäjiä, jotka voivat kukin seurata omia tapahtumiaan.

## Käyttäjät

Sovelluksessa on vain yksi käyttäjätyyppi eli tavallinen käyttäjä.

## Toteutetut toiminnot

### Ennen kirjautumista

* Käyttäjä voi luoda järjestelmään uuden käyttäjätunnuksen
    * Käyttäjätunnus ei saa olla entuudestaan käytössä. Kirjautumista varten rekisteröitymisen yhteydessä tulee myös asettaa salasana.
* Jos käyttäjällä on olemassa oleva käyttäjätunnus, hän voi kirjautua sisään. Jos käyttäjätunnus ja salasana ovat oikein, kirjautuminen onnistuu. Muussa tapauksessa ohjelma antaa virheilmoituksen.

### Kirjautumisen jälkeen

Kirjautunut käyttäjä voi:

* lisätä uuden tapahtuman
    * Tapahtumaan liittyy tapahtumapäivä, tyyppi (meno vai tulo), summa, kategoria ja vapaaehtoinen kuvaus.
* listata tapahtumat
    * Käyttäjä voi listata kaikki lisäämänsä tapahtumat. Hän voi myös suodattaa tapahtumia ajankohdan tai kategorian mukaan.
* poistaa tai muokata tapahtumia
    * Käyttäjä voi valita haluamansa tapahtuman ja muokata haluamiaan tietoja. Tapahtuman voi myös poistaa kokonaan. Vahinkojen minimoimiseksi käyttäjältä varmistetaan vielä ennen lopullista poistoa, haluaako hän todella poistaa tapahtuman.
* tarkastella, lisätä ja poistaa kategorioita
    * Kategorioiden tarkoitus on auttaa tapahtumien ryhmittelyssä. Sovelluksessa on valmiina ennalta asetettuja kategorioita (esim. *asuminen*, *ruoka ja päivittäistavarat*, *ajoneuvot ja liikenne*). Käyttäjä kuitenkin pystyy poistamaan sekä valmiita että itse luotuja kategorioita.
* kirjautua ulos.

## Jatkokehitysideoita

Tulevaisuudessa sovellusta voidaan täydentää lisäämällä esimerkiksi seuraavia toimintoja:

* Laajemmat oikeudet omaavan pääkäyttäjän lisääminen
* Käyttäjätunnuksen tai salasanan vaihtaminen
* Useiden erillisten budjettien luominen samalle käyttäjälle
* Tapahtumien tarkastelu graafisesti esim. pylväs- ja ympyrädiagrammien avulla