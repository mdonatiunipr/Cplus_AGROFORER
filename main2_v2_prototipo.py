"""
DST Sostenibilità e Carbonio — v2 PROTOTIPO (23/09/2026, Ana Barezi)
=====================================================================
Prototipo per la riunione con Michele e Lisa del 24/09/2026. NON è una versione
definitiva: molti valori numerici qui sotto sono PROPOSTE non ancora validate,
segnalate esplicitamente con "[PROPOSTA]" nei commenti e nei testi mostrati
all'utente. Alcuni punti restano deliberatamente NON implementati perché
richiedono una decisione di architettura di Michele (vedi i blocchi
"NON IMPLEMENTATO" più sotto e la tabella tabella_criteri_fonti_C+AgroForER.xlsx,
scheda "Discussione con Michele e Lisa").

Compatibilità con il form attuale (index2.html): tutti i campi nuovi sono
OPZIONALI (default None) — il form esistente continua a funzionare senza
modifiche. Se un campo nuovo non viene inviato, il relativo criterio è
semplicemente ignorato nel punteggio (nessun errore, nessun bonus/malus).

Cosa è stato aggiunto rispetto a main2.py originale:
  1. Fix del bug "orizzonte" (già proposto il 21/09/2026, invariato qui)
  2. Fix del bug "settore" (raccolto ma mai usato — ora attivato) [PROPOSTA]
     AGGIORNAMENTO 23/09/2026: settore non è più una <select> a scelta
     singola ("agricolo"/"forestale"/"agroforestale"/"altro") ma un
     multi-select di codici ISIC Rev.4 (Sezione A, Divisioni 01 e 02 —
     Divisione 03 "fishing" ESCLUSA su conferma di Ana, 23/09/2026). Fonte:
     United Nations, ISIC Rev.4, Statistical Papers Series M No. 4/Rev.4 —
     https://unstats.un.org/unsd/publication/seriesm/seriesm_4rev4e.pdf.
     Un'azienda può dichiarare più codici (es. sia coltivazione che
     selvicoltura).
     AGGIORNAMENTO 23/09/2026 (bis, su richiesta di Ana — semplificazione):
     il multi-select è sceso dal livello Gruppo (11 voci — 011-017, 021-024)
     al livello Divisione (2 voci — 01, 02), perché la logica di punteggio
     (ha_codice_forestale/ha_codice_agricolo più sotto) usa da sempre solo
     il prefisso di Divisione — il dettaglio di Gruppo non alimentava nulla,
     era raccolto solo per essere mostrato nel riepilogo finale. Il dettaglio
     dei Gruppi non è sparito: è ora nel tooltip di ciascuna Divisione.
  3. 9 criteri nuovi, opzionali, corrispondenti alle righe "✓" della tabella
     Excel (Fatturato, dipendenti, ESG, PGFS certificato, dati biomassa/SOC/
     biodiversità, investimenti in compensazione, richiesta dati clienti,
     responsabile interno) [tutti PROPOSTA]
  4. Campo finanziamenti_transizione ora raccolto (Famiglia 4, form v2) ma
     SENZA ruolo nel punteggio — la tabella lo segna esplicitamente come
     "Contesto — logica non ancora definita": qui esiste solo per non perdere
     il dato finché Michele/Lisa non decidono come usarlo.
  5. AGGIORNAMENTO 23/09/2026 (su richiesta di Ana): il campo aggregato
     certificazioni_esistenti riceve una disaggregazione parziale, solo
     raccolta/presentazione, NESSUN nuovo punteggio — certificazione_tipo
     (biologica/forestale/entrambe, le stesse 4 fasce già definite nella
     tabella Excel per questa riga), che si rivela nel form solo quando la
     risposta principale è "Sì".
  5b. AGGIORNAMENTO 25/09/2026 (su richiesta di Ana, dopo ricerca): RIMOSSO
      il sottocampo partecipazione_esg_livello (medaglia EcoVadis
      Bronzo/Argento/Oro/Platino/Committed), introdotto il 23/09 e mai
      collegato a un punteggio. La tabella "Criteri e fonti" (nota M16)
      segnalava la rilevanza del criterio EcoVadis per il profilo delle
      aziende target come domanda aperta da decidere con Michele; la
      ricerca non ha trovato aziende agricole/forestali tra i casi EcoVadis
      italiani reperiti (concentrati su manifatturiero, ICT, trasporti,
      edilizia) — solo il caso aneddotico già citato in tabella (filiera
      Davines). Resta il campo base partecipazione_esg (Sì/In corso/No),
      che PUNTEGGIA regolarmente (blocco sopra) e non è stato toccato.
  6. AGGIORNAMENTO 23/09/2026 (feedback dall'officina con Michele e Lisa):
     il campo, rinominato esperienza_pratiche_agroecologiche (era
     esperienza_pratiche_rigenerative — "agroecologica" è il termine più
     corretto per queste pratiche), rivela — quando la risposta è "pilota" o
     "consolidata" — un multi-select di 12 PRATICHE CONCRETE e verificabili
     (rotazione colturale, cover crop, agroforestazione, riciclo sostanza
     organica, ecc.), non più i 13 Principi HLPE come voci di selezione: i
     principi sono astrazioni di governance (es. "Land and Natural Resource
     Governance", "Fairness", "Participation") che un'azienda non può
     dichiarare di "applicare" in modo verificabile — correzione richiesta da
     Ana il 23/09/2026 dopo aver visto la prima versione. Le pratiche sono
     tratte da FAO TAPE Step 1 / CAET (Characterization of Agroecological
     Transition — https://www.fao.org/agroecology/database/tape) e dagli
     eco-schemi della PAC 2023-2027 italiani (MASAF —
     https://www.masaf.gov.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/12126),
     ciascuna con un tooltip che la ricollega al Principio HLPE
     dell'Agroecology Coalition più pertinente. Campo pratiche_agroecologiche:
     solo raccolta/presentazione, NESSUN nuovo punteggio.
  7. AGGIORNAMENTO 25/09/2026 (su richiesta di Ana): superficie_bosco riceve
     ora un bonus ADDITIVO a fasce (oltre al bonus fisso +15 originale,
     invariato) ancorato a soglie in ettari verificate su standard reali:
     Gold Standard "Smallholder" LUF (≤3 ha), FSC SLIMF (default globale
     <100 ha) e Gold Standard "Microscale" LUF (≤500 ha). La soglia italiana
     per il PGFS (Testo Unico Forestale) NON è stata usata: è demandata alle
     Regioni senza un numero nazionale unico, e quella dell'Emilia-Romagna
     non è stata reperita — vedi commento nel blocco di punteggio per il
     dettaglio delle fonti. Punteggi delle fasce [PROPOSTA], non validati.

  8. AGGIORNAMENTO 25/09/2026 (su richiesta di Ana): aggiunto il nuovo MOTORE
     A PESI 1-4 (motore_pesi.py, funzione valuta_percorsi_pesi) — implementa
     il sistema di punteggio della tabella "Criteri e fonti" ristrutturata il
     25/09/2026 (classi per criterio, peso 1-4 per percorso). Gira in
     PARALLELO a valuta_percorsi() qui sotto, che resta INVARIATA: i due
     sistemi vengono mostrati insieme nel risultato, chiaramente etichettati
     come distinti (vedi sezione "Sistema a pesi (provvisorio)" in
     index2.html). Aggregazione: media semplice dei pesi delle classi
     determinate dalle risposte, per percorso — SOLO sui criteri per cui il
     form raccoglie già il dato corrispondente (22 dei 26 criteri della
     tabella; i 4 non ancora collegati — es. "Tipologia di standard
     adottato" — sono elencati in motore_pesi.CRITERI_NON_COLLEGATI e
     semplicemente esclusi dalla media, non contati come zero). I pesi sono
     ancora quelli [PROPOSTA] della tabella Excel: la fonte prevista per i
     valori definitivi è il questionario ai 50 stakeholder (non ancora
     raccolto) — quando disponibile, si sostituiscono SOLO i numeri in
     motore_pesi.CRITERI, senza toccare questa logica. Filtro vs. floor
     (decisione condivisa con Ana): nessuna esclusione rigida di percorsi —
     un criterio "debole" (es. superficie_totale <15ha) riceve un peso
     basso, non un'esclusione; il malus emerge dalla media, senza bisogno
     dei casi speciali is_piccola/is_inesperta della logica originale.

  9. AGGIORNAMENTO 25/09/2026 (su richiesta di Ana): collegato il criterio
     "Disponibilità di dati per la misurazione delle emissioni di CO2
     (Scopo 1, 2 e 3)" (prima in CRITERI_NON_COLLEGATI). Nuovo campo form
     dedicato misurazione_scope_ghg (Sezione 3 di index2.html, select a 4
     opzioni: No / Scope 1 / Scope 1+2 / Scope 1+2+3) — SEPARATO dal campo
     aggregato dati_disponibili (bassi/media/alti), che resta l'unico usato
     dalla LOGICA ORIGINALE e non è stato toccato. Usato solo dal motore a
     pesi (form_pesi), non da valuta_percorsi().

Cosa NON è stato toccato (richiede decisione di Michele — vedi scheda
Discussione):
  - I campi aggregati certificazioni_esistenti e dati_disponibili NON sono
    stati disaggregati: restano esattamente come nell'originale.
  - Bonus condiviso (non cumulativo) tra superficie_bosco e
    nuova_piantumazione nella LOGICA ORIGINALE: un'azienda con entrambe >0
    riceve lo stesso +15 di un'azienda con una sola — segnalato in tabella,
    non risolto qui (le nuove fasce si aggiungono solo sopra a
    superficie_bosco, nuova_piantumazione resta come nell'originale).
  - "Finanziamenti bancari per transizione ecologica" è raccolto ma senza
    ruolo nella logica (vedi punto 4 sopra).
"""

