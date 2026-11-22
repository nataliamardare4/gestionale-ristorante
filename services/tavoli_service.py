from exceptions import TavoloNonTrovatoError
from models.tavolo import Tavolo

class TavoliService:
    """Gestisce la sala e lo stato di disponibilità dei tavoli."""

    def __init__(
        self,
        tavoli_iniziali: tuple[dict[str, int]] | list[dict[str, int]] | list[tuple[int, int]] | None = None,
    ) -> None:
        """Inizializza il dizionario dei tavoli e popola la sala dai dati iniziali."""
        # 1. Inizializza la collezione interna per memorizzare i tavoli 
        self._tavoli: dict[int, Tavolo] = {}
        # 2. Itera sui dati iniziali forniti (estraendo numero e posti)
        if tavoli_iniziali is not None:
            for item in tavoli_iniziali:
                numero = None
                posti = None
                if isinstance(item, dict):
                    numero=item.get("numero")
                    posti=item.get("posti")
                elif isinstance(item, (tuple, list)) and len(item) >= 2:
                    numero, posti = item[0], item[1]
                else:
                    continue
                # Istanzia il Tavolo (la validazione scatterà nel costruttore del Tavolo)
                tavolo = Tavolo(numero=numero, posti=posti)
                self._tavoli[tavolo.numero] = tavolo

    def elenco(self) -> list[Tavolo]:
        """Restituisce tutti i tavoli ordinati per numero crescente."""
        # 1. Restituisci la lista di tutti i tavoli ordinati per numero progressivo.
        return sorted(self._tavoli.values(), key=lambda t: t.numero)

    def trova(self, numero: int) -> Tavolo:
        """Restituisce il tavolo per numero o solleva TavoloNonTrovatoError."""
        # 1. Cerca il tavolo nella collezione interna tramite il numero identificativo.
        try:
            num_int = int(numero)
        except (ValueError, TypeError):
            raise TavoloNonTrovatoError(numero_tavolo=numero)
        # 2. Se non presente, solleva TavoloNonTrovatoError.
        if num_int not in self._tavoli:
            raise TavoloNonTrovatoError(numero_tavolo=num_int)
        return self._tavoli[num_int]

    def liberi(self) -> list[Tavolo]:
        """Restituisce l'elenco dei soli tavoli che risultano liberi."""
        # 1. Filtra e restituisci solo i tavoli della sala che risultano attualmente liberi.
        return [t for t in self.elenco() if t.libero] 


if __name__ == "__main__":
    servizio_tavoli = TavoliService([{"numero": 1, "posti": 2}, {"numero": 2, "posti": 4}])
    print("Liberi:", [t.numero for t in servizio_tavoli.liberi()])

