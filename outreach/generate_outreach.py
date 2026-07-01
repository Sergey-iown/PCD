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
import json
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
    ("Dennis Phillips", "Partner, Private Client", "Morr & Co", "United Kingdom", "Guest"),
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
    # --- Added from business cards collected at the event (not on the printed list) ---
    ("Tim Pearson-Burton", "Director", "Linvia Group", "Monaco", "Guest"),
    ("James Carroll", "Aircraft Sales & Acquisitions, EMEA & Asia", "Duncan Aviation", "United Kingdom", "Guest"),
    ("Cecilia Weng Song", "Private Client Manager, Giving & Impact Services", "Charities Aid Foundation (CAF)", "United Kingdom", "Guest"),
    ("Peter Ahluwalia", "Co-Founder & Partner, Head of Active Strategies", "LeoVest Partners AG", "Switzerland", "Guest"),
    ("Eric Lord", "Registered Representative", "Texture Capital", "United States", "Guest"),
    ("Lionel Freitas", "Contact (Dixcart Portugal)", "Dixcart Portugal Lda", "Portugal", "Guest"),
]

# People you met in person (from business cards). They get a MET badge, are
# promoted to Tier 1A, and carry email/phone where the card showed them.
# (name: (email, phone)). Name must match the entry in ATTENDEES exactly.
CONTACT_DETAILS = {
    "Guillaume Grisel": ("guillaume.grisel@swlegal.ch", "+41 22 707 8000"),
    "Lee Penrose": ("lee@sandstone.tax", ""),
    "Atef Elmarakby": ("atef.elmarakby@goodlawintl.com", "+44 20 7139 9255"),
    "Ali Stennett": ("ali@conexus.im", "+44 7624 225083"),
    "Richard Steele": ("richard.steele@isio.com", "+44 7920 637876"),
    "Dennis Phillips": ("dennis.phillips@morrlaw.com", "+44 20 8971 1050"),
    "Derek Baglietto": ("derek.baglietto@turicum.com", "+350 200 441144"),
    "Stuart Dalmedo": ("stuart.dalmedo@isolas.gi", "+350 2000 1892"),
    "Tim Pearson-Burton": ("tburton@linviagroup.com", "+377 97 97 82 00"),
    "James Carroll": ("james.carroll@duncanaviation.com", "+44 7411 534053"),
    "Cecilia Weng Song": ("cawengsong@cafonline.org", "+44 3000 123342"),
    "Peter Ahluwalia": ("peter.ahluwalia@leovest.com", "+41 58 513 89 97"),
    "Eric Lord": ("eric@texture.capital", "+1 513 463 7371"),
    "Lionel Freitas": ("lionel.freitas@dixcart.com", "+351 291 225019"),
}
MET = set(CONTACT_DETAILS)


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
                 "conexus", "csc global", "group eleven", "dixcart"]
    if (any(f in c for f in fiduciary) or "trust" in p or "fiduciary" in p
            or ("corporate" in p and "service" in p)):
        return "trust_fiduciary"

    if ("philanthropic" in c or "gift fund" in c or "charities aid" in c
            or "giving" in p or "impact services" in p):
        return "philanthropy"
    if "ebury" in c or "currency" in c:
        return "fx_payments"
    if "property" in c or "data centre" in c or "mortgages" in c:
        return "property"
    if "immigration" in p:
        return "immigration"

    invest = ["sarasin", "charles stanley", "james hambro", "longview",
              "luxury capital", "oakcean", "arc & co", "isio", "hampden capital",
              "capital international", "birchin lane", "leovest", "texture capital"]
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