from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from motore_pesi import valuta_percorsi_pesi

# ISIC Rev.4, Sezione A ("Agriculture, forestry and fishing") — solo Divisioni
# 01 e 02: la Divisione 03 (Fishing and aquaculture) è ESCLUSA su conferma di
# Ana (23/09/2026), non pertinente al target del progetto.
#
# FONTE UFFICIALE (confermata da Ana, 23/09/2026): United Nations, International
# Standard Industrial Classification of All Economic Activities, Revision 4,
# Statistical Papers Series M No. 4/Rev.4, Section A "Agriculture, forestry
# and fishing" — https://unstats.un.org/unsd/publication/seriesm/seriesm_4rev4e.pdf
# AGGIORNAMENTO 23/09/2026 (su richiesta di Ana — semplificazione): sceso dal livello Gruppo
# (11 voci) al livello Divisione (2 voci), l'unico livello che la logica di punteggio usa
# davvero (vedi ha_codice_forestale/ha_codice_agricolo più sotto). Il dettaglio dei Gruppi
# resta consultabile nel tooltip di ciascuna Divisione nel form (index2.html).
ISIC_LABELS = {
    "01": "Agricoltura, zootecnia e caccia (Divisione 01)",
    "02": "Silvicoltura e utilizzo di aree forestali (Divisione 02)",
}

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="DST Sostenibilità e Carbonio",
    description="Strumento di orientamento agli schemi di certificazione ESG e Carbon per aziende agricole e forestali.",
    version="2.0.0",
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

