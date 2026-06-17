# PCD London 2026 — iOWN outreach kit

Outreach materials for following up with attendees of the **PCD London Conference**
(Drapers' Hall, City of London — Wednesday, 17 June 2026), where Sergey Bezborodov
presented **iOWN** (wealth & business architecture for international families).

## What's here

| File | What it is |
|------|------------|
| `attendees_prioritized.csv` | **Start here.** All 143 contacts, sorted by priority tier, each with a personalised LinkedIn connection note, a segment, a "why" reason, and a one-click LinkedIn search link. |
| `connection_messages.md` | The personalised notes grouped by tier — open, click search link, **Connect → Add a note**, paste. |
| `outreach_tracker.csv` | Working tracker (tier + ready message + status columns) — mark Connected / Note sent / Email sent / Replied. |
| `greetings_email.md` | Post-event greetings email draft (subject + body + variants) for the email channel. |
| `linkedin_connection_note.md` | Generic note templates (reference; `connection_messages.md` is the per-person version). |
| `generate_outreach.py` | Source script that builds the CSVs + messages (re-run to regenerate). |

## Prioritisation (how the tiers were set)

iOWN is a Swiss *wealth & business architect* serving international/HNW families and
their advisers, so contacts are scored by how directly they can **refer business or
partner**:

- **Tier 1 — priority (71):** senior decision-makers / referral sources at the core
  segments — private banking, trust & fiduciary, private-client law, private-client
  tax, wealth & investment — plus the two event hosts. Work these first.
- **Tier 2 — relevant (63):** juniors at those same firms (longer nurture) and
  adjacent services — business development, philanthropy, FX/payments, immigration,
  property, and jurisdiction-promotion bodies.
- **Tier 3 — long tail (9):** government/diplomatic (relationship, not commercial),
  PR, and hard-to-place firms. Connect when you have time.

Tiering is a heuristic from each person's title + firm — feel free to re-rank in the
CSV. (Re-run `python3 generate_outreach.py` to rebuild after edits.)

## "Can't I automate it instead of clicking 140 times?"

Short answer: **automate the email, do LinkedIn semi-manually for Tier 1–2 only.**

- **LinkedIn personalised invites can't be safely bulk-sent.** LinkedIn has no API/
  feature to send connection notes in bulk. Third-party browser bots (Waalaxy,
  Dux-Soup, LinkedHelper, HeyReach, …) automate the clicking but **violate LinkedIn's
  User Agreement**, and ~140 personalised invites in a short burst is exactly the
  pattern that gets accounts **restricted or banned**. Not worth risking your account.
- **This kit removes the typing, not the click.** Each note is pre-written and
  personalised, so a connect is: search link → Connect → Add a note → paste. Doing
  this for ~80 Tier 1–2 people, spread over a week (keep well under ~100 invites/
  week), is the safe, high-quality play. The Tier 3 long tail can be skipped or sent
  as plain invites (no note).
- **Email is the channel to scale.** Mail-merge is fully legitimate. Use
  `greetings_email.md` with your mail client / a mail-merge tool to reach the whole
  list at once — once you have email addresses (the guest list has none).

## Suggested workflow

1. **LinkedIn, Tier 1 today**, Tier 2 over the next few days — copy-paste from
   `connection_messages.md`, prioritising people you actually met.
2. **Email** everyone you have / can find an address for, using the draft.
3. **Track** in `outreach_tracker.csv`.

## Regenerating

```bash
python3 generate_outreach.py
```
Edit the `ATTENDEES` list, the `classify()` rules, or the message `CLAUSES` in the
script, then re-run. The script validates every note against the 300-char limit.
