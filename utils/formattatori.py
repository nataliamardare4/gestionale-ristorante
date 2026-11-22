from models.piatto import Piatto
from models.tavolo import Tavolo


def formatta_euro(valore: float) -> str:
    """Formatta un numero float con 2 cifre decimali e simbolo € (es. 12.5 -> '12.50 €')."""
    return f"{valore:.2f} €"


def titolo(testo: str) -> str:
    """Crea un'intestazione di sezione racchiusa tra due linee orizzontali di '='."""
    linea: str = "=" * 44
    return f"\n{linea}\n  {testo.upper()}\n{linea}"


def formatta_menu(piatti: list[Piatto]) -> str:
    """Formatta l'elenco dei piatti raggruppandoli visivamente sotto la loro categoria."""
    if not piatti:
        return "(nessun piatto)"
    linee: list[str] = []
    categoria_corrente: str | None = None

    # Ordina i piatti prima per categoria e poi per ID per raggrupparli in modo coerente
    piatti_ordinati: list[Piatto] = sorted(piatti, key=lambda p: (p.categoria, p.id_piatto))

    for piatto in piatti_ordinati:
        # Quando cambia la categoria rispetto alla precedente, inserisce l'etichetta [CATEGORIA]
        if piatto.categoria != categoria_corrente:
            categoria_corrente = piatto.categoria
            linee.append(f"\n[{categoria_corrente.upper()}]")
        # Aggiunge la stringa formattata del piatto (str(piatto))
        linee.append(str(piatto))
    # Unisce tutte le righe con il ritorno a capo
    return "\n".join(linee)

def formatta_tavoli(tavoli: list[Tavolo]) -> str:
    """Formatta la lista dei tavoli producendo una riga per ciascun tavolo."""
    if not tavoli:
        return "(nessun tavolo)"
    # Converte ciascun tavolo in stringa e li concatena
    return "\n".join(str(tavolo) for tavolo in tavoli)

def formatta_classifica(classifica: list[tuple[str, int]]) -> str:
    """Formatta la classifica dei piatti con numerazione progressiva a partire da 1."""
    if not classifica:
        return "(nessuna vendita)"
    # 'enumerate(..., start=1)' produce 1., 2., 3. per ciascun elemento
    return "\n".join(
        f"{posizione}. {nome} - {quantita} porzioni"
        for posizione, (nome, quantita) in enumerate(classifica, start=1)
    )

def formatta_incassi(incassi: dict[str, float]) -> str:
    """Formatta il resoconto degli incassi allineando categoria a sinistra e importo a destra."""
    if not incassi:
        return "(nessun incasso)"
    return "\n".join(
        f"{categoria:<12} {formatta_euro(importo):>12}"
        for categoria, importo in incassi.items()
    )

if __name__ == "__main__":
    print(titolo("Test Formattatori"))
    print(formatta_euro(15))
    print(formatta_classifica([("Carbonara", 10), ("Tiramisù", 5)]))
