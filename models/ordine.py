from exceptions import DatiNonValidiError, OrdineChiusoError, PiattoNonTrovatoError
from models.piatto import Piatto
from models.tavolo import Tavolo


APERTO: str = "aperto"
CHIUSO: str = "chiuso"


class RigaOrdine:
    """Una riga dello scontrino: conserva piatto, quantità e prezzo congelato."""

    def __init__(self, piatto: Piatto, quantita: int) -> None:
        """Memorizza il piatto, la quantità e congela piatto.prezzo."""
        # Valida che la quantità sia un intero positivo
        if not isinstance(quantita, int) or quantita <= 0:
            raise DatiNonValidiError(
                campo="quantita",
                valore_errato=quantita,
                motivo="La quantità ordinata deve essere un intero maggiore di zero."
            )
        # 1. Assegna il piatto e la quantità ai rispettivi attributi d'istanza.
        self.piatto = piatto
        self.quantita: int = quantita
        # 2. Salva il prezzo unitario del piatto in un apposito attributo d'istanza.
        self.prezzo_unitario = piatto.prezzo
        
    @property
    def subtotale(self) -> float:
        """Calcola prezzo_unitario * quantita arrotondato a 2 decimali."""
        # 1. Calcola il prezzo unitario moltiplicato per la quantità e arrotonda a due decimali il risultato.
        return round(self.prezzo_unitario * self.quantita, 2)

class Ordine:
    """Gestisce le righe d'ordine associate a un tavolo."""

    def __init__(self, tavolo: Tavolo) -> None:
        """Inizializza un ordine per il tavolo specificato in stato APERTO."""
        # 1. Salva il tavolo di riferimento nel relativo attributo d'istanza.
        self.tavolo: Tavolo = tavolo
        # 2. Inizializza la collezione delle righe d'ordine come lista vuota.
        self.righe: list[RigaOrdine] = []
        # 3. Imposta lo stato iniziale dell'ordine su aperto.
        self.stato: str = APERTO   

    def _verifica_modificabile(self) -> None:
        """Solleva OrdineChiusoError se lo stato dell'ordine è CHIUSO."""
        # 1. Controlla lo stato dell'ordine: se è chiuso, solleva OrdineChiusoError.
        if self.stato == CHIUSO:
            raise OrdineChiusoError(id_ordine=id(self))
        
    def _trova_riga(self, id_piatto: int|str) -> RigaOrdine | None:
        """Cerca una riga con il piatto specificato per ID, oppure restituisce None."""
        id_target = Piatto.normalizza_id(id_piatto)
        return next(
            (
                riga 
                for riga in self.righe
                if Piatto.normalizza_id(riga.piatto.id_piatto) == id_target
            ),
            None,
        )        
        
    def aggiungi(self, piatto: Piatto, quantita: int = 1) -> None:
        """Aggiunge una quantità di un piatto (se presente incrementa, altrimenti crea nuova riga)."""
        # 1. Verifica che l'ordine sia modificabile chiamando il controllo dedicato.
        self._verifica_modificabile() 
        # 2. Valida la quantità: se non è positiva, solleva DatiNonValidiError.
        if not isinstance(quantita, int) or quantita <= 0:
            raise DatiNonValidiError(
                campo="quantita",
                valore_errato=quantita,
                motivo="La quantità da aggiungere deve essere un intero positivo."
            )
        # 3. Cerca se il piatto è già presente tra le righe dell'ordine.
        riga_esistente = self._trova_riga(piatto.id_piatto)
        # 4. Se la riga esiste già incrementa la quantità, altrimenti crea una nuova riga d'ordine e aggiungila alla collezione.
        if riga_esistente is not None:
            riga_esistente.quantita += quantita
        else:
            nuova_riga = RigaOrdine(piatto, quantita)
            self.righe.append(nuova_riga)

    def rimuovi(self, id_piatto: int, quantita: int | None = None) -> None:
        """Rimuove porzioni o l'intera riga di un piatto dall'ordine."""        
        # 1. Verifica che l'ordine sia modificabile.
        self._verifica_modificabile()
        # 2. Cerca la riga corrispondente all'ID del piatto; se non presente, solleva PiattoNonTrovatoError.
        riga = self._trova_riga(id_piatto)
        if riga is None:
            raise PiattoNonTrovatoError(id_piatto=id_piatto)
        # 3. Se la quantità da togliere non è indicata oppure supera o eguaglia le porzioni presenti, rimuovi l'intera riga.
        if quantita is not None:
            if isinstance(quantita, bool) or not isinstance(quantita, int) or quantita <= 0:
                raise DatiNonValidiError(
                    campo="quantita",
                    valore_errato=quantita,
                    motivo="La quantità da rimuovere deve essere un intero positivo."
                )
        # 4. Se la quantità da togliere è minore o uguale a zero, solleva DatiNonValidiError.
        if quantita is None or quantita >= riga.quantita:
            self.righe.remove(riga)
        # 5. Negli altri casi decrementa la quantità della riga.
        else:
            riga.quantita -= quantita
            
    @property
    def totale(self) -> float:
        """Calcola la somma monetaria di tutti i subtotali delle righe."""
        # 1. Calcola la somma dei subtotali di ogni riga presente e arrotonda a due decimali il risultato.
        return round(sum(riga.subtotale for riga in self.righe), 2) #- > estrae il subtotale calcolato (prezzo unitario congelato × quantità)

    def chiudi(self) -> None:
        """Chiude l'ordine. Solleva eccezioni se già chiuso o se privo di righe."""
        # 1. Verifica che l'ordine sia modificabile.
        self._verifica_modificabile()
        # 2. Se l'ordine non ha alcuna riga, solleva DatiNonValidiError (non è consentito chiudere un ordine vuoto).
        if not self.righe:
            raise DatiNonValidiError(campo="righe", valore_errato=self.righe, motivo="Non e consentito chiudere un ordine vuoto")
        # 3. Aggiorna lo stato dell'ordine su chiuso.
        self.stato = CHIUSO

    def __str__(self) -> str:
        """Genera lo scontrino testuale dell'ordine con tutte le voci e il totale finale."""
        # Intestazione con identificativo tavolo e stato dell'ordine
        linee: list[str] = [f"--- Tavolo {self.tavolo.numero} ({self.stato}) ---"]
        # Per ogni riga d'ordine: quantità allineata a destra, nome piatto a sinistra, subtotale
        for riga in self.righe:
            linee.append(
                f"{riga.quantita:>2} x {riga.piatto.nome:<24} {riga.subtotale:>8.2f} €"
            )
        # Linea divisoria di 40 trattini
        linee.append("-" * 40)
        # Riga finale del totale complessivo
        linee.append(f"{'TOTALE':<29} {self.totale:>8.2f} €")
        return "\n".join(linee)


if __name__ == "__main__":
    tavolo = Tavolo(1, 4)
    ordine = Ordine(tavolo)
    piatto = Piatto(1, "Carbonara", "primo", 10.5)
    ordine.aggiungi(piatto, 2)
    print(ordine)
