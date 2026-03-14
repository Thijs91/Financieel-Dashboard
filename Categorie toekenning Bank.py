# ============================================================
# IMPORTS
# ============================================================
import pandas as pd
import re
import os
from datetime import datetime
from difflib import SequenceMatcher

# ============================================================
# INSTELLINGEN
# ============================================================
FUZZY_THRESHOLD = 80  # fuzzy match score tussen 0–100

# ============================================================
# BESTANDSPADEN
# ============================================================
csv_bank_path = r"C:\...\Transactie-historie.csv" #Path waar csv van de bank staat
categorisatie_path = r"C:\...\Categorie.md" #Path waar MD categorie indeling staat
export_dir = r"C:\...\Bank" #Path waar het resultaat heen moet

# ============================================================
# BASIC CLEANUP
# ============================================================
def clean_text(t):
    if pd.isna(t):
        return ""
    t = str(t).lower().strip()
    return re.sub(r"\s+", " ", t)

# ============================================================
# HULPFUNCTIES
# ============================================================
def bepaal_toe_af(bedrag):
    if pd.isna(bedrag):
        return ""
    if bedrag < 0:
        return "Af"
    if bedrag > 0:
        return "Toe"
    return "Nul"

# ============================================================
# 1. MD-BESTAND INLEZEN (MET ALIAS ONDERSTEUNING)
# ============================================================
def load_classification_file(path):
    """
    Leest een MD-bestand met regels binnen ```csv-blokken in een van de twee vormen:

    1) Volledige vorm (5 kolommen):
       categorie ; subcategorie ; detail ; canonical ; alias(sen)

    2) Compacte vorm (4 kolommen):
       categorie ; subcategorie ; detail ; canonical
       → canonical wordt zowel canonical als enige alias
    """

    if not os.path.exists(path):
        raise FileNotFoundError(f"categorisatie.md niet gevonden: {path}")

    inside_block = False
    mapping = {}

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()

            if raw.startswith("```csv"):
                inside_block = True
                continue

            if raw.startswith("```"):
                inside_block = False
                continue
            
            if not inside_block:
                continue

            if raw == "" or raw.startswith("#"):
                continue

            parts = raw.split(";")

            if len(parts) < 4:
                print(f"[WAARSCHUWING] Ongeldige regel in md (te weinig kolommen): {raw}")
                continue

            categorie    = parts[0].strip()
            subcategorie = parts[1].strip()
            detail       = parts[2].strip()

            if len(parts) == 4:
                # Compacte vorm: maar check of er komma's in zitten!
                raw_value = parts[3]
                if "," in raw_value:
                    # Behandel het als een lijst aliassen, pak de eerste als canonical
                    aliases_list = [clean_text(a) for a in raw_value.split(",")]
                    canonical = aliases_list[0] # Pak de eerste als standaard
                    aliases = aliases_list
                else:
                    canonical = clean_text(raw_value)
                    aliases = [canonical]
            else:
                # Volledige 5-koloms vorm: canonical vóór alias
                canonical_raw = parts[3]
                alias_raw     = parts[4]

                canonical = clean_text(canonical_raw)
                aliases = [clean_text(a) for a in alias_raw.split(",")]
                # canonical ook als alias toevoegen
                if canonical not in aliases:
                    aliases.append(canonical)

            if not canonical:
                print(f"[WAARSCHUWING] Lege canonical in regel: {raw}")
                continue

            mapping[canonical] = {
                "aliases": aliases,
                "Categorie": categorie,
                "Sub": subcategorie,
                "Detail": detail,
            }

    return mapping

# ============================================================
# 2. SNS CSV KOLOMDETECTIE
# ============================================================
def load_bank_csv(csv_bank_path):

    with open(csv_bank_path, "r", encoding="utf-8") as f:
        first_line = f.readline()

    n_cols = first_line.count(";") + 1

    temp_cols = [f"col{i}" for i in range(n_cols)]
    df = pd.read_csv(csv_bank_path, sep=";", header=None, names=temp_cols)

    sns_cols = [
        "Datum_1", "Eigen_rekening", "Tegen_rekening", "Ontvanger",
        "C5", "C6", "C7", "Valuta_1", "Saldo", "Valuta_2",
        "Bedrag", "Datum_2", "Datum_3", "Transactie_code",
        "Betaalwijze", "Transactie_ID", "C17", "Omschrijving",
        "Indicator", "Bank_categorie"
    ]

    df.columns = sns_cols[:n_cols]
    return df

