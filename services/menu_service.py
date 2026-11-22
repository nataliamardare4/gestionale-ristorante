from models.menu import Menu
from models.piatto import Piatto


class MenuService:
    """Interfaccia operativa per il catalogo piatti del ristorante."""

    def __init__(
        self,
        piatti_iniziali: list[dict[str, str | float]] | list[tuple[str, str, float]] | None = None,
    ) -> None:
        """Inizializza il Menu interno e carica gli eventuali piatti iniziali."""
        # 1. Inizializza l'istanza del menù nel relativo attributo d'istanza protetto.
        self._menu: Menu = Menu()
        # 2. Se vengono forniti dati iniziali, itera sui record (estraendo nome, categoria/portata e prezzo)
        if piatti_iniziali is not None:
            for item in piatti_iniziali:
                if isinstance(item, dict):
                    categoria_val = item.get("categoria") if "categoria" in item else item.get("portata")
                    # Estrae i dati dal dizionario
                    piatto = Piatto(
                        id_piatto=item.get("id_piatto"),
                        nome=item.get("nome"),
                        categoria=categoria_val,
                        prezzo=item.get("prezzo"),
                        disponibile=item.get("disponibile", True)
                    )
                elif isinstance(item, tuple) and len(item) >= 3:
                    # Estrae i dati dalla tupla (es. (nome, categoria, prezzo))
                    piatto = Piatto(
                        id_piatto=None,
                        nome=item[0],
                        categoria=item[1],
                        prezzo=item[2]
                    )
                else:
                    continue  # Salta formati non riconosciuti
                #    e registrali nel menù richiamando il metodo di aggiunta.
                self._menu.aggiungi(piatto)

    def aggiungi_piatto(self, nome: str, categoria: str, prezzo: float) -> Piatto:
        """Crea un piatto con prossimo ID libero, lo registra e lo restituisce."""
        # 1. Richiedi al menù il prossimo identificativo progressivo disponibile.
        id_prossimo = self._menu.prossimo_id()
        # 2. Crea la nuova istanza di Piatto con i parametri forniti.
        nuovo_piatto = Piatto(
            id_piatto=id_prossimo,
            nome=nome,
            categoria=categoria,
            prezzo=prezzo,
            disponibile=True
        )
        # 3. Registra il piatto nel menù e restituisci l'oggetto creato.
        self._menu.aggiungi(nuovo_piatto)
        return nuovo_piatto
    
    def modifica_prezzo(self, id_piatto: int, nuovo_prezzo: float) -> Piatto:
        """Trova il piatto per ID e ne aggiorna il prezzo."""
        # 1. Individua il piatto tramite il suo ID.
        piatto = self._menu.trova(id_piatto)
        # 2. Aggiorna il prezzo del piatto (la validazione scatterà nella property).
        piatto.prezzo = nuovo_prezzo
        # 3. Restituisci il piatto aggiornato.
        return piatto

    def imposta_disponibilita(self, id_piatto: int, disponibile: bool) -> Piatto:
        """Trova il piatto per ID e ne modifica il flag disponibile."""
        # 1. Individua il piatto tramite il suo ID.
        piatto_trovato = self._menu.trova(id_piatto)
        # 2. Aggiorna lo stato di disponibilità del piatto.
        piatto_trovato.disponibile = disponibile
        # 3. Restituisci il piatto aggiornato.
        return piatto_trovato

    def rimuovi_piatto(self, id_piatto: int) -> Piatto:
        """Rimuove un piatto dal menù dato il suo identificativo."""
        # 1. Rimuovi il piatto delegando l'operazione al menù e restituisci il piatto rimosso.
        id_piatto_rimosso = self._menu.rimuovi(id_piatto)
        return id_piatto_rimosso
    
    def trova(self, id_piatto: int|str) -> Piatto: 
        """Trova un piatto per ID o solleva PiattoNonTrovatoError."""
        # 1. Delega la ricerca per ID al menù sottostante.
        return self._menu.trova(id_piatto)

    def elenco(self) -> list[Piatto]:
        """Restituisce la lista di tutti i piatti presenti a menù."""
        # 1. Delega al menù la restituzione di tutti i piatti.
        return self._menu.tutti()

    def per_categoria(self, categoria: str) -> list[Piatto]:
        """Filtra i piatti per categoria."""
        # 1. Delega al menù il filtro per categoria.
        return self._menu.per_categoria(categoria)

    def cerca(self, testo: str) -> list[Piatto]:
        """Cerca i piatti per sottostringa nel nome."""
        # 1. Delega al menù la ricerca per testo.
        return self._menu.cerca(testo)


if __name__ == "__main__":
    servizio_menu = MenuService([{"nome": "Pizza Margherita", "categoria": "primo", "prezzo": 8.0}])
    print("Piatti caricati:", len(servizio_menu.elenco()))
    
