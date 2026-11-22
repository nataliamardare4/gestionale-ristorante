from collections.abc import Iterator
from exceptions import DatiNonValidiError, PiattoNonTrovatoError
from models.piatto import Piatto


class Menu:
    """Collezione dei piatti del ristorante indicizzati per ID."""

    def __init__(self) -> None:
        """Inizializza una collezione vuota per i piatti."""
        # 1. Inizializza un dizionario nell'attributo d'istanza protetto (chiave: ID, valore: istanza del piatto).
        self._piatti: dict[str, Piatto] = {}
        
    def aggiungi(self, piatto: Piatto) -> None:
        """Aggiunge un piatto al menù. Solleva DatiNonValidiError se l'ID esiste già."""
        # 1. Controlla se l'ID del piatto è già presente nella collezione dei piatti.
        if piatto.id_piatto in self._piatti:  
        # 2. Se è già presente, solleva DatiNonValidiError.
            raise DatiNonValidiError(
                campo="id_piatto",
                valore_errato=piatto.id_piatto,
                motivo=f"Esiste gia un piatto con ID{piatto.id_piatto} nel menu."
            )
        # 3. Altrimenti memorizza il piatto nella collezione associandolo al suo ID.
        self._piatti[piatto.id_piatto] = piatto 

    def rimuovi(self, id_piatto: int) -> Piatto:
        """Rimuove e restituisce il piatto con l'ID specificato."""
        # Standardizziamo l'ID nel formato stringa a 3 cifre
        id_str = str(id_piatto).zfill(3)
        # 1. Recupera il piatto tramite il metodo di ricerca interno
        # (in questo modo riusi il controllo di esistenza).
        piatto_rimosso = self.trova(id_str)
        # 2. Rimuovi l'elemento dalla collezione interna.
        self._piatti.pop(id_str)
        # 3. Restituisci il piatto appena rimoss
        return piatto_rimosso

    def trova(self, id_piatto: int) -> Piatto:
        """Cerca un piatto per ID. Solleva PiattoNonTrovatoError se assente."""
        # 1. Cerca il piatto nella collezione interna tramite il suo identificativo.
        id_piatto_str = str(id_piatto).zfill(3)
        if id_piatto_str not in self._piatti:
            raise PiattoNonTrovatoError(id_piatto=id_piatto_str)
        # 2. Se non presente, intercetta l'errore e solleva l'eccezione 
        # di dominio PiattoNonTrovatoError.
        # restituisce l'oggetto Piatto pronto per essere usato
        return self._piatti[id_piatto_str]
    
    def tutti(self) -> list[Piatto]:
        """Restituisce una copia a lista di tutti i piatti."""
        # 1. Estrai e restituisci una nuova lista contenente tutti i piatti presenti.
        return list(self._piatti.values())

    def per_categoria(self, categoria: str) -> list[Piatto]:
        """Restituisce la lista dei piatti filtrati per categoria (case-insensitive)."""
        # 1. Normalizza la stringa della categoria ripulendola da spazi e convertendola in minuscolo.
        categoria_normalizzata = str(categoria).strip().lower()
        # 2. Filtra e restituisci la lista dei piatti corrispondenti.
        return [piatto for piatto in self._piatti.values() if piatto.categoria == categoria_normalizzata]

    def disponibili(self) -> list[Piatto]:
        """Restituisce solo i piatti attualmente disponibili."""
        # 1. Filtra e restituisci solo i piatti che risultano disponibili.
        return [piatto for piatto in self._piatti.values() if piatto.disponibile]

    def cerca(self, testo: str) -> list[Piatto]:
        """Restituisce i piatti il cui nome contiene 'testo' (case-insensitive)."""
        # 1. Normalizza il testo cercato in minuscolo.
        testo_normalizzato = str(testo.strip().lower())
        # 2. Filtra e restituisci i piatti il cui nome contiene la porzione di testo cercata.
        return [piatto for piatto in self._piatti.values() if testo_normalizzato in piatto.nome.lower()]

    def prossimo_id(self) -> int:
        """Restituisce il prossimo ID progressivo libero (max ID + 1, oppure 1 se vuoto)."""
        # 1. Calcola il massimo tra gli ID presenti maggiorato di 1.
        if not self._piatti:
            return 1
        # 2. Gestisce il caso in cui la collezione sia ancora vuota.
        id_numerici = [int(id_str) for id_str in self._piatti.keys()]
        return max(id_numerici) + 1

    def __len__(self) -> int:
        """Numero totale di piatti nel menù."""
        # 1. Restituisci il numero totale di piatti memorizzati nella collezione interna.
        return len(self._piatti)

    def __iter__(self) -> Iterator[Piatto]:
        """Iteratore sui piatti ordinati per ID crescente."""
        # 1. Ordina i piatti per ID crescente e restituisci il relativo iteratore per consentire il ciclo for.
        return iter(self._piatti[id_str] for id_str in sorted(self._piatti))  


if __name__ == "__main__":
    menu = Menu()
    menu.aggiungi(Piatto(1, "Margherita", "primo", 8.0))
    print("Totale piatti:", len(menu))
    print("Piatto 1:", menu.trova(1))




