from models.ordine import Ordine
from services.ordini_service import OrdiniService


class ReportService:
    """Statistiche aggregate e report di vendita del ristorante."""
    # -> con la Dependency Injection e la separazione delle responsabilità:
    
    def __init__(self, ordini_service: OrdiniService) -> None:
        """Inizializza il servizio memorizzando il riferimento al servizio ordini."""
        # 1. Salva il riferimento al servizio ordini nell'apposito attributo d'istanza.
        self.ordine_service = ordini_service

    def _ordini(self) -> list[Ordine]:
        """Restituisce lo storico aggiornato degli ordini chiusi."""
        # 1. Recupera la lista aggiornata degli ordini chiusi interrogando il servizio ordini.
        return self.ordine_service.storico

    def incasso_totale(self) -> float:
        """Somma i totali di tutti gli ordini chiusi."""
        # 1. Calcola la somma dei totali di tutti gli ordini chiusi e arrotonda a due decimali il risultato.
        return round(sum((o.totale for o in self._ordini()), 0.0), 2)
    
    def scontrino_medio(self) -> float:
        """Importo medio per ordine chiuso (0.0 se non ci sono ordini nello storico)."""
        # 1. Recupera gli ordini chiusi dallo storico.
        ordini = self._ordini()
        if not ordini:
        # 2. Se non ci sono ordini, restituisci 0.0 per evitare la divisione per zero.
            return 0.0
        # 3. Altrimenti calcola l'incasso totale diviso per il numero di ordini e arrotonda a due decimali il risultato.
        else:
            return  round(self.incasso_totale() / len(ordini), 2)

    def incasso_per_categoria(self) -> dict[str, float]:
        """Dizionario categoria -> totale incassato, ordinato in modo decrescente."""
        # 1. Inizializza una struttura per accumulare gli incassi raggruppati per categoria.
        totali_per_categoria: dict[str, float] = {}
        # 2. Itera su ciascun ordine chiuso e sulle relative righe, accumulando i subtotali nella rispettiva categoria.
        for ordine in self._ordini():
            for riga in ordine.righe:
                categoria = riga.piatto.categoria
                totali_per_categoria[categoria] = (
                    totali_per_categoria.get(categoria, 0.0) + riga.subtotale
                ) 
        # 3. Ordina le categorie per incasso decrescente.
        ordinati = sorted(
            ((cat, round(totale, 2)) for cat, totale in totali_per_categoria.items()),
            key=lambda item: item[1],
            reverse=True,
        )
        # 4. Restituisci il dizionario con gli importi arrotondati a due decimali.
        return dict(ordinati)

    def quantita_per_piatto(self) -> dict[str, int]:
        """Dizionario nome_piatto -> totale porzioni vendute."""
        # 1. Inizializza una struttura per conteggiare le porzioni vendute per ciascun piatto.
        porzioni_vendute: dict[str, int] = {}
        # 2. Itera su tutti gli ordini chiusi e sulle rispettive righe, sommando le quantità per ciascun nome di piatto.
        for ordine in self._ordini():
            for riga in ordine.righe:
                nome_piatto = riga.piatto.nome
                porzioni_vendute[nome_piatto] = (
                    porzioni_vendute.get(nome_piatto, 0) + riga.quantita
                )
        # 3. Restituisci il dizionario delle quantità vendute.
        return porzioni_vendute

    def classifica_piatti(self, n: int = 3) -> list[tuple[str, int]]:
        """Restituisce le prime n posizioni di (nome_piatto, porzioni_vendute)."""
        if n <= 0:
            return []
        # 1. Ottieni il conteggio delle porzioni vendute per piatto.
        conteggio = self.quantita_per_piatto() 
        # 2. Ordina gli elementi per quantità venduta decrescente.
        ordinati = sorted(conteggio.items(), key=lambda item: item[1], reverse=True) 
        # 3. Estrai e restituisci i primi n elementi.
        return ordinati[:n]

    def piatto_piu_venduto(self) -> tuple[str, int] | None:
        """Restituisce la tupla del piatto più venduto, o None se non ci sono vendite."""
        # 1. Richiedi la classifica per il primo elemento.
        classifica = self.classifica_piatti(n=1)
        # -> Chiedendo solo n=1, se non ci sono ordini o piatti venduti ricevi []
        # 2. Se la classifica non è vuota restituisci il primo elemento, altrimenti restituisci None.
        if classifica:
            return classifica[0]
        return None
        
