# CATEGORISATIEBESTAND
>Formaat per regel: categorie;subcategorie;detail;canonical;alias      
>Meerdere aliassen scheiden met een komma.  
>Commentaarregels (# …) worden genegeerd.


# ===========================
# BASIS / BANK / INCASSO
# ===========================
```csv
Bank kosten;Roodstand;--;roodstand
Bank kosten;Betaalrekening;--;kosten gebruik betaalrekening
```
# ===========================
# HUISHOUDEN / INTERN (vrije tekst overboekingen)
# ===========================
```csv
Huishouden;Intern;Gezamenlijke kosten - Bijdrage ABBA;gemeenschappelijke kosten;gemeenschappelijke kosten
Huishouden;Intern;Gezamenlijke kosten - Bijdrage PINK;huishoud geld; huishoudgeld, huishoud

Huishouden;Intern;Spaarrekening;IBAN

Huishouden;Intern;Bijdrage ABBA;IBAN
Huishouden;Intern;Bijdrage PINK;IBAN
```

# ===========================
# ZORG
# ===========================
```csv
Zorg;Vergoeding;--;vergoeding;vergoedingen
```

# ===========================
# BELASTINGEN
# ===========================
```csv
Belastingen;Gemeente;--;gemeentelijke belastingen
Belastingen;Regionale Belasting Groep;--;IncassoID
Belastingen;Wegenbelasting;Auto;Kenteken;IncassoID
Belastingen;Belastingdienst;--;belastingdienst;bd belastingdienst,teruggave belastingdienst,belasting teruggave
```

# ===========================
# KINDEROPVANG
# ===========================
```csv
Kinderen;Kinderopvang;Toeslag;kinderopvangtoeslag;voorschot kinderopvangtoeslag,kinderopvangtoeslag voorschot,kinderopvangtoeslag,kinderopvangtoeslag berekening definitief
Kinderen;Kinderopvang;ZwartGat;IncassoID;ZwartGat;zwart gat
Kinderen;Kinderopvang;Bijdrage kinderopvang;kinderopvang;kinderopvang bijdrage,aanvulling kinderopvang tbv,voor kinderopvang,t.b.v. kinderopvang

Kinderen;Kinderbijslag;SVB;svb;sociale verzekeringsbank,kinderbijslag
```

# ===========================
# VERZEKERINGEN & HYPOTHEEK
# ===========================
```csv
Hypotheek;Hypotheek;hypotheek;IncassoID;hypotheek
Hypotheek;Hypotheek;Hypotheek (intern);hypotheekdeel;hypotheekdeel,hypotheek deel

Verzekering;Woonverzekering;--;woonverzekering
Verzekering;Rechtsbijstand;--;rechtsbijstand
```

# ===========================
# UTILITEITEN / ABONNEMENTEN
# ===========================
```csv
Utiliteit;Energie;Coolblue Energie;coolblue energie

Abonnement;Internet/Mobiel;KPN;kpn;kpn.com,kpn factuur
Abonnement;Internet/Mobiel;Ziggo;ziggo;ziggo.com,ziggo factuur
Abonnement;Internet/Mobiel;vodafoon;vodafoon;vodafoon.com,vodafoon factuur

Abonnement;Streaming;Video-HBO;hbo max;hbomax
Abonnement;Streaming;Video-Netflix;netflix
Abonnement;Krant;Trouw;trouw
Abonnement;Krant;NRC;NRC
```

# ===========================
# VERZORGING & DROGISTERIJ
# ===========================
```csv
Verzorging;Drogist;Etos;etos
Verzorging;Drogist;Kruidvat;kruidvat

Verzorging;Kapper;Overig;kapper;kapper
```

# ===========================
# SUPERMARKTEN
# ===========================
```csv
Huishouden;Boodschappen;Supermarkt;albert heijn;ah,appie
Huishouden;Boodschappen;Supermarkt;lidl
Huishouden;Boodschappen;Supermarkt;aldi
Huishouden;Boodschappen;Supermarkt;dirk vd broek;dirk
Huishouden;Boodschappen;Supermarkt;jumbo
Huishouden;Boodschappen;Supermarkt;plus
Huishouden;Boodschappen;Supermarkt;coop
Huishouden;Boodschappen;Supermarkt;spar
Huishouden;Boodschappen;Supermarkt;deen
Huishouden;Boodschappen;Supermarkt;edah
Huishouden;Boodschappen;Supermarkt;poiesz
```

# ===========================
# BAKKERS / SLAGERS / KAAS / OVERIG BOODSCHAPPEN
# ===========================
```csv
Huishouden;Boodschappen;Bakker;bakkerij 't stoepje;stoepje
Huishouden;Boodschappen;Slager;keurslager
Huishouden;Boodschappen;Kaasboer;kaasboer
Huishouden;Boodschappen;Kaasboer;Kaaswaag
Huishouden;Boodschappen;Boerderijwinkel;boerderijwinkel
Huishouden;Boodschappen;Eieren;sumup

Huishouden;Boodschappen;Groothandel;sligro
Huishouden;Boodschappen;Groothandel;hanos
Huishouden;Boodschappen;Groothandel;makro

Huishouden;Boodschappen;Overig;boodschappen

Huishouden;Schrijfgerij;Bruna;bruna
```

# ===========================
# HUIS, TUIN & DIER
# ===========================
```csv
Huis;Huis;Bouwmateriaal;Bauhaus;bauhaus
Huis;Huis;Bouwmateriaal;Hornbach;hornbach
Huis;Huis;Bouwmateriaal;Toolstation;toolstation
Huis;Huis;Bouwmateriaal;Gamma;gamma
Huis;Huis;Bouwmateriaal;Praxis;praxis
Huis;Huis;Bouwmateriaal;Karwei;Karwei

Huis;Dieren;Pets Place;pets place

Huis;Tuin;Welkoop;welkoop
Huis;Tuin;Intratuin;intratuin
Huis;Tuin;Aveve;aveve
```

# ===========================
# AUTO / TANKEN / LADEN
# ===========================
```csv
Auto;Parkeren;YellowBrick;IncassoID
Auto;Parkeren;Parkeren - overig;parkeren;pargeergarage
Auto;Wasstraat;Washers;Washers
Auto;Wasstraat;Carwash Plus;carwashplus

Auto;Onderhoud;Partspoint;partspoint
Auto;Onderhoud;ANWB;anwb
Auto;Onderhoud;Wittebrug;wittebrug

Auto;Laden;Shell;IncassoID;recharge
Auto;Laden;Allego;allego
Auto;Laden;Fastned;fastned
Auto;Laden;Ionity;ionity
Auto;Laden;Greenflux;greenflux
Auto;Laden;Tesla;tesla

Auto;Tanken;Shell;shell
Auto;Tanken;BP;bp
Auto;Tanken;Total;totalenergies;total
Auto;Tanken;Esso;esso
Auto;Tanken;Texaco;texaco
Auto;Tanken;Q8;q8
Auto;Tanken;Avia;avia
Auto;Tanken;TanQ;tanqyou;tanq
Auto;Tanken;Tamoil;tamoil
```

# ===========================
# OV / MOBILITEIT
# ===========================
```csv
Vervoer;OV;NS;ns;nsnl
Vervoer;OV;Eurostar;eurostar
Vervoer;OV;RET;ret
Vervoer;OV;HTM;htm
Vervoer;OV;GVB;gvb
Vervoer;OV;Arriva;arriva
Vervoer;OV;Connexxion;connexxion
Vervoer;OV;Flixbus;flixbus;flix

Vervoer;Taxi;Uber;uber
Vervoer;Taxi;Bolt;bolt
Vervoer;Taxi;Lyft;lyft
```

# ===========================
# KLEDING & MODE
# ===========================
```csv
Kleding;Mode;--;hm;h&m
Kleding;Mode;--;we fashion
Kleding;Mode;--;zara
Kleding;Mode;--;primark
Kleding;Mode;--;bershka
Kleding;Mode;--;pull and bear;pull&bear
Kleding;Mode;--;c&a;ca
Kleding;Mode;--;scotch & soda
Kleding;Mode;--;jack & jones;jackjones
Kleding;Mode;--;vero moda

Kleding;Warenhuis;Hema;hema
Kleding;Warenhuis;Zeeman;zeeman

Kleding;Lingerie;Hunkemoller;hunkemoller;hunkemoeller

Kleding;Schoenen;--;van haren
Kleding;Schoenen;--;footlocker
Kleding;Schoenen;--;sacha
Kleding;Schoenen;Nelson;nelson

Kleding;Tweedehands;Vinted;vinted

Kleding;Sport;Decathlon;decathlon
Kleding;Sport;Intersport;intersport
Kleding;Sport;Aktie Sport;aktiesport
Kleding;Sport;Daka;daka
Kleding;Sport;Sport2000;sport2000

```

# ===========================
# ELEKTRONICA / WINKELS
# ===========================
```csv
Elektronica;Aankopen;Mediamarkt;mediamarkt;media markt
Elektronica;Aankopen;CoolBlue;coolblue
Elektronica;Aankopen;Expert;expert
Elektronica;Aankopen;BCC;bcc
Elektronica;Aankopen;Apple Store;apple store
Elektronica;Aankopen;Google Store;google store
Elektronica;Aankopen;Kijkshop;kijkshop

Huishouden;Meubels;Ikea;ikea
```

# ===========================
# HORECA & FASTFOOD
# ===========================
```csv
Horeca;Koffie;--;starbucks
Horeca;Koffie;--;espresso house

Horeca;Bezorging;Thuisbezorgd;thuisbezorgd

Horeca;Restaurant;--;Konijnenvoer
Horeca;Restaurant;--;De Librije

Horeca;Fastfood;--;mcdonalds;mcd
Horeca;Fastfood;--;burger king
Horeca;Fastfood;--;kfc
Horeca;Fastfood;--;dominos
Horeca;Fastfood;--;new york pizza
Horeca;Fastfood;--;subway
```

# ===========================
# LOGISTIEK
# ===========================
```csv
Logistiek;Pakketdiensten;PostNL;postnl
Logistiek;Pakketdiensten;DHL;dhl
Logistiek;Pakketdiensten;UPS;ups
Logistiek;Pakketdiensten;GLS;gls
Logistiek;Pakketdiensten;DPD;dpd
```

# ===========================
# UITJES
# ===========================
```csv
Vrije Tijd;Museum;Rijksmuseum;Rijks museum
```

# ===========================
# OVERIG (RETAIL / HOBBY / KAARTEN)
# ===========================
```csv
Huishouden;Overig;Blokker;blokker
Huishouden;Overig;Wibra;wibra
Huishouden;Overig;Dille en Kamille;dille en kamille
Huishouden;Overig;Bol;bol.com;bol com
Huishouden;Overig;Geld opnamen;geldmaat

Cadeaus;Speelgoed;Intertoys;intertoys
```
