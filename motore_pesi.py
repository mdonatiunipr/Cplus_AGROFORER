"""
DST — Motore a pesi 1-4 (PROTOTIPO, 25/09/2026, Ana Barezi)
=============================================================
Implementa il nuovo sistema di punteggio basato sulla tabella
"Criteri e fonti" (tabella_criteri_fonti_C+AgroForER.xlsx, 25/09/2026):
ogni criterio ha una o più CLASSI (fasce numeriche o categorie), e ogni
classe ha un peso da 1 a 4 per ciascuno dei 4 percorsi di valorizzazione
(Crediti di Carbonio, Crediti di Sostenibilità, Bilancio di Sostenibilità,
Inventario delle Emissioni).

STATO: PROVVISORIO. I pesi qui sotto sono le proposte [PROPOSTA] della
tabella Excel, NON ANCORA validate da Michele né derivate dai risultati
del questionario ai 50 stakeholder (che è la fonte prevista per i valori
definitivi — vedi scheda "Discussione con Michele e Lisa", riga 5). Quando
quei risultati saranno disponibili, la sostituzione avviene SOLO nei
valori del dizionario CRITERI qui sotto: la logica di classificazione e
aggregazione (questo file) non cambia.

Questo motore NON sostituisce valuta_percorsi() in main2_v2_prototipo.py:
gira in PARALLELO, additivamente, come già stabilito per tutte le altre
proposte di questa sessione (vedi docstring di main2_v2_prototipo.py). I
due sistemi vengono mostrati insieme nel risultato finale, chiaramente
etichettati come sistemi distinti.

Aggregazione: media semplice dei pesi (1-4) delle classi determinate dalle
risposte dell'utente, per ciascun percorso — SOLO sui criteri per cui
esiste già un campo nel form (vedi FIELD_MAP). Un criterio del quale il
form non raccoglie ancora il dato (es. "Tipologia di standard adottato",
"Disponibilità dati consumo risorse" — vedi CRITERI_NON_COLLEGATI sotto)
è escluso dalla media, non conteggiato come zero: aggiungerlo in futuro
richiede solo di aggiungere la sua voce a FIELD_MAP, senza toccare la
logica di aggregazione.

Filtro vs. floor (decisione condivisa con Ana, 25/09/2026): NESSUN
criterio qui applica un'esclusione rigida di un percorso. Una classe
"debole" (es. superficie_totale < 15ha) riceve semplicemente un peso
basso (1) invece che alto (4): l'effetto "malus" emerge naturalmente
dalla media, senza bisogno di logica speciale — a differenza del sistema
a punti originale, che aveva bisogno di is_piccola/is_inesperta come casi
espliciti.
"""

from typing import Dict, List, Optional, Union

PERCORSI = ("crediti_carbonio", "crediti_sostenibilita", "bilancio_sostenibilita", "inventario_emissioni")
_COLONNA = {"crediti_carbonio": "cc", "crediti_sostenibilita": "cs", "bilancio_sostenibilita": "bs", "inventario_emissioni": "ie"}


def _pesi(cc: int, cs: int, bs: int, ie: int) -> Dict[str, int]:
    return {"crediti_carbonio": cc, "crediti_sostenibilita": cs, "bilancio_sostenibilita": bs, "inventario_emissioni": ie}


