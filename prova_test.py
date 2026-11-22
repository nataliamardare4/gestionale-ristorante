from unittest.mock import patch

from cli.input_utils import chiedi_conferma, chiedi_intero, chiedi_prezzo, chiedi_testo
from cli.interfaccia import Interfaccia
from exceptions import (
    DatiNonValidiError,
    OrdineChiusoError,
    OrdineNonTrovatoError,
    PiattoNonDisponibileError,
    PiattoNonTrovatoError,
    TavoloOccupatoError,
)
from models.ordine import Ordine
from models.piatto import Bevanda, Piatto
from models.tavolo import Tavolo
from services.menu_service import MenuService
from services.ordini_service import OrdiniService
from services.report_service import ReportService
from services.tavoli_service import TavoliService
from utils.formattatori import formatta_menu


def test_menu_service() -> None:
    ms = MenuService([("Carbonara", "primo", 12.0), ("Tiramisu", "dolce", 6.5)])
    piatti_iniziali = ms.elenco()
    id_primo = piatti_iniziali[0].id_piatto
    id_dolce = piatti_iniziali[1].id_piatto

    p_nuovo = ms.aggiungi_piatto("Lasagna", "primo", 13.0)

    assert len(ms.elenco()) == 3
    assert ms.trova(id_primo).nome == "Carbonara"
    assert ms.trova(int(id_primo)).nome == "Carbonara"

    ms.modifica_prezzo(id_primo, 14.0)
    assert ms.trova(id_primo).prezzo == 14.0

    ms.imposta_disponibilita(id_dolce, False)
    assert ms.trova(id_dolce).disponibile is False
    assert len(ms.per_categoria("primo")) == 2
    assert len(ms.cerca("lasag")) == 1

    ms.rimuovi_piatto(p_nuovo.id_piatto)
    assert len(ms.elenco()) == 2

    try:
        ms.trova(999)
        raise AssertionError("Doveva sollevare PiattoNonTrovatoError")
    except PiattoNonTrovatoError:
        pass

    try:
        ms.modifica_prezzo(id_primo, -3.0)
        raise AssertionError("Doveva sollevare DatiNonValidiError")
    except DatiNonValidiError:
        pass

    print("OK test_menu_service")


def test_formattazione_menu() -> None:
    piatti = [
        Piatto(1, "Carbonara", "primo", 12.0),
        Piatto(2, "Tiramisu", "dolce", 6.0),
        Bevanda(3, "Acqua naturale", 2.5, alcolica=False),
        Piatto(4, "Lasagna", "primo", 13.5),
    ]
    testo = formatta_menu(piatti)
    assert "[BEVANDA]" in testo
    assert "Carbonara" in testo
    print("OK test_formattazione_menu")


def test_modelli_piatto_e_ordine() -> None:
    assert Piatto.normalizza_id(1) == "001"
    assert Piatto.normalizza_id("7") == "007"
    assert Piatto.normalizza_id("012") == "012"

    for bad_id in ("abc", 0, -2, True):
        try:
            Piatto.normalizza_id(bad_id)
            raise AssertionError(f"ID non valido accettato: {bad_id!r}")
        except DatiNonValidiError:
            pass

    ordine = Ordine(Tavolo(1, 4))
    piatto = Piatto(1, "Pasta", "primo", 10.0)
    ordine.aggiungi(piatto, 3)
    ordine.rimuovi(1, 1)
    assert ordine.righe[0].quantita == 2

    for bad_qta in (0, -1, True):
        try:
            ordine.rimuovi(1, bad_qta)
            raise AssertionError(f"Quantità non valida accettata: {bad_qta!r}")
        except DatiNonValidiError:
            pass

    ordine.rimuovi(1)
    assert len(ordine.righe) == 0
    print("OK test_modelli_piatto_e_ordine")


