# Continued Game Miner discovery — 2026-10-13

## Scope

Manual follow-up after the 2026-09-20 focused scans. This pass did **not** treat repository names, README claims, stars, or Game Miner scores as evidence of gameplay quality or market demand.

The pass first revisited the still-unreviewed repositories surfaced by the narrow Phaser incremental / fishing / mining searches, then ran additional focused GitHub searches around low-production loops: sorting, cleanup, salvage, claw-machine, collection, one-button and idle mechanics.

Priority remains:

1. compact browser/mobile interaction,
2. tangible reward / unlock / collection loop,
3. low content and production burden,
4. code-backed mechanic that can be tested quickly,
5. no inference of commercial demand without separate evidence.

## Strong candidates for live testing

### 1. ClickMining — `isa4ac/ClickMining`

Repo: https://github.com/isa4ac/ClickMining  
Author-hosted build: https://ajwhite00.github.io/ClickMining/

**Confirmed in code:**

- Tap/click a rock to damage it.
- Breaking a rock reveals a random mineral reward.
- The reward must be manually collected into a capacity-limited backpack.
- Backpack contents are sold for coins.
- Coins buy pickaxe power and backpack capacity.
- An Auto Miner unlock costs 350 coins; its damage and speed can then be upgraded.
- More valuable rock tiers can be purchased/unlocked.
- Input for the core mining/reward flow uses Phaser pointer events.

**Why it matters:** this is the cleanest new example of the target structure:

`tap → anticipation → visible random reward → capacity pressure → sell → upgrade → stronger/new target → automation`

It is much closer to a small progression game than a pure score arcade. It is also already a static browser game, making it a strong next Pages test.

**Status:** HIGH PRIORITY — deploy/play before drawing conclusions about feel or balance.

---

### 2. Kindworks House Cleanup — `kindworksgames/kindworks-house-cleanup`

Repo: https://github.com/kindworksgames/kindworks-house-cleanup

**Confirmed in code:**

- Mobile-first Phaser/Vite.
- Stage 1: drag individual objects into Compost / Recycle / Rubbish bins.
- Wrong bin records a mistake and returns the object.
- Stage 2: press and sweep over dirt particles with a vacuum/brush interaction.
- Completion requires at least 95% cleaned.
- Stars depend on mistakes: 3 stars for zero mistakes, 2 for <=2, otherwise 1.
- Level progress is saved locally.
- Difficulty is parameterized up to 750 levels; later bands increase object count and dust count rather than requiring hundreds of handcrafted scenes.

**Why it matters:** two tactile chores create a stronger sense of completion than a single reaction test, while production remains mostly procedural. It tests whether “visible mess → clean state → stars → next level” is satisfying enough to support a very cheap content model.

**Status:** HIGH PRIORITY for mobile tactile-loop testing. Long-term economy is thin, so this is a mechanic/retention test rather than a ready monetization thesis.

---

### 3. ORBIT Daily — `Ricko-Shaha/orbit-daily`

Repo: https://github.com/Ricko-Shaha/orbit-daily

**Confirmed in code:**

- Fully playable `standalone.html`.
- One input: tap/Space reverses orbital direction.
- Incoming hazards are generated deterministically from the UTC date.
- The same date always produces the same board.
- Best score is stored locally per day.
- Instant retry.
- Phaser scale mode is FIT and pointer input is wired directly.

**Why it matters:** extremely low production burden. Its interesting part is not progression but a repeatable **daily challenge** wrapper around a one-button skill game. Useful as a retention experiment that is structurally different from idle/progression projects.

**Status:** MEDIUM-HIGH PRIORITY — trivial to put on Pages, but evaluate as a daily-skill product, not as an incremental game.

---

### 4. Claw Machine — `variuzstudio/claw-machine-v1`

Repo: https://github.com/variuzstudio/claw-machine-v1

**Confirmed in code:**

