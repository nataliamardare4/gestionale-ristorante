import math

def chiedi_testo(messaggio: str) -> str:
    """Chiede una stringa non vuota all'utente, ripetendo in caso di input vuoto."""
    # 1. Avvia un ciclo per continuare a richiedere l'input finché non è valido.
    while True:
        testo = input(f"{messaggio}: ").strip()
    # 2. Acquisisci l'input ripulendolo dagli spazi periferici.
    # 3. Se la stringa contiene testo restituiscila, altrimenti mostra un messaggio di errore e richiedi nuovamente.
        if testo:
            return testo
        print("Errore: il testo non puo essere vuoto. Riprova")

def chiedi_intero(
    messaggio: str,
    minimo: int | None = None,
    massimo: int | None = None,
) -> int:
    """Chiede un intero, verificando opzionalmente l'intervallo [minimo, massimo]."""
    # 1. Avvia un ciclo di richiesta.
    while True:
        grezzo = input(f"{messaggio}: ").strip()
        # 2. Tenta la conversione dell'input in intero; se fallisce con errore di conversione, avvisa l'utente e richiedi di nuovo.
        try:
            valore = int(grezzo)
        except ValueError:
            print("Errore: inserisci un numero intero valido.")    
            continue
        # 3. Se è impostato un valore minimo e il numero è inferiore, avvisa l'utente.
        if minimo is not None and valore < minimo:
            print(f"Errore: il valore deve essere maggiore o uguale a {minimo}.")
            continue
        # 4. Se è impostato un valore massimo e il numero è superiore, avvisa l'utente.
        if massimo is not None and valore > massimo:
            print(f"Errore: il valore deve essere minore o uguale a {massimo}.")
            continue
        # 5. Se tutti i vincoli sono rispettati, restituisci il numero.
        return valore


def chiedi_prezzo(messaggio: str) -> float:
    """Chiede un prezzo positivo (> 0), gestendo sia la virgola sia il punto decimale."""
    # 1. Avvia un ciclo di richiesta.
    while True:
        # 2. Acquisisci l'input gestendo sia il punto che l'eventuale 
        # virgola decimale.
        grezzo = input(f"{messaggio}: ").strip().replace(",", ".")
        # 3. Tenta la conversione a numero decimale; se fallisce, avvisa l'utente e richiedi nuovamente.
        try:
            valore = float(grezzo)
        except ValueError:
            print("Errore: inserisci un importo numerico valido (es. 12.50 o 12,50).")
            continue
        # 4. Verifica che il valore sia strettamente maggiore di zero; se non lo è, avvisa l'utente.
        if not math.isfinite(valore) or valore <= 0: 
            print("Errore: il prezzo deve essere maggiore di zero.")
            continue
        # 5. Restituisci il prezzo valido e arrotonda a due decimali il risultato.
        return round(valore, 2)


def chiedi_conferma(messaggio: str) -> bool:
    """Chiede una risposta (s/n). Restituisce True per sì/s, False per no/n."""
    # 1. Avvia un ciclo di richiesta normalizzando la risposta in minuscolo.
    while True:
        # 2. Se la risposta corrisponde a un'affermazione (es. 's', 'si', 'sì'), restituisci True.
        risposta = input(f"{messaggio} (s/n): ").strip().lower()
        # 3. Se corrisponde a una negazione (es. 'n', 'no'), restituisci False.
        if risposta in {"s", "si", "sì"}:
            return True
        # 4. Altrimenti avvisa l'utente della risposta non valida e ripeti.
        if risposta in {"n", "no"}:
            return False
        print("Errore: rispondi con 's' (si) oppure 'n' (no).")

def leggi_float(prompt: str, minimo: float | None = None) -> float: 
    """Legge un numero decimale accettando anche la virgola come separatore."""
    while True:
        grezzo = input(prompt).strip().replace(",", ".")
        try:
            valore = float(grezzo)
        except ValueError:
            print("Inserisci un numero valido (es. 12.50 oppure 12,50).")
            continue

        if minimo is not None and valore < minimo:
            print(f"Il valore deve essere almeno {minimo}.")
            continue

        return valore
