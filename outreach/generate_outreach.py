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


def main() -> None:
    attendees_path = HERE / "attendees.csv"
    tracker_path = HERE / "outreach_tracker.csv"

    with attendees_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Name", "Position", "Company", "Country", "Role", "LinkedIn_Search_URL"])
        for name, position, company, country, role in ATTENDEES:
            w.writerow([name, position, company, country, role,
                        linkedin_search_url(name, company)])

    with tracker_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Name", "Company", "Country", "Role",
                    "LinkedIn_Search_URL",
                    "Connected (Y/N)", "Connect_Note_Sent (Y/N)",
                    "Email_Sent (Y/N)", "Replied (Y/N)", "Notes"])
        for name, _position, company, country, role in ATTENDEES:
            w.writerow([name, company, country, role,
                        linkedin_search_url(name, company),
                        "", "", "", "", ""])

    print(f"Wrote {attendees_path.name} and {tracker_path.name} "
          f"({len(ATTENDEES)} contacts).")


if __name__ == "__main__":
    main()
