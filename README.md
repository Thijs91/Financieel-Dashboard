# Bank Export Categorisatie Tool en Dashboard

Een privacy-vriendelijke, lokale (web)applicatie om banktransacties (CSV) te visualiseren. Het project is **100% Privacy** vriendelijk. Je bankgegevens verlaten nooit je PC en er zijn geen servers en/of cloud-opslag nodig nadat je de bankgegevens hebt gedownload. De (web)applicatie draait lokaal en ook offline.
  

Dit project bevat een Python-script en een categorisatiebestand om banktransacties automatisch te categoriseren. Het script leest een CSV-bestand met banktransacties, past categorisatieregels toe, en exporteert het resultaat in een gestructureerd formaat.   

## Bestanden

### 1. `Categorie toekenning Bank.py`

Dit Python-script voert de volgende stappen uit:

- **Laden van categorisatieregels**: Leest het `Categorie.md`-bestand en parseert de regels voor categorisatie.
- **Laden van banktransacties**: Leest een CSV-bestand met banktransacties en detecteert automatisch de kolommen.
- **Normaliseren van omschrijvingen**: Maakt omschrijvingen van transacties uniform voor betere matching.
- **Categoriseren van transacties**: Past verschillende matching-strategieën toe om transacties te categoriseren:
  - Exacte match op canonical naam
  - Exacte match op aliases
  - Woord-boundary match
  - Substring match
  - Partial word match
  - Fuzzy match (met drempelwaarde)
  - IBAN match (fallback)
- **Exporteren van resultaten**: Slaat de gecategoriseerde transacties op in CSV-bestanden.

### 2. `Categorie.md`

Dit bestand bevat de categorisatieregels in een gestructureerd formaat. Elke regel definieert een categorie, subcategorie, detail, canonical naam, en optionele aliases. Het bestand is ingedeeld in secties voor verschillende soorten uitgaven, zoals:

- **Bank kosten**: Kosten voor rekeningen en incasso's.
- **Huishouden**: Interne overboekingen, boodschappen, en huishoudelijke uitgaven.
- **Zorg**: Vergoedingen en zorgkosten.
- **Belastingen**: Gemeentelijke, regionale, en nationale belastingen.
- **Kinderopvang**: Toeslagen en bijdragen voor kinderopvang.
- **Verzekeringen & Hypotheek**: Hypotheek en verzekeringskosten.
- **Utiliteiten & Abonnementen**: Energie, internet, streamingdiensten, en abonnementen.
- **Verzorging & Drogisterij**: Uitgaven aan drogisterijen en kappers.
- **Supermarkten**: Uitgaven aan verschillende supermarkten.
- **Bakkers / Slagers / Kaas / Overig boodschappen**: Specifieke boodschappen.
- **Huis, Tuin & Dier**: Uitgaven aan bouwmaterialen, tuinartikelen, en dierenbenodigdheden.
- **Auto / Tanken / Laden**: Kosten voor parkeren, wasstraten, onderhoud, laden, en tanken.
- **OV / Mobiliteit**: Openbaar vervoer en taxi's.
- **Kleding & Mode**: Kleding, schoenen, en accessoires.
- **Elektronica / Winkels**: Aankopen van elektronica en meubels.
- **Horeca & Fastfood**: Uitgaven aan restaurants, cafés, en fastfood.
- **Logistiek**: Kosten voor pakketdiensten.
- **Uitjes**: Uitgaven aan musea en andere uitjes.
- **Overig**: Diverse andere uitgaven.

## Gebruik

1. **Instellingen**: Pas de bestandslocaties aan in het Python-script:
   - `csv_bank_path`: Locatie van het CSV-bestand met banktransacties.
   - `categorisatie_path`: Locatie van het `Categorie.md`-bestand.
   - `export_dir`: Locatie waar de resultaten worden opgeslagen.

2. **Uitvoeren**: Voer het script uit om de transacties te categoriseren en de resultaten te exporteren.

3. **Resultaten**: De gecategoriseerde transacties worden opgeslagen in CSV-bestanden in de opgegeven exportdirectory.

## Voorbeeld

Een voorbeeld van een categorisatieregel in `Categorie.md`:

```csv
Huishouden;Boodschappen;Supermarkt;albert heijn;ah,appie
```

Dit betekent:
- **Categorie**: Huishouden
- **Subcategorie**: Boodschappen
- **Detail**: Supermarkt
- **Canonical naam**: albert heijn
- **Aliassen**: ah, appie

Transacties met omschrijvingen die overeenkomen met "albert heijn", "ah", of "appie" worden gecategoriseerd onder "Huishouden > Boodschappen > Supermarkt".

## Dashboard

Het project bevat ook een `Dashboard.html`-bestand dat een interactief financieel dashboard biedt. Dit dashboard biedt de volgende functionaliteiten:

- **Financieel Overzicht**: Visualiseert inkomsten en uitgaven per maand met behulp van grafieken.
- **Categorisatie Analyse**: Toont een verdeling van uitgaven per categorie in een cirkeldiagram.
- **Geïmporteerde Data**: Laat de ruwe transactiegegevens zien in een tabelvorm.
- **Periode Selectie**: Gebruik een slider om een specifieke periode te selecteren voor analyse.
- **Thema Ondersteuning**: Schakel tussen licht en donker thema voor betere leesbaarheid.

### Gebruik van het Dashboard

1. **Uploaden van Data**: Laad een CSV-bestand met gecategoriseerde transacties om het dashboard te vullen.
2. **Analyse**: Bekijk de grafieken en tabellen voor inzicht in je financiële gegevens.
3. **Exporteren**: Gebruik de knoppen om de gegevens te exporteren of af te drukken.

Meer informatie over het dashboard zie `README_Dashboard.md`

## Licentie

Dit project is bedoeld voor persoonlijk gebruik en kan vrij worden aangepast en uitgebreid.   

Dit project is beschikbaar onder de MIT-licentie.