- Touch-friendly left/right controls.
- Hold GRAB to lower the claw; release to attempt the grab.
- Seven visual prize types with different score values.
- Base grab chance is 95%.
- Successful grabs can still slip during retraction with a 2% chance check.
- The prize is physically carried to a chute, then a celebration overlay is shown.
- Successful prize delivery awards score and removes the item from the machine.

**Why it matters:** the core action has anticipation and a concrete reveal/reward object. It is a useful reference for the structure:

`position → commit → suspense → physical prize → reveal/celebration`

The current project has score rather than a real collection/economy, so its long-term loop is incomplete for our goal.

**Status:** MEDIUM-HIGH PRIORITY as a feel/reward experiment. If the grab itself feels good, a collection/unlock layer would be the obvious separate hypothesis.

---

### 5. Henry's Dig Adventure — depth-vs-attempt mechanic

Repo: https://github.com/PCebs-dev/Henrys-Dig-Adventure

The full project is much larger than our target, so this is **not** a recommendation to reuse its entire game.

**Confirmed isolated mechanic:**

- Each tile tracks its own `digCount`.
- Repeated digs on the same tile move into deeper reward tables.
- First dig has a high empty chance.
- Second and third+ digs increasingly favor better gem tiers.
- Some map locations contain buried chests that only trigger after a required depth.
- Cave visits have a limited number of digs.

**Why it matters:** a very cheap risk/allocation decision emerges from almost no content:

`spend a limited dig on a fresh unknown spot OR keep digging the same spot for deeper/better loot`

This is one of the strongest isolated mechanics in the pass because it can be implemented without the full exploration/adventure shell.

**Status:** HIGH PRIORITY as a prototype mechanic; LOW PRIORITY as a whole-project port.

## Secondary / control candidates

### Dungeon Idle — `mexedes/dungeon-idle`

Confirmed complete low-art idle skeleton: monsters generate DPS, heroes traverse the dungeon, taps grant bonus gold, floors unlock from total gold, traps multiply output, offline earnings are capped, and prestige grants Dungeon Gems.

Useful as a reference implementation / economy control because it is cheap visually and genuinely wired. Mechanically it is generic, so it does not currently outrank ClickMining.

### All-Things-JS Phaser Fishing — `All-Things-JS/phaser-fishing`

Compact loop: start fishing, react to three randomly appearing arrow prompts, catch a fish, carry it to an oven, cook it, then consume the cooked fish to add five seconds to the next fishing attempt.

The circular resource idea — **catch → cook → buy more opportunity to catch** — is more interesting than the surrounding prototype. There is no confirmed long-term economy or collection.

### Factory Sort — `williamwhorton/factory-sort`

Real Phaser sorting game with touch/tap interactions, conveyor speed progression and three increasingly fast levels. No meaningful meta progression found. Useful as a conveyor input reference, not a current product candidate.

### Recycle — `Omhet/recycle-game`

Swipe-based waste sorting with changing bin types, lives, increasing difficulty and score persistence. Polished arcade loop, but again mostly score chasing rather than tangible progression.

## Rejected / deprioritized in this pass

