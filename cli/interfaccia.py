from collections.abc import Callable #=> 
from cli.input_utils import (
    chiedi_conferma,
    chiedi_intero,
    chiedi_prezzo,
    chiedi_testo,
)
from exceptions import RistoranteError
from models.piatto import CATEGORIE
from services.menu_service import MenuService
from services.ordini_service import OrdiniService
from services.report_service import ReportService
from services.tavoli_service import TavoliService
from utils.formattatori import (
    formatta_classifica,
    formatta_euro,
    formatta_incassi,
    formatta_menu,
    formatta_tavoli,
    titolo,
)


class Interfaccia:
    """Menu interattivo a terminale del ristorante."""

    def __init__(
        self,
        menu_service: MenuService,
        tavoli_service: TavoliService,
        ordini_service: OrdiniService,
        report_service: ReportService,
    ) -> None:
        """Inietta i servizi applicativi."""
        # 1. Salva i quattro servizi nei relativi attributi d'istanza protetti.
        self._menu_service = menu_service
        self._tavoli_service = tavoli_service
        self._ordini_service = ordini_service
        self._report_service = report_service

    def _esegui(self, azione: Callable[[], None]) -> None:
        """Esegue un'azione catturando SOLO RistoranteError per stampare messaggi amichevoli."""
        # 1. Esegui l'azione all'interno di un blocco di protezione.
        
        r'''
        Se non ci fosse try ... except RistoranteError, quando l'utente prova un'operazione non consentita
        — per esempio aprire un ordine su un tavolo già occupato (TavoloOccupatoError) o aggiungere 
        un piatto esaurito (PiattoNonDisponibileError) — Python interromperebbe bruscamente il programma 
        stampando un traceback rosso e facendo crashare l'app
        '''
        # 2. Intercetta esclusivamente gli errori del dominio ristorante e mostra un messaggio amichevole all'utente.
        try:
            azione()
        except RistoranteError as e:
            print(f"\n[Attenzione] {e}")
        
        r'''
        Se facessi except Exception:, nasconderesti i bug reali del codice (come AttributeError 
        per un nome attributo sbagliato, TypeError per argomenti errati, KeyError o 
        ZeroDivisionError inattesi), facendo sembrare che sia un "normale errore dell'utente"
        quando invece il programma ha un difetto da sistemare. Intercettando solo RistoranteError 
        (e gestendo KeyboardInterrupt / EOFError in avvia() per un'uscita pulita con Ctrl+C / Ctrl+D), 
        gli errori di dominio vengono gestiti con garbo e i bug veri emergono chiaramente
        '''

    def _ciclo_menu(
        self,
        intestazione: str,
        voci: dict[str, tuple[str, Callable[[], None]]],
        etichetta_zero: str,
    ) -> None:
        """Visualizza un menu da un dizionario scelta -> (descrizione, callback) e smista la chiamata."""
        # 1. Avvia il ciclo del menu.
        while True:
            # 2. Mostra l'intestazione formattata e l'elenco delle opzioni con le descrizioni, includendo l'opzione di uscita con etichetta_zero.
            print(titolo(intestazione))
            for chiave, (descrizione, _) in voci.items():
                print(f" {chiave}. {descrizione}")
            print(f" 0. {etichetta_zero}")
            # 3. Acquisisci la scelta dell'utente.
            scelta = chiedi_testo("Scelta")
            # 4. Se l'utente seleziona "0", esci dal ciclo del menu corrente.
            if scelta == "0":
                break
            # 5. Se la scelta non appartiene alle voci previste, avvisa l'utente e richiedi nuovamente.
            voce = voci.get(scelta)
            if voce is None:
                print("\n[Attenzione] Scelta non valida. Riprova.")
                continue
            # 6. Altrimenti esegui in modo protetto la funzione associata alla voce selezionata.
            _, callable = voce 
            self._esegui(callable)
    def avvia(self) -> None:
        """Avvia il menu principale dell'applicazione gestendo l'uscita pulita con Ctrl+C / Ctrl+D."""
        # 1. Configura le voci del menu principale collegandole ai rispettivi sottomenu:
        voci_principali: dict[str, tuple[str, Callable[[], None]]] = {
            "1": ("Gestione Menu", self._menu_piatti),
            "2": ("Gestione Tavoli", self._menu_tavoli),
            "3": ("Gestione Ordini", self._menu_ordini),
            "4": ("Report e Statistiche", self._menu_report),
        }
        # 2. Avvia il ciclo del menu gestendo l'interruzione da tastiera per un'uscita pulita senza messaggi anomali.
        try:
            self._ciclo_menu("Gestionale Ristorante", voci_principali, "Esci")
        except (KeyboardInterrupt, EOFError):
            print("\nInterruzione rilevata.")
        # 3. Mostra un messaggio di saluto all'uscita.
        finally:
            print("\nArrivederci e buon lavoro!")

    # ==================================================================
    # SEZIONE MENÙ
    # ==================================================================
    def _menu_piatti(self) -> None:
        # 1. Configura le voci del sottomenu piatti e avvia il relativo ciclo di menu.
        voci: dict[str, tuple[str, Callable[[], None]]] = {
            "1": ("Visualizza menu completo", self._mostra_menu),
            "2": ("Filtra piatti per categoria", self._mostra_per_categoria),
            "3": ("Cerca piatto per nome", self._cerca_piatto),
            "4": ("Aggiungi nuovo piatto", self._aggiungi_piatto),
            "5": ("Modifica prezzo piatto", self._modifica_prezzo),
            "6": ("Cambia disponibilita piatto", self._cambia_disponibilita),
            "7": ("Rimuovi piatto", self._rimuovi_piatto),
        }
        self._ciclo_menu("Menu del Giorno", voci, "Torna al menu principale")

    def _mostra_menu(self) -> None:
        # 1. Recupera tutti i piatti dal servizio menù e mostrali formattati a video.
        piatti = self._menu_service.elenco()
        print(formatta_menu(piatti))

    def _mostra_per_categoria(self) -> None:
        # 1. Mostra all'utente le categorie disponibili.
        print(f"\nCategorie disponibili: {', '.join(CATEGORIE)}")
        # 2. Acquisisci la categoria desiderata.
        categoria = chiedi_testo("Categoria").lower()
        # 3. Recupera i piatti filtrati dal servizio menù e mostrali a video formattati.
        piatti = self._menu_service.per_categoria(categoria)
        print(formatta_menu(piatti))

    def _cerca_piatto(self) -> None:
        # 1. Acquisisci il testo da cercare.
        termine = chiedi_testo("Testo da cercare")
        piatti = self._menu_service.cerca(termine)
        # 2. Cerca i piatti tramite il servizio menù e mostrali a video formattati.
        print(formatta_menu(piatti))

    def _aggiungi_piatto(self) -> None:
        # 1. Acquisisci nome, categoria e prezzo del piatto usando le apposite funzioni di input.
        nome = chiedi_testo("Nome piatto")
        print(f"Categoria disponibili: {', '.join(CATEGORIE)}")
        categoria = chiedi_testo("Categoria").lower()
        prezzo = chiedi_prezzo("Prezzo")        
        # 2. Richiedi al servizio menù di aggiungere il piatto con i dati raccolti.
        piatto = self._menu_service.aggiungi_piatto(nome, categoria, prezzo)
        # 3. Mostra un messaggio di conferma con il piatto appena creato.
        print(f"\nPiatto aggiunto con successo: {piatto}")

    def _modifica_prezzo(self) -> None:
        # 1. Acquisisci l'identificativo del piatto e il nuovo prezzo.
        id_piatto = chiedi_intero("ID piatto", minimo=1)
        nuovo_prezzo = chiedi_prezzo("Nuovo prezzo")
        # 2. Richiedi al servizio menù di aggiornare il prezzo e mostra il piatto aggiornato.
        piatto = self._menu_service.modifica_prezzo(id_piatto, nuovo_prezzo)
        print(f"\nPrezzo aggiornato: {piatto}")

    def _cambia_disponibilita(self) -> None:
        # 1. Acquisisci l'identificativo del piatto e la nuova disponibilità.
        id_piatto = chiedi_intero("ID piatto", minimo=1)
        # 2. Richiedi al servizio menù di aggiornare la disponibilità e mostra la conferma.
        disponibile = chiedi_conferma("Impostare il piatto come disponibile?")
        piatto = self._menu_service.imposta_disponibilita(id_piatto, disponibile)
        stato = "disponibile" if disponibile else "non disponibile"
        print(f"\nDisponibilita aggiornata ({stato}): {piatto}")

    def _rimuovi_piatto(self) -> None:
        # 1. Acquisisci l'identificativo del piatto e chiedi conferma dell'operazione.
        id_piatto = chiedi_intero("ID piatto da rimuovere", minimo=1)
        # 2. Se confermato, richiedi al servizio menù la rimozione e mostra un messaggio di avvenuta cancellazione.
        if not chiedi_conferma("Confermi la rimozione del piatto?"):
            return
        self._menu_service.rimuovi_piatto(id_piatto)
        print(f"\nPiatto #{id_piatto} rimosso dal menu.")
        
    # ==================================================================
    # SEZIONE TAVOLI
    # ==================================================================
    def _menu_tavoli(self) -> None:
        # 1. Configura le voci per il sottomenu tavoli e avvia il relativo ciclo di menu.
        voci: dict[str, tuple[str, Callable[[], None]]] = {
            "1": ("Visualizza tutti i tavoli", self._mostra_tavoli),
            "2": ("Visualizza solo i tavoli liberi", self._mostra_tavoli_liberi)
        }
        self._ciclo_menu("Sala e Tavoli", voci, "Torna al menu principale")

    def _mostra_tavoli(self) -> None:
        # 1. Recupera tutti i tavoli dal servizio tavoli e mostrali a video formattati.
        tavoli = self._tavoli_service.elenco()
        print(formatta_tavoli(tavoli))

    def _mostra_tavoli_liberi(self) -> None:
        # 1. Recupera solo i tavoli liberi dal servizio tavoli e mostrali a video formattati.
        tavoli = self._tavoli_service.liberi()
        print(formatta_tavoli(tavoli))

    # ==================================================================
    # SEZIONE ORDINI
    # ==================================================================
    def _menu_ordini(self) -> None:
        # 1. Configura le voci per il sottomenu ordini e avvia il relativo ciclo di menu.
        voci: dict[str, tuple[str, Callable[[], None]]] = {
            "1": ("Apri ordine su tavolo", self._apri_ordine),
            "2": ("Aggiungi piatto a ordine", self._aggiungi_a_ordine),
            "3": ("Rimuovi piatto da ordine", self._togli_da_ordine),
            "4": ("Vedi conto / ordine di un tavolo", self._vedi_conto),
            "5": ("Chiudi e salda ordine", self._chiudi_ordine),
            "6": ("Mostra ordini aperti", self._mostra_ordini_aperti),
        }
        self._ciclo_menu("Gestione Ordini", voci, "Torna al menu principale")
        
    def _apri_ordine(self) -> None:
        # 1. Acquisisci il numero del tavolo.
        num_tavolo = chiedi_intero("Numero tavolo", minimo=1)
        # 2. Richiedi al servizio ordini di aprire un ordine per quel tavolo e mostra conferma.
        ordine = self._ordini_service.apri_ordine(num_tavolo)
        print(f"\nOrdine aperto per il tavolo {num_tavolo}: {ordine}")

    def _aggiungi_a_ordine(self) -> None:
        # 1. Acquisisci il numero del tavolo e mostra il menù per facilitare la scelta.
        num_tavolo = chiedi_intero("Numero tavolo", minimo=1)
        print(formatta_menu(self._menu_service.elenco()))
        id_piatto = chiedi_intero("ID piatto", minimo=1)
        # 2. Acquisisci l'identificativo del piatto e la quantità desiderata.
        quantita = chiedi_intero("Quantita", minimo=1)
        # 3. Aggiungi il piatto all'ordine tramite il servizio ordini e mostra il totale parziale formattato.
        ordine = self._ordini_service.aggiungi_piatto(num_tavolo, id_piatto, quantita)
        print(f"\nPiatto aggiunto. Totale parziale: {formatta_euro(ordine.totale)}")

    def _togli_da_ordine(self) -> None:
        # 1. Acquisisci il numero del tavolo, l'identificativo del piatto e quante porzioni 
        # togliere (indicando che 0 rimuove tutto).
        num_tavolo = chiedi_intero("Numero tavolo", minimo=1)
        id_piatto = chiedi_intero("ID piatto", minimo=1)
        quantita = chiedi_intero("Quantita da rimuover (0 = rimuove tutto)", minimo=0)
        # 2. Se l'utente indica 0 imposta la rimozione totale, altrimenti passa la quantità specificata.
        qta_arg = None if quantita == 0 else quantita
        ordine = self._ordini_service.rimuovi_piatto(num_tavolo, id_piatto, qta_arg)
        # 3. Richiedi la rimozione al servizio ordini e mostra il totale parziale aggiornato.
        print(f"\nAggiornamento eseguito. Totale parziale: {formatta_euro(ordine.totale)}")

    def _vedi_conto(self) -> None:
        # 1. Acquisisci il numero del tavolo.
        num_tavolo = chiedi_intero("Numero tavolo", minimo=1)
        # 2. Recupera l'ordine aperto del tavolo dal servizio ordini e stampalo a video.
        ordine = self._ordini_service.ordine_aperto(num_tavolo)
        print(f"\n{ordine}")

    def _chiudi_ordine(self) -> None:
        # 1. Acquisisci il numero del tavolo e mostra lo scontrino corrente.
        num_tavolo = chiedi_intero("Numero tavolo", minimo=1)
        ordine_corrente = self._ordini_service.ordine_aperto(num_tavolo)
        # 2. Chiedi conferma all'utente per procedere con la chiusura e il pagamento.
        print(f"\nConto corrente:\n{ordine_corrente}")
        if not chiedi_conferma("Conferma la chiusura e il pagamento dell'ordine?"):
            print("\nChiusura ordine annullata.")
            return
            # 3. Se confermato, chiudi l'ordine tramite il servizio ordini e mostra il totale incassato e la liberazione del tavolo.
        ordine_chiuso = self._ordini_service.chiudi_ordine(num_tavolo)
        print(
            f"\nOrdine chiuso! Totale incassato: {formatta_euro(ordine_chiuso.totale)}. "
            f"Il tavolo {num_tavolo} e ora libero."
        )

    def _mostra_ordini_aperti(self) -> None:
        # 1. Recupera la lista degli ordini aperti dal servizio ordini.
        aperti = self._ordini_service.ordini_aperti()
        # 2. Se non vi sono ordini aperti mostra un avviso, altrimenti stampa ciascun ordine.
        if not aperti:
            print("\nNessun ordine attualmente aperto.")
            return
        for ordine in aperti:
            print(f"\n{ordine}")

    # ==================================================================
    # SEZIONE REPORT
    # ==================================================================
    def _menu_report(self) -> None:
        # 1. Configura le voci del sottomenu report e avvia il relativo ciclo di menu.
        voci: dict[str, tuple[str, Callable[[], None]]] = {
            "1": ("Incasso totale", self._report_incasso),
            "2": ("Incassi per categoria", self._report_categorie),
            "3": ("Classifica primi 3 piatti", self._report_classifica),
            "4": ("Scontrino medio", self._report_medio),
        }
        self._ciclo_menu("Report e Statistiche", voci, "Torna al menu principale")
        
    def _report_incasso(self) -> None:
        # 1. Recupera l'incasso totale dal servizio report e stampalo formattato in euro.
        totale = self._report_service.incasso_totale()
        print(f"\nIncasso totale: {formatta_euro(totale)}")

    def _report_categorie(self) -> None:
        # 1. Recupera gli incassi per categoria dal servizio report e stampali formattati a video.
        incassi = self._report_service.incasso_per_categoria()
        print(f"\n{formatta_incassi(incassi)}")

    def _report_classifica(self) -> None:
        # 1. Recupera la classifica dei primi 3 piatti dal servizio report e stampala formattata a video.
        classifica = self._report_service.classifica_piatti(3)
        print(f"\n{formatta_classifica(classifica)}")

    def _report_medio(self) -> None:
        # 1. Recupera lo scontrino medio dal servizio report e stampalo formattato in euro.
        medio = self._report_service.scontrino_medio()
        print(f"\nScontrino medio: {formatta_euro(medio)}")
