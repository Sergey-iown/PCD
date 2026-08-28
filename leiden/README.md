# ITC Leiden alumni — LinkedIn connect kit

Everything needed to connect with the **186 other alumni** on the participant list for
**Leiden Event 2026 — Milestone Conference ITC Leiden, Celebrating 50 Years of Teaching
Excellence** (28–29 August 2026, Rapenburg 65, Leiden).

The roster is 187 alumni across 21 classes (1998–1999 → 2018–2019), 53 countries.
Sergey Bezborodov is **#60, class of 2006–2007**, so he is filtered out of the list —
leaving 186 to connect with.

## Start here

Open **`leiden_connect.html`** in a browser (double-click it — it is a single self-contained
file, no server or internet needed to load).

For each person you get one primary button: **Copy note & open LinkedIn ↗**. It

1. copies a personalised connection note to your clipboard,
2. opens a LinkedIn people search for that person in a new tab, and
3. ticks them off your list.

On the LinkedIn tab you press **Connect → Add a note → paste → Send**. That last step is
deliberately yours — see *Why it isn't automated* below.

### What else is in the interface

| Control | What it does |
|---|---|
| **List / Focus** | List = scroll everyone. Focus = one person at a time, big button, `Enter` to connect, `→` to skip, `←` to go back. Focus is the fastest way to grind through a batch. |
| **Sort: closest to my class** | Default. Puts your own class of 2006–07 first, then 2005–06 and 2007–08, and so on outwards. Nearest classes have the highest acceptance rate, so work outwards from the middle. |
| **Class / country filters** | Do one class at a time, or everyone now in Switzerland, etc. |
| **Note: at the event / after the event / neutral** | Switches the wording of every note. Use *at the event* on 28–29 August, *after the event* in the days following, *neutral* later on. |
| **hide done** | On by default, so the list shrinks as you go. |
| **Progress bar + "in the last 24h"** | Tracks how many invites you have fired today and warns past 20 — LinkedIn throttles roughly 100–200 invitations per week. |
| **name only / Google** | Fallback searches for anyone the default search misses. For the three people who go by a second name (Sharon Huang, Jessica Chu, Alina Yaroshchuk) there is an extra button with the alternate name. |
| **Download progress CSV** | Exports who you have done and when, for your own records. |

Progress is stored in your browser's local storage, on that machine and browser only —
so use the same browser each session, and export the CSV if you want a durable copy.

## The note

Each note is personalised on class year and stays inside LinkedIn's 200-character
invitation limit (the longest is 182). Two shapes, picked automatically:

- **Same class (2006–07)** — Edward Attard, Balthasar Denger, Hiroyuki Kato,
  Valentino Rosselli, Houlu Yang:
  > Hi Edward, we were in the same ITC Leiden class (2006–07). Connecting here at the 50-year Leiden Event — hope to say hello over the two days. Best, Sergey
- **Every other class:**
  > Hi Vikram, fellow ITC Leiden alum — I was class of 2006–07, you 2009–10. Connecting here at the 50-year Leiden Event — hope to say hello over the two days. Best, Sergey

## Files

| File | What it is |
|---|---|
| `leiden_connect.html` | **The interface.** Open in a browser. Self-contained, all 186 people embedded. |
| `participants.csv` | All 186 as a spreadsheet: class, countries, both LinkedIn search links, a Google fallback, the ready note, and an empty Status column. |
| `generate_leiden.py` | Source script with the transcribed roster. Re-run `python3 generate_leiden.py` to rebuild the CSV and the HTML. |
| `template.html` | The HTML/CSS/JS shell the generator fills with participant data. Edit this, not `leiden_connect.html`. |

## Why it isn't automated

LinkedIn's user agreement forbids scraping and automated connecting, and accounts that
send bulk automated invitations get restricted. There is also no public API for sending
invitations. So this kit does the boring part — the right person, the right note, the
right order, the tracking — and leaves the actual Connect click to you. In practice a
click every few seconds in Focus mode gets through a class per sitting.

Pacing that keeps an account safe: **~20 invitations a day**, spread across the day.
At that rate all 186 take about ten days. Invitations with a note are also worth more
than bare ones — the acceptance rate is meaningfully higher, which is the whole point
of the personalised text.