def test_ordini_e_report_service() -> None:
    ms = MenuService([("Carbonara", "primo", 12.0), ("Tiramisu", "dolce", 6.0), ("Acqua", "bevanda", 3.0)])
    ts = TavoliService([(1, 4), (2, 2)])
    os_srv = OrdiniService(ms, ts)
    rs = ReportService(os_srv)

    piatti_menu = ms.elenco()
    id_primo = piatti_menu[0].id_piatto
    id_dolce = piatti_menu[1].id_piatto
    id_bevanda = piatti_menu[2].id_piatto

    assert rs.incasso_totale() == 0.0
    assert rs.scontrino_medio() == 0.0
    assert rs.piatto_piu_venduto() is None
    assert rs.classifica_piatti(3) == []

    try:
        os_srv.ordine_aperto(1)
        raise AssertionError("Doveva sollevare OrdineNonTrovatoError")
    except OrdineNonTrovatoError:
        pass

    os_srv.apri_ordine(1)
    assert len(os_srv.ordini_aperti()) == 1

    try:
        os_srv.apri_ordine(1)
        raise AssertionError("Doveva sollevare TavoloOccupatoError")
    except TavoloOccupatoError:
        pass

    try:
        os_srv.chiudi_ordine(1)
        raise AssertionError("Doveva sollevare DatiNonValidiError su ordine vuoto")
    except DatiNonValidiError:
        pass

    os_srv.aggiungi_piatto(1, id_primo, 2)
    os_srv.aggiungi_piatto(1, id_dolce, 1)
    os_srv.rimuovi_piatto(1, id_primo, 1)
    ordine_1 = os_srv.chiudi_ordine(1)
    assert ordine_1.totale == 18.0
    assert len(os_srv.ordini_aperti()) == 0
    assert len(os_srv.storico) == 1
    assert ts.trova(1).libero is True

    try:
        ordine_1.aggiungi(ms.trova(id_bevanda), 1)
        raise AssertionError("Doveva sollevare OrdineChiusoError")
    except OrdineChiusoError:
        pass

    ms.imposta_disponibilita(id_bevanda, False)
    os_srv.apri_ordine(2)
    try:
        os_srv.aggiungi_piatto(2, id_bevanda, 1)
        raise AssertionError("Doveva sollevare PiattoNonDisponibileError")
    except PiattoNonDisponibileError:
        pass

    ms.imposta_disponibilita(id_bevanda, True)
    os_srv.aggiungi_piatto(2, id_primo, 3)
    os_srv.aggiungi_piatto(2, id_bevanda, 2)
    os_srv.chiudi_ordine(2)

    assert rs.incasso_totale() == 60.0
    assert rs.scontrino_medio() == 30.0
    assert rs.quantita_per_piatto()["Carbonara"] == 4
    assert rs.piatto_piu_venduto() == ("Carbonara", 4)
    assert rs.incasso_per_categoria() == {"primo": 48.0, "dolce": 6.0, "bevanda": 6.0}
    assert rs.classifica_piatti(2) == [("Carbonara", 4), ("Acqua", 2)]
    print("OK test_ordini_e_report_service")


def test_input_utils() -> None:
    with patch("builtins.input", side_effect=["   ", "  Carbonara  "]):
        assert chiedi_testo("Nome piatto") == "Carbonara"

    with patch("builtins.input", side_effect=["abc", "0", "10", "4"]):
        assert chiedi_intero("Posti tavolo", minimo=1, massimo=8) == 4

    with patch("builtins.input", side_effect=["ciao", "0", "-5", "12,5"]):
        assert chiedi_prezzo("Prezzo") == 12.5

    with patch("builtins.input", side_effect=["forse", "SÌ"]):
        assert chiedi_conferma("Confermi") is True

    with patch("builtins.input", side_effect=["no"]):
        assert chiedi_conferma("Confermi") is False

    print("OK test_input_utils")


def test_interfaccia_navigazione() -> None:
    ms = MenuService([("Carbonara", "primo", 12.0)])
    ts = TavoliService([(1, 4)])
    os_srv = OrdiniService(ms, ts)
    rs = ReportService(os_srv)
    cli = Interfaccia(ms, ts, os_srv, rs)

    with patch("builtins.input", side_effect=["1", "1", "0", "0"]):
        cli.avvia()

    print("OK test_interfaccia_navigazione")


if __name__ == "__main__":
    test_menu_service()
    test_formattazione_menu()
    test_modelli_piatto_e_ordine()
    test_ordini_e_report_service()
    test_input_utils()
    test_interfaccia_navigazione()
    print("TUTTI I TEST COMPLETATI CON SUCCESSO!")