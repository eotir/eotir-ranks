# Decisions and open questions

Date: 2026-10-09. This document records user direction separately from assistant recommendations.

## Ryan's directions

| ID | Direction | Scope/status |
|---|---|---|
| R-01 | Discover sources/repos and write AGENTS.md, INTENT.md and continuity docs | Authorized and implemented |
| R-02 | Strongly favor Combine Galactic Empire plaques plus another comprehensive table | Preferred starting direction; exact geometry/mapping unapproved |
| R-03 | Keep source precedence MOSTLY undecided; military first; find common middle ground | Use the provisional Navy/Marine/Army intersection; no broad source override |
| R-04 | Rename project files for safe web/Linux names | Authorized; 22 supplied files renamed with unchanged hashes; original names retained in manifest |
| R-05 | After documentation/reference review, begin separate rectangular beveled/textured colored tiles, then plaque combinations | Candidate rendering authorized; code cylinders separate initially |
| R-06 | Store kept/approved images locally; consider this an asset repository | All project candidates and later keepers live here with version/provenance history |
| R-07 | Long-term destination content/ranks and content/uniforms in codex-monarch; separate build workspace now, transfer later | Intended architecture; no canonical transfer or type change authorized in this session |
| R-08 | Prefer native local reads/writes over Desktop Commander MCP | Use native tools when available; connected-app reads still use their connector where appropriate |
| R-09 | Add black, white, purple, grey, silver, gold, orange and further color tiles for future mix-and-match; consider specialty branches/departments/divisions | Expanded candidate palette authorized; specialty/color meanings remain undecided |
| R-10 | Start putting military plaques together from the bottom upward | First E-1…E-7 candidate series implemented; remaining grades pending |
| R-11 | Use the Combine grey/blue family shared across military grades for the first E-1…E-7 drafts | Explicit draft-direction selection; not exact visual/assignment approval |
| R-12 | Supply a goal prompt for the entire military chart, other-branch candidates, more research, current HTML and an independent eotir-ranks GitHub repo | Prompt saved in docs/GOAL-PROMPT.md; full goal and repository setup are not started merely by drafting the prompt |

## Inherited rulings verified in current project documents

- Archived Navy shoulder boards are concepts only (Ryan, 2026-10-07, current music uniform working spec).
- Existing Standard/Shield/Stratus marks have distinct designs and entitlement rules; read the latest dated rulings before use.
- High Command heraldry entitlement has no supplied exhaustive grade membership map. Do not derive it from HC prefixes alone.
- Candidate/selected/approved/locked/published are separate states. This session does not approve its generated candidates by saving or displaying them.

## Open decisions — do not resolve silently

| ID | Question | Needed before |
|---|---|---|
| O-01 | Exact tile aspect ratio, bevel, texture, palette and backing treatment | Locking the tile system |
| O-02 | Preferred comprehensive companion: Whatsahonda recommended; Taivaansusi remains useful comparison | Adopting a plaque mapping rule |
| O-03 | Beyond the selected shared enlisted draft direction, how many rows/tiles and what color sequence for officer/command/high-command ranks? Branch-distinct or shared patterns? | Full plaque chart; all final assignments still require approval |
| O-04 | Plaques versus separate enlisted devices, and which dress variants | Full military insignia coverage |
| O-05 | Shared upper tiers, Throne and nonmilitary hierarchy/source reconciliation | Expanding beyond common military ground |
| O-06 | Era, rank, appointment, authorization-cylinder and High Command entitlement distinctions | Uniform regulations/canon promotion |
| O-07 | Git repository setup/remote, record schema and asset ownership after canonical transfer | Durable managed transfer workflow |
| O-08 | D1 need and first-class rank/uniform type support in canon-service | DB implementation/deployment |
| O-09 | Which exact candidates are selected and approved | Keeper promotion; new versions need their own approvals |
| O-10 | How should specialty branches/departments/divisions use the expanded palette: accents on shared rank patterns, separate palettes or another method? | Any specialty color assignment |

## Recommendations, not rulings

- Begin the preferred visual direction with a small tile palette and a few unassigned plaque studies, not all 69 military cells at once.
- Use the local workspace as review/staging; transfer only approved material to the canonical repo.
- Keep exact pattern composition machine-readable and eventually deterministic, so a full chart cannot drift from the approved individual assets.
- Use a small alternate design study only when it helps evaluate the preferred design; do not expand this into an unrelated visual overhaul.
- Keep a local keeper/candidate split and content hashes. Do not overwrite a selected/approved image during iteration.
- Compare shared rank patterns with a department accent tile against separate department palettes. Accents may preserve rank recognition more easily; separate palettes offer greater visual distinction but require more patterns and accessibility checks. This is a recommendation, not an adopted rule.

