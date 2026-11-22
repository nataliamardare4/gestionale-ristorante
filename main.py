"""Punto d'ingresso del gestionale ristorante."""

from cli.interfaccia import Interfaccia
from data.dati_iniziali import MENU, TAVOLI
from services.menu_service import MenuService
from services.ordini_service import OrdiniService
from services.report_service import ReportService
from services.tavoli_service import TavoliService


def main() -> None:
    """Inizializza i servizi, crea l'interfaccia e avvia il programma."""
    # 1. Istanzia il servizio menu e il servizio tavoli passando i rispettivi dati di avvio.
    menu_service = MenuService(MENU)
    tavoli_service = TavoliService(TAVOLI)
    # 2. Istanzia il servizio ordini iniettando i servizi menu e tavoli da cui dipende.
    ordini_service = OrdiniService(menu_service, tavoli_service)
    # 3. Istanzia il servizio report collegandolo al servizio ordini.
    report_service = ReportService(ordini_service)
    # 4. Istanzia l'interfaccia utente passando tutti i servizi necessari.
    interfaccia = Interfaccia(menu_service, tavoli_service, ordini_service, report_service)
    # 5. Avvia l'interfaccia utente.
    interfaccia.avvia()


if __name__ == "__main__":
    main()

