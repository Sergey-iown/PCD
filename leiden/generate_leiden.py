#!/usr/bin/env python3
"""Build the ITC Leiden alumni LinkedIn connect kit.

Source: "Leiden Event 2026 - Milestone Conference ITC Leiden, Celebrating 50 Years
of Teaching Excellence" participant list (187 alumni, 21 classes, 28-29 Aug 2026,
Rapenburg 65, Leiden). The roster below is transcribed from that PDF.

Outputs (re-run with `python3 generate_leiden.py`):
  participants.csv     all 187 alumni + LinkedIn search links + a ready note
  leiden_connect.html  the click-through helper (open in a browser)

Nothing here talks to LinkedIn. It only builds search URLs and copies text to the
clipboard; you press Connect yourself.
"""
import csv
import json

ME_NO = 60                 # Sergey Bezborodov, class of 2006-2007
ME_CLASS = "2006–2007"

# (no, class, first name, family name, country during study, current country)
ROSTER = [
    (1, '1998–1999', 'Itzik', 'Amiel', 'Israel', 'Netherlands'),
    (2, '1999–2000', 'Conrad', 'Cassar Torregiani', 'Malta', ''),
    (3, '1999–2000', 'Juan', 'Martinez', 'Spain', ''),
    (4, '1999–2000', 'Louis', 'Nouel', 'Venezuela', 'Netherlands'),
    (5, '1999–2000', 'Erki', 'Uustalu', 'Estonia', ''),
    (6, '2000–2001', 'Yuri', 'Matsubara', 'Japan', ''),
    (7, '2000–2001', 'Roustam', 'Vakhitov', 'Russia', 'Netherlands'),
    (8, '2001–2002', 'Antonio', 'Alvarado Weffer', 'Venezuela', 'Luxembourg'),
    (9, '2001–2002', 'Anna', 'Bürchner', 'Hungary', ''),
    (10, '2001–2002', 'Emidio', 'Cacciapuoti', 'Italy', ''),
    (11, '2001–2002', 'Luis Javier', 'Garcia', 'Spain', ''),
    (12, '2001–2002', 'Johann', 'Hattingh', 'South Africa', ''),
    (13, '2001–2002', 'Lari', 'Hintsanen', 'Finland', ''),
    (14, '2001–2002', 'Irene', 'Mayans', 'Argentina', 'Switzerland'),
    (15, '2001–2002', 'Malgorzata', 'McElfresh', 'United States', ''),
    (16, '2001–2002', 'Barbara Emma Maria Luisa', 'Pizzoni', 'Italy', ''),
    (17, '2001–2002', 'Rafael', 'Rivera', 'Panama', ''),
    (18, '2001–2002', 'Raffaele', 'Russo', 'Italy', ''),
    (19, '2002–2003', 'Silvio', 'Cilia', 'Malta', ''),
    (20, '2002–2003', 'Stefano', 'Grilli', 'Italy', ''),
    (21, '2002–2003', 'Marek', 'Herm', 'Estonia', ''),
    (22, '2002–2003', 'Jacob', 'Houlie', 'Israel', ''),
    (23, '2002–2003', 'Alberto', 'Iadevaia', 'Italy', ''),
    (24, '2002–2003', 'Pál', 'Jalsovszky', 'Hungary', ''),
    (25, '2002–2003', 'Angel', 'Juarez', 'Spain', ''),
    (26, '2002–2003', 'Silvia', 'Kotanidis', 'Italy', ''),
    (27, '2002–2003', 'Eduardo', 'Meloni', 'Argentina', ''),
    (28, '2002–2003', 'Wolfgang', 'Oepen', 'Germany', ''),
    (29, '2002–2003', 'Yuri', 'Revenko', 'Kazakhstan', 'Canada'),
    (30, '2002–2003', 'Antonio', 'Valle', 'Switzerland', ''),
    (31, '2003–2004', 'Paulo', 'Bento', 'Brazil', ''),
    (32, '2003–2004', 'Linda', 'Brosens', 'Belgium', ''),
    (33, '2003–2004', 'Michele', 'Gusmeroli', 'Italy', ''),
    (34, '2003–2004', 'Lars Andreas', 'Henie', 'Norway', ''),
    (35, '2003–2004', 'Rolan', 'Jankelevits', 'Estonia', ''),
    (36, '2003–2004', 'Tiago', 'Neves', 'Portugal', ''),
    (37, '2003–2004', 'Federico', 'Pacelli', 'Italy', ''),
    (38, '2003–2004', 'Edoardo Patrick', 'Pedrazzini', 'Italy', ''),
    (39, '2003–2004', 'Francesco', 'Piani', 'Italy', ''),
    (40, '2003–2004', 'Anna', 'Scapa Passalacqua', 'Peru', ''),
    (41, '2003–2004', 'Safina', 'Smak Gregoor', 'Netherlands', ''),
    (42, '2003–2004', 'Rita', 'Szudoczky', 'Hungary', ''),
    (43, '2003–2004', 'Fernando', 'Tonanni', 'Brazil', ''),
    (44, '2003–2004', 'Claudia', 'Vargas', 'Colombia', 'France'),
    (45, '2003–2004', 'Emiliano', 'Zanotti', 'Italy', ''),
    (46, '2004–2005', 'Katri', 'Aarnio Kurz', '', 'Switzerland'),
    (47, '2004–2005', 'Walter', 'Andreoni', 'Italy', ''),
    (48, '2004–2005', 'Renata', 'Fontana', 'Brazil', 'United States'),
    (49, '2004–2005', 'Natalia', 'Luchkova', 'Russia', 'Netherlands'),
    (50, '2004–2005', 'Ramona', 'Piscopo', 'Malta', 'Switzerland'),
    (51, '2004–2005', 'Dhaval J.', 'Sanghavi', 'India', ''),
    (52, '2004–2005', 'Ichwan', 'Sukardi', 'Indonesia', ''),
    (53, '2004–2005', 'Giovanni', 'Vivona', 'Italy', ''),
    (54, '2005–2006', 'Svetlana', 'Bugayeva', 'Kazakhstan', 'Italy'),
    (55, '2005–2006', 'Jeronimo', 'Chavarria', 'Mexico', 'Luxembourg'),
    (56, '2005–2006', 'Laura', 'Greco', 'Italy', ''),
    (57, '2005–2006', 'Michael', 'Kandev', 'Canada', ''),
    (58, '2005–2006', 'Filippo', 'Santececchi', 'Italy', ''),
    (59, '2006–2007', 'Edward', 'Attard', 'Malta', ''),
    (60, '2006–2007', 'Sergey', 'Bezborodov', 'Kazakhstan', 'Switzerland'),
    (61, '2006–2007', 'Balthasar', 'Denger', 'Brazil', 'Netherlands'),
    (62, '2006–2007', 'Hiroyuki', 'Kato', 'Japan', ''),
    (63, '2006–2007', 'Valentino', 'Rosselli', 'Switzerland', ''),
    (64, '2006–2007', 'Houlu', 'Yang', 'China', 'Switzerland'),
    (65, '2007–2008', 'Chiara', 'Bardini', 'Italy', 'Luxembourg'),
    (66, '2007–2008', 'Gustavo', 'Carmona Sanches', 'Brazil', ''),
    (67, '2007–2008', 'Andrea', 'Detweiler', 'United States', ''),
    (68, '2007–2008', 'Bruno', 'Garrido', 'Brazil', ''),
    (69, '2007–2008', 'Yimin', 'Kou', 'China', ''),
    (70, '2007–2008', 'Onute', 'Krisciunaite', 'Lithuania', 'Luxembourg'),
    (71, '2007–2008', 'Carolina', 'Landim', 'Brazil', ''),
    (72, '2007–2008', 'Renata', 'Ramos Teixeira', '', 'France'),
    (73, '2007–2008', 'Paolo', 'Tripoli', 'Italy', ''),
    (74, '2008–2009', 'Leonardo Joao', 'Santos', 'Portugal', ''),
    (75, '2009–2010', 'Vikram', 'Chand', 'India', 'Switzerland'),
    (76, '2009–2010', 'Jia-Ying', 'Chua', 'Singapore', ''),
    (77, '2009–2010', 'Conor', 'Delaney', 'Ireland', ''),
    (78, '2009–2010', 'Filip', 'Delepiere', 'Belgium', ''),
    (79, '2009–2010', 'Andres', 'Gonzales', 'Colombia', ''),
    (80, '2009–2010', 'José', 'Guerra', 'Portugal', ''),
    (81, '2009–2010', 'Thomas', 'Hermie', 'Belgium', ''),
    (82, '2009–2010', 'Naoual', 'Jidal', 'Morocco', ''),
    (83, '2009–2010', 'Alejandro Enrique', 'Perez Colorado', 'Mexico', ''),
    (84, '2009–2010', 'Monica', 'Sada Garibay', 'Mexico', ''),
    (85, '2009–2010', 'Edgar', 'Santos Gomes', 'Brazil', ''),
    (86, '2009–2010', 'Raffaele', 'Villa', 'Italy', ''),
    (87, '2010–2011', 'Alina', 'Huseinova (Yaroshchuk)', 'Greece', ''),
    (88, '2010–2011', 'Stavros', 'Soupashis', 'Cyprus', ''),
    (89, '2011–2012', 'Kadambari', 'Chari', 'India', 'Luxembourg'),
    (90, '2011–2012', 'Ignacio', 'Gordillo', 'Spain', ''),
    (91, '2011–2012', 'Ying', 'Gu', 'China', 'Netherlands'),
    (92, '2011–2012', 'Rocio', 'Rivas Canales', 'Peru', ''),
    (93, '2011–2012', 'Roberto', 'Santos', 'Mexico', 'Luxembourg'),
    (94, '2011–2012', 'Francisco', 'Sepúlveda', 'Chile', ''),
    (95, '2011–2012', 'Giselle', 'Solis', 'Costa Rica', 'Luxembourg'),
    (96, '2011–2012', 'Diana', 'Tapia', 'Mexico', 'Belgium'),
    (97, '2012–2013', 'Gábor', 'Baranyai', 'Hungary', ''),
    (98, '2012–2013', 'Ramazan', 'Biçer', 'Turkey', ''),
    (99, '2012–2013', 'Rodrigo', 'Flores Benavides', 'Peru', 'United States'),
    (100, '2012–2013', 'Xiaoyan (Sharon)', 'Huang', 'China', ''),
    (101, '2012–2013', 'Yu', 'Jin', 'China', ''),
    (102, '2012–2013', 'Emily', 'Muyaa', 'Kenya', ''),
    (103, '2012–2013', 'Rezan', 'Okten', 'Netherlands', ''),
    (104, '2012–2013', 'Kazuko', 'Ota', 'Japan', ''),
    (105, '2012–2013', 'Domenico', 'Pezzella', 'Italy', ''),
    (106, '2012–2013', 'Vigdís Tinna', 'Sigurvaldadóttir', 'Iceland', ''),
    (107, '2013–2014', 'Francesco', 'Cardone', 'Italy', ''),
    (108, '2013–2014', 'Ankitha', 'Dange', 'India', ''),
    (109, '2013–2014', 'Avisha', 'Sood', 'India', ''),
    (110, '2013–2014', 'Ivan', 'Zammit', 'Malta/Denmark', ''),
    (111, '2014–2015', 'Alberto', 'Allegra', 'Italy', ''),
    (112, '2014–2015', 'Ashish', 'Apte', 'India', 'Ireland'),
    (113, '2014–2015', 'Adam', 'Becker', 'United States', ''),
    (114, '2014–2015', 'Paula', 'Beneitez', 'Spain', ''),
    (115, '2014–2015', 'Timmy', 'Borg Olivier', 'Malta', ''),
    (116, '2014–2015', 'Eter', 'Burkadze', 'Georgia', ''),
    (117, '2014–2015', 'Marco', 'Busia', 'Italy', ''),
    (118, '2014–2015', 'Shi (Jessica)', 'Chu', '', 'China'),
    (119, '2014–2015', 'Tommaso', 'Fonti', 'Italy', ''),
    (120, '2014–2015', 'Maria Cristina', 'Hernandez Barcelo', 'Dominican Republic', ''),
    (121, '2014–2015', 'Jorge Manuel', 'Sousa', 'Portugal', ''),
    (122, '2014–2015', 'Raghuram', 'Srinivasan', 'India', 'United Kingdom'),
    (123, '2015–2016', 'Ragnar Tjörvi', 'Baldursson', 'Iceland', 'Sweden'),
    (124, '2015–2016', 'Caio', 'Casiraghi', 'Italy', 'Luxembourg'),
    (125, '2015–2016', 'Gaurav', 'Deshpande', 'India', 'Netherlands'),
    (126, '2015–2016', 'Rongjiao', 'Fu', 'China', ''),
    (127, '2015–2016', 'Radhika', 'Karadkar', 'India', ''),
    (128, '2015–2016', 'Marta', 'Martino', 'Italy', ''),
    (129, '2015–2016', 'Eduardo', 'Orellana Polo', 'Mexico', ''),
    (130, '2015–2016', 'Anna', 'Ratzenhofer', 'Austria', 'Netherlands'),
    (131, '2015–2016', 'Edgar Andres', 'Ruiz Van den Enden', 'Colombia', ''),
    (132, '2015–2016', 'Vilmar Freyr', 'Saevarsson', 'Iceland', ''),
    (133, '2015–2016', 'Suhas', 'Sagar', 'India', ''),
    (134, '2015–2016', 'Wei Hwa', 'See', 'Singapore', ''),
    (135, '2015–2016', 'Oleksii', 'Sydoryn', 'Ukraine', 'United Arab Emirates'),
    (136, '2016–2017', 'Mery', 'Alvarado', 'Peru', 'Netherlands'),
    (137, '2016–2017', 'Ana Rita', 'Carvalho', 'Portugal', ''),
    (138, '2016–2017', 'Charlotte', 'Chen', 'China', ''),
    (139, '2016–2017', 'Victor', 'Cherulli', 'Brazil', 'Netherlands'),
    (140, '2016–2017', 'Antonino', 'Ferraro', 'Italy', 'Germany'),
    (141, '2016–2017', 'Luca', 'Galliani', 'Italy', ''),
    (142, '2016–2017', 'Tiago', 'Guarnieri Feracioli', 'Brazil', 'Switzerland'),
    (143, '2016–2017', 'Dalton', 'Hirata', 'Brazil', 'Netherlands'),
    (144, '2016–2017', 'Ariel', 'Hou', 'China', 'Netherlands'),
    (145, '2016–2017', 'Elaine Yi', 'Long', 'China', ''),
    (146, '2016–2017', 'Macarena', 'Lopez Tello', 'Spain', ''),
    (147, '2016–2017', 'Tetiana', 'Polonska', 'Ukraine', ''),
    (148, '2016–2017', 'Olesia', 'Skalenko', 'Ukraine', 'Luxembourg'),
    (149, '2017–2018', 'Pamela', 'Alvarado', 'Costa Rica', ''),
    (150, '2017–2018', 'Ruben', 'Cohen Pellico', 'Spain', 'Netherlands'),
    (151, '2017–2018', 'Eduardo', 'Gutierrez Hernandez', '', 'Luxembourg'),
    (152, '2017–2018', 'Aras', 'Görkem', 'Turkey', ''),
    (153, '2017–2018', 'Kostiantyn', 'Karaianov', 'Ukraine', ''),
    (154, '2017–2018', 'Monique', 'Malan', 'South Africa', 'Luxembourg'),
    (155, '2017–2018', 'Andrés Felipe', 'Mejía Vega', 'Colombia', ''),
    (156, '2017–2018', 'Navita', 'Parwanda', 'India', ''),
    (157, '2017–2018', 'Giuseppe Francesco', 'Patti', 'Italy', ''),
    (158, '2017–2018', 'Gonzalo', 'Suffiotti', 'Chile', ''),
    (159, '2018–2019', 'Sumeir', 'Ahuja', 'India', ''),
    (160, '2018–2019', 'David B.', 'Borinsky', 'United States', ''),
    (161, '2018–2019', 'Giovanni', 'Caroli', 'Italy', ''),
    (162, '2018–2019', 'William', 'Cyrelli', 'Brazil', ''),
    (163, '2018–2019', 'Kristina', 'Dudukchyan', 'Armenia', ''),
    (164, '2018–2019', 'Shikhar', 'Garg', 'India', 'Netherlands'),
    (165, '2018–2019', 'Isabella', 'Giraldo', 'Colombia', ''),
    (166, '2018–2019', 'Armen', 'Gyurjyan', 'Armenia', ''),
    (167, '2018–2019', 'Karen', 'Hernandez', 'Colombia', ''),
    (168, '2018–2019', 'Gautam', 'Kapil', 'India', ''),
    (169, '2018–2019', 'Sochara', 'Krautsch', 'Cambodgia', ''),
    (170, '2018–2019', 'Yifei', 'Li', 'Ukraine', 'Luxembourg'),
    (171, '2018–2019', 'Yueqi', 'Li', 'China', ''),
    (172, '2018–2019', 'Zoe Xiangxin', 'Li', 'Netherlands', ''),
    (173, '2018–2019', 'Beijia', 'Liu', 'China', 'Netherlands'),
    (174, '2018–2019', 'Antonio', 'Merola', 'Italy', ''),
    (175, '2018–2019', 'Ameya', 'Mithe', 'India', 'United Kingdom'),
    (176, '2018–2019', 'Oscar', 'Munevar', 'Colombia', ''),
    (177, '2018–2019', 'Nandita', 'Narayan', 'India', ''),
    (178, '2018–2019', 'Mohit', 'Parekh', 'India', ''),
    (179, '2018–2019', 'Warissing', 'Ramkooling', 'Thailand', ''),
    (180, '2018–2019', 'Jefferson', 'Ramos', 'Brazil', ''),
    (181, '2018–2019', 'Catarina', 'Ribeiro', 'Portugal', 'Luxembourg'),
    (182, '2018–2019', 'Efrain', 'Rodriguez Alzza', 'Peru', ''),
    (183, '2018–2019', 'Eduardo', 'Sanchez Paz', 'Spain', 'Netherlands'),
    (184, '2018–2019', 'Tina', 'Scicluna', 'Italy', ''),
    (185, '2018–2019', 'Ana Paula Maia', 'Soto', 'Brazil', ''),
    (186, '2018–2019', 'Liudmila', 'Titova', 'Russia', ''),
    (187, '2018–2019', 'Ying', 'Yan', 'Netherlands', ''),]