## Complete-chart goal invocation — 2026-10-09

Ryan invoked docs/GOAL-PROMPT.md: complete all 69 military cells and other-branch candidate coverage, maintain HTML, deterministic component composition, local assets, private eotir/eotir-ranks creation and scoped commits/pushes. This supersedes the earlier pending-invocation checkpoint. The private repository exists; pushed delivery must be verified separately. Draft officer/command/specialty mappings are authorized proposals; no exact visual, rank assignment, canon or production approval is implied.

## Public repository and static review publication — 2026-10-09

Ryan explicitly requested making eotir/eotir-ranks public and serving its static HTML using GitHub Pages. This supersedes the private-visibility requirement for this repository. Public candidate review does not approve assets, rank assignments or canon; all existing candidate states remain unchanged. Serve main at the repository root with index.html forwarding to assets/catalog-review.html and .nojekyll preserving static files. Excluded private exports remain local.

## Fiction clarification and review redesign — 2026-10-09

Ryan: payroll/personnel is all fiction in the sci-fi universe. Prior privacy framing was incorrect and does not establish a prohibition on publishing fictional material. Ryan requested dark mode only, smaller fonts/previews and a redesign. Use compact dark tables with expandable evidence and plain dark plaque backgrounds by default; optional dark checkerboard previews actual transparent edges. PNGs have real alpha outside the physical plaque; metal backing and tiles are opaque. No visual/assignment/canon approval is implied by the UI request.

## Cylinder research and Claude Design integration — 2026-10-09

Ryan authorized code-cylinder research primarily from supplied image/source references, with rank/class/grade associations, followed by the Claude Design site redesign. Supplied handoffs: D:\eotir\projects\.handoffs\Rank Plaque Catalog - Standalone.html and EOTIR-Ranks-site3.zip. Extract the full archive only into ignored staging and promote ranks-relevant presentation files. This is a site design change, not replacement/approval of plaque designs. Initial cylinder design and 69 military associations are proposals with null approval; other branch/shared mappings remain unresolved. See CODE-CYLINDERS.md for wearer/viewer conflicts and alternatives.

## Full-size cylinder options first

Ryan rejected the first-pass pixelated cylinder design and supplied nine new photo/illustration references including WebP and AVIF. He then clarified: render several options at large size and good quality first, retain original full-size gallery images, and fit/downscale later. Three separately saved reference-conditioned candidates now stage that design review. No adoption, cylinder-count change or rank preview replacement is implied.

## Cylinder base acceptance and engraved heraldry studies — 2026-10-09

Ryan said all three v2 cylinder options are good. This accepts the three base design directions for continued development; preserve their exact local masters and provenance. It does not approve subsequently generated engraved versions, establish universal cylinder-count entitlement or promote a rank/uniform document to canon.

Ryan requested the approved Imperial Republic Standard or Imperial Republic Shield engraved into the cylinders, with silver and gold versions and gold for High Command. Twelve v3 studies are saved: three accepted base directions × two distinct approved mark identities × two metal treatments. Keep every new engraving/version a candidate until Ryan reviews its exact image. Exact source conditioning, prompts, PNG hashes and dimensions are recorded in data/code-cylinder-engravings-v3.json. Their heraldry is reference-conditioned, not proven pixel-identical to locked anchors; gold may read as raised relief/inlay and needs review.

The verified music heraldry authority assigns the Shield to defense/military/security/police/intelligence and the Standard to civilian/government/patriotic use. Ryan explicitly requested both as design studies; that request does not grant the Standard new military wearer entitlement. Gold indicates High Command within the appropriate mark group; no exhaustive rank/person membership map exists. Do not infer membership from an HC grade prefix. The Standard is the bird inside the Shield with the border removed, not the different Stratus Phoenix.

Use neutral silver engraved metal, preserving the Shield's approved silhouette rather than reproducing its cyan-looking reference illumination as a new rank color. Locked Standard and clean Shield reference masters have opaque charcoal backgrounds; their backgrounds are not part of the engraved device. Shield transparent support parents have unresolved fringes and are unsuitable for direct compositing.

Ryan requires the gallery to use the supplied Claude Design presentation, not the interim standalone gallery design. Integrate the full-size studies into that presentation while preserving native downloads, local master bytes and review history. No cylinder assignments, count conventions or existing plaque designs change as part of this engraving/gallery work.