# =====================================================================
# CRITERI — estratti da tabella_criteri_fonti_C+AgroForER.xlsx (25/09/2026)
# Ogni criterio ha una lista ordinata di classi con i pesi [PROPOSTA] per
# i 4 percorsi. Per i criteri "numerico" l'ordine determina anche le
# soglie di classificazione (vedi classify_numerico).
# =====================================================================
CRITERI: Dict[str, Dict] = {
    "fatturato_annuo": {
        "label": "Fatturato annuo (€)", "tipo": "numerico",
        "classi": [
            {"nome": "Micro: < 2 mln €", "soglia_max": 2_000_000, "pesi": _pesi(1, 2, 3, 4)},
            {"nome": "Piccola: 2-10 mln €", "soglia_max": 10_000_000, "pesi": _pesi(1, 2, 4, 4)},
            {"nome": "Media: 10-50 mln €", "soglia_max": 50_000_000, "pesi": _pesi(3, 3, 3, 3)},
            {"nome": "Grande: > 50 mln €", "soglia_max": None, "pesi": _pesi(4, 4, 4, 4)},
        ],
    },
    "numero_dipendenti": {
        "label": "Numero di dipendenti (n.)", "tipo": "numerico",
        "classi": [
            {"nome": "Micro: < 10", "soglia_max": 10, "pesi": _pesi(1, 2, 3, 4)},
            {"nome": "Piccola: 10-49", "soglia_max": 50, "pesi": _pesi(1, 2, 4, 4)},
            {"nome": "Media: 50-249", "soglia_max": 250, "pesi": _pesi(3, 3, 3, 3)},
            {"nome": "Grande: >= 250", "soglia_max": None, "pesi": _pesi(4, 4, 4, 4)},
        ],
    },
    "superficie_totale": {
        "label": "Superficie totale aziendale (ha)", "tipo": "numerico",
        "classi": [
            {"nome": "< 15 ha", "soglia_max": 15, "pesi": _pesi(1, 2, 3, 3)},
            {"nome": ">= 15 ha", "soglia_max": None, "pesi": _pesi(4, 3, 3, 3)},
        ],
    },
    "superficie_bosco": {
        "label": "Superficie forestale (ha)", "tipo": "numerico",
        "classi": [
            {"nome": "0-3 ha (Smallholder GS)", "soglia_max": 3, "pesi": _pesi(1, 2, 3, 3)},
            {"nome": "3-100 ha (SLIMF/FSC)", "soglia_max": 100, "pesi": _pesi(2, 3, 3, 3)},
            {"nome": "100-500 ha (Microscale GS)", "soglia_max": 500, "pesi": _pesi(3, 3, 3, 3)},
            {"nome": "> 500 ha", "soglia_max": None, "pesi": _pesi(4, 4, 3, 3)},
        ],
    },
    "nuova_piantumazione": {
        "label": "Superficie da destinare a nuova piantumazione (ha)", "tipo": "numerico",
        "classi": [
            {"nome": "0-3 ha (Smallholder GS, per analogia A/R)", "soglia_max": 3, "pesi": _pesi(1, 2, 3, 3)},
            {"nome": "3-100 ha (SLIMF/FSC, per analogia)", "soglia_max": 100, "pesi": _pesi(2, 3, 3, 3)},
            {"nome": "100-500 ha (Microscale GS, per analogia A/R)", "soglia_max": 500, "pesi": _pesi(3, 3, 3, 3)},
            {"nome": "> 500 ha", "soglia_max": None, "pesi": _pesi(4, 4, 3, 3)},
        ],
    },
    "superficie_agricola": {
        "label": "Superficie agricola produttiva (ha)", "tipo": "numerico",
        "classi": [
            {"nome": "Piccola: < 20 ha", "soglia_max": 20, "pesi": _pesi(1, 2, 2, 2)},
            {"nome": "Media: 20-100 ha", "soglia_max": 100, "pesi": _pesi(1, 3, 2, 3)},
            {"nome": "Grande: >= 100 ha", "soglia_max": None, "pesi": _pesi(1, 3, 3, 4)},
        ],
    },
    "orizzonte": {
        "label": "Orizzonte temporale dell'impegno (anni)", "tipo": "numerico",
        "classi": [
            {"nome": "< 10 anni", "soglia_max": 10, "pesi": _pesi(1, 2, 2, 2)},
            {"nome": "10-19 anni", "soglia_max": 20, "pesi": _pesi(2, 3, 3, 3)},
            {"nome": ">= 20 anni", "soglia_max": None, "pesi": _pesi(4, 3, 3, 3)},
        ],
    },
    "budget": {
        "label": "Budget disponibile per investimento/verifica", "tipo": "categorico",
        "classi": [
            {"nome": "Basso", "match": ["basso"], "pesi": _pesi(1, 1, 2, 2)},
            {"nome": "Medio", "match": ["medio"], "pesi": _pesi(2, 3, 3, 3)},
            {"nome": "Alto", "match": ["alto"], "pesi": _pesi(4, 4, 3, 3)},
        ],
    },
    "partecipazione_esg": {
        "label": "Partecipazione a schemi ESG/ranking", "tipo": "categorico",
        "classi": [
            {"nome": "No", "match": ["no"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "In corso", "match": ["in_corso"], "pesi": _pesi(1, 2, 2, 1)},
            {"nome": "Sì", "match": ["si"], "pesi": _pesi(2, 4, 3, 2)},
        ],
    },
    "piano_gestione_forestale": {
        "label": "Piano di Gestione Forestale Sostenibile Certificato", "tipo": "categorico",
        "classi": [
            {"nome": "No", "match": ["no"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "Sì", "match": ["si"], "pesi": _pesi(4, 3, 2, 1)},
        ],
    },
    "richiesta_dati_clienti": {
        "label": "Richiesta di dati/report ambientali da clienti", "tipo": "categorico",
        "classi": [
            {"nome": "No, mai richiesto", "match": ["no"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "Sì, questionari informali", "match": ["informale"], "pesi": _pesi(1, 2, 2, 2)},
            {"nome": "Sì, piattaforme strutturate", "match": ["strutturata"], "pesi": _pesi(1, 4, 3, 2)},
        ],
    },
    "dati_biomassa_forestale": {
        "label": "Disponibilità di dati sulla crescita della biomassa forestale", "tipo": "categorico",
        "classi": [
            {"nome": "Assenti", "match": ["assenti"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "Parziali", "match": ["parziali"], "pesi": _pesi(2, 1, 1, 1)},
            {"nome": "Strutturati", "match": ["strutturati"], "pesi": _pesi(4, 2, 1, 1)},
        ],
    },
    "soc_misurazione": {
        "label": "Misurazione del Carbonio Organico del Suolo (SOC)", "tipo": "categorico",
        "classi": [
            {"nome": "Nessuna analisi", "match": ["nessuna"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "Analisi chimico-fisica di base", "match": ["base"], "pesi": _pesi(1, 2, 2, 1)},
            {"nome": "Analisi microbiologiche avanzate", "match": ["avanzata"], "pesi": _pesi(1, 3, 3, 1)},
            {"nome": "Indici biologici complessi", "match": ["complessa"], "pesi": _pesi(1, 4, 3, 1)},
        ],
    },
    "biodiversita_indicatori": {
        # AGGIORNATO 25/09/2026 su richiesta di Ana: la tabella aveva separato "Biodiversità
        # fungina" e "Biodiversità epigea" in due criteri distinti (Blocco B §9.3 usa due
        # scale diverse), ma Ana ha chiesto di tenerli riuniti in un unico criterio generico
        # sia nel form sia nel questionario agli stakeholder — i pesi delle due scale erano
        # comunque quasi identici (differivano solo di 1 punto su Bilancio di Sostenibilità
        # al livello massimo: fungina=2, epigea=3). Pesi qui = quelli della scala "epigea"
        # (monitoraggio bioacustico validato in letteratura: Fraixedas et al. 2020; D'Amato
        # et al. 2024; André 2025), più realistici della scala fungina per l'autocompilazione
        # da parte delle PMI target (la classe più alta della scala fungina richiedeva analisi
        # di laboratorio del DNA fungino, regione ITS).
        "label": "Disponibilità di indicatori di biodiversità e di qualità biologica del suolo", "tipo": "categorico",
        "classi": [
            {"nome": "Nessun rilievo", "match": ["nessuno"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "Rilievi qualitativi occasionali", "match": ["qualitativo"], "pesi": _pesi(1, 2, 2, 1)},
            {"nome": "Monitoraggio sistematico e strutturato", "match": ["sistematico"], "pesi": _pesi(1, 4, 3, 1)},
        ],
    },
    "investimenti_compensazione_esterna": {
        "label": "Investimenti già effettuati in compensazione esterna", "tipo": "categorico",
        "classi": [
            {"nome": "No", "match": ["no"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "Sì", "match": ["si"], "pesi": _pesi(4, 2, 1, 1)},
        ],
    },
    "esperienza_pratiche_agroecologiche": {
        "label": "Esperienza pregressa in pratiche agroecologiche o certificazioni", "tipo": "categorico",
        "classi": [
            {"nome": "Nessuna", "match": ["nessuna"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "Pilota in corso", "match": ["pilota"], "pesi": _pesi(1, 3, 2, 1)},
            {"nome": "Consolidata", "match": ["consolidata"], "pesi": _pesi(1, 4, 3, 2)},
        ],
    },
    "finanziamenti_transizione": {
        "label": "Finanziamenti bancari per transizione ecologica", "tipo": "categorico",
        "classi": [
            {"nome": "No", "match": ["no"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "Sì, canali ordinari", "match": ["ordinari"], "pesi": _pesi(1, 2, 2, 1)},
            {"nome": "Sì, linee dedicate ESG", "match": ["dedicati"], "pesi": _pesi(2, 4, 3, 2)},
        ],
    },
    "responsabile_interno": {
        "label": "Presenza di un responsabile interno o team dedicato", "tipo": "categorico",
        "classi": [
            {"nome": "No", "match": ["no"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "Sì", "match": ["si"], "pesi": _pesi(2, 2, 3, 3)},
        ],
    },
    "certificazioni_possedute": {
        "label": "Certificazioni possedute (PEFC, FSC, biologico, ...)", "tipo": "categorico",
        "classi": [
            {"nome": "Nessuna certificazione", "match": ["nessuna"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "Certificazione biologica", "match": ["biologica"], "pesi": _pesi(1, 3, 2, 1)},
            {"nome": "Certificazione forestale", "match": ["forestale"], "pesi": _pesi(3, 4, 2, 1)},
            {"nome": "Entrambe", "match": ["entrambe"], "pesi": _pesi(3, 4, 3, 1)},
        ],
    },
    "misurazione_scope_ghg": {
        # AGGIUNTO 25/09/2026 su richiesta di Ana: era in CRITERI_NON_COLLEGATI (nessun campo
        # form dedicato), ora ha un campo proprio (misurazione_scope_ghg) in index2.html,
        # Sezione 3 — separato dal campo aggregato dati_disponibili (bassi/media/alti, usato
        # solo dalla LOGICA ORIGINALE), che resta invariato.
        "label": "Disponibilità di dati per la misurazione delle emissioni di CO2 (Scopo 1, 2 e 3)", "tipo": "categorico",
        "classi": [
            {"nome": "No", "match": ["no"], "pesi": _pesi(1, 1, 1, 1)},
            {"nome": "Scope 1 soltanto", "match": ["scope1"], "pesi": _pesi(1, 1, 2, 2)},
            {"nome": "Scope 1 + 2", "match": ["scope1_2"], "pesi": _pesi(1, 2, 2, 3)},
            {"nome": "Scope 1 + 2 + 3", "match": ["scope1_2_3"], "pesi": _pesi(2, 3, 3, 4)},
        ],
    },
    "settore_isic": {
        "label": "Settore prevalente (ISIC Divisioni 01 e 02)", "tipo": "multi-categorico",
        "classi": [
            {"nome": "Divisione 01 — Agricoltura, zootecnia e caccia", "match": ["01"], "pesi": _pesi(1, 2, 2, 4)},
            {"nome": "Divisione 02 — Silvicoltura e aree forestali", "match": ["02"], "pesi": _pesi(4, 2, 1, 1)},
        ],
    },
}

# Criteri della tabella per cui il form NON raccoglie ancora il dato
# corrispondente: restano DOCUMENTATI qui (per non perdere il lavoro fatto
# sulla tabella) ma sono esclusi dal calcolo finché non esiste un campo
# form dedicato — vedi FIELD_MAP sotto, che è l'unica fonte di verità su
# cosa è "collegato".
CRITERI_NON_COLLEGATI = [
    "Adozione di standard per la contabilizzazione e il controllo delle emissioni GHG",
    "Tipologia di standard adottato",
    "Disponibilità di dati sul consumo di risorse (carburanti, energia elettrica, ecc.)",
]


def classify_numerico(criterio_key: str, valore: Optional[float]) -> Optional[dict]:
    """Trova la prima classe la cui soglia_max non e' superata dal valore
    (None = nessun limite superiore, ultima classe). Ritorna None se valore
    e' None (campo non compilato) o negativo."""
    if valore is None or valore < 0:
        return None
    for classe in CRITERI[criterio_key]["classi"]:
        if classe["soglia_max"] is None or valore <= classe["soglia_max"]:
            return classe
    return None  # non dovrebbe mai accadere (l'ultima classe ha sempre soglia_max=None)


def classify_categorico(criterio_key: str, valore_grezzo: Optional[str]) -> Optional[dict]:
    """Trova la classe il cui elenco 'match' contiene il valore grezzo del
    form (case-insensitive). Ritorna None se il valore e' vuoto o non
    riconosciuto."""
    if not valore_grezzo:
        return None
    valore_norm = valore_grezzo.strip().lower()
    for classe in CRITERI[criterio_key]["classi"]:
        if valore_norm in classe["match"]:
            return classe
    return None


def classify_certificazioni_possedute(certificazioni_esistenti: Optional[str], certificazione_tipo: Optional[str]) -> Optional[dict]:
    """Combina i due campi esistenti del form (booleano aggregato +
    disaggregazione parziale) nella classe corretta delle 4 previste dalla
    tabella. Se il booleano e' 'si' ma il tipo non e' stato specificato,
    ritorna None (dato insufficiente per classificare con certezza) invece
    di indovinare."""
    if certificazioni_esistenti == "no":
        return classify_categorico("certificazioni_possedute", "nessuna")
    if certificazioni_esistenti == "si" and certificazione_tipo:
        return classify_categorico("certificazioni_possedute", certificazione_tipo)
    return None


def valuta_percorsi_pesi(form: dict) -> dict:
    """Motore additivo a pesi 1-4. Riceve il DIZIONARIO dei valori del form
    (stessi nomi di campo di valuta_percorsi in main2_v2_prototipo.py) e
    ritorna, per ciascun percorso, il punteggio medio (1-4 e in
    percentuale), il numero di criteri usati nel calcolo e il dettaglio
    criterio-per-criterio (per trasparenza/debug in fase di demo).

    NESSUNA eccezione viene sollevata per input mancanti: un criterio non
    classificabile (campo vuoto, valore non riconosciuto, o criterio non
    ancora collegato — vedi CRITERI_NON_COLLEGATI) viene semplicemente
    escluso dalla media di quel percorso, non trattato come zero.
    """
    contributi: Dict[str, List[float]] = {p: [] for p in PERCORSI}
    dettaglio: List[dict] = []

    def _registra(criterio_key: str, classe: Optional[dict]):
        if classe is None:
            dettaglio.append({"criterio": CRITERI[criterio_key]["label"], "classe": None, "usato": False})
            return
        for percorso in PERCORSI:
            contributi[percorso].append(classe["pesi"][percorso])
        dettaglio.append({"criterio": CRITERI[criterio_key]["label"], "classe": classe["nome"], "usato": True})

    # ---- criteri numerici ----
    for chiave in ("fatturato_annuo", "numero_dipendenti", "superficie_totale", "superficie_bosco",
                   "nuova_piantumazione", "superficie_agricola", "orizzonte"):
        _registra(chiave, classify_numerico(chiave, form.get(chiave)))

    # ---- criteri categorici a mappatura diretta ----
    for chiave in ("budget", "partecipazione_esg", "piano_gestione_forestale", "richiesta_dati_clienti",
                   "dati_biomassa_forestale", "soc_misurazione", "investimenti_compensazione_esterna",
                   "esperienza_pratiche_agroecologiche", "finanziamenti_transizione", "responsabile_interno",
                   "misurazione_scope_ghg"):
        _registra(chiave, classify_categorico(chiave, form.get(chiave)))

    # ---- biodiversita' e qualita' biologica del suolo: criterio unico e generico
    # (fungina + epigea riunite su richiesta di Ana, 25/09/2026 — vedi commento su
    # CRITERI["biodiversita_indicatori"] sopra) ----
    _registra("biodiversita_indicatori", classify_categorico("biodiversita_indicatori", form.get("biodiversita_indicatori")))

    # ---- certificazioni possedute: combinazione di due campi esistenti ----
    _registra("certificazioni_possedute", classify_certificazioni_possedute(
        form.get("certificazioni_esistenti"), form.get("certificazione_tipo")))

    # ---- settore ISIC: multi-select, ogni codice selezionato contribuisce
    # indipendentemente (un'azienda con codici in entrambe le divisioni
    # riceve il contributo di entrambe le classi, non solo una) ----
    settore = form.get("settore") or []
    codici_isic_validi = {c["match"][0] for c in CRITERI["settore_isic"]["classi"]}
    for codice in settore:
        if codice in codici_isic_validi:
            _registra("settore_isic", classify_categorico("settore_isic", codice))
        else:
            dettaglio.append({"criterio": CRITERI["settore_isic"]["label"], "classe": None, "usato": False})

    risultati = {}
    for percorso in PERCORSI:
        valori = contributi[percorso]
        media_1_4 = sum(valori) / len(valori) if valori else None
        risultati[percorso] = {
            "media_1_4": round(media_1_4, 2) if media_1_4 is not None else None,
            "percentuale": round((media_1_4 - 1) / 3 * 100) if media_1_4 is not None else None,
            "n_criteri_usati": len(valori),
        }

    return {
        "percorsi": risultati,
        "n_criteri_totali_collegati": len(CRITERI) + 1,  # +1 perche' settore_isic puo' contribuire piu' volte
        "dettaglio": dettaglio,
        "criteri_non_collegati": CRITERI_NON_COLLEGATI,
    }
