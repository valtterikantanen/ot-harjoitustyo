import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_uuden_kassapaatteen_rahamaara_on_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_alussa_myytyja_edullisia_lounaita_on_nolla(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_alussa_myytyja_maukkaita_lounaita_on_nolla(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    # syo_edullisesti_kateisella-funktion testausta

    def test_syo_edullisesti_kateisella_palauttaa_oikean_vaihtorahan_kun_rahaa_on(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500), 260)

    def test_syo_edullisesti_kateisella_lisaa_oikean_maaran_rahaa_kassaan_kun_rahaa_on(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_syo_edullisesti_kateisella_lisaa_myytyjen_lounaiden_maaraa_kun_rahaa_on(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_edullisesti_kateisella_palauttaa_koko_summan_vaihtorahana_kun_ei_rahaa(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(100), 100)

    def test_syo_edullisesti_kateisella_ei_lisaa_rahaa_kassaan_kun_ei_rahaa(self):
        self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_syo_edullisesti_kateisella_ei_lisaa_myytyjen_lounaiden_maaraa_kun_ei_rahaa(self):
        self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.edulliset, 0)

    # syo_maukkaasti_kateisella-funktion testausta

    def test_syo_maukkaasti_kateisella_palauttaa_oikean_vaihtorahan_kun_rahaa_on(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)

    def test_syo_maukkaasti_kateisella_lisaa_oikean_maaran_rahaa_kassaan_kun_rahaa_on(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_syo_maukkaasti_kateisella_lisaa_myytyjen_lounaiden_maaraa_kun_rahaa_on(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_maukkaasti_kateisella_palauttaa_koko_summan_vaihtorahana_kun_ei_rahaa(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(200), 200)

    def test_syo_maukkaasti_kateisella_ei_lisaa_rahaa_kassaan_kun_ei_rahaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_syo_maukkaasti_kateisella_ei_lisaa_myytyjen_lounaiden_maaraa_kun_ei_rahaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    # syo_edullisesti_kortilla-funktion testausta

    def test_syo_edullisesti_kortilla_veloittaa_oikean_summan_kun_rahaa_on(self):
        mk = Maksukortti(1000)
        self.kassapaate.syo_edullisesti_kortilla(mk)
        self.assertEqual(str(mk), "saldo: 7.6")

    def test_syo_edullisesti_kortilla_palauttaa_true_kun_rahaa_on(self):
        mk = Maksukortti(1000)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(mk), True)

    def test_syo_edullisesti_kortilla_lisaa_myytyjen_lounaiden_maaraa_kun_rahaa_on(self):
        mk = Maksukortti(1000)
        self.kassapaate.syo_edullisesti_kortilla(mk)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_edullisesti_kortilla_ei_kasvata_kassan_rahamaaraa_kun_rahaa_on(self):
        mk = Maksukortti(1000)
        self.kassapaate.syo_edullisesti_kortilla(mk)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_syo_edullisesti_kortilla_veloittaa_oikean_summan_kun_ei_rahaa(self):
        mk = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(mk)
        self.assertEqual(str(mk), "saldo: 1.0")

    def test_syo_edullisesti_kortilla_palauttaa_false_kun_ei_rahaa(self):
        mk = Maksukortti(100)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(mk), False)

    def test_syo_edullisesti_kortilla_ei_lisaa_myytyjen_lounaiden_maaraa_kun_ei_rahaa(self):
        mk = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(mk)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_syo_edullisesti_kortilla_ei_kasvata_kassan_rahamaaraa_kun_ei_rahaa(self):
        mk = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(mk)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    # syo_maukkaasti_kortilla-funktion testausta

    def test_syo_maukkaasti_kortilla_veloittaa_oikean_summan_kun_rahaa_on(self):
        mk = Maksukortti(1000)
        self.kassapaate.syo_maukkaasti_kortilla(mk)
        self.assertEqual(str(mk), "saldo: 6.0")

    def test_syo_maukkaasti_kortilla_palauttaa_true_kun_rahaa_on(self):
        mk = Maksukortti(1000)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(mk), True)

    def test_syo_maukkaasti_kortilla_lisaa_myytyjen_lounaiden_maaraa_kun_rahaa_on(self):
        mk = Maksukortti(1000)
        self.kassapaate.syo_maukkaasti_kortilla(mk)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_maukkaasti_kortilla_ei_kasvata_kassan_rahamaaraa_kun_rahaa_on(self):
        mk = Maksukortti(1000)
        self.kassapaate.syo_maukkaasti_kortilla(mk)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_syo_maukkaasti_kortilla_veloittaa_oikean_summan_kun_ei_rahaa(self):
        mk = Maksukortti(200)
        self.kassapaate.syo_maukkaasti_kortilla(mk)
        self.assertEqual(str(mk), "saldo: 2.0")

    def test_syo_maukkaasti_kortilla_palauttaa_false_kun_ei_rahaa(self):
        mk = Maksukortti(200)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(mk), False)

    def test_syo_maukkaasti_kortilla_ei_lisaa_myytyjen_lounaiden_maaraa_kun_ei_rahaa(self):
        mk = Maksukortti(200)
        self.kassapaate.syo_maukkaasti_kortilla(mk)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_maukkaasti_kortilla_ei_kasvata_kassan_rahamaaraa_kun_ei_rahaa(self):
        mk = Maksukortti(200)
        self.kassapaate.syo_maukkaasti_kortilla(mk)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    # lataa_rahaa_kortille-funktion testausta

    def test_kortin_saldo_kasvaa_ladatessa_kun_summa_positiivinen(self):
        mk = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(mk, 1000)
        self.assertEqual(str(mk), "saldo: 20.0")

    def test_kassan_rahamaara_kasvaa_ladatessa_kun_summa_positiivinen(self):
        mk = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(mk, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 101000)

    def test_kortin_saldo_ei_muutu_ladatessa_kun_summa_negatiivinen(self):
        mk = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(mk, -1000)
        self.assertEqual(str(mk), "saldo: 10.0")

    def test_kassan_rahamaara_ei_muutu_ladatessa_kun_summa_negatiivinen(self):
        mk = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(mk, -1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)