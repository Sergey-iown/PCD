#!/usr/bin/env python3
"""
Generate the PCD London (17 Jun 2026) outreach kit for iOWN.

Outputs (written next to this script):
  - attendees.csv         : full attendee list + a ready LinkedIn people-search link per person
  - outreach_tracker.csv  : working tracker to mark connected / emailed / replied

Source: PCD "Guest List - London Conference, Wednesday 17 June 2026" PDF.
Sergey Bezborodov (iOWN) is the sender and is excluded from the outreach list.

Title/company/country were aligned row-by-row from the PDF. A few attendees
had no title printed in the source; those are left blank on purpose.
"""

import csv
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent

# role: "Host" for the event hosts, "Guest" otherwise.
# (name, position, company, country, role)
ATTENDEES = [
    # --- Hosts ---
    ("David Bell", "Founder", "PCD", "United Kingdom", "Host"),
    ("Ken Chapman", "Director", "Birchin Lane Wealth Advisory", "United Kingdom", "Host"),
    # --- Guests ---
    ("Adrian Pilcher", "Partner", "ISOLAS LLP", "Gibraltar", "Guest"),
    ("Alfred Liu", "Partner", "Forsters LLP", "United Kingdom", "Guest"),
    ("Ali Stennett", "Managing Director", "Conexus Limited", "Isle of Man", "Guest"),
    ("Alison Teare", "Head of Locate, Isle of Man", "Locate Isle of Man", "Isle of Man", "Guest"),
    ("Anahita Kar", "Associate", "Luxury Capital Partners", "Switzerland", "Guest"),
    ("Andre Pimenta", "General Manager", "Oakcean Capital", "United Kingdom", "Guest"),
    ("Andrea Vicari", "Founder", "VicariAvvocati", "Italy", "Guest"),
    ("Andrew Brown", "Business Development Manager", "Stonewell Limited", "Isle of Man", "Guest"),
    ("Andrew Deane", "Founder", "Deane Consulting", "United Kingdom", "Guest"),
    ("Anna-Luise Botzenhardt", "Client Services Director", "HFL", "Guernsey", "Guest"),
    ("Anne-Lise Delafontaine", "Tax lawyer", "Altara Tax", "France", "Guest"),
    ("Anthony Hamilton", "Chief Operations Officer", "Astero Falcon", "United Kingdom", "Guest"),
    ("Anthony Rose", "Senior Tax Partner", "Simmons Gainsford", "United Kingdom", "Guest"),
    ("Atef Elmarakby", "Managing Partner", "GOOD LAW INTL", "United Kingdom", "Guest"),
    ("Belaid Jheengoor", "Director", "Alexanders Group", "Bermuda", "Guest"),
    ("Callan Anderson", "CEO", "HKCS Group", "Hong Kong", "Guest"),
    ("Caoimhe Crawford", "", "", "United Kingdom", "Guest"),
    ("Carl Barros", "Chairman", "The Bridge Group", "United Kingdom", "Guest"),
    ("Caroline Cohen", "Founder", "The French Law Practice", "United Kingdom", "Guest"),
    ("Cécile Civiale Vuillier", "Founding Partner", "META OCTAV", "Switzerland", "Guest"),
    ("Celia St. John", "Investment Manager", "Sarasin & Partners LLP", "United Kingdom", "Guest"),
    ("Chad Phillips", "Business Development Director", "Suntera Global", "Jersey", "Guest"),
    ("Charlotte Milner-Barry", "Senior Relationship Manager", "Prism the Gift Fund", "United Kingdom", "Guest"),
    ("Cherelyn Elbourne", "", "", "Isle of Man", "Guest"),
    ("Christian Scali", "Managing Shareholder", "Scali Rasmussen", "United States", "Guest"),
    ("Claire Chisnall", "Senior Associate", "Consilia Legal", "United Kingdom", "Guest"),
    ("Damian Prentice", "Principal", "AESI", "United Kingdom", "Guest"),
    ("Dan Amroussi", "Associate", "Stewarts", "United Kingdom", "Guest"),
    ("David Kilshaw", "Head of Private Client Wealth Solutions", "Rothschild & Co", "United Kingdom", "Guest"),
    ("David Sussman", "Senior Director - Private Capital Services", "JTC", "Jersey", "Guest"),
    ("Dennis Philips", "Partner, Private Client", "Morr & Co", "United Kingdom", "Guest"),
    ("Derek Baglietto", "Senior Relationship Manager", "Turicum Private Bank", "Gibraltar", "Guest"),
    ("Dilip Varma", "Chairman and CEO", "Everest Data Centre", "United Kingdom", "Guest"),
    ("Dominic Wertheimer", "Director", "Lornham Property", "United Kingdom", "Guest"),
    ("Edward Leigh", "Director – Private Capital Services", "JTC", "Isle of Man", "Guest"),
    ("Elena Myers", "Business Development Executive", "Prism the Gift Fund", "United Kingdom", "Guest"),
    ("Elvira Verdin", "Executive Director", "Julius Baer", "Monaco", "Guest"),
    ("Emily Phillips", "Senior Tax Manager", "Abacus Trust Group", "Isle of Man", "Guest"),
    ("Emily Tweed", "US/UK Tax Associate Director", "Sestini & Co (part of the Shaw Gibbs Group)", "United Kingdom", "Guest"),
    ("Emma Kiver", "Barrister", "1EC Barristers", "United Kingdom", "Guest"),
    ("Emma Moffat", "Portfolio Manager", "James Hambro", "United Kingdom", "Guest"),
    ("Estella Prince", "Legal Director", "Hagen Wolf Solicitors", "United Kingdom", "Guest"),
    ("Gabrielle Patrick", "Co-Founder and Chief Executive Officer", "Knabu", "United Kingdom", "Guest"),
    ("Gill Mabbett", "Relationship Manager", "Locate Guernsey", "Guernsey", "Guest"),
    ("Gonçalo Figueira", "Partner", "EDGE - Sociedade de Advogados SP RL", "Portugal", "Guest"),
    ("Graeme Privett", "Partner, Head of Private Client Tax", "HaysMac LLP", "United Kingdom", "Guest"),
    ("Greg Malone", "Partner", "Arbion", "United Kingdom", "Guest"),
    ("Gregory Perdon", "Investment Manager", "Charles Stanley", "United Kingdom", "Guest"),
    ("Guillaume Grisel", "Partner", "Schellenberg Wittmer", "Switzerland", "Guest"),
    ("Gulnara Long", "Director", "Longview Advisors", "United Kingdom", "Guest"),
    ("Hakan Cortelek", "Chairman", "Beyond Global Partners", "United Kingdom", "Guest"),
    ("Hanneke Farrand", "Managing Director", "Farrand Global Ltd", "Isle of Man", "Guest"),
    ("Harry Bradstreet", "Private Banking Executive", "Arbuthnot Latham", "United Kingdom", "Guest"),
    ("Harvey Dixon", "Senior Associate", "Aston Currency Management", "United Kingdom", "Guest"),
    ("Hayley Kelly", "Manager, Trust & Corporate", "Oak Group", "Isle of Man", "Guest"),
    ("Helen MacLeod", "Senior Associate", "Burges Salmon LLP", "United Kingdom", "Guest"),
    ("Helen Mehdipour", "PR & Corporate Communications Manager", "Union Bancaire Privée (UK) Limited", "United Kingdom", "Guest"),
    ("Henrietta Coldman", "Senior Investment Manager", "Sarasin & Partners LLP", "United Kingdom", "Guest"),
    ("Hilesh Chavda", "Partner – Private Client", "Spencer West", "United Kingdom", "Guest"),
    ("Hydi Yip", "Director", "Union Bancaire Privée (UK) Limited", "United Kingdom", "Guest"),
    ("Ian Bond", "Senior Sales Executive - EIS", "Ebury", "United Kingdom", "Guest"),
    ("Irene Morrison", "Head of Client Development", "Cains", "Isle of Man", "Guest"),
    ("James Fleming", "Chairman", "Arc & Co.", "United Kingdom", "Guest"),
    ("James Kipping", "Tax Partner", "MHA", "United Kingdom", "Guest"),
    ("James Sturla", "Head of Private Client Business Development", "Hampden Capital Plc", "United Kingdom", "Guest"),
    ("James Watlington", "Founder & Chairman", "Alexanders Bermuda", "Bermuda", "Guest"),
    ("Janice Higgins", "Business Development Director", "Group Eleven", "Isle of Man", "Guest"),
    ("Jeffy Lai", "Senior Secretarial Officer", "HKCS Group", "Hong Kong", "Guest"),
    ("Jen Wang", "", "CKGSB Europe", "United Kingdom", "Guest"),
    ("Jerome Lartaud", "Director", "Domus Holmes Property Finder", "United Kingdom", "Guest"),
    ("Jessie Hu", "Director – Private Client Tax", "Brebners Chartered Accountants", "United Kingdom", "Guest"),
    ("Jo Stoddart", "Director", "Locate Guernsey", "Guernsey", "Guest"),
    ("Joe Young", "Partner", "Astraea", "United Kingdom", "Guest"),
    ("John Hilson", "Business Development Director", "Suntera Global", "United Kingdom", "Guest"),
    ("Johnston Busingye", "High Commissioner", "Rwanda in UK", "United Kingdom", "Guest"),
    ("Jonathan Burt", "Partner", "Charles Russell Speechlys LLP", "United Kingdom", "Guest"),
    ("Joseph Kabakeza", "First Counsellor", "Rwanda in UK", "United Kingdom", "Guest"),
    ("Julia Weber", "Senior Vice President", "Broadgate Advisers SA", "Switzerland", "Guest"),
    ("Kate Ovenden", "Partner - Corporate", "Appleby", "Guernsey", "Guest"),
    ("Kateryna Horynovych", "Associate Director", "Azets", "United Kingdom", "Guest"),
    ("Kateryna Viy", "Founding Partner", "META OCTAV", "Switzerland", "Guest"),
    ("Katrina Abela", "Founding Partner", "Vaia Legal", "Malta", "Guest"),
    ("Kelly Greig", "Partner", "Kingsley Napley LLP", "United Kingdom", "Guest"),
    ("Kim Luce", "Head of Private Wealth", "TMF Group", "United Kingdom", "Guest"),
    ("Lara Sturge", "Head of Strategic Partnerships", "Fidux", "United Kingdom", "Guest"),
    ("Laura Clapton", "Director", "Consilia Legal", "United Kingdom", "Guest"),
    ("Lee Penrose", "Head of Strategic Development", "Sandstone Tax", "Isle of Man", "Guest"),
    ("Lorraine Ahia", "Director", "The Bridge Group", "United Kingdom", "Guest"),
    ("Louise Palmer", "Tax Partner", "Ostberg Sinclair & Co", "United Kingdom", "Guest"),
    ("Luca d'Altilia", "Client Director", "Linvia Group", "Monaco", "Guest"),
    ("Luciana Palmisano", "Commercial Director, Private Clients", "Obbard Limited", "United Kingdom", "Guest"),
    ("Luis Ugedo", "MD EMEA Sales", "Etops", "Switzerland", "Guest"),
    ("Mahendree Naidoo", "Partner", "Lester Aldridge", "United Kingdom", "Guest"),
    ("Manuel Ostheider", "Senior Relationship Manager", "Turicum Private Bank", "Gibraltar", "Guest"),
    ("Mark Pierce", "Senior Private Banker", "Hassium Asset Management LLP", "United Kingdom", "Guest"),
    ("Mark Watson", "Head of Private Client Market Strategy", "CSC Global", "Guernsey", "Guest"),
    ("Mark Woodford", "Senior Director", "JTC", "Jersey", "Guest"),
    ("Michael Crowe", "CEO", "Finance Isle of Man", "Isle of Man", "Guest"),
    ("Mike Travers", "Director", "Conexus Limited", "Isle of Man", "Guest"),
    ("Monica Khaleghi", "Private Banker", "Coutts & Co", "United Kingdom", "Guest"),
    ("Myra Leung", "Senior Associate", "Burges Salmon LLP", "United Kingdom", "Guest"),
    ("Natalia Alvarez", "Director", "Ascentium", "United Kingdom", "Guest"),
    ("Natalie Pinon", "Director, Business Development", "National Philanthropic Trust UK", "United Kingdom", "Guest"),
    ("Natasha Southam", "Senior Associate", "Seddons GSC LLP", "United Kingdom", "Guest"),
    ("Nick Wood", "Partner", "Sarasin & Partners LLP", "United Kingdom", "Guest"),
    ("Oliver Thommen", "MD EMEA Sales", "Etops", "Switzerland", "Guest"),
    ("Olivia Carter", "Senior Associate", "Forsters LLP", "United Kingdom", "Guest"),
    ("Ona Ike", "Director, Senior International Wealth Specialist", "UBP", "United Kingdom", "Guest"),
    ("Owen Quinn", "Investment Manager", "Sarasin & Partners LLP", "United Kingdom", "Guest"),
    ("Peter Cheng", "Director", "BDO LLP", "United Kingdom", "Guest"),
    ("Philip Penrose", "Head of Business Development", "Capital International", "Isle of Man", "Guest"),
    ("Richard Cook", "Director", "The Bridge Group", "United Kingdom", "Guest"),
    ("Richard Steele", "Director", "Isio Private Office", "United Kingdom", "Guest"),
    ("Rob O'Connor", "Business Development Manager", "Finance Isle of Man", "Isle of Man", "Guest"),
    ("Rose Muigai", "Solicitor (UK) Advocate (K)", "GlascoteRose Advocates", "Kenya", "Guest"),
    ("Ross Welland", "Tax Partner", "Brebners Chartered Accountants", "United Kingdom", "Guest"),
    ("Sacha Wooldridge", "Partner, Head of Immigration", "Birketts LLP", "United Kingdom", "Guest"),
    ("Sam Jossi", "IHT Protection Specialist", "SPF Private Clients", "United Kingdom", "Guest"),
    ("Samantha Davidson", "Comma consulting ME", "Comma Consulting", "United Arab Emirates", "Guest"),
    ("Sarah Lau", "Head of Asia Pacific and Greater China Desk", "Irwin Mitchell LLP", "United Kingdom", "Guest"),
    ("Sarah Lee", "Partner", "Penningtons Manches Cooper LLP", "United Kingdom", "Guest"),
    ("Serhan Aysever", "Managing Partner", "Beyond Global Partners", "United Kingdom", "Guest"),
    ("Seymour Banks", "Tideway Ambassador", "Tideway", "United Kingdom", "Guest"),
    ("Sharon Shimmin", "Head of Business Development", "Capital International", "United Kingdom", "Guest"),
    ("Sheba Raza", "Founder", "Proxima Advisory", "United Kingdom", "Guest"),
    ("Simon Fearnhead", "Director", "Stonewell Limited", "Isle of Man", "Guest"),
    ("Simon Voisin", "Managing Director", "Coriats Trust Company (Jersey) Limited", "Jersey", "Guest"),
    ("Simone Marston", "Associate", "Seddons GSC LLP", "United Kingdom", "Guest"),
    ("Stefan Velvick", "Director Development", "National Philanthropic Trust UK", "United Kingdom", "Guest"),
    ("Stephen Rothwell", "Partner", "Sarasin & Partners LLP", "United Kingdom", "Guest"),
    ("Steven Quayle", "Director & Head of Banking & Finance", "Cains", "Isle of Man", "Guest"),
    ("Stuart Dalmedo", "Partner", "ISOLAS LLP", "Gibraltar", "Guest"),
    ("Tendai Kariwo", "Director, Development", "National Philanthropic Trust UK", "United Kingdom", "Guest"),
    ("Tim Harrison", "Founder and CEO", "Arkus Consulting Limited", "United Kingdom", "Guest"),
    ("Tim Houghton", "Market Head, Channel Islands", "TMF Group", "Jersey", "Guest"),
    ("Tim Morgan", "Partner", "Appleby", "Jersey", "Guest"),
    ("Tim Walford-Fitzgerald", "Director", "HaysMac LLP", "United Kingdom", "Guest"),
    ("Tom Blackmore", "Senior Relationship Manager", "Butterfield Mortgages Limited", "United Kingdom", "Guest"),
    ("Tom Rutherford", "Director", "LOTUC Consulting Ltd", "United Kingdom", "Guest"),
    ("Victoria Younghusband", "Partner", "M.B.KEMP LLP", "United Kingdom", "Guest"),
    ("Vitorine Bajada", "Partner Lawyer", "Dingli & Dingli Law Firm", "Malta", "Guest"),
]


def linkedin_search_url(name: str, company: str) -> str:
    """A LinkedIn people-search deep link: pre-fills name + company so the
    right profile is usually the first result. One click, then 'Connect'."""
    keywords = f"{name} {company}".strip()
    q = urllib.parse.urlencode({"keywords": keywords})
    return f"https://www.linkedin.com/search/results/people/?{q}"


def first_name(name: str) -> str:
    return name.split()[0]


# ---------------------------------------------------------------------------
# Segmentation: which kind of contact is this, for iOWN (a Swiss "wealth &
# business architect" serving international/HNW families and their advisers)?
# ---------------------------------------------------------------------------
def classify(position: str, company: str) -> str:
    p, c = position.lower(), company.lower()

    if "rwanda" in c or "high commissioner" in p or "counsellor" in p:
        return "government"
    if "locate" in c or "finance isle of man" in c:
        return "jurisdiction"
    if "pr &" in p or "communications" in p:
        return "pr"

    banks = ["julius baer", "union bancaire", "ubp", "coutts", "arbuthnot",
             "turicum", "rothschild", "hassium", "butterfield mortgages",
             "broadgate"]
    if any(b in c for b in banks) or "private banker" in p or "private banking" in p:
        return "private_bank"

    tax_firms = ["haysmac", "mha", "sestini", "simmons gainsford", "brebners",
                 "bdo", "azets", "ostberg", "altara", "sandstone tax"]
    if "tax" in p or "tax" in c or any(t in c for t in tax_firms):
        return "tax"

    law_firms = ["isolas", "forsters", "charles russell", "kingsley napley",
                 "penningtons", "stewarts", "spencer west", "appleby",
                 "schellenberg", "burges salmon", "birketts", "irwin mitchell",
                 "morr & co", "seddons", "hagen wolf", "consilia legal",
                 "vaia legal", "good law", "french law practice", "dingli",
                 "m.b.kemp", "glascoterose", "edge -", "1ec barristers",
                 "lester aldridge", "cains"]
    if (any(l in c for l in law_firms)
            or any(k in p for k in ["lawyer", "solicitor", "advocate", "barrister", "legal"])
            or "avvocati" in c or "advogados" in c or "law firm" in c):
        return "law"

    fiduciary = ["jtc", "suntera", "tmf", "oak group", "coriats", "abacus",
                 "hfl", "stonewell", "fidux", "obbard", "alexanders", "hkcs",
                 "conexus", "csc global", "group eleven"]
    if (any(f in c for f in fiduciary) or "trust" in p or "fiduciary" in p
            or ("corporate" in p and "service" in p)):
        return "trust_fiduciary"

    if "philanthropic" in c or "gift fund" in c:
        return "philanthropy"
    if "ebury" in c or "currency" in c:
        return "fx_payments"
    if "property" in c or "data centre" in c or "mortgages" in c:
        return "property"
    if "immigration" in p:
        return "immigration"

    invest = ["sarasin", "charles stanley", "james hambro", "longview",
              "luxury capital", "oakcean", "arc & co", "isio", "hampden capital",
              "capital international", "birchin lane"]
    if (any(w in c for w in invest)
            or any(k in p for k in ["investment manager", "portfolio manager",
                                    "wealth", "private office", "international wealth"])):
        return "investment"

    if any(k in p for k in ["business development", "relationship manager",
                            "strategic partnership", "sales"]):
        return "bd"
    return "other"


CORE_SEGMENTS = {"private_bank", "trust_fiduciary", "law", "tax", "investment"}
TIER2_SEGMENTS = {"bd", "philanthropy", "fx_payments", "immigration",
                  "property", "jurisdiction"}

SEGMENT_LABEL = {
    "host": "event host", "private_bank": "private banking",
    "trust_fiduciary": "trust / fiduciary", "law": "private-client law",
    "tax": "private-client tax", "investment": "wealth / investment",
    "bd": "business development", "philanthropy": "philanthropy",
    "fx_payments": "FX / payments", "immigration": "immigration",
    "property": "property / real estate", "jurisdiction": "jurisdiction promotion",
    "government": "government / diplomatic", "pr": "PR / communications",
    "other": "advisory / other",
}


def seniority(position: str) -> str:
    p = position.lower()
    if not p:
        return "unknown"
    if "partner" in p and "associate" not in p:
        return "senior"
    senior_kw = ["founder", "ceo", "chief", "chairman", "managing partner",
                 "managing director", "managing shareholder", "head of",
                 "director", "principal", "senior vice president", "market head",
                 "general manager"]
    if any(k in p for k in senior_kw):
        return "senior"
    return "junior"


def tier_and_reason(role, segment, level):
    label = SEGMENT_LABEL[segment]
    if role == "Host":
        return 1, "Event host — thank-you + key network node"
    if segment in CORE_SEGMENTS and level == "senior":
        return 1, f"Senior {label} contact — direct referral source / decision-maker"
    if segment in CORE_SEGMENTS:
        return 2, f"{label.capitalize()} contact ({level}) — nurture / future referral"
    if segment in TIER2_SEGMENTS:
        return 2, f"{label.capitalize()} — adjacent to iOWN's clients"
    if segment == "other" and level == "senior":
        return 2, "Senior advisory contact — worth a personal connect"
    if segment == "government":
        return 3, "Government / diplomatic — relationship, not commercial"
    return 3, f"{label.capitalize()} — long-tail / lower priority"


# ---------------------------------------------------------------------------
# Personalised LinkedIn connection note (<= 300 chars, LinkedIn's limit).
# ---------------------------------------------------------------------------
LIMIT = 300
PREFIX = ("Hi {first}, great being among the PCD crowd at Drapers' Hall — I "
          "presented iOWN, wealth & business architecture for international families.")
SUFFIX = " Let's stay connected. Best, Sergey"

CLAUSES = {  # segment: (with-company, plain)
    "private_bank": ("Trusted private bankers like those at {company} matter hugely to the families we serve.",
                     "Trusted private bankers are central to the families we serve."),
    "trust_fiduciary": ("We work closely with fiduciary teams like {company} on cross-border structures.",
                        "We work closely with fiduciary and trustee teams on cross-border structures."),
    "law": ("I often collaborate with private-client lawyers such as {company} on international structuring.",
            "I often collaborate with private-client lawyers on international structuring."),
    "tax": ("Cross-border tax expertise like {company}'s is exactly what our families rely on.",
            "Cross-border tax expertise is exactly what our families rely on."),
    "investment": ("Lots of common ground with the wealth and investment work at {company}.",
                   "Lots of common ground with the wealth and investment side of your work."),
    "bd": ("Feels like real overlap between iOWN and {company} worth exploring.",
           "Feels like there could be real overlap worth exploring."),
    "philanthropy": ("Philanthropy is close to many of our families' plans — I'd love to hear more about {company}.",
                     "Philanthropy is close to many of our families' plans and I'd love to hear more."),
    "fx_payments": ("International clients often need FX and payments partners like {company}.",
                    "International clients often need strong FX and payments partners."),
    "immigration": ("Globally mobile families regularly need immigration counsel like {company}'s.",
                    "Globally mobile families regularly need trusted immigration counsel."),
    "property": ("Our international clients frequently ask about UK property, where {company} looks very relevant.",
                 "Our international clients frequently ask about UK property and real estate."),
    "jurisdiction": ("Jurisdictional insight like {company}'s is invaluable for our international clients.",
                     "Jurisdictional insight is invaluable for our international clients."),
    "pr": ("Great to connect after a brilliant event.",
           "Great to connect after a brilliant event."),
    "other": ("I really enjoyed the conversations and would value comparing notes.",
              "I really enjoyed the conversations and would value comparing notes."),
}


def connection_message(role, segment, name, company):
    first = first_name(name)
    if role == "Host":
        return (f"Hi {first}, thank you for a superb PCD London at Drapers' Hall "
                f"— a privilege to present iOWN, wealth & business architecture for "
                f"international families. Truly grateful for the platform and glad to "
                f"connect. Best, Sergey")
    if segment == "government":
        return (f"Hi {first}, a real honour to share the room with you at the PCD "
                f"London conference at Drapers' Hall, where I presented iOWN. I'd "
                f"value staying connected. With respect, Sergey")

    with_co, plain = CLAUSES.get(segment, CLAUSES["other"])
    prefix = PREFIX.format(first=first)
    for clause in (with_co.format(company=company), plain):
        msg = f"{prefix} {clause}{SUFFIX}"
        if len(msg) <= LIMIT:
            return msg
    return f"{prefix}{SUFFIX}"  # last resort


def main() -> None:
    rows = []
    for name, position, company, country, role in ATTENDEES:
        seg = "host" if role == "Host" else classify(position, company)
        level = seniority(position)
        tier, reason = tier_and_reason(role, seg, level)
        msg = connection_message(role, seg, name, company)
        rows.append({
            "Name": name, "First_Name": first_name(name), "Position": position,
            "Company": company, "Country": country, "Role": role,
            "Tier": tier, "Segment": SEGMENT_LABEL[seg], "Priority_Reason": reason,
            "Connection_Message": msg, "Msg_Len": len(msg),
            "LinkedIn_Search_URL": linkedin_search_url(name, company),
        })

    # Sort: Tier asc, then Host first, then by name.
    rows.sort(key=lambda r: (r["Tier"], 0 if r["Role"] == "Host" else 1, r["Name"]))

    # 1) Prioritised master CSV
    cols = ["Tier", "Name", "First_Name", "Position", "Company", "Country",
            "Role", "Segment", "Priority_Reason", "Connection_Message",
            "LinkedIn_Search_URL"]
    with (HERE / "attendees_prioritized.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    # 2) Working tracker (with tier + ready message)
    with (HERE / "outreach_tracker.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Tier", "Name", "Company", "Country", "Segment",
                    "Connection_Message", "LinkedIn_Search_URL",
                    "Connected (Y/N)", "Note_Sent (Y/N)", "Email_Sent (Y/N)",
                    "Replied (Y/N)", "Notes"])
        for r in rows:
            w.writerow([r["Tier"], r["Name"], r["Company"], r["Country"],
                        r["Segment"], r["Connection_Message"],
                        r["LinkedIn_Search_URL"], "", "", "", "", ""])

    # 3) Copy-paste sheet, grouped by tier
    with (HERE / "connection_messages.md").open("w", encoding="utf-8") as f:
        f.write("# Personalised LinkedIn connection notes — PCD London, "
                "17 June 2026\n\n")
        f.write("Grouped by priority tier. For each person: open the search link, "
                "click their profile, **Connect → Add a note**, paste the message. "
                "Every note is within LinkedIn's 300-character limit.\n\n")
        f.write("Work top-down: **Tier 1 first** (the people most worth your time), "
                "then Tier 2. Spread invites over several days.\n")
        tier_titles = {1: "Tier 1 — priority (senior referral sources, decision-makers, hosts)",
                       2: "Tier 2 — relevant (nurture, adjacent services, juniors at key firms)",
                       3: "Tier 3 — long tail (connect when you have time)"}
        for tier in (1, 2, 3):
            group = [r for r in rows if r["Tier"] == tier]
            f.write(f"\n## {tier_titles[tier]}  ({len(group)})\n\n")
            for r in group:
                pos = f"{r['Position']}, " if r["Position"] else ""
                f.write(f"- **{r['Name']}** — {pos}{r['Company']} ({r['Country']})  \n")
                f.write(f"  [LinkedIn search]({r['LinkedIn_Search_URL']})  \n")
                f.write(f"  > {r['Connection_Message']}\n\n")

    longest = max(rows, key=lambda r: r["Msg_Len"])
    counts = {t: sum(1 for r in rows if r["Tier"] == t) for t in (1, 2, 3)}
    print(f"Wrote attendees_prioritized.csv, outreach_tracker.csv, "
          f"connection_messages.md ({len(rows)} contacts).")
    print(f"Tier counts: {counts}")
    print(f"Longest message: {longest['Msg_Len']} chars ({longest['Name']}) "
          f"[limit {LIMIT}]")


if __name__ == "__main__":
    main()
