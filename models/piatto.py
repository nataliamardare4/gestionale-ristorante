from typing import Literal, get_args
from exceptions import DatiNonValidiError
Categoria = Literal["antipasto", "primo", "secondo", "dolce", "bevanda"]
CATEGORIE: tuple[str, ...] = get_args(Categoria)

class Piatto:
    """Rappresenta un piatto del menù con validazione interna dei campi."""
    # Contatore di classe per generare ID automatici progressivi
    _contatore = 1

    def __init__(
        self,
        id_piatto: int,
        nome: str,
        categoria: Categoria,
        prezzo: float,
        disponibile: bool = True,
    ) -> None:
        """Inizializza un piatto assegnando i campi attraverso le relative property."""
        if id_piatto is None:
            self.id_piatto = Piatto.normalizza_id(Piatto._contatore)
            Piatto._contatore += 1  # Incrementa per il prossimo piatto
        else:           
            self.id_piatto = Piatto.normalizza_id(id_piatto)
        self.nome = nome
        self.categoria = categoria
        self._prezzo = prezzo 
        self.disponibile = disponibile 
        
    @property
    def nome(self) -> str:
        """Restituisce il nome del piatto."""
        return self._nome 

    @nome.setter
    def nome(self, valore: str) -> None:
        """Valida e imposta il nome (stringa non vuota dopo lo strip)."""
        # 1. Converti il valore in stringa e ripuliscilo dagli spazi periferici.
        valore_pulito = str(valore).strip()
        
        # 2. Se la stringa risultante è vuota, solleva DatiNonValidiError.
        if not valore_pulito:
            raise DatiNonValidiError(
                campo="nome", 
                valore_errato=valore, 
                motivo="Il nome del piatto non può essere vuoto."
            )
        
        # 3. Assegna il valore al relativo attributo d'istanza protetto.
        self._nome = valore_pulito

    @property
    def categoria(self) -> str:
        """Restituisce la categoria del piatto in minuscolo."""
        return self._categoria

    @categoria.setter
    def categoria(self, valore: Literal[Categoria]) -> None:
        """Valida e imposta la categoria (deve appartenere alla tupla CATEGORIE)."""
        # 1. Rimuovi spazi e converti in caratteri minuscoli.
        valore_pulito = str(valore).strip().lower()
        # 2. Controlla se il valore appartiene alle categorie 
        # ammesse; altrimenti solleva DatiNonValidiError.
        if valore_pulito not in CATEGORIE:
            raise DatiNonValidiError(
                campo="categoria",
                valore_errato =valore,
                motivo=f"Categoria non valida. Scegli tra: {CATEGORIE}"
            )
        # 3. Assegna il valore al relativo attributo d'istanza protetto.
        self._categoria = valore_pulito

   
        '''
        i prezzi non si salvano mai come float, ma si salvano come (int) 
        rappresentando i centesimi (es. 10 euro diventano 1000 centesimi).
        Perché i computer gestiscono i float con una approssimazione
        In un ristorante accumulando arrotondamenti di centesimi, si 
        rischierebbe di ritrovarsi con conti sballati!
        Memorizzarli come interi in centesimi azzera completamente questo rischio.
        '''
        
    @property 
    def prezzo(self) -> float:
        '''Restituisce il prezzo unitario del piatto'''
        return self._prezzo
    @prezzo.setter 
    def prezzo(self, valore:float) -> None:
        '''Valida e imposta il prezzo (deve essere un numero maggiore di zero)'''
        if isinstance(valore, bool) or not isinstance(valore, (int, float)) or valore <= 0:
            raise DatiNonValidiError(
                campo="prezzo",
                valore_errato=valore,
                motivo="Il prezzo deve essere un numero maggiore di zero"
            )
        self._prezzo = float(valore)
        
        '''
        Senza setter, potresti assegnare per sbaglio 0, un numero negativo (-5.0) o 
        un tipo non numerico (oppure un bool, che in Python è sottoclasse di int!
        '''
    
    @staticmethod
    def normalizza_id(valore: int | str)-> str:
        '''Valida e Formatta l'ID del piatto come stinga a 3 cifre (es. 1->'001').'''        
        if isinstance(valore, bool):
            raise DatiNonValidiError(
                campo="id_piatto",
                valore_errato=valore,
                motivo="L'ID del piatto non puo essere un booleano.",
            )
        if isinstance(valore, int):
            numero = valore
        elif isinstance(valore, str):
            testo = valore.strip()
            if not testo.isdigit(): 
                raise DatiNonValidiError(
                    campo="id_piatto",
                    valore_errato=valore,
                    motivo="L'ID del piatto deve contenere solo cifre numeriche positive.",
                )
            numero = int(testo)
        else:
            raise DatiNonValidiError(
                campo="id_piatto",
                valore_errato=valore,
                motivo="L'ID del piatto deve essere un intero o una stringa numerica.",
            )
        if numero <= 0: 
            raise DatiNonValidiError(
                campo="id_piatto",
                valore_errato=valore,
                motivo="L'ID del piatto deve essere maggiore di zero."
            )
        return str(numero).zfill(3)
        
    '''
    validare che sia effettivamente un booleano (isinstance(valore, bool)) 
    e salvarlo in self._disponibile (evitando che venga assegnata per errore 
    una stringa come "false" o 0 senza controllo, o tenendo uniforme 
    l'incapsulamento con le altre proprietà).
    
    solleva DatiNonValidiError se non è un bool
    '''
    @property
    def disponibile(self) -> bool:
        '''Restituisce la disponibilita del piatto'''
        return self._disponibile
    
    @disponibile.setter
    def disponibile(self, valore: bool) -> None:
        '''Valida e imposta la disponibilita del piatto'''
        if not isinstance(valore, bool):
            raise DatiNonValidiError(
                campo="disponibile",
                valore_errato=valore,
                motivo="La disponibilita deve essere un valore booleano (True/False)",
            )
        self._disponibile = valore
        
    def __str__(self) -> str:
        """Rappresentazione leggibile per il menù a terminale."""
        # Se il piatto non è disponibile, prepara un'etichetta di avviso
        stato: str = "" if self.disponibile else "  [non disponibile]"
        return f"{self.id_piatto:>3}. {self.nome:<26} {self.prezzo:>7.2f} €{stato}"

    def __repr__(self) -> str:
        """Rappresentazione tecnica dettagliata per lo sviluppatore."""
        return (
            f"Piatto(id_piatto={self.id_piatto}, nome={self.nome!r}, "
            f"categoria={self.categoria!r}, prezzo={self.prezzo}, "
            f"disponibile={self.disponibile})"
        )

class Bevanda(Piatto):
    """Sottoclasse di Piatto che aggiunge l'attributo booleano alcolica."""

    def __init__(
        self,
        id_piatto: int,
        nome: str,
        prezzo: float,
        alcolica: bool = False,
        disponibile: bool = True,
    ) -> None:
        """Inizializza una bevanda richiamando la classe superiore e imposta la categoria fissa 'bevanda'."""
        # 1. Richiama il costruttore della classe superiore impostando la categoria fissa a bevanda.
        super().__init__(
            id_piatto=id_piatto,
            nome=nome,
            categoria="bevanda",
            prezzo=prezzo,
            disponibile=disponibile
        )
        # 2. Assegna l'attributo d'istanza per indicare se la bevanda è alcolica.
        self.alcolica = alcolica
        
    def __str__(self) -> str:
        """Aggiunge l'indicazione '(alcolica)' se previsto."""
        etichetta: str = "  (alcolica)" if self.alcolica else ""
        return super().__str__() + etichetta


if __name__ == "__main__":
    piatto = Piatto(1, "Carbonara", "primo", 10.5)
    print(piatto)
    bevanda = Bevanda(2, "Vino rosso", 4.5, alcolica=True)
    print(bevanda)
    
    
    
 
