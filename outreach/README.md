# PCD London 2026 — iOWN outreach kit

Outreach materials for following up with attendees of the **PCD London Conference**
(Drapers' Hall, City of London — Wednesday, 17 June 2026), where Sergey Bezborodov
presented **iOWN** (wealth & business architecture for international families).

## What's here

| File | What it is |
|------|------------|
| `top_targets.md` | **Start here.** The ~25 highest-value contacts (Tier 1A), each with its personalised LinkedIn note **and** email opener. Do these first. |
| `attendees_prioritized.csv` | All 143 contacts, banded 1A → 3, each with a personalised LinkedIn note, a personalised email opener, a segment, a "why" reason, and a one-click LinkedIn search link. |
| `connection_messages.md` | The personalised LinkedIn notes grouped by band — open, click search link, **Connect → Add a note**, paste. |
| `outreach_tracker.csv` | Working tracker (band + ready message + email opener + status columns) — mark Connected / Note sent / Email sent / Replied. |
| `greetings_email.md` | Post-event greetings email draft (subject + body + variants); drop a per-person `Email_Opener` in after the salutation. |
| `linkedin_connection_note.md` | Generic note templates (reference; `connection_messages.md` is the per-person version). |
| `generate_outreach.py` | Source script that builds the CSVs + messages (re-run to regenerate). |

## Prioritisation (how the tiers were set)

iOWN is a Swiss *wealth & business architect* serving international/HNW families and
their advisers, so contacts are scored by how directly they can **refer business or
partner**:

- **Tier 1A — top targets (25):** the trimmed shortlist. Tier-1 contacts ranked by
  seniority (founders, CEOs, heads, partners), segment fit, and jurisdiction (Swiss /
  Monaco / Channel Islands / IoM / Gibraltar / Bermuda wealth hubs), plus the hosts.
  **Start here** — see `top_targets.md`.
- **Tier 1B — priority (46):** the rest of the senior referral sources / decision-
  makers at the core segments (private banking, trust & fiduciary, private-client law,
  private-client tax, wealth & investment).
- **Tier 2 — relevant (63):** juniors at those same firms (longer nurture) and
  adjacent services — business development, philanthropy, FX/payments, immigration,
  property, and jurisdiction-promotion bodies.
- **Tier 3 — long tail (9):** government/diplomatic (relationship, not commercial),
  PR, and hard-to-place firms. Connect when you have time.

Banding is a heuristic from each person's title + firm + country — feel free to
re-rank in the CSV, or change `TOP_TARGET_COUNT` / the scoring in the script and
re-run (`python3 generate_outreach.py`).

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

1. **LinkedIn, Tier 1A today** (`top_targets.md`), then 1B / 2 over the next few days —
   copy-paste from `connection_messages.md`, prioritising people you actually met.
2. **Email** everyone you have / can find an address for: paste their `Email_Opener`
   after "Dear <first name>," in the `greetings_email.md` body, then send / mail-merge.
3. **Track** in `outreach_tracker.csv`.

## Regenerating

```bash
python3 generate_outreach.py
```
Edit the `ATTENDEES` list, the `classify()` rules, or the message `CLAUSES` in the
script, then re-run. The script validates every note against the 300-char limit.