SCHEMI = {
    "crediti_carbonio": {
        "titolo": "Crediti di Carbonio",
        "categoria": "Mercati Volontari",
        "icona": "🌿",
        "descrizione": "Progetti a lungo termine per generare crediti scambiabili derivanti dall'assorbimento o riduzione certificata di CO2.",
        "adatto_a": "Grandi aziende agricole o forestali con ampie superfici e capacità di investimento pluriennale.",
        "requisiti": [
            "Addizionalità del progetto",
            "Monitoraggio rigoroso su lungo periodo",
            "Certificazione di terza parte (es. Verra, Gold Standard)"
        ],
        "vantaggi": [
            "Generazione di nuove fonti di reddito",
            "Massima valorizzazione climatica"
        ],
        "criticita": [
            "Costi di implementazione e certificazione molto elevati",
            "Inadatto a superfici ridotte"
        ],
        "complessita": "Alta",
        "output": "Crediti di carbonio verificati"
    },
    "crediti_sostenibilita": {
        "titolo": "Crediti di Sostenibilità (Biodiversità)",
        "categoria": "Mercati Volontari",
        "icona": "🦋",
        "descrizione": "Schemi innovativi per remunerare gli impatti positivi generati su biodiversità, acqua e salute del suolo.",
        "adatto_a": "Aziende strutturate focalizzate su pratiche rigenerative avanzate, agroecologia e tutela degli habitat.",
        "requisiti": [
            "Definizione di metriche ecologiche precise",
            "Applicazione di pratiche rigenerative",
            "Verifica degli indicatori ambientali"
        ],
        "vantaggi": [
            "Valorizzazione dei servizi ecosistemici",
            "Pionierismo sui nuovi mercati della natura"
        ],
        "criticita": [
            "Mercato emergente e standard ancora in evoluzione",
            "Necessità di competenze tecniche specializzate"
        ],
        "complessita": "Alta",
        "output": "Certificati di impatto ambientale / Crediti di biodiversità"
    },
    "bilancio_sostenibilita": {
        "titolo": "Bilancio di Sostenibilità",
        "categoria": "Reporting ESG",
        "icona": "📊",
        "descrizione": "Documento strutturato per comunicare agli stakeholder le performance ambientali, sociali e di governance (ESG).",
        "adatto_a": "Tutte le aziende, particolarmente consigliato a PMI e imprese che si avvicinano per la prima volta alla sostenibilità.",
        "requisiti": [
            "Raccolta dati aziendali (consumi, risorse umane)",
            "Analisi delle tematiche rilevanti",
            "Redazione documentale trasparente"
        ],
        "vantaggi": [
            "Rafforza la reputazione aziendale e il legame col territorio",
            "Migliora l'accesso al credito e la risposta ai clienti",
            "Ottimo trampolino di lancio per future certificazioni"
        ],
        "criticita": [
            "Richiede organizzazione interna per la raccolta dati",
            "Non genera direttamente crediti vendibili"
        ],
        "complessita": "Bassa - Media",
        "output": "Report ESG (Bilancio di Sostenibilità)"
    },
    "inventario_emissioni": {
        "titolo": "Inventario delle Emissioni (Carbon Footprint)",
        "categoria": "Analisi Climatica",
        "icona": "🏭",
        "descrizione": "Quantificazione scientifica dei gas serra emessi dall'azienda, fondamentale per avviare strategie di decarbonizzazione.",
        "adatto_a": "Aziende che necessitano di conoscere il proprio impatto climatico per filiera o per redigere piani di riduzione.",
        "requisiti": [
            "Mappatura delle fonti emissive (Scope 1, 2, 3)",
            "Raccolta dati di consumo energetico e materiali",
            "Applicazione di fattori di conversione standard (es. GHG Protocol)"
        ],
        "vantaggi": [
            "Identifica le inefficienze energetiche",
            "Requisito sempre più richiesto dalle grandi filiere agroalimentari"
        ],
        "criticita": [
            "Calcolo delle emissioni indirette (Scope 3) spesso complesso",
            "Deve essere accompagnato da un piano di riduzione reale"
        ],
        "complessita": "Media",
        "output": "Report della Carbon Footprint aziendale"
    }
}


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def valuta_percorsi(
    settore: List[str],
    superficie_totale: float,
    superficie_bosco: float,
    superficie_agricola: float,
    superficie_altra: float,
    nuova_piantumazione: float,
    motivazioni: List[str],
    dati_disponibili: str,
    orizzonte: float,
    budget: str,
    certificazioni_esistenti: str,
    # ---- campi nuovi v2 (tutti opzionali — compatibili col form attuale) ----
    fatturato_annuo: Optional[float] = None,
    numero_dipendenti: Optional[float] = None,
    partecipazione_esg: Optional[str] = None,           # "no" | "in_corso" | "si"
    certificazione_tipo: Optional[str] = None,          # "biologica" | "forestale" | "entrambe" — disaggregazione parziale di certificazioni_esistenti; solo versione, non punteggio
    piano_gestione_forestale: Optional[str] = None,     # "si" | "no"
    dati_biomassa_forestale: Optional[str] = None,       # "assenti" | "parziali" | "strutturati"
    soc_misurazione: Optional[str] = None,               # "nessuna" | "base" | "avanzata" | "complessa"
    biodiversita_indicatori: Optional[str] = None,        # "nessuno" | "qualitativo" | "sistematico"
    investimenti_compensazione_esterna: Optional[str] = None,  # "si" | "no"
    compensazione_esterna_dettaglio: Optional[str] = None,  # testo libero (progetto/area) — raccolto solo se "si"; solo versione, non punteggio
    esperienza_pratiche_agroecologiche: Optional[str] = None,  # "nessuna" | "pilota" | "consolidata" — disaggregazione parziale di certificazioni_esistenti (Famiglia 5); solo versione, non punteggio. Rinominato da esperienza_pratiche_rigenerative il 23/09/2026.
    pratiche_agroecologiche: Optional[List[str]] = None,  # codici di pratiche agroecologiche concrete (FAO TAPE/CAET + eco-schemi PAC) — raccolto solo se pilota/consolidata; solo versione, non punteggio
    richiesta_dati_clienti: Optional[str] = None,        # "no" | "informale" | "strutturata" — solo versione, non punteggio
    responsabile_interno: Optional[str] = None,          # "si" | "no" — solo versione, non punteggio
    finanziamenti_transizione: Optional[str] = None,     # "no" | "ordinari" | "dedicati" — raccolto, NESSUN punteggio (ruolo non definito)
):
    punteggi = {chiave: 20.0 for chiave in SCHEMI}  # Base di partenza
    motivi = {chiave: [] for chiave in SCHEMI}

    # ================= LOGICA ORIGINALE (invariata) =================

    # Soglia <15ha: CONFERMATA dal team di progetto (Ana Barezi, 21/09/2026) sulla base dei casi
    # reali seguiti nel progetto — al di sotto di questa soglia i crediti di carbonio non sono
    # economicamente viabili in autonomia (sarebbe necessaria un'aggregazione tra più aziende).
    is_piccola = superficie_totale < 15
    is_inesperta = (dati_disponibili == "bassi" and certificazioni_esistenti == "no")

    if is_piccola and is_inesperta:
        punteggi["crediti_carbonio"] -= 50
        punteggi["crediti_sostenibilita"] -= 50
        punteggi["bilancio_sostenibilita"] += 40
        punteggi["inventario_emissioni"] += 15

        motivi["bilancio_sostenibilita"].append("Essendo una realtà di piccole dimensioni alla prima esperienza, il Bilancio di Sostenibilità è lo strumento ideale e più conveniente per iniziare.")
        motivi["crediti_carbonio"].append("Schema fortemente sconsigliato: l'azienda è troppo piccola e l'assenza di dati/esperienza rende l'investimento non conveniente.")
        motivi["crediti_sostenibilita"].append("Schema non adatto alle attuali dimensioni aziendali e al livello di maturità dei dati.")

    if is_piccola and not is_inesperta:
        punteggi["crediti_carbonio"] -= 30
        motivi["crediti_carbonio"].append("Le dimensioni aziendali ridotte limitano la fattibilità economica dei crediti di carbonio (sarebbe necessaria un'aggregazione).")

    if certificazioni_esistenti == "si":
        punteggi["bilancio_sostenibilita"] += 10
        punteggi["crediti_sostenibilita"] += 15
        motivi["crediti_sostenibilita"].append("L'esperienza pregressa con certificazioni facilita l'accesso a schemi complessi sulla sostenibilità.")

    if superficie_bosco > 0 or nuova_piantumazione > 0:
        punteggi["crediti_carbonio"] += 15
        if not is_piccola:
            motivi["crediti_carbonio"].append("Presenza di aree boscate o potenzialità di nuova piantumazione.")

    if superficie_agricola > 0:
        punteggi["crediti_sostenibilita"] += 10
        punteggi["inventario_emissioni"] += 10

    # Orizzonte temporale — CORREZIONE 21/09/2026 (proposta già condivisa, invariata)
    if orizzonte >= 20:
        punteggi["crediti_carbonio"] += 20
        motivi["crediti_carbonio"].append(
            "L'orizzonte dichiarato rispetta la soglia minima di 20 anni richiesta dal registro "
            "nazionale dei crediti di carbonio (decreto MASAF-MASE 17/10/2025)."
        )
    elif orizzonte >= 10:
        punteggi["crediti_carbonio"] -= 10
        motivi["crediti_carbonio"].append(
            "L'orizzonte dichiarato è inferiore alla soglia minima di 20 anni richiesta dal registro "
            "nazionale dei crediti di carbonio: un impegno più lungo lo renderebbe idoneo."
        )
    else:
        punteggi["crediti_carbonio"] -= 30
        motivi["crediti_carbonio"].append(
            "L'orizzonte dichiarato è troppo breve per soddisfare la soglia minima di 20 anni "
            "richiesta dal registro nazionale dei crediti di carbonio (decreto MASAF-MASE "
            "17/10/2025): il progetto non sarebbe idoneo alla registrazione allo stato attuale."
        )

    # ================= NOVITÀ V2 — TUTTE "[PROPOSTA]", DA VALIDARE =================

    # --- Fix bug "settore" (raccolto ma mai usato nell'originale) ---
    # AGGIORNAMENTO 23/09/2026: settore è ora un multi-select di codici ISIC
    # Rev.4 (Divisione 01 = agricolo, Divisione 02 = forestale), non più una
    # scelta singola — un'azienda può dichiarare codici di ENTRAMBE le
    # divisioni (es. azienda agroforestale). Per questo i due bonus sotto
    # NON sono più if/elif (mutuamente esclusivi come nell'originale a
    # scelta singola): un'azienda con codici in entrambe le divisioni riceve
    # entrambi i bonus, non solo uno.
    ha_codice_forestale = any(codice.startswith("02") for codice in settore)
    ha_codice_agricolo = any(codice.startswith("01") for codice in settore)

    if ha_codice_forestale:
        punteggi["crediti_carbonio"] += 10
        motivi["crediti_carbonio"].append(
            "Settore dichiarato (silvicoltura/attività forestali, ISIC Divisione 02) "
            "coerente con progetti di assorbimento di carbonio."
        )
    if ha_codice_agricolo:
        punteggi["inventario_emissioni"] += 5
        motivi["inventario_emissioni"].append(
            "Settore dichiarato (agricoltura/zootecnia, ISIC Divisione 01) rilevante "
            "per la mappatura delle emissioni di filiera."
        )

    # --- Superficie forestale (ha) — fasce (AGGIORNAMENTO 25/09/2026, su richiesta di Ana) ---
    # Il bonus originale (+15 se superficie_bosco>0 o nuova_piantumazione>0, sopra, INVARIATO)
    # resta. Qui si aggiunge un bonus ADDITIVO a fasce, ancorato a soglie reali di ettari usate da
    # standard di certificazione forestale/carbonio, così una proprietà molto piccola e una da
    # centinaia di ettari non ricevono più lo stesso trattamento binario. Soglie verificate
    # (settembre 2026):
    #   - Gold Standard, definizione "Smallholder" (Land Use & Forestry): proprietà ≤3 ha —
    #     https://globalgoals.goldstandard.org/standards/RU_2021-LUF-smallholder-definition.pdf
    #   - FSC SLIMF (Small and Low Intensity Managed Forests), soglia globale di default: <100 ha —
    #     https://connect.fsc.org/slimf-standard (i singoli Paesi possono adattarla; il valore
    #     nazionale italiano NON è stato verificato)
    #   - Gold Standard, definizione "Microscale" (Land Use & Forestry): area progetto ≤500 ha —
    #     stessa fonte RU 2021 sopra
    # NON VERIFICATO: la soglia italiana per il Piano di Gestione Forestale Semplificato (Testo
    # Unico Forestale, D.Lgs 34/2018) — il decreto attuativo demanda la soglia massima di superficie
    # alle Regioni, senza un numero nazionale unico; la soglia per l'Emilia-Romagna non è stata
    # reperita. Le fasce sotto NON la usano. Punteggi (5/10/15/20) sono una prima proposta di Ana,
    # non ancora validati da Michele — vedi scheda "Discussione con Michele e Lisa".
    if superficie_bosco > 3:
        if superficie_bosco <= 100:
            punteggi["crediti_carbonio"] += 5
            motivi["crediti_carbonio"].append(
                "Superficie forestale tra 3 e 100 ha (soglia SLIMF/FSC, default globale): "
                "piccola proprietà forestale, un'aggregazione tra più aziende resta generalmente "
                "necessaria per rendere conveniente la verifica di terza parte."
            )
        elif superficie_bosco <= 500:
            punteggi["crediti_carbonio"] += 10
            motivi["crediti_carbonio"].append(
                "Superficie forestale tra 100 e 500 ha (soglia \"microscale\" Gold "
                "Standard, Land Use & Forestry): proprietà di dimensione media, l'aggregazione può "
                "essere ancora utile ma la verifica individuale diventa più praticabile."
            )
        else:
            punteggi["crediti_carbonio"] += 15
            motivi["crediti_carbonio"].append(
                "Superficie forestale oltre 500 ha: dimensione compatibile con una "
                "verifica di terza parte individuale, senza necessità di aggregazione con altre "
                "proprietà."
            )
    elif superficie_bosco > 0:
        motivi["crediti_carbonio"].append(
            "Superficie forestale ≤3 ha (soglia \"smallholder\" Gold Standard, Land Use "
            "& Forestry): l'accesso ai crediti di carbonio è realistico solo tramite meccanismi di "
            "aggregazione/progetti di gruppo (es. Verra Grouped Projects) — nessun bonus di fascia "
            "aggiuntivo oltre al bonus di base."
        )

    # --- Fatturato annuo (soglie EU SME — fonte confermata; punteggio [PROPOSTA]) ---
    if fatturato_annuo is not None:
        if fatturato_annuo < 2_000_000:
            punteggi["bilancio_sostenibilita"] += 10
            motivi["bilancio_sostenibilita"].append(
                "Microimpresa (< 2 mln €, soglia EU SME): il Bilancio di Sostenibilità "
                "è il punto di partenza più accessibile."
            )
        elif fatturato_annuo >= 10_000_000:
            punteggi["crediti_carbonio"] += 5
            motivi["crediti_carbonio"].append(
                "Dimensione aziendale (≥ 10 mln €, soglia EU SME) compatibile con "
                "investimenti pluriennali."
            )

    # --- Numero dipendenti (soglie EU SME — fonte confermata; punteggio [PROPOSTA]) ---
    if numero_dipendenti is not None:
        if numero_dipendenti < 10:
            punteggi["bilancio_sostenibilita"] += 5
            motivi["bilancio_sostenibilita"].append(
                "Microimpresa (< 10 dipendenti, soglia EU SME)."
            )
        elif numero_dipendenti >= 50:
            punteggi["crediti_carbonio"] += 5
            motivi["crediti_carbonio"].append(
                "Struttura organizzativa (≥ 50 dipendenti) compatibile con progetti "
                "più complessi."
            )

    # --- Partecipazione a schemi ESG / ranking (EcoVadis, CDP, ecc.) ---
    if partecipazione_esg == "si":
        punteggi["crediti_sostenibilita"] += 15
        punteggi["bilancio_sostenibilita"] += 10
        motivi["crediti_sostenibilita"].append(
            "Partecipazione già attiva a schemi ESG/ranking di terze parti."
        )
    elif partecipazione_esg == "in_corso":
        punteggi["bilancio_sostenibilita"] += 5
        motivi["bilancio_sostenibilita"].append(
            "Partecipazione a schemi ESG in corso di valutazione."
        )

    # --- Tipo di certificazione posseduta (disaggregazione parziale di
    # certificazioni_esistenti) — SOLO versione/presentazione, NESSUN punteggio
    # aggiuntivo: il bonus resta quello del campo aggregato certificazioni_esistenti
    # sopra (nota ‡ della tabella). Qui il dato è solo raccolto in vista di una
    # futura disaggregazione da validare con Michele.
    if certificazione_tipo == "biologica":
        motivi["crediti_sostenibilita"].append(
            "Certificazione biologica (Reg. UE 2018/848)."
        )
    elif certificazione_tipo == "forestale":
        motivi["crediti_carbonio"].append(
            "Certificazione forestale (FSC o PEFC)."
        )
    elif certificazione_tipo == "entrambe":
        motivi["crediti_carbonio"].append(
            "Certificazione forestale E biologica: doppio "
            "standard già in atto."
        )

    # --- Piano di Gestione Forestale Sostenibile Certificato (FSC/PEFC) ---
    if piano_gestione_forestale == "si":
        punteggi["crediti_carbonio"] += 15
        motivi["crediti_carbonio"].append(
            "Piano di Gestione Forestale Certificato: spesso prerequisito nei "
            "protocolli di certificazione del carbonio forestale (dati PEFC 2025: +28% "
            "assorbimento medio rispetto a bosco non gestito)."
        )

    # --- Disponibilità dati sulla crescita della biomassa forestale ---
    _biomassa_punti = {"assenti": 0, "parziali": 5, "strutturati": 10}
    if dati_biomassa_forestale in _biomassa_punti and _biomassa_punti[dati_biomassa_forestale] > 0:
        punteggi["crediti_carbonio"] += _biomassa_punti[dati_biomassa_forestale]
        motivi["crediti_carbonio"].append(
            f"Dati sulla crescita della biomassa forestale: livello "
            f"'{dati_biomassa_forestale}'."
        )

    # --- Misurazione del Carbonio Organico del Suolo (SOC) ---
    _soc_punti = {"nessuna": 0, "base": 5, "avanzata": 10, "complessa": 15}
    if soc_misurazione in _soc_punti and _soc_punti[soc_misurazione] > 0:
        punteggi["crediti_sostenibilita"] += _soc_punti[soc_misurazione]
        motivi["crediti_sostenibilita"].append(
            f"Misurazione del Carbonio Organico del Suolo: livello "
            f"'{soc_misurazione}'."
        )

    # --- Indicatori di biodiversità (proxy qualitativo semplificato) ---
    _biodiv_punti = {"nessuno": 0, "qualitativo": 5, "sistematico": 15}
    if biodiversita_indicatori in _biodiv_punti and _biodiv_punti[biodiversita_indicatori] > 0:
        punteggi["crediti_sostenibilita"] += _biodiv_punti[biodiversita_indicatori]
        motivi["crediti_sostenibilita"].append(
            f"Monitoraggio di biodiversità: livello '{biodiversita_indicatori}'."
        )

    # --- Investimenti già effettuati in compensazione esterna ---
    if investimenti_compensazione_esterna == "si":
        punteggi["crediti_carbonio"] += 10
        motivi["crediti_carbonio"].append(
            "Esperienza pregressa in compensazione esterna: continuità naturale "
            "verso i Crediti di Carbonio."
        )
        # AGGIORNAMENTO 23/09/2026 (su richiesta di Ana): dettaglio testuale facoltativo
        # (progetto/area), SOLO presentazione, NESSUN punteggio aggiuntivo oltre al +10 sopra.
        if compensazione_esterna_dettaglio:
            motivi["crediti_carbonio"].append(
                "Dettaglio dichiarato: "
                f"{compensazione_esterna_dettaglio}"
            )

    # --- Esperienza pregressa in pratiche agroecologiche o certificazioni (Famiglia 5) —
    # disaggregazione parziale di certificazioni_esistenti (nota ‡ della tabella): SOLO
    # versione/presentazione, NESSUN punteggio aggiuntivo oltre al blocco certificazioni_esistenti
    # sopra. Le 3 fasce sono quelle già definite nella tabella Excel per questa riga. Campo
    # rinominato da esperienza_pratiche_rigenerative il 23/09/2026 ("agroecologica" è il termine
    # corretto per queste pratiche — richiesto da Ana).
    if esperienza_pratiche_agroecologiche == "pilota":
        motivi["crediti_sostenibilita"].append(
            "Pratiche agroecologiche in fase pilota: percorso "
            "già avviato, non ancora consolidato."
        )
    elif esperienza_pratiche_agroecologiche == "consolidata":
        motivi["crediti_sostenibilita"].append(
            "Esperienza consolidata in pratiche agroecologiche "
            "o schemi di certificazione: continuità pregressa concreta."
        )

    # --- Pratiche agroecologiche concrete — SOLO versione/presentazione, NESSUN punteggio.
    # Raccolto solo quando esperienza_pratiche_agroecologiche è "pilota" o "consolidata" (vedi
    # revealer nel form). AGGIORNAMENTO 23/09/2026: sostituiti i 13 Principi HLPE (troppo astratti
    # da "applicare" per un'azienda — es. "Governance della terra", "Equità", "Partecipazione" non
    # sono pratiche aziendali verificabili) con pratiche concrete e verificabili, tratte da FAO
    # TAPE Step 1/CAET (https://www.fao.org/agroecology/database/tape) e dagli eco-schemi PAC
    # 2023-2027 italiani (MASAF). Ogni pratica resta ricollegata al Principio HLPE più pertinente
    # solo a fini di tooltip/framing, non come voce di selezione.
    if pratiche_agroecologiche:
        etichette_pratiche = {
            "rotazione_colturale": "Rotazione delle colture",
            "cover_crop": "Copertura vegetale del suolo (cover crop / inerbimento)",
            "diversificazione_colturale": "Diversificazione colturale",
            "agroforestazione": "Agroforestazione",
            "riciclo_sostanza_organica": "Riciclo della sostanza organica (letame, compost, residui)",
            "riduzione_input_chimici": "Riduzione degli input chimici di sintesi",
            "sementi_locali": "Sementi o razze locali/aziendali",
            "benessere_animale": "Benessere animale e pascolo estensivo",
            "irrigazione_efficiente": "Gestione idrica efficiente",
            "fasce_impollinatori": "Fasce inerbite e habitat per impollinatori",
            "filiera_corta": "Filiera corta e vendita diretta",
            "paesaggio_tradizionale": "Conservazione del paesaggio agricolo tradizionale",
        }
        nomi_selezionati = [etichette_pratiche.get(codice, codice) for codice in pratiche_agroecologiche]
        motivi["crediti_sostenibilita"].append(
            "Pratiche agroecologiche concrete già applicate in "
            "azienda (FAO TAPE / eco-schemi PAC): " + ", ".join(nomi_selezionati) + "."
        )

    # --- Richiesta dati da clienti/capofiliera — SOLO versione/presentazione, nessun punteggio ---
    if richiesta_dati_clienti == "strutturata":
        motivi["bilancio_sostenibilita"].append(
            "I clienti richiedono dati strutturati (es. "
            "piattaforme certificate): il Bilancio verrà presentato in versione allineata a "
            "questi standard."
        )

    # --- Responsabile interno / team dedicato — SOLO versione/presentazione, nessun punteggio ---
    if responsabile_interno == "si":
        motivi["bilancio_sostenibilita"].append(
            "Presenza di un responsabile interno dedicato: "
            "maggiore prontezza organizzativa per l'implementazione."
        )

    # NON IMPLEMENTATO (richiede decisione di Michele/Lisa — vedi scheda Discussione):
    #   - finanziamenti_transizione: raccolto in futuro, ma la tabella lo segna come "Contesto —
    #     logica non ancora definita". Nessun punteggio finché non si decide il ruolo.
    #   - Nessuna disaggregazione di certificazioni_esistenti / dati_disponibili.

    # ================= MOTIVAZIONI (invariato) =================
    regole_motivazioni = {
        "vendita_crediti": [
            ("crediti_carbonio", 40, "Interesse esplicito per il mercato dei crediti di carbonio."),
            ("crediti_sostenibilita", 35, "Interesse a valorizzare i servizi ecosistemici sui mercati.")
        ],
        "compensazione": [
            ("inventario_emissioni", 35, "Prima di compensare è obbligatorio calcolare il proprio inventario delle emissioni."),
            ("crediti_carbonio", 10, "Potenziale interesse a sviluppare progetti di compensazione in-house.")
        ],
        "report_sostenibilita": [
            ("bilancio_sostenibilita", 45, "Obiettivo primario coincidente con lo strumento del Bilancio di Sostenibilità.")
        ],
        "misurare_emissioni": [
            ("inventario_emissioni", 45, "Perfetta aderenza all'obiettivo di misurazione della Carbon Footprint.")
        ],
        "riduzione_emissioni": [
            ("inventario_emissioni", 30, "L'inventario è il punto di partenza per ogni piano di riduzione emissiva.")
        ],
        "gestione_sostenibile": [
            ("bilancio_sostenibilita", 25, "Il bilancio permette di rendicontare al meglio la gestione sostenibile intraprese."),
            ("crediti_sostenibilita", 15, "Possibilità di convertire le buone pratiche in crediti riconosciuti.")
        ],
        "richiesta_clienti": [
            ("bilancio_sostenibilita", 25, "Ottimo strumento per rispondere alle esigenze di trasparenza della filiera."),
            ("inventario_emissioni", 20, "Spesso la filiera richiede i dati sulle emissioni (Scope 3 dei clienti).")
        ],
        "reputazione": [
            ("bilancio_sostenibilita", 30, "Il Bilancio ESG è lo strumento principe per il ritorno reputazionale.")
        ],
        "biodiversita": [
            ("crediti_sostenibilita", 40, "Forte allineamento con gli obiettivi di valorizzazione della biodiversità.")
        ]
    }

    for motivazione in motivazioni:
        for schema, punti, testo in regole_motivazioni.get(motivazione, []):
            punteggi[schema] += punti
            if testo not in motivi[schema]:
                motivi[schema].append(testo)

    # Dati e Budget (invariato)
    if dati_disponibili == "alti":
        punteggi["inventario_emissioni"] += 15
        punteggi["crediti_carbonio"] += 15
    elif dati_disponibili == "bassi":
        punteggi["inventario_emissioni"] -= 10
        motivi["inventario_emissioni"].append("Richiederà uno sforzo iniziale per l'impostazione della raccolta dati.")

    if budget == "alto":
        punteggi["crediti_carbonio"] += 20
        punteggi["crediti_sostenibilita"] += 20
    elif budget == "basso":
        punteggi["crediti_carbonio"] -= 20
        punteggi["crediti_sostenibilita"] -= 20
        punteggi["bilancio_sostenibilita"] += 10
        motivi["bilancio_sostenibilita"].append("Percorso affrontabile anche con budget limitati.")

    # Calcolo Finale
    risultati = []
    for chiave, valore in punteggi.items():
        percentuale = round(clamp(valore, 0, 100))
        risultati.append(
            {
                "chiave": chiave,
                "compatibilita": percentuale,
                "motivi": motivi[chiave][:6],  # limite alzato a 6 per mostrare anche le novità v2 in demo
                **SCHEMI[chiave],
            }
        )

    risultati.sort(key=lambda x: x["compatibilita"], reverse=True)
    return risultati


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index2.html",
        context={"result": None, "error": None, "form": {}},
    )


