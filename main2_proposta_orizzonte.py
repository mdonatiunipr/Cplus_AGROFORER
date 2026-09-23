from pathlib import Path
from typing import List
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="DST Sostenibilità e Carbonio v2",
    description="Strumento avanzato per l'orientamento agli schemi di certificazione ESG e Carbon.",
    version="2.0.0",
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Limite a 4 schemi come richiesto, con schede di presentazione sintetica
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
    settore: str,
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
):
    punteggi = {chiave: 20.0 for chiave in SCHEMI} # Base di partenza
    motivi = {chiave: [] for chiave in SCHEMI}

    # Analisi dimensionali e di esperienza (Core Business Logic per PMI/Neofiti)
    # Soglia <15ha: CONFERMATA dal team di progetto (Ana Barezi, 21/09/2026) sulla base dei casi
    # reali seguiti nel progetto — al di sotto di questa soglia i crediti di carbonio non sono
    # economicamente viabili in autonomia (sarebbe necessaria un'aggregazione tra più aziende).
    # Non è più una soglia arbitraria senza fonte: da ridiscutere con Michele solo se emergono
    # nuovi casi che la contraddicono.
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

    # Superfici e settori
    if superficie_bosco > 0 or nuova_piantumazione > 0:
        punteggi["crediti_carbonio"] += 15
        if not is_piccola:
            motivi["crediti_carbonio"].append("Presenza di aree boscate o potenzialità di nuova piantumazione.")
            
    if superficie_agricola > 0:
        punteggi["crediti_sostenibilita"] += 10
        punteggi["inventario_emissioni"] += 10

    # Orizzonte temporale dell'impegno (anni) — CORREZIONE 21/09/2026: il campo era raccolto nel
    # form ma non veniva mai usato qui (bug segnalato da Ana Barezi). Soglia esterna: il registro
    # nazionale dei crediti di carbonio (decreto interministeriale MASAF-MASE 17/10/2025, gestito
    # da CREA) richiede un impegno minimo di 20 anni per i progetti forestali di carbonio.
    # NB: i valori di bonus/malus sotto sono una PRIMA PROPOSTA (Ana Barezi) — da validare con
    # Michele prima di considerarli definitivi; solo la soglia dei 20 anni ha fonte esterna certa.
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

    # Motivazioni
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

    # Dati e Budget
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
                "motivi": motivi[chiave][:4], # Limite a 4 motivazioni per pulizia UI
                **SCHEMI[chiave],
            }
        )

    # Ordinamento per compatibilità decrescente
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
    settore: str = Form(...),
    superficie_totale: float = Form(...),
    superficie_bosco: float = Form(0),
    superficie_agricola: float = Form(0),
    superficie_altra: float = Form(0),
    nuova_piantumazione: float = Form(0),
    motivazioni: List[str] = Form(default=[]),
    dati_disponibili: str = Form(...),
    orizzonte: float = Form(...),  # CORREZIONE 21/09/2026: era str e mai usato; ora anni dichiarati
    budget: str = Form(...),
    certificazioni_esistenti: str = Form(...),
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

    risultati = valuta_percorsi(
        settore=settore, superficie_totale=superficie_totale, superficie_bosco=superficie_bosco,
        superficie_agricola=superficie_agricola, superficie_altra=superficie_altra,
        nuova_piantumazione=nuova_piantumazione, motivazioni=motivazioni,
        dati_disponibili=dati_disponibili, orizzonte=orizzonte, budget=budget,
        certificazioni_esistenti=certificazioni_esistenti,
    )

    profilo = {
        "superficie_totale": superficie_totale,
        "superficie_bosco": superficie_bosco,
        "superficie_agricola": superficie_agricola,
        "superficie_altra": superficie_altra,
        "nuova_piantumazione": nuova_piantumazione,
        "settore": settore.capitalize()
    }

    return templates.TemplateResponse(
        request=request,
        name="index2.html",
        context={"result": risultati, "profilo": profilo, "error": None, "form": form},
    )