# ============================================================
# 3. CANONICALISERING
# ============================================================
def normaliseer_omschrijving(raw):
    """
    Maakt een 'canonieke' omschrijving voor matching.

    Speciale behandeling voor SEPA-incasso's.
    Outputformaat (vaste kolommen):

        Omschrijving | Incassant ID | Kenmerk Machtiging | IBAN

        Omschrijving:
          Alles wat na 'Europese incasso:' staat,
          minus Incassant ID, Kenmerk Machtiging, IBAN en bijbehorende labels.

    Overige omschrijvingen - Niet incasso:
      generieke opschoning + verwijdering van bekende bank-ruis (NL banken),
      vooral stukken als "<bankcode> ... referentie: ..." of "... ref: ..."
    """

    if pd.isna(raw):
        return ""

    s = str(raw)

    # ------------------------------------------------------
    # 0. ALGEMEEN: STRIP ALLE IBANS (NL, BE, DE, FR, GB)
    # ------------------------------------------------------
    def strip_iban(text):
    # IBAN patterns voor NL, BE, DE, FR, GB
        patterns = {
            "NL": r"\bNL\d{2}[A-Z]{4}\d{10}(?=[\s\-]|$)",  # NL: 2 letters, 2 cijfers, 4 letters, 10 cijfers
            "BE": r"\bBE\d{2}[A-Z]{4}\d{12}(?=[\s\-]|$)",  # BE: 2 letters, 2 cijfers, 4 letters, 12 cijfers
            "DE": r"\bDE\d{2}[A-Z]{4}\d{10}\d{2}(?=[\s\-]|$)",  # DE: 2 letters, 2 cijfers, 4 letters, 10 cijfers + 2 cijfers (checksum)
            "FR": r"\bFR\d{2}[A-Z]{5}\d{5}\d{11}\d{2}(?=[\s\-]|$)",  # FR: 2 letters, 2 cijfers, 5 letters, 5 cijfers, 11 cijfers, 2 cijfers (checksum)
            "GB": r"\bGB\d{2}[A-Z]{4}\d{14}(?=[\s\-]|$)",  # GB: 2 letters, 2 cijfers, 4 letters, 14 cijfers
            }

        # Vervang alle IBANs door "[IBAN]"
        for pattern in patterns.values():
            text = re.sub(pattern, "[IBAN]", text, flags=re.IGNORECASE)

        return text

    s = strip_iban(s)
    print(s)

    # ------------------------------------------------------
    # 1. SPECIALE CASE: SEPA / EUROPESE INCASSO
    # ------------------------------------------------------
    low = s.lower()
    if (
        "europese incasso" in low
        or "incassant id" in low
        or "incassantid" in low
        or "kenmerk machtiging" in low):
        # A) Incassant ID (Creditor ID)
        m_inc = re.search(r"incassant\s*id\s*:\s*([A-Z0-9]+)", s, flags=re.IGNORECASE)
        incassant_id = m_inc.group(1).strip() if m_inc else ""

        # B) Kenmerk Machtiging
        m_ken = re.search(r"kenmerk\s*machtiging\s*:\s*([A-Z0-9\-]+)", s, flags=re.IGNORECASE)
        kenmerk = m_ken.group(1).strip(" -\t\r\n") if m_ken else ""

        # C) IBAN (optioneel, echte rekening-IBAN; NIET creditor-id)
        m_iban = re.search(r"\[IBAN\]", s)
        iban = "[IBAN]" if m_iban else ""

        # D) Omschrijving = alles na "Europese incasso:" minus incassant/kenmerk/iban/labels
        omschrijving = ""
        m_after = re.search(r"europese incasso:\s*(.*)", s, flags=re.IGNORECASE)
        if m_after:
            oms = m_after.group(1)
            oms = re.split(r"-\s*incassant\s*id\s*:", oms, flags=re.IGNORECASE)[0]
            oms = re.split(r"-\s*incassantid\s*:", oms, flags=re.IGNORECASE)[0]
            oms = re.split(r"-\s*kenmerk\s*machtiging\s*:", oms, flags=re.IGNORECASE)[0]
            oms = re.sub(r"\b(incassant\s*id|incassantid|kenmerk\s*machtiging|iban)\b", "", oms, flags=re.IGNORECASE)
            oms = re.sub(r"\s{2,}", " ", oms)
            oms = oms.strip(" -.,\t\r\n")
            omschrijving = oms

        result = f"{omschrijving} | {incassant_id} | {kenmerk} | {iban}"
        return clean_text(result)

    # ------------------------------------------------------
    # 2. GENERIEKE OPSCHOONLOGICA (niet-incasso)
    # ------------------------------------------------------
    text = s.lower()

    # ---- bank-ruis (NL) -------------------------------------------------
    # lijst met (vaak voorkomende) bankcodes/namen die in omschrijving kunnen staan
    bank_markers = [
        "nlingb",      # ING
        "ing", "ingb",
        "rabobank", "rabo", "rabo bank",
        "abnamro", "abn amro", "abn", "amro",
        "sns", "snsbank",
        "asn", "asnbank",
        "triodos", "triodosbank",
        "regiobank", "regio bank",
        "knab",
        "bunq",
        "van lanschot", "vanlanschot", "vl bank",
        "deutsche bank", "db",
        "bnp", "bnp paribas",
        "handelsbanken",
        "revolut",
        "n26",
        "wise",
    ]

    # 1) Als er "referentie:" (of ref:) in voorkomt: knip vanaf die marker tot einde
    #    Dit pakt ".... referentie: t" en laat de merchant-tekst ervoor intact.
    text = re.sub(r"\b(referentie|reference|ref)\s*:\s*.*$", "", text)

    # 2) Als er een bankmarker voorkomt en daarna ergens "referentie/ref" (in welke volgorde dan ook),
    #    knip dan vanaf de bankmarker tot einde (defensief maar effectief).
    #    Voorbeeld: ".... nlingb referentie: t" → knip vanaf nlingb
    bank_union = "|".join(re.escape(b) for b in sorted(bank_markers, key=len, reverse=True))
    text = re.sub(rf"\b({bank_union})\b.*\b(referentie|reference|ref)\b.*$", "", text)

    # 3) Soms staat alleen de bankmarker achteraan zonder "referentie:".
    #    knippen alleen als die marker aan het EINDE staat (dus niet midden in normale tekst).
    text = re.sub(rf"\b({bank_union})\b\s*$", "", text)
    # --------------------------------------------------------------------

    # bestaande opschoning
    text = re.sub(r"mcc:\d+", "", text)
    text = re.sub(r"kv\d+", "", text)
    text = re.sub(r">+", "", text)
    text = re.sub(r"\d{1,2}u\d{2}", "", text)
    text = re.sub(r"\d{1,2}:\d{2}", "", text)
    text = re.sub(r"\d{1,2}\.\d{1,2}\.\d{2,4}", "", text)
    text = re.sub(r"\b\d+[.,]\d+\b", "", text)
    text = re.sub(r"[\*\-_/\\|]+", " ", text)
    text = re.sub(r"\s+", " ", text)

    # Verwijder alleen reeksen van 4 of meer cijfers (waarschijnlijk IDs/kenmerken)
    text = re.sub(r"\b\d{4,}\b", " ", text)

    return clean_text(text)