import re
from urllib.parse import quote_plus

EVENT = "the ITC Leiden 50-year Leiden Event"


def short_class(cls):
    """'2011–2012' -> '2011–12'."""
    a, b = cls.split("–")
    return f"{a}–{b[2:]}"


def name_parts(first, family):
    """Greeting name, plus a clean 'First Last' for searching.

    Handles the two shapes the roster uses: a western alias in brackets
    ('Shi (Jessica)' -> greet Jessica) and a maiden/alternate family name in
    brackets ('Huseinova (Yaroshchuk)' -> search both).
    """
    alias = re.search(r"\((.+?)\)", first)
    base_first = re.sub(r"\s*\(.*?\)\s*", " ", first).strip()
    if alias:
        greeting = alias.group(1)
    else:
        toks = base_first.split()
        greeting = " ".join(toks[:2]) if len(toks) == 2 else toks[0]

    fam_alt = re.search(r"\((.+?)\)", family)
    base_family = re.sub(r"\s*\(.*?\)\s*", " ", family).strip()

    search = f"{base_first} {base_family}"
    alt = None
    if alias:
        alt = f"{alias.group(1)} {base_family}"
    elif fam_alt:
        alt = f"{base_first} {fam_alt.group(1)}"
    return greeting, search, alt


def relation(cls):
    if cls == ME_CLASS:
        return "we were in the same ITC Leiden class (2006–07)"
    return f"fellow ITC Leiden alum — I was class of 2006–07, you {short_class(cls)}"