- `youtringscamera/WorldFishingLife` — project skeleton; `Game/main.ts` is effectively empty.
- `ypy-ifa/Elden-Thing` — false-positive Java university project, not a compact Phaser incremental.
- `Raksoiv/phaser-incremental-1` — tiny unit-spawn prototype; no meaningful economy/progression confirmed.
- `Krugalo/Incremental` — real Vue incremental code, but generic generators/currencies with weak tactile or reward identity.
- `thechaoticatmospheres/little-waters` — substantial aquarium simulation with water chemistry, breeding, plants, marketplace and automation; interesting but far beyond the current production-burden target.
- `giovanniypro-web/empire-idle` — broad management incremental with employees, departments, market, stocks, missions and large prestige trees; too system-heavy.
- `SpaceSquare640/Core-Idle` — clean deterministic idle engineering reference, but the playable demo is mainly resource accumulation + upgrade shop and lacks a tactile hook.
- `GreenEyeGM/Voidwork` — promising README, but its roadmap still contains TODOs for applying important spaceship upgrade effects (including auto-mine) to gameplay; do not treat the promised loop as complete.
- `patrickkang/run-robot` — functional one-button Flappy-style runner, but too familiar and no progression.
- `8Bts/Bear_The_Fisher` — working fishing score arcade with sharks and size-based score bonuses, but no meaningful long-term progression was found.
- `yossava/phaser-aquarium` — very large asset/content footprint (many fish/backgrounds/decorations) and long-form economy; unsuitable for the present low-production search.
- `mooreInteractive/loot-hoarder` — real chest/loot/inventory loop, but full RPG combat, equipment, skill tree, dungeon content and large art burden make the whole project too expensive. Keep only the chest/reveal presentation as a reference.
- `willcoming/neon-salvage` — substantial wave/build combat system (99-wave structure, multiple surge/resonance/trial systems); far beyond the intended simplicity.
- `jasonpanghf/solar-salvager` — coherent 90-second auto-shoot survival/challenge game with local history/share links, but it is primarily arcade score competition rather than a low-burden progression/collection loop.

## Current order for Pages/live playtests

1. **ClickMining** — strongest complete progression/reward candidate.
2. **Kindworks House Cleanup** — strongest tactile completion candidate.
3. **Claw Machine** — strongest anticipation / physical prize candidate.
4. **ORBIT Daily** — cheapest daily-retention experiment.
5. **Henry's Dig mechanic** — prototype separately rather than porting the whole game.
6. **Dungeon Idle** — useful control case for a generic low-art idle economy.

These ranks are **research priority, not commercial potential**. Demand, retention and monetization remain unmeasured.


---

## Recursive follow-up — tactile machines, reveal loops and hybrid mechanics

This continuation deliberately moved away from generic idle/clicker searches and targeted physical-feeling browser loops: repair, machinery, merge hybrids, gacha/reveal, cleanup and short service interactions. README claims were checked against implementation files where a project was promoted.

### HIGH — Fix It! — `masonlet/fix-it`

Repo: https://github.com/masonlet/fix-it

A particularly strong **tactile repair** candidate.

Confirmed in code:

- Broken items move along a conveyor.
- Tapping a fault opens a short timed repair minigame.
- Six implemented minigame types are wired through `MinigameManager`: tap, pump, drag, spin, swipe and timing.
- Pumping tracks pointer movement; spinning measures clockwise circular drag; the timing game has a rotating needle, multiple hit zones and explicit miss allowance.
- Successful repair removes one fault; later items can contain multiple faults.
- Difficulty independently ramps belt speed, item spawn interval and available minigame time.
- The design explicitly targets mouse and touch and adaptive portrait/landscape layouts.

Why it matters: it gets much more tactile variety from a small reusable verb set than a handcrafted level game. The useful structure is:

`moving object → spot fault → 2–4 s physical gesture → immediate fixed-state payoff → next object / more faults`.

Whole-game production burden is above ClickMining or ORBIT, but still bounded because six reusable repair verbs can service many object skins.

**Status: HIGH PRIORITY live mobile test.** For testing game feel, it currently outranks Gearworks.

### HIGH — Super Serious Gacha Simulator — `keyshooter/juniper-game-jam-26-clean-version`

Repo: https://github.com/keyshooter/juniper-game-jam-26-clean-version

Godot rather than Phaser, but unusually close to the project's original low-input/reward-loop target.

Confirmed in code:

- The player physically rotates the gachapon crank; clockwise pointer rotation is accumulated and every full 360° emits a capsule-spawn event.
- Capsule rarity is selected through weighted tables.
- Purchased upgrades modify rarity probabilities.
- A capsule immediately pays currency based on its value and a purchased money multiplier.
- Shop items also support passive money generation.
- The run has a concrete target: reach 100,000 money.
- The project includes distinct rarity presentation/particles and capsule visuals.

Useful structure:

`one repeated physical action → capsule anticipation → rarity reveal → currency → payout/odds/automation upgrade → better future reveals`.