# ============================================================
# 4. FUZZY MATCH
# ============================================================
def fuzzy_match(needle, keys, threshold=FUZZY_THRESHOLD):
    """
    Fuzzy match met een gecombineerde score:
    - SequenceMatcher ratio
    - token overlap (woorden die overeenkomen)
    """
    needle = clean_text(needle)
    needle_tokens = set(needle.split())

    best_score = 0
    best_key = None

    for k in keys:
        k_norm = clean_text(k)
        k_tokens = set(k_norm.split())

        # klassieke ratio
        ratio = SequenceMatcher(None, needle, k_norm).ratio()

        # token overlap (hoeveel van k zit in needle)
        if k_tokens:
            overlap = len(needle_tokens & k_tokens) / len(k_tokens)
        else:
            overlap = 0.0

        score = int((0.75 * ratio + 0.25 * overlap) * 100)

        if score > best_score:
            best_score = score
            best_key = k_norm

    if best_score >= threshold:
        return best_key, best_score

    return None, 0

# ============================================================
# 5. MATCHING ENGINE — MET ALIASLOGICA
# ============================================================
def match_categorie(row, mapping):

    oms = clean_text(row["Omschrijving_clean"])
    tegen = clean_text(row.get("Tegen_rekening", ""))

    # -------------------------------
    # 1. EXACT CANONICAL MATCH
    # -------------------------------
    if oms in mapping:
        m = mapping[oms]
        return (
            m["Categorie"],
            m["Sub"],
            m["Detail"],
            oms,
            "1 - CANONICAL_EXACT",
        )

    # -------------------------------
    # 2. EXACT ALIAS MATCH (hele string)
    # -------------------------------
    for canonical, info in mapping.items():
        if oms in info["aliases"]:
            return (
                info["Categorie"],
                info["Sub"],
                info["Detail"],
                canonical,
                "2 - ALIAS_EXACT",
            )

    # -------------------------------
    # 3. WORD-BOUNDARY MATCH (canonical + aliases)
    # -------------------------------
    for canonical, info in mapping.items():
        # Voeg canonical toe aan de lijst met aliases
        all_possible_matches = [canonical] + info["aliases"]
        for match in all_possible_matches:
            a = clean_text(match)
            if not a:
                continue
            if re.search(rf"\b{re.escape(a)}\b", oms):
                return (
                    info["Categorie"],
                    info["Sub"],
                    info["Detail"],
                    canonical,
                    "3 - WORD_MATCH",
                )
    # -------------------------------
    # 4. SUBSTRING MATCH (canonical + aliases)
    # -------------------------------
    for canonical, info in mapping.items():
        all_possible_matches = [canonical] + info["aliases"]
        for match in all_possible_matches:
            a = clean_text(match)
            # Alleen doen bij langere woorden om matches op "is", "de", "en" te voorkomen
            if len(a) < 4: 
                continue
            
            if a in oms: # Letterlijke substring check
                return (
                    info["Categorie"],
                    info["Sub"],
                    info["Detail"],
                    canonical,
                    "4 - SUBSTRING_MATCH",
                )

    # -------------------------------
    # 5. PARTIAL WORD MATCH (canonical + aliases)
    # -------------------------------
    for canonical, info in mapping.items():
        # Voeg canonical toe aan de lijst met aliases
        all_possible_matches = [canonical] + info["aliases"]
        for match in all_possible_matches:
            a = clean_text(match)
            if len(a) < 3:
                continue
            # Split match en omschrijving in tokens (woorden)
            match_tokens = set(a.split())
            oms_tokens = set(oms.split())
            # Als alle tokens van de match in de omschrijving zitten, match!
            if match_tokens.issubset(oms_tokens):
                return (
                    info["Categorie"],
                    info["Sub"],
                    info["Detail"],
                    canonical,
                    "5 - PARTIAL_TOKEN_MATCH",
                )
            
    # -------------------------------
    # 6. FUZZY MATCH (canonical + aliases)
    # -------------------------------
    all_matches = []
    match_to_canonical = {}

    for canonical, info in mapping.items():
        # Voeg canonical toe aan de lijst met aliases
        all_possible_matches = [canonical] + info["aliases"]
        for match in all_possible_matches:
            match_norm = clean_text(match)
            if not match_norm:
                continue
            all_matches.append(match_norm)
            match_to_canonical[match_norm] = canonical

    fuzzy_key, fuzzy_score = fuzzy_match(oms, all_matches)

    if fuzzy_key:
        canonical = match_to_canonical[fuzzy_key]
        m = mapping[canonical]
        return (
            m["Categorie"],
            m["Sub"],
            m["Detail"],
            canonical,
            f"6 - FUZZY_MATCH {fuzzy_score}",
        )
    
    # -------------------------------
    # 7. IBAN DIRECT MATCH (fallback)
    #    Alleen als er geen tekstmatch is gevonden.
    # -------------------------------
    if tegen and len(tegen) > 5: # Simpele check of er een rekeningnummer is
        for canonical, info in mapping.items():
            if tegen in info["aliases"]:
                return (
                    info["Categorie"],
                    info["Sub"],
                    info["Detail"],
                    canonical,
                    "7 - IBAN_HARD_MATCH",
                )
    # -------------------------------
    # 8. GEEN MATCH
    # -------------------------------
    return "Onbekend", "--", "--", oms, "0 - NO_MATCH"

