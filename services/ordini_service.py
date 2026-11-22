from exceptions import OrdineNonTrovatoError, PiattoNonDisponibileError
from models.ordine import Ordine, CHIUSO
from services.menu_service import MenuService
from services.tavoli_service import TavoliService



class OrdiniService:
    """Gestisce l'apertura, l'aggiornamento e la chiusura degli ordini sui tavoli."""

    def __init__(self, menu_service: MenuService, tavoli_service: TavoliService) -> None:
        """Riceve i servizi dipendenti e inizializza il registro ordini aperti e lo storico."""
        # 1. Memorizza i riferimenti ai servizi collaboratori nei relativi attributi d'istanza.        
        self.menu_service = menu_service
        self.tavoli_service = tavoli_service
        # 2. Inizializza la collezione per tracciare gli ordini 
        self._ordini_attivi: dict[int, Ordine] = {}
        # 3. Inizializza la collezione per conservare lo storico degli ordini chiusi.
        self._storico_ordini: list[Ordine] = []

    def apri_ordine(self, numero_tavolo: int) -> Ordine:
        """Occupa il tavolo e apre un nuovo ordine associato."""
        # 1. Recupera il tavolo tramite il servizio tavoli.
        tavolo = self.tavoli_service.trova(numero_tavolo)
        # 2. Occupa il tavolo PRIMA di creare l'ordine.
        tavolo.occupa()
        #    Se il tavolo è già occupato, solleverà l'errore bloccando l'operazione in modo atomico.
        # 3. Crea il nuovo ordine per quel tavolo.
        nuovo_ordine = Ordine(tavolo=tavolo)
        # 4. Registra l'ordine tra quelli aperti e restituiscilo.
        self._ordini_attivi[numero_tavolo] = nuovo_ordine
        return nuovo_ordine
    
    def ordine_aperto(self, numero_tavolo: int) -> Ordine:
        """Restituisce l'ordine aperto per il tavolo indicato o solleva OrdineNonTrovatoError."""
        tavolo = self.tavoli_service.trova(numero_tavolo)
        # 1. Cerca l'ordine corrispondente al numero del tavolo tra quelli aperti.
        if tavolo.numero not in self._ordini_attivi:
        # 2. Se non presente, solleva OrdineNonTrovatoError.
            raise OrdineNonTrovatoError(numero_tavolo=tavolo.numero)
        return self._ordini_attivi[tavolo.numero]

    def aggiungi_piatto(
        self,
        numero_tavolo: int,
        id_piatto: int,
        quantita: int = 1,
    ) -> Ordine:
        """Aggiunge un piatto all'ordine se esiste ed è disponibile."""
        # 1. Recupera l'ordine aperto del tavolo indicato.
        ordine = self.ordine_aperto(numero_tavolo)
        # 2. Recupera il piatto dal servizio menù tramite l'ID.
        piatto = self.menu_service.trova(id_piatto)
        # 3. Controlla che il piatto sia disponibile; se non lo è, solleva PiattoNonDisponibileError.
        if not piatto.disponibile:
            raise PiattoNonDisponibileError(nome_piatto=piatto.nome)
        # 4. Aggiungi il piatto all'ordine e restituisci l'ordine aggiornato.
        ordine.aggiungi(piatto, quantita)       
        return ordine

    def rimuovi_piatto(
        self,
        numero_tavolo: int,
        id_piatto: int,
        quantita: int | None = None,
    ) -> Ordine:
        """Rimuove porzioni o l'intero piatto dall'ordine."""
        # 1. Recupera l'ordine aperto del tavolo indicato.
        ordine = self.ordine_aperto(numero_tavolo)
        # 2. Rimuovi il piatto dall'ordine e restituisci l'ordine aggiornato.
        ordine.rimuovi(id_piatto, quantita)
        return ordine

    def chiudi_ordine(self, numero_tavolo: int) -> Ordine:
        """Chiude l'ordine, libera il tavolo, lo rimuove dagli aperti e lo archivia nello storico."""
        # 1. Recupera l'ordine aperto del tavolo indicato.
        ordine = self.ordine_aperto(numero_tavolo)
        # 2. Chiudi l'ordine (se l'ordine è vuoto solleverà eccezione e il tavolo rimarrà occupato).
        ordine.chiudi()
        # 3. Libera il tavolo associato all'ordine.
        self.tavoli_service.trova(numero_tavolo).libera()
        # 4. Rimuovi l'ordine da quelli aperti.
        self._ordini_attivi.pop(numero_tavolo)
        # 5. Archivia l'ordine nello storico e restituiscilo.
        self._storico_ordini.append(ordine)
        return ordine
        
    @property
    def storico(self) -> list[Ordine]:
        """Restituisce una copia della lista degli ordini chiusi."""
        # 1. Restituisci una copia della lista dello storico per proteggere la collezione interna.
        return [o for o in self._storico_ordini if o.stato == CHIUSO]

    def ordini_aperti(self) -> list[Ordine]:
        """Restituisce la lista di tutti gli ordini aperti al momento."""
        # 1. Restituisci la lista di tutti gli ordini attualmente in corso.
        return list(self._ordini_attivi.values()) 
    