This is the closest source-backed mechanic found so far to the previously discussed “simple action → anticipation/visual reward → next unlock” structure. The original project is Godot and has more art than ClickMining, so it is stronger as a **mechanic thesis/reference** than as the easiest Pages mirror.

**Status: HIGH PRIORITY mechanic reference / author-build playtest.**

### MEDIUM-HIGH — Gearworks — `GraFreak0/Gear-Shift`

Repo: https://github.com/GraFreak0/Gear-Shift

Confirmed:

- Machines travel along a conveyor.
- Missing parts are dragged from a tray into machine slots.
- Wrong/right interaction, early-fix bonuses and combo chains are implemented around the moving objects.
- Skills include belt freeze, slow motion and an automatic wrench.
- Upgrade/meta systems and mobile layout handling exist.
- Conveyor geometry changes with level.

It is a real compact machine-repair game, but **Fix It! is the stronger tactile reference** because its faults invoke genuinely different gestures rather than mostly part matching.

**Status: MEDIUM-HIGH live-test candidate.**

### MEDIUM-HIGH — Kitchen Merge — `prod-broke-again/kitchen-merge`

Repo: https://github.com/prod-broke-again/kitchen-merge

Confirmed:

- 6×6 merge board.
- Identical items progress through a five-step chain from seed to feast.
- Low-tier items are automatically dropped over time.
- Spawn charges regenerate and can be replenished through a rewarded action.
- A shift is won by producing the required number of max-tier feasts and lost when the board is jammed with no merge.
- Max-tier creation gives currency.
- The platform layer already separates local and Yandex Games SDK behavior; production output is static HTML5.

This is technically extremely close to deployment-ready for the user's target platforms. Its weakness is originality: the core merge loop is familiar, so it needs live evidence that the specific pacing/reward presentation is unusually sticky before treating it as a product thesis.

**Status: MEDIUM-HIGH control candidate; strong deployment fit, weaker novelty.**

### MEDIUM-HIGH — Merge Bowl — `mitchallen/game-merge-101`

Repo: https://github.com/mitchallen/game-merge-101

Confirmed:

- Finger/mouse aims a bowling-style lane and one tap launches the current puck.
- Same-tier puck collisions merge upward.
- Two max-tier pucks clear for a large bonus.
- Settled pieces accumulating back across the foul line cause game over.
- The next puck is previewed and best score persists locally.
- Rendering is Three.js but textures are generated procedurally; collision/merge physics are a compact custom 2D implementation.

Why it matters: it turns the familiar Suika merge rule into a more active, directional input. This gives the player a tactile shot and a chain-reaction payoff without requiring handcrafted content.

**Status: MEDIUM-HIGH live-test candidate.**

### MEDIUM — Kindworks Waste Cleanup — `kindworksgames/kindworks-waste-cleanup`

Confirmed:

- Layered rubbish pieces can only be selected when exposed.
- Selected pieces enter a five-slot tray.
- Three equal pieces disappear/recycle.
- Full tray before clearing the stack loses the level.
- Touch controls and local progression are wired.
- The repository contains 750 layouts.

Mechanically functional and mobile-friendly, but it is close to the familiar “triple tile / match tray” family and depends on a large layout catalog for its advertised campaign.

**Status: MEDIUM reference, below House Cleanup.**

### MEDIUM — Astro Stack — `dzyamik/cozy-stack`

A polished Suika-style physics merge with an 11-tier collection book, deterministic daily challenge and persistent streak/theme unlock layers. Mobile input and a Pages-ready build are present.

The retention wrappers are useful references, but the central mechanic is already highly familiar. Do not rank it above more differentiated loops merely because its implementation is mature.

### ISOLATED IDEA ONLY — Mycelium — `liuyuling528-oss/mycelium`

The whole project is too system-heavy for the production-burden target, but one mechanic is unusual: expanding a spatial network toward richer distant resources is penalized by transport loss and congestion, so “grow outward” is not automatically optimal.

Keep only this compact hypothesis:

`cheap nearby output vs costly route to richer distant node`.

