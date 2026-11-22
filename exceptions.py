"""Eccezioni del dominio del ristorante."""

class RistoranteError(Exception):
    """Classe base per tutti gli errori specifici del dominio ristorante."""
    pass 


class DatiNonValidiError(RistoranteError):
    """Sollevata quando un dato non rispetta 
    i vincoli (es. prezzo <= 0, nome vuoto, posti <= 0)."""
    
    def __init__(self, campo:str, valore_errato, motivo:str)->None:
        
        """Inizializza l'eccezione salvando i dettagli e componendo il messaggio."""
        self.campo = campo 
        self.valore_errato = valore_errato
        self.motivo = motivo
        testo_errore = f"Errore di validazione sul campo '{campo}': valore inserito '{valore_errato}'. Motivo: {motivo}"
        super().__init__(testo_errore)
 
class PiattoNonTrovatoError(RistoranteError):
    """Sollevata quando si cerca un piatto con un ID non presente a menu."""

    def __init__(self, id_piatto: int|str) -> None: 
        """Inizializza l'eccezione salvando l'id_piatto e componendo il messaggio."""
        self.id_piatto = id_piatto
        messaggio_errore = f"Errore: Il piatto con ID '{id_piatto}' non è presente nel menu."
        super().__init__(messaggio_errore)
        

class PiattoNonDisponibileError(RistoranteError):
    """Sollevata quando si ordina un piatto presente a menu ma non disponibile/esaurito."""
    def __init__(self, nome_piatto: str) -> None:
        """Inizializza l'eccezione salvando il piatto e componendo il messaggio."""
        self.nome_piatto = nome_piatto
        testo_errore = f"Spiacenti, il piatto '{nome_piatto}' è attualmente esaurito."
        super().__init__(testo_errore)


class TavoloNonTrovatoError(RistoranteError):
    """Sollevata quando si cerca un tavolo con un numero inesistente."""
    def __init__(self, numero_tavolo: int)-> None:
        self.numero_tavolo = numero_tavolo
        messaggio_nr_tav_errato = f"Spiacenti, il numero del tavolo {numero_tavolo} e inesistente." 
        super().__init__(messaggio_nr_tav_errato)

class TavoloOccupatoError(RistoranteError):
    """Sollevata quando si tenta di occupare o aprire un ordine su un tavolo già occupato."""
    
    def __init__(self, numero_tavolo: int, ordine: object | None = None) -> None:
        self.numero_tavolo = numero_tavolo
        self.ordine = ordine
        messaggio = f"Il tavolo {numero_tavolo} è già occupato."
        super().__init__(messaggio)

class OrdineChiusoError(RistoranteError):
    """Sollevata quando si tenta di modificare o chiudere un ordine già saldato."""
    def __init__(self, id_ordine: int)-> None:
        self.id_ordine = id_ordine
        mess_ordine_saldato = f"Spiacenti, l'ordine nr. {id_ordine} non e modificabile. Ordine gia saldato"
        super().__init__(mess_ordine_saldato)


class OrdineNonTrovatoError(RistoranteError):
    """Sollevata quando si cerca l'ordine di un tavolo che non ne ha uno aperto."""
    def __init__(self, numero_tavolo:int)->None:
        self.numero_tavolo = numero_tavolo
        messaggio = f"Spiacenti, nessun ordine aperto trovato per il tavolo {numero_tavolo}."
        super().__init__(messaggio)