def note(greeting, cls, tone="event"):
    """LinkedIn connection note, kept inside the 200-character invite limit."""
    rel = relation(cls)
    tail = {
        "event": "Connecting here at the 50-year Leiden Event — hope to say hello over the two days.",
        "after": "Good to be part of the 50-year Leiden Event — connecting to keep in touch beyond it.",
        "plain": "Would like to connect and stay in touch through the ITC Leiden network.",
    }[tone]
    text = f"Hi {greeting}, {rel}. {tail} Best, Sergey"
    if len(text) > 200:  # fall back to the shortest form
        text = f"Hi {greeting}, fellow ITC Leiden alum (class of 2006–07). {tail} Best, Sergey"[:200]
    return text


def li_url(keywords):
    return "https://www.linkedin.com/search/results/people/?keywords=" + quote_plus(keywords)


def build():
    people = []
    for no, cls, first, family, study, current in ROSTER:
        if no == ME_NO:
            continue
        greeting, search, alt = name_parts(first, family)
        based = current or study
        people.append({
            "no": no,
            "cls": cls,
            "clsShort": short_class(cls),
            "name": f"{first} {family}",
            "greet": greeting,
            "search": search,
            "alt": alt,
            "study": study,
            "current": current,
            "based": based,
            "same": cls == ME_CLASS,
            "gap": abs(int(cls.split("–")[0]) - int(ME_CLASS.split("–")[0])),
            "liLeiden": li_url(f'"{search}" Leiden'),
            "liName": li_url(search),
            "liAlt": li_url(f'"{alt}" Leiden') if alt else "",
            "google": "https://www.google.com/search?q="
                      + quote_plus(f'site:linkedin.com/in "{search}" Leiden tax'),
        })
    return people


def write_csv(people, path="participants.csv"):
    cols = ["No", "Class", "Name", "Country during study", "Current country",
            "Same class as me", "LinkedIn search (name + Leiden)",
            "LinkedIn search (name only)", "Google fallback",
            "Connection note", "Status"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for p in people:
            w.writerow([p["no"], p["cls"], p["name"], p["study"], p["current"],
                        "yes" if p["same"] else "", p["liLeiden"], p["liName"],
                        p["google"], note(p["greet"], p["cls"]), ""])
    return path


def write_html(people, path="leiden_connect.html"):
    with open("template.html", encoding="utf-8") as fh:
        tpl = fh.read()
    payload = json.dumps(people, ensure_ascii=False, separators=(",", ":"))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(tpl.replace("/*DATA*/", payload))
    return path


if __name__ == "__main__":
    people = build()
    print(f"{len(people)} alumni (roster {len(ROSTER)} minus you)")
    print("wrote", write_csv(people))
    print("wrote", write_html(people))