Do not import the project's full disease, AI rival, tree, colony, strain and prestige systems into a small MVP.

### Deprioritized after inspection

- `mrwuss/idle` / Pressure Works — sophisticated hydraulic idle with flow/pressure/heat, R&D, departments, staff and prestige; far too system-heavy for the current search.
- `giovanniypro-web/empire-idle` — broad company-management tree rather than a compact physical loop.
- `risingore/gear-arena` / SOUL STRIKE — an interesting “charge, then one decisive button” combat idea, but the actual project carries substantial enemies, bosses, build/loadout, story and asset burden.
- `Stiggstogg/machines` / MACHINE DISCO — observe-and-reproduce rhythm patterns, but its identity relies heavily on authored music/levels.
- `warrenrross/Five-Element-Crafting` — clever ordered-pair crafting and discovery system, but roughly 100 entities / 110 recipes plus a second puzzle mode make it content-heavy.
- `masterhan/sugarspark-bakery` and `abrahamambedkar-debug/food-empire` — functioning service/economy games, but customer/recipe/NPC content pushes them away from the ultra-small target.

## Revised research-priority queue

For immediate **live feel tests**, not commercial validation:

1. **ClickMining** — complete low-cost progression/reward loop.
2. **Fix It!** — strongest varied tactile interaction loop.
3. **Super Serious Gacha Simulator** — strongest simple-action / rarity-reveal / upgrade thesis; test author build first.
4. **Kindworks House Cleanup** — visible before/after completion and tactile chores.
5. **Claw Machine** — physical prize anticipation.
6. **Merge Bowl** — differentiated active merge hybrid.
7. **ORBIT Daily** — minimal one-button daily-retention control.
8. **Kitchen Merge** — technically deployment-ready familiar merge control.
9. **Henry's Dig depth mechanic** — prototype the isolated choice rather than porting the whole project.
10. **Dungeon Idle** — generic low-art idle economy control.

The gacha and repair findings strengthen the case that the next search should continue around **physical action + reveal/reward**, rather than generic idle generators or large management games.


### MEDIUM-HIGH + external gameplay signal — Parcel Master — `benjames-171/parcel-master`

Repo: https://github.com/benjames-171/parcel-master

This candidate is unusual in the current list because it has both inspected implementation **and** independent jam feedback.

Confirmed in code:

- Parcels continuously travel along tile-based conveyor paths.
- Junctions have a small valid-direction set; interacting with a junction cycles its output direction.
- Parcels have types and must reach the matching output/bin.
- A wrong delivery costs one of three stars; reaching zero ends the run.
- Some parcels can cycle type while travelling, forcing attention/memory.
- The repository defines 9 levels and 3 difficulty bands with saved per-level star progress.

External signal from Gamedev.js Jam 2026:

- Won the Open Source challenge.
- Ranked #18 in Gameplay and #22 Overall in the jam results shown on itch.
- Expert feedback specifically praised the very simple interaction, escalating pressure, satisfying routing and replayability.

Production caveat: the core verb is tiny, but the original gets much of its longevity from authored conveyor layouts. A product inspired by it would need either procedural layouts or a cheap level-generation workflow to preserve the low-production target.

**Status: MEDIUM-HIGH live-test candidate, with stronger external gameplay evidence than most repositories in this research.**

### EXTERNAL SIGNAL ONLY — Junkbot Repair

Jam page: https://fatalfencer.itch.io/junkbot-repair

The source repository was not found in the GitHub search pass, so this is **not** promoted to a code-confirmed candidate yet.

Observed/publicly described loop:

- A mobile-oriented conveyor sorting / hidden-object activity.
- The game shows which junk parts are required to repair a robot; the player finds/sorts those parts from the junk conveyor.
- Ranked #14 Overall in Gamedev.js Jam 2026 and #2 in Graphics; public jam feedback includes positive comments on its addictive/chill sorting feel.

Keep it as a playtest/reference lead. Do not infer implementation burden until source or a deeper teardown is available.
