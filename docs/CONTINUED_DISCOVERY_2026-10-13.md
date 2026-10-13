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
