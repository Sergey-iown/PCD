# PCD London 2026 — iOWN outreach kit

Outreach materials for following up with attendees of the **PCD London Conference**
(Drapers' Hall, City of London — Wednesday, 17 June 2026), where Sergey Bezborodov
presented **iOWN**.

## What's here

| File | What it is |
|------|------------|
| `attendees.csv` | All 143 attendees (2 hosts + guests; you are excluded). Name, title, company, country, and a **one-click LinkedIn people-search link** per person. |
| `outreach_tracker.csv` | Working tracker — mark each person Connected / Note sent / Email sent / Replied as you go. |
| `linkedin_connection_note.md` | Ready-to-paste LinkedIn connection notes (under the 300-char limit), with variants. |
| `greetings_email.md` | Post-event greetings email draft (subject + body + variants). |
| `generate_outreach.py` | Source script that builds the two CSVs (re-run to regenerate). |

## Why this is a kit and not "done for you"

Two parts of the request can't be automated from here, so the kit makes them as fast
as possible to do yourself:

1. **LinkedIn connecting** — there's no LinkedIn integration available, and bulk
   automated invites violate LinkedIn's User Agreement and risk account restrictions.
   So: each row in `attendees.csv` has a `LinkedIn_Search_URL` that pre-fills the
   person's name + company. Click it → open their profile → **Connect → Add a note**
   → paste from `linkedin_connection_note.md`. ~2 clicks each.
2. **Email** — the guest list has no email addresses, and there's no mail-sending
   tool here. Use `greetings_email.md` with your own mail client / mail-merge once you
   have addresses.

## Suggested workflow

1. **Prioritise.** Sort `attendees.csv` by the people you actually met, then by your
   highest-value targets (private banks, trust/family-office, private-client law/tax).
2. **Connect on LinkedIn in batches.** Spread invites over several days (keep well
   under ~100/week). Use the note variants; personalise the first line.
3. **Email** the people you have / can find addresses for, using the draft.
4. **Track** progress in `outreach_tracker.csv`.

## Regenerating the data

```bash
python3 generate_outreach.py
```

Edit the `ATTENDEES` list in the script to fix any title/company or add notes, then
re-run. (Titles/companies were aligned row-by-row from the source PDF; a couple of
attendees had no title printed and are intentionally left blank.)
