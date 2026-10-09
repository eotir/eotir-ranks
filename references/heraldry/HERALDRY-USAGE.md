# Phoenix names and wearer entitlement
Date: 2026-10-04
Authority: Ryan's latest naming/usage ruling in the anchor-registry chat. Supersedes the earlier same-day broad Gold Phoenix reservation.

| Design / material | Canonical name | Worn by | Stable registry id |
| --- | --- | --- | --- |
| Original unshielded gold bird | Gold Stratus (Gold Stratus Phoenix) | Members of the Royal First Family (Marc, Nicole, Ashlee); the Royal Imperial Throne; the Supreme Ruler's Chief of Staff (Terrisa Klone) | phoenix |
| Original unshielded silver bird | Silver Stratus (Silver Stratus Phoenix) | Royal Family members outside the Royal First Family; Agents of the Throne | phoenix-silver |
| Shield enclosing the other bird, gold | Gold Imperial Republic Shield (Gold Shield) | Defense/military/security/police/intelligence members of high command | phoenix-shield-gold |
| Shield enclosing the other bird, silver | Silver Imperial Republic Shield (Silver Shield) | Everyone else in defense/military/security/police/intelligence | phoenix-shield-silver |
| Interior shield bird alone, gold | Gold Imperial Republic Standard | Civilians/government officials/patriots who are members of high command | imperial-republic-standard-gold |
| Interior shield bird alone, silver | Silver Imperial Republic Standard | Everyone else in civilian/government/patriotic use | imperial-republic-standard-silver |

## Clarifications (Ryan, 2026-10-04, anchor-format brainstorm)
- **"Phoenix" alone is ambiguous.** It is also the name of a character and a ship, may name a
  doctrine, and more. Always qualify the mark: Gold/Silver Stratus, Gold/Silver Standard,
  Gold/Silver Shield.
- **The three phoenix marks:** the Imperial Republic Standard (phoenix without the shield; a.k.a.
  Gold Standard / Silver Standard); the Imperial Republic Shield (phoenix inside the shield; a.k.a.
  Gold Shield / Silver Shield); the Stratus Phoenix (a different bird design; a.k.a. Gold Stratus /
  Silver Stratus). Gold = high command (Standard/Shield) or the Throne/First Family/Chief of Staff
  (Stratus); silver = everyone else in that mark's group.
- **Shield wearers include intelligence**, alongside defense, military, security and police.
- **Gold Stratus names the Royal First Family as Marc, Nicole and Ashlee**, with the Throne, and
  includes the Supreme Ruler's Chief of Staff (Terrisa Klone). **Resolved (Ryan, 2026-10-04): the
  entitlement belongs to the Chief of Staff ROLE.** Terrisa wears Gold Stratus because she is the
  Supreme Ruler's Chief of Staff, not because she is Terrisa. (The registry previously called her
  "the only documented exception"; that wording is superseded.)

## Design identity and approval
Stratus and Standard are DIFFERENT bird designs. The Standard must preserve the bird currently inside the Imperial Republic Shield, removing only its border. Do not extract the Stratus bird instead. The cyan/violet asset `phoenix-shield` is the existing production-brand treatment of the Imperial Republic Shield; the wearer ruling specifies gold and silver, not a cyan/violet rank entitlement.

Names and wearer rules are Ryan-approved. Preserve each existing asset's approval status; naming does not silently approve a prior CANDIDATE. Ryan approved both Standard renders on 2026-10-04; both are now LOCKED. Future new variants still require review before keeper promotion. Ryan approved the Gold Shield (`phoenix-shield-gold`) on 2026-10-04; it is now LOCKED (it had been a CANDIDATE, kept separate from its name/usage ruling). The same day he confirmed Gold Stratus (`phoenix`), which had no status at all, as LOCKED. Existing Silver Shield and Silver Stratus remain LOCKED. Ryan locked the remaining status-less marks on 2026-10-05: `phoenix-shield` (cyan/violet production brand), `hapes`, `house-stratus`. Every heraldry entry is now LOCKED. High command is recorded verbatim; specific ranks and membership were not supplied and must not be invented.

## Compatibility and scope

Executor press-podium ruling (Ryan, 2026-10-04): civilian government announcement podiums use the Imperial Republic Standard, the same Phoenix without the Shield. This supersedes his earlier request to place shielded Phoenix marks on this song's podiums. Preserve prior images/verdicts as history; submit replacement versions for review. This is an institutional podium placement ruling, not a change to character wearer entitlement or production-brand end cards.
Keep existing registry ids, source asset filenames and storyboard references. Use name/full_name for canon. Display names come from each anchor file's `name` (generated into `catalog-labels.json` `byId`); `labels.logos` is a stage-A fallback only. note carries usage to the catalog. Preserve documented era gates and exceptions. Branding on end cards is separate from in-world wearer entitlement. This ruling does not automatically replace insignia on locked character anchors or released videos.

## Sources and records
- videos/refs/anchors/ (anchor files; source of truth)
- videos/refs/registry.json (generated)
- videos/refs/catalog-labels.json (`byId` block generated)
- docs/sessions/2026-10-04-anchor-registry-management.md
- refs/_candidates/imperial-republic-standard-2026-10-04/REVIEW.md (render provenance/review gate)
- gold-heraldry-lock_2026-10-04-publication.json (Gold Shield + Gold Stratus LOCKED rows published to D1 and verified live; registry commit 3e3062c1)

## Publication verification
Five existing anchor labels/notes are live and equal canonical source. All five existing CDN assets byte-match their local originals and decode. Receipt: phoenix-names_2026-10-04-publication.json. Local rebuild passed (120 anchors), 89 focused parser/data tests passed. Standard source candidates are preserved at native 1254x1254; Ryan subsequently approved keeper promotion. Their publication receipt is imperial-republic-standard_2026-10-04-publication.json.

## Standard approval and live verification
Ryan approved both Standard keepers, 2026-10-04. Gold/silver Standard anchors are LOCKED and published. Both CDN PNGs byte-match approved candidates; authenticated anchor API matches canonical metadata. Receipt: imperial-republic-standard_2026-10-04-publication.json. Rebuild: 122 anchors; 89 focused tests passed. No additional generation or changes to existing Shield/Stratus imagery.