@app.post("/valuta", response_class=HTMLResponse)
async def valuta(
    request: Request,
    settore: List[str] = Form(default=[]),
    superficie_totale: float = Form(...),
    superficie_bosco: float = Form(0),
    superficie_agricola: float = Form(0),
    superficie_altra: float = Form(0),
    nuova_piantumazione: float = Form(0),
    motivazioni: List[str] = Form(default=[]),
    dati_disponibili: str = Form(...),
    orizzonte: float = Form(...),
    budget: str = Form(...),
    certificazioni_esistenti: str = Form(...),
    # campi nuovi v2 — opzionali, il form attuale non li invia e va bene così.
    # fatturato_annuo/numero_dipendenti arrivano come str e vengono convertiti a
    # mano sotto: un <input type="number"> lasciato vuoto invia "" al server, e
    # "" non è un float valido — Optional[float] = Form(None) darebbe errore 422
    # in quel caso. Con str si evita il crash e si tratta "" come "non compilato".
    fatturato_annuo: Optional[str] = Form(None),
    numero_dipendenti: Optional[str] = Form(None),
    partecipazione_esg: Optional[str] = Form(None),
    certificazione_tipo: Optional[str] = Form(None),
    piano_gestione_forestale: Optional[str] = Form(None),
    dati_biomassa_forestale: Optional[str] = Form(None),
    soc_misurazione: Optional[str] = Form(None),
    biodiversita_indicatori: Optional[str] = Form(None),
    investimenti_compensazione_esterna: Optional[str] = Form(None),
    compensazione_esterna_dettaglio: Optional[str] = Form(None),
    esperienza_pratiche_agroecologiche: Optional[str] = Form(None),
    pratiche_agroecologiche: List[str] = Form(default=[]),
    richiesta_dati_clienti: Optional[str] = Form(None),
    responsabile_interno: Optional[str] = Form(None),
    finanziamenti_transizione: Optional[str] = Form(None),
    # AGGIUNTO 25/09/2026 su richiesta di Ana: collega il criterio "Disponibilità
    # di dati per la misurazione delle emissioni di CO2 (Scopo 1, 2 e 3)" — vedi
    # motore_pesi.py CRITERI["misurazione_scope_ghg"]. Usato SOLO dal motore a
    # pesi: la LOGICA ORIGINALE (valuta_percorsi) continua a usare solo
    # dati_disponibili, invariata.
    misurazione_scope_ghg: Optional[str] = Form(None),
):
    form = {
        "settore": settore,
        "superficie_totale": superficie_totale,
        "superficie_bosco": superficie_bosco,
        "superficie_agricola": superficie_agricola,
        "superficie_altra": superficie_altra,
        "nuova_piantumazione": nuova_piantumazione,
        "motivazioni": motivazioni,
        "dati_disponibili": dati_disponibili,
        "orizzonte": orizzonte,
        "budget": budget,
        "certificazioni_esistenti": certificazioni_esistenti,
        "certificazione_tipo": certificazione_tipo,
        "partecipazione_esg": partecipazione_esg,
        "investimenti_compensazione_esterna": investimenti_compensazione_esterna,
        "compensazione_esterna_dettaglio": compensazione_esterna_dettaglio,
        "esperienza_pratiche_agroecologiche": esperienza_pratiche_agroecologiche,
        "pratiche_agroecologiche": pratiche_agroecologiche,
        "misurazione_scope_ghg": misurazione_scope_ghg,
    }

    valori_superficie = [superficie_totale, superficie_bosco, superficie_agricola, superficie_altra, nuova_piantumazione]

    if orizzonte < 0:
        return templates.TemplateResponse(
            request=request, name="index2.html",
            context={"result": None, "error": "L'orizzonte temporale non può essere negativo.", "form": form},
            status_code=400,
        )

    if any(v < 0 for v in valori_superficie):
        return templates.TemplateResponse(
            request=request, name="index2.html",
            context={"result": None, "error": "Le superfici non possono assumere valori negativi.", "form": form},
            status_code=400,
        )

    somma_superfici = superficie_bosco + superficie_agricola + superficie_altra
    if somma_superfici > superficie_totale + 0.01:
        return templates.TemplateResponse(
            request=request, name="index2.html",
            context={"result": None, "error": "La somma parziale delle superfici supera la superficie aziendale totale.", "form": form},
            status_code=400,
        )

    if not motivazioni:
        return templates.TemplateResponse(
            request=request, name="index2.html",
            context={"result": None, "error": "Selezionare almeno una motivazione per proseguire.", "form": form},
            status_code=400,
        )

    if not settore:
        return templates.TemplateResponse(
            request=request, name="index2.html",
            context={"result": None, "error": "Selezionare almeno un codice ISIC del settore prevalente.", "form": form},
            status_code=400,
        )

    def _parse_float_opzionale(valore: Optional[str]) -> Optional[float]:
        """Converte '' o None in None; una stringa numerica valida nel suo float."""
        if valore is None or valore.strip() == "":
            return None
        try:
            return float(valore)
        except ValueError:
            return None

    fatturato_annuo_num = _parse_float_opzionale(fatturato_annuo)
    numero_dipendenti_num = _parse_float_opzionale(numero_dipendenti)

    risultati = valuta_percorsi(
        settore=settore, superficie_totale=superficie_totale, superficie_bosco=superficie_bosco,
        superficie_agricola=superficie_agricola, superficie_altra=superficie_altra,
        nuova_piantumazione=nuova_piantumazione, motivazioni=motivazioni,
        dati_disponibili=dati_disponibili, orizzonte=orizzonte, budget=budget,
        certificazioni_esistenti=certificazioni_esistenti,
        fatturato_annuo=fatturato_annuo_num, numero_dipendenti=numero_dipendenti_num,
        partecipazione_esg=partecipazione_esg,
        certificazione_tipo=certificazione_tipo,
        piano_gestione_forestale=piano_gestione_forestale,
        dati_biomassa_forestale=dati_biomassa_forestale, soc_misurazione=soc_misurazione,
        biodiversita_indicatori=biodiversita_indicatori,
        investimenti_compensazione_esterna=investimenti_compensazione_esterna,
        compensazione_esterna_dettaglio=compensazione_esterna_dettaglio,
        esperienza_pratiche_agroecologiche=esperienza_pratiche_agroecologiche,
        pratiche_agroecologiche=pratiche_agroecologiche,
        richiesta_dati_clienti=richiesta_dati_clienti, responsabile_interno=responsabile_interno,
        finanziamenti_transizione=finanziamenti_transizione,
    )

    profilo = {
        "superficie_totale": superficie_totale,
        "superficie_bosco": superficie_bosco,
        "superficie_agricola": superficie_agricola,
        "superficie_altra": superficie_altra,
        "nuova_piantumazione": nuova_piantumazione,
        # settore è ora una lista di codici ISIC — mostriamo le etichette leggibili, non i codici grezzi
        "settore": ", ".join(ISIC_LABELS.get(codice, codice) for codice in settore),
    }

    # ---- Motore a pesi 1-4 (AGGIUNTO 25/09/2026, additivo — vedi motore_pesi.py) ----
    # Usa un dizionario a parte con gli stessi nomi di campo del form: non riusa `form`
    # sopra perché quel dict tiene solo i campi rilevanti per il ri-popolamento del
    # form in caso di errore, non tutti i campi che il motore a pesi usa.
    form_pesi = {
        "settore": settore,
        "superficie_totale": superficie_totale,
        "superficie_bosco": superficie_bosco,
        "nuova_piantumazione": nuova_piantumazione,
        "superficie_agricola": superficie_agricola,
        "orizzonte": orizzonte,
        "budget": budget,
        "certificazioni_esistenti": certificazioni_esistenti,
        "certificazione_tipo": certificazione_tipo,
        "fatturato_annuo": fatturato_annuo_num,
        "numero_dipendenti": numero_dipendenti_num,
        "partecipazione_esg": partecipazione_esg,
        "piano_gestione_forestale": piano_gestione_forestale,
        "richiesta_dati_clienti": richiesta_dati_clienti,
        "dati_biomassa_forestale": dati_biomassa_forestale,
        "soc_misurazione": soc_misurazione,
        "biodiversita_indicatori": biodiversita_indicatori,
        "investimenti_compensazione_esterna": investimenti_compensazione_esterna,
        "esperienza_pratiche_agroecologiche": esperienza_pratiche_agroecologiche,
        "finanziamenti_transizione": finanziamenti_transizione,
        "responsabile_interno": responsabile_interno,
        "misurazione_scope_ghg": misurazione_scope_ghg,
    }
    risultati_pesi = valuta_percorsi_pesi(form_pesi)
    # arricchisce ciascun percorso con titolo/icona (SCHEMI) per il template, senza
    # toccare la struttura ritornata da valuta_percorsi_pesi (usata anche nei test)
    risultati_pesi_display = []
    for chiave in ("crediti_carbonio", "crediti_sostenibilita", "bilancio_sostenibilita", "inventario_emissioni"):
        dati = risultati_pesi["percorsi"][chiave]
        risultati_pesi_display.append({"chiave": chiave, **dati, **SCHEMI[chiave]})
    risultati_pesi_display.sort(
        key=lambda x: (x["percentuale"] is None, -(x["percentuale"] or 0))
    )

    return templates.TemplateResponse(
        request=request,
        name="index2.html",
        context={
            "result": risultati, "profilo": profilo, "error": None, "form": form,
            "risultati_pesi": risultati_pesi_display,
            "risultati_pesi_dettaglio": risultati_pesi["dettaglio"],
            "risultati_pesi_non_collegati": risultati_pesi["criteri_non_collegati"],
        },
    )
