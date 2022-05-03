# Ohjelmistotekniikka-kurssin palautusrepositorio

Tämä repositorio on laadittu Helsingin yliopiston kevään 2022 kurssille **Ohjelmistotekniikka**, ja se täydentyy tulevien viikkojen aikana.

## Harjoitustyön kuvaus

Sovelluksen avulla käyttäjä voi seurata henkilökohtaista talouttaan. Seuranta tapahtuu pitämällä kirjaa tuloista ja menoista sekä tarkastelemalla kirjattuja tapahtumia joko tekstimuodossa tai graafisesti. Sovellukseen voi rekisteröityä useita käyttäjiä, jotka voivat seurata omia tapahtumiaan.

## Julkaisut (releaset)

* [Viikko 5](https://github.com/valtterikantanen/ot-harjoitustyo/releases/tag/viikko5)

* [Viikko 6](https://github.com/valtterikantanen/ot-harjoitustyo/releases/tag/viikko6)

## Dokumentaatio

* [Vaatimusmäärittely](https://github.com/valtterikantanen/ot-harjoitustyo/blob/master/dokumentaatio/vaatimusmaarittely.md)

* [Käyttöohje](https://github.com/valtterikantanen/ot-harjoitustyo/blob/master/dokumentaatio/kayttoohje.md)

* [Työaikakirjanpito](https://github.com/valtterikantanen/ot-harjoitustyo/blob/master/dokumentaatio/tuntikirjanpito.md)

* [Changelog](https://github.com/valtterikantanen/ot-harjoitustyo/blob/master/dokumentaatio/changelog.md)

* [Arkkitehtuurikuvaus](https://github.com/valtterikantanen/ot-harjoitustyo/blob/master/dokumentaatio/arkkitehtuuri.md)

## Asennus ja käyttö

Tarvittavien kirjastojen asentaminen
```
$ poetry install
```
Alustustoimenpiteiden suorittaminen
```
$ poetry run invoke build
```
Ohjelman suorittaminen
```
$ poetry run invoke start
```
Testien suorittaminen
```
$ poetry run invoke test
```
Testikattavuusraportin luominen
```
$ poetry run invoke coverage-report
```
Pylint-tarkistusten suorittaminen
```
$ poetry run invoke lint
```