# ---------------------------------------------------------------------------
# Per-person email opener: a warm first line for greetings_email.md, dropped in
# after "Dear {first_name},". Longer/warmer than the LinkedIn note (no char cap).
# ---------------------------------------------------------------------------
EMAIL_OPENERS = {
    "host": ("Thank you again for having me at PCD London — presenting iOWN to that "
             "room at Drapers' Hall was a genuine highlight, and I'm grateful to you "
             "and the PCD team for the platform."),
    "private_bank": ("It was a pleasure to share the room with you at PCD London. The "
                     "families iOWN works with so often rely on trusted private bankers "
                     "like the team at {company}, so I suspect there's real common ground "
                     "between us."),
    "trust_fiduciary": ("It was a pleasure to be among fellow private-client professionals "
                        "at PCD London. iOWN works hand-in-hand with fiduciary and trustee "
                        "teams like {company} on cross-border structures, so I'd love to "
                        "find time to compare notes."),
    "law": ("It was a pleasure to be in the room with you at PCD London. The international "
            "structuring work you do at {company} is exactly where iOWN so often partners "
            "with private-client lawyers, and I'd welcome the chance to explore where we "
            "overlap."),
    "tax": ("It was a pleasure to be among fellow advisers at PCD London. Cross-border tax "
            "expertise like {company}'s is precisely what the families iOWN works with "
            "depend on, so I'd love to stay in touch."),
    "investment": ("It was a pleasure to be in the room with you at PCD London. There's a "
                   "lot of common ground between iOWN and the wealth and investment work "
                   "you do at {company}, and I'd value comparing notes."),
    "bd": ("It was a pleasure to connect at PCD London. I suspect there's meaningful "
           "overlap between iOWN and {company}, and I'd welcome the chance to explore it."),
    "philanthropy": ("It was a pleasure to be among fellow private-client professionals at "
                     "PCD London. Philanthropy features in many of the families iOWN works "
                     "with, so I'd love to learn more about {company}'s work."),
    "fx_payments": ("It was a pleasure to share the room at PCD London. iOWN's international "
                    "clients regularly need strong FX and payments partners like {company}, "
                    "so I'd welcome staying in touch."),
    "immigration": ("It was a pleasure to be among fellow advisers at PCD London. The "
                    "globally mobile families iOWN works with frequently need immigration "
                    "counsel like {company}'s, and I'd value keeping in touch."),
    "property": ("It was a pleasure to be in the room at PCD London. iOWN's international "
                 "clients often ask about UK property, where {company} looks highly "
                 "relevant, so I'd welcome staying connected."),
    "jurisdiction": ("It was a pleasure to be at PCD London. Jurisdictional insight like "
                     "{company}'s is invaluable to the international clients iOWN works "
                     "with, and I'd value staying in touch."),
    "government": ("It was an honour to share the room with you at PCD London at Drapers' "
                   "Hall, where I was presenting iOWN. I'd be glad to stay in touch."),
    "pr": ("It was a pleasure to be among the PCD London crowd at Drapers' Hall, where I "
           "presented iOWN. I'd be glad to stay connected."),
    "other": ("It was a pleasure to be among fellow professionals at PCD London. I really "
              "enjoyed the conversations around the event, and I'd value comparing notes on "
              "where iOWN and your work might align."),
}


def email_opener(segment, company):
    template = EMAIL_OPENERS.get(segment, EMAIL_OPENERS["other"])
    if "{company}" in template and not company:
        return EMAIL_OPENERS["other"]
    return template.format(company=company)


# ---------------------------------------------------------------------------
# Score Tier-1 contacts to trim a tight "Tier 1A" of top targets.
# ---------------------------------------------------------------------------
TOP_TARGET_COUNT = 25


def target_score(segment, position, country):
    p, s = position.lower(), 0
    s += {"host": 6, "private_bank": 5}.get(segment, 4 if segment in CORE_SEGMENTS else 2)
    if any(k in p for k in ["founder", "ceo", "chief exec", "chairman"]):
        s += 5
    elif any(k in p for k in ["managing partner", "managing director",
                              "managing shareholder", "senior director"]):
        s += 4
    elif "head of" in p:
        s += 4
    elif ("partner" in p and "associate" not in p) or "principal" in p:
        s += 3
    elif "director" in p:
        s += 2
    else:
        s += 1
    if country in {"Switzerland", "Monaco"}:
        s += 3
    elif country in {"Jersey", "Guernsey", "Isle of Man", "Gibraltar", "Bermuda"}:
        s += 2
    else:
        s += 1
    return s


BAND_RANK = {"1A": 0, "1B": 1, "2": 2, "3": 3}


# ---------------------------------------------------------------------------
# Compliant copy-paste accelerator (NOT a bot): a self-contained HTML page.
# "Copy note" puts the personalised message on the clipboard; "Open profile"
# opens the LinkedIn search tab. YOU click Connect/Send on LinkedIn yourself —
# nothing here automates LinkedIn, so there's no User-Agreement / ban risk.
# Progress is remembered in the browser (localStorage).
# ---------------------------------------------------------------------------
HELPER_HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PCD London outreach helper</title>
<style>
 :root{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
 body{margin:0;background:#f4f5f7;color:#1d2129}
 header{position:sticky;top:0;background:#0a66c2;color:#fff;padding:14px 20px;box-shadow:0 1px 4px rgba(0,0,0,.2)}
 header h1{margin:0;font-size:18px}
 .bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:10px;font-size:13px}
 .bar input,.bar select{padding:6px 8px;border:none;border-radius:6px;font-size:13px}
 .bar label{color:#dbe9fb}
 .note{background:#fff3cd;color:#664d03;padding:8px 20px;font-size:12.5px;border-bottom:1px solid #ffe69c}
 main{padding:16px 20px;max-width:980px;margin:0 auto}
 .card{background:#fff;border-radius:8px;padding:14px 16px;margin-bottom:12px;box-shadow:0 1px 3px rgba(0,0,0,.08)}
 .card.done{opacity:.5}
 .top{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:baseline}
 .name{font-weight:600;font-size:15px}
 .meta{color:#65676b;font-size:13px}
 .badge{font-size:11px;font-weight:700;padding:2px 7px;border-radius:10px;color:#fff}
 .b1A{background:#0a66c2}.b1B{background:#378fe9}.b2{background:#6b7280}.b3{background:#9ca3af}
 .met{background:#1a7f37;margin-left:6px}
 .msg{background:#f0f2f5;border-radius:6px;padding:9px 11px;margin:9px 0;font-size:13.5px;white-space:pre-wrap}
 .actions{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
 button,a.btn{font:inherit;font-size:13px;border:none;border-radius:6px;padding:7px 12px;cursor:pointer;text-decoration:none;display:inline-block}
 .copy{background:#0a66c2;color:#fff}.copy.email{background:#1a7f37}.copy.addr{background:#7a3ea0}
 .open{background:#e4e6eb;color:#050505}
 .chk{margin-left:auto;font-size:13px;color:#444;user-select:none}
 .count{color:#dbe9fb;margin-left:auto}
</style></head><body>
<header>
 <h1>PCD London 2026 — outreach helper</h1>
 <div class="bar">
  <label>Band <select id="band">
    <option value="">all</option><option>1A</option><option>1B</option>
    <option value="2">2</option><option value="3">3</option></select></label>
  <label><input type="checkbox" id="metonly"> met in person only</label>
  <label><input type="checkbox" id="hidedone"> hide done</label>
  <input id="q" placeholder="search name / company…" size="22">
  <span class="count" id="count"></span>
 </div>
</header>
<div class="note">Human-in-the-loop, not a bot: this only copies text and opens tabs.
 You press Connect / Send on LinkedIn yourself. Spread invites over several days.</div>
<main id="list"></main>
<script>
const DATA = __DATA__;
const store = JSON.parse(localStorage.getItem('pcd_done')||'{}');
const save = ()=>localStorage.setItem('pcd_done', JSON.stringify(store));
const el = (h)=>{const t=document.createElement('template');t.innerHTML=h.trim();return t.content.firstChild;};
function render(){
 const band=document.getElementById('band').value;
 const met=document.getElementById('metonly').checked;
 const hide=document.getElementById('hidedone').checked;
 const q=document.getElementById('q').value.toLowerCase();
 const list=document.getElementById('list'); list.innerHTML='';
 let shown=0;
 for(const p of DATA){
  if(band && p.band!==band) continue;
  if(met && !p.met) continue;
  if(hide && store[p.id]) continue;
  if(q && !(p.name+' '+p.company).toLowerCase().includes(q)) continue;
  shown++;
  const contact=[p.emailaddr,p.phone].filter(Boolean).join(' · ');
  const mailBtn=p.emailaddr?`<button class="copy addr" data-c="addr">Copy email address</button>`:'';
  const card=el(`<div class="card ${store[p.id]?'done':''}">
   <div class="top"><span><span class="name">${p.name}</span>
     <span class="badge b${p.band}">${p.band}</span>${p.met?'<span class="badge met">MET</span>':''}
     <div class="meta">${p.position?p.position+' · ':''}${p.company} · ${p.country}</div>
     ${contact?`<div class="meta">📇 ${contact}</div>`:''}</span></div>
   <div class="msg">${p.msg}</div>
   <div class="actions">
     <button class="copy" data-c="msg">Copy note</button>
     <button class="copy email" data-c="opener">Copy email opener</button>
     ${mailBtn}
     <a class="btn open" href="${p.url}" target="_blank" rel="noopener">Open profile search ↗</a>
     <label class="chk"><input type="checkbox" ${store[p.id]?'checked':''} data-done> done</label>
   </div></div>`);
  card.querySelector('[data-c="msg"]').onclick=()=>copy(p.msg, card.querySelector('[data-c="msg"]'),'Copy note');
  card.querySelector('[data-c="opener"]').onclick=()=>copy(p.opener, card.querySelector('[data-c="opener"]'),'Copy email opener');
  if(p.emailaddr) card.querySelector('[data-c="addr"]').onclick=()=>copy(p.emailaddr, card.querySelector('[data-c="addr"]'),'Copy email address');
  card.querySelector('[data-done]').onchange=(e)=>{store[p.id]=e.target.checked;save();render();};
  list.appendChild(card);
 }
 document.getElementById('count').textContent=shown+' shown · '+Object.values(store).filter(Boolean).length+' done';
}
function copy(text,btn,label){navigator.clipboard.writeText(text).then(()=>{btn.textContent='Copied ✓';setTimeout(()=>btn.textContent=label,1200);});}
for(const id of ['band','metonly','hidedone','q']) document.getElementById(id).addEventListener('input',render);
render();
</script></body></html>
"""


def write_helper(rows):
    data = [{
        "id": r["Name"], "name": r["Name"], "position": r["Position"],
        "company": r["Company"], "country": r["Country"], "band": r["Band"],
        "met": bool(r.get("Met")), "msg": r["Connection_Message"],
        "opener": r["Email_Opener"], "emailaddr": r["Email"], "phone": r["Phone"],
        "url": r["LinkedIn_Search_URL"],
    } for r in rows]
    html = HELPER_HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    (HERE / "outreach_helper.html").write_text(html, encoding="utf-8")


def main() -> None:
    rows = []
    for name, position, company, country, role in ATTENDEES:
        seg = "host" if role == "Host" else classify(position, company)
        level = seniority(position)
        tier, reason = tier_and_reason(role, seg, level)
        met = name in MET
        email, phone = CONTACT_DETAILS.get(name, ("", ""))
        if met:
            reason = "MET IN PERSON — " + reason
        rows.append({
            "Name": name, "First_Name": first_name(name), "Position": position,
            "Company": company, "Country": country, "Role": role,
            "Met": "Y" if met else "", "Email": email, "Phone": phone,
            "Tier": tier, "_seg": seg, "Segment": SEGMENT_LABEL[seg],
            "Priority_Reason": reason,
            "Connection_Message": connection_message(role, seg, name, company),
            "Email_Opener": email_opener(seg, company),
            "Msg_Len": len(connection_message(role, seg, name, company)),
            "_score": target_score(seg, position, country) + (100 if met else 0),
            "LinkedIn_Search_URL": linkedin_search_url(name, company),
        })

    # Band the Tier-1 group: top TOP_TARGET_COUNT by score => "1A", rest "1B".
    # Anyone met in person is promoted straight to 1A regardless of tier.
    tier1 = sorted((r for r in rows if r["Tier"] == 1),
                   key=lambda r: (-r["_score"], r["Name"]))
    top_ids = {id(r) for r in tier1[:TOP_TARGET_COUNT]}
    for r in rows:
        if r["Met"] or id(r) in top_ids:
            r["Band"] = "1A"
        elif r["Tier"] == 1:
            r["Band"] = "1B"
        else:
            r["Band"] = str(r["Tier"])

    rows.sort(key=lambda r: (BAND_RANK[r["Band"]],
                             0 if r["Met"] else 1,
                             0 if r["Role"] == "Host" else 1,
                             -r["_score"], r["Name"]))

    # 1) Prioritised master CSV
    cols = ["Band", "Tier", "Met", "Name", "First_Name", "Position", "Company",
            "Country", "Role", "Email", "Phone", "Segment", "Priority_Reason",
            "Connection_Message", "Email_Opener", "LinkedIn_Search_URL"]
    with (HERE / "attendees_prioritized.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    # 2) Working tracker (with band + ready message + email opener)
    with (HERE / "outreach_tracker.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Band", "Met", "Name", "Company", "Country", "Email", "Phone",
                    "Segment", "Connection_Message", "Email_Opener",
                    "LinkedIn_Search_URL", "Connected (Y/N)", "Note_Sent (Y/N)",
                    "Email_Sent (Y/N)", "Replied (Y/N)", "Notes"])
        for r in rows:
            w.writerow([r["Band"], r["Met"], r["Name"], r["Company"], r["Country"],
                        r["Email"], r["Phone"], r["Segment"],
                        r["Connection_Message"], r["Email_Opener"],
                        r["LinkedIn_Search_URL"], "", "", "", "", ""])

    # 3) Copy-paste sheet, grouped by band
    band_titles = {
        "1A": "Tier 1A — TOP TARGETS (start here: ~25 highest-value, do first)",
        "1B": "Tier 1B — priority (other senior referral sources / decision-makers)",
        "2": "Tier 2 — relevant (nurture, adjacent services, juniors at key firms)",
        "3": "Tier 3 — long tail (connect when you have time)",
    }
    with (HERE / "connection_messages.md").open("w", encoding="utf-8") as f:
        f.write("# Personalised LinkedIn connection notes — PCD London, "
                "17 June 2026\n\n")
        f.write("Grouped by priority band. For each person: open the search link, "
                "click their profile, **Connect → Add a note**, paste the message. "
                "Every note is within LinkedIn's 300-character limit.\n\n")
        f.write("Work top-down: **Tier 1A first**, then 1B, then 2. Spread invites "
                "over several days.\n")
        for band in ("1A", "1B", "2", "3"):
            group = [r for r in rows if r["Band"] == band]
            f.write(f"\n## {band_titles[band]}  ({len(group)})\n\n")
            for r in group:
                pos = f"{r['Position']}, " if r["Position"] else ""
                f.write(f"- **{r['Name']}** — {pos}{r['Company']} ({r['Country']})  \n")
                f.write(f"  [LinkedIn search]({r['LinkedIn_Search_URL']})  \n")
                f.write(f"  > {r['Connection_Message']}\n\n")

    # 4) Top-targets one-pager: LinkedIn note + email opener for the ~25 in 1A
    with (HERE / "top_targets.md").open("w", encoding="utf-8") as f:
        top = [r for r in rows if r["Band"] == "1A"]
        f.write("# Top targets — PCD London (Tier 1A)\n\n")
        f.write(f"The {len(top)} highest-value contacts to reach first — by seniority, "
                "segment fit with iOWN, and jurisdiction. Each has a LinkedIn note **and** "
                "an email opener (drop the opener in after \"Dear <first name>,\" in "
                "`greetings_email.md`).\n\n")
        for i, r in enumerate(top, 1):
            pos = f"{r['Position']}, " if r["Position"] else ""
            met = " ✅ **MET IN PERSON**" if r["Met"] else ""
            f.write(f"### {i}. {r['Name']} — {pos}{r['Company']} ({r['Country']}){met}\n")
            f.write(f"*{r['Priority_Reason']}* · [LinkedIn search]({r['LinkedIn_Search_URL']})\n\n")
            if r["Email"] or r["Phone"]:
                bits = " · ".join(x for x in (r["Email"], r["Phone"]) if x)
                f.write(f"**Contact:** {bits}\n\n")
            f.write(f"**LinkedIn note:** {r['Connection_Message']}\n\n")
            f.write(f"**Email opener:** {r['Email_Opener']}\n\n")

    # 5) Compliant copy-paste accelerator (open in a browser)
    write_helper(rows)

    longest = max(rows, key=lambda r: r["Msg_Len"])
    counts = {b: sum(1 for r in rows if r["Band"] == b) for b in ("1A", "1B", "2", "3")}
    print(f"Wrote attendees_prioritized.csv, outreach_tracker.csv, "
          f"connection_messages.md, top_targets.md, outreach_helper.html "
          f"({len(rows)} contacts).")
    print(f"Band counts: {counts}")
    print(f"Longest LinkedIn note: {longest['Msg_Len']} chars ({longest['Name']}) "
          f"[limit {LIMIT}]")


if __name__ == "__main__":
    main()
