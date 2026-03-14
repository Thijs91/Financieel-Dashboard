# Interactive Bank Dashboard

Een privacy-vriendelijke, lokaal-eerst webapplicatie om banktransacties (CSV) te visualiseren. Dit dashboard vervangt traditionele Excel draaitabellen door een moderne, interactieve interface die volledig in de browser draait.

## Belangrijkste Functies

- **100% Privacy:** Je bankgegevens verlaten nooit je browser. Geen servers, geen cloud-opslag.
- **Interactieve Pivot Tabel:** Navigeer door je uitgaven via een uitklapbare hiërarchie (Categorie > Subcategorie > Detail).
- **Financiële Trends:** Visuele weergave van inkomsten vs. uitgaven en categorieverdelingen via Chart.js.
- **Periode Filtering:** Selecteer eenvoudig specifieke maanden via een interactieve tijd-slider.
- **Dark & Light Mode:** Volledige ondersteuning voor zowel lichte als donkere thema's.
- **PDF Export:** Genereer een schoon financieel overzicht (zonder ruwe gegevens) voor je eigen administratie.

### Interactieve Pivot Tabel
De tabel in het tabblad **"Financieel Overzicht"** is hiërarchisch opgebouwd. Klik op de pijl (`▸`) voor een categorie om de subcategorieën en details uit te klappen. Onderaan de tabel vind je het **Netto Resultaat** per maand (Inkomsten + Uitgaven).

### Periode Slider
Nadat de gegevens zijn ingeladen, verschijnt er een slider. Hiermee kun je het tijdsbereik aanpassen. De grafieken en de tabel worden direct bijgewerkt wanneer je de slider verschuift.

### PDF Export
Gebruik de knop **"Exporteer PDF"** rechtsboven om een printvriendelijke versie van je overzicht te maken. De ruwe transactiegegevens worden automatisch weggelaten uit de export voor een schoon overzicht.


## Gebruik

Er is geen installatie of backend nodig.

1.  Download de repository of kopieer de bestanden.
2.  Open `Dashboard.html` in een moderne webbrowser (Chrome, Firefox, Edge).
3.  Upload je gecategoriseerde CSV-bestand.

## CSV-Specificaties

Het dashboard verwacht een **puntkomma-gescheiden (`;`)** CSV-bestand met minimaal de volgende kolommen in de kopregel:

| Veldnaam | Status | Beschrijving | Voorbeeld |
| :--- | :--- | :--- | :--- |
| **Datum** | **Verplicht** | Transactiedatum (`D-M-YYYY` of `DD-MM-YYYY`). | `15-03-2026` |
| **Bedrag** | **Verplicht** | De financiële waarde (gebruik `,` of `.` voor decimalen). | `-45,50` of `1200.00` |
| **Categorie** | Optioneel* | De hoofdgroep voor de pivot-tabel en grafieken. | `Vaste lasten` |
| **Subcategorie** | Optioneel* | Het tweede niveau in de hiërarchie. | `Huur` |
| **Detail** | Optioneel* | Het diepste niveau (bijv. de winkel of omschrijving). | `Woningbouwvereniging` |

*\* Indien deze velden ontbreken, worden transacties gegroepeerd onder "Ongecategoriseerd" of "--".*

#### Verder relevant:
*   **Duizendtal-scheiding:** Gebruik **geen** scheidingsteken voor duizendtallen (`1200,50` in plaats van `1.200,50`).
*   **Lege regels:** Deze worden automatisch overgeslagen tijdens het inladen.


## Gebruikte Technologieën

- **Vanilla JS/HTML5/CSS3:** Geen frameworks nodig voor maximale snelheid en eenvoud.
- **[PapaParse](https://www.papaparse.com/):** Voor snelle en robuuste CSV-verwerking.
- **[Chart.js](https://www.chartjs.org/):** Voor interactieve grafieken.
- **[noUiSlider](https://refreshless.com/nouislider/):** Voor de tijd-range slider.

## Privacy & Veiligheid

Omdat dit een statische HTML-applicatie is, is er geen risico op datalekken via een server. Alle verwerking vindt plaats in het werkgeheugen (RAM) van je eigen computer. Zodra je de tab sluit, worden de data uit het geheugen gewist.

## Licentie

Dit project is bedoeld voor persoonlijk gebruik en kan vrij worden aangepast en uitgebreid.   

Dit project is beschikbaar onder de MIT-licentie.