# ============================================================
# 6. ONBEKENDE VERKOPERS
# ============================================================
def detecteer_onbekende(df, mapping):

    mapping_aliases = set()
    for info in mapping.values():
        mapping_aliases.update(info["aliases"])

    seen = set(df["Omschrijving_clean"].unique())

    onbekend = sorted(list(seen - mapping_aliases - {""}))

    #print("\n==== Nieuwe verkopers ==================================")
    #for o in onbekend:
    #    print(f"{o}")

    print("\nVoorgestelde regels:")
    for o in onbekend:
        print(f"{o};{o};Onbekend;--;--")

    print("========================================================\n")

# ============================================================
# 7. PROCESSOR
# ============================================================
def process_bank_csv():

    print("[INFO] Laden categorisatie...")
    mapping = load_classification_file(categorisatie_path)

    print("[INFO] Laden SNS CSV...")
    df = load_bank_csv(csv_bank_path)

    df["Bedrag"] = pd.to_numeric(df["Bedrag"].astype(str).str.replace(",", "."), errors="coerce")
    df["Saldo"]  = pd.to_numeric(df["Saldo"].astype(str).str.replace(",", "."), errors="coerce")
    df["Datum_1"] = pd.to_datetime(df["Datum_1"], format="%d-%m-%Y", errors="coerce")
    
    # Toe/Af kolom op basis van Bedrag
    df["Toe/Af"] = df["Bedrag"].apply(bepaal_toe_af)

    print("[INFO] Canonicaliseren...")
    df["Omschrijving_clean"] = df["Omschrijving"].apply(normaliseer_omschrijving)

    print("[INFO] Categoriseren...")
    df[["Categorie", "Subcategorie", "Detail", "Canonical_naam", "Match_source"]] = \
        df.apply(lambda row: pd.Series(match_categorie(row, mapping)), axis=1)

    # Vind de eerste en laatste datum in de kolom 'Datum_1'
    eerste_datum = df["Datum_1"].min().strftime('%Y%m%d')
    laatste_datum = df["Datum_1"].max().strftime('%Y%m%d')

    os.makedirs(export_dir, exist_ok=True)
    out_csv = os.path.join(export_dir, f"bank_export_cat_{eerste_datum}_{laatste_datum}_export_datum_{datetime.now().strftime('%Y%m%d')}.csv")

    # ============================================================
    # EXPORT-FORMATTERING (decimale komma voor SNS)
    # ============================================================

    # --- Totaal overzicht ---
    df_export = df.copy()
    export_decimal_cols = ["Saldo", "Bedrag"]
    
    for col in export_decimal_cols:
        if col in df_export.columns:
            df_export[col] = (
                df_export[col]
                .apply(lambda x: "" if pd.isna(x) else f"{x:.2f}")
                .str.replace(".", ",", regex=False)
            )

    df_export.to_csv(out_csv, sep=";", index=False, encoding="utf-8-sig")

    print(f"[OK] Export totaal voltooid → {out_csv}")

    # --- Schoon overzicht ---
    # --- Kolommen selecteren, hernoemen en ordenen ---
    df_export_schoon = df_export[[
        "Datum_1", "Categorie", "Subcategorie", "Detail", "Bedrag",
        "Toe/Af", "Saldo", "Eigen_rekening", "Tegen_rekening",
        "Omschrijving", "Canonical_naam", "Match_source"
    ]].rename(columns={"Datum_1": "Datum"})

    # --- Bestandslocatie ---
    out_csv_schoon = os.path.join(export_dir, f"bank_export_cat_schoon_{eerste_datum}_{laatste_datum}_export_datum_{datetime.now().strftime('%Y%m%d')}.csv")

    df_export_schoon.to_csv(out_csv_schoon, sep=";", index=False, encoding="utf-8-sig")

    print(f"[OK] Export Schoon voltooid → {out_csv_schoon}")

    # --- Onbekende omschrijvingen weergeven ---
    detecteer_onbekende(df, mapping)

    return df

# ============================================================
# 8. RUN
# ============================================================
if __name__ == "__main__":
    df = process_bank_csv()
    print("Klaar.")
