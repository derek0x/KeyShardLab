# ShardWeaver Vault

ShardWeaver Vault is a solo web3 tools project that mimics how a personal developer would prototype a secure key sharding workflow. The goal is to capture the feel of an evening hobby project, documenting small incremental improvements, and shipping a lightweight CLI that helps me sketch safe key shard layouts.

## Concept

- Generate random recovery shards for arbitrary secret material (mnemonics, API keys, contracts) and tag them with metadata.
- Suggest storage guidance based on a simple risk matrix so that shards can be distributed across devices or trusted friends.
- Keep everything offline-friendly; the project is designed to run locally with zero dependencies on the blockchain or network.

## Features to ship

1. CLI-based generator that writes a deterministic shard pack for a given secret string.
2. Metadata profiling (storage location labels, risk notes, last verification date).
3. A logging helper that stores change notes for every shard bundle in an append-only text log.

## Architecture sketch

- `src/cli.py`: Entry point for orchestrating shard generation and metadata capture.
- `src/ledger.py`: Utilities for formatting shard bundles, aligning them with storage guidance, and generating log entries.
- `data/`: Example payloads, templates, and helper manifests.

## Next steps

1. Build a prototype CLI flow that gathers a secret phrase, splits it, and records metadata.
2. Add a storage planner that recommends safe split counts and backup locations.
3. Document every increment in `CHANGELOG.md` to keep the solo dev vibe.

Note: This project is intentionally small and personal; no build system or heavy automation is required. Everything is kept textual to stay true to the mock solo-lab experience.

## Usage snapshot

```bash
python -m src.cli --secret "my mnemonic phrase" --label "Ledger Warmup" --count 4
```

The command prints every shard, the seal hash, and a friendly risk reminder. Additionally, it now prints the planner suggestions (distribution and note) and the log entry stores the recommended distribution for future journaling.

## Storage planning notes

Every bundle now pairs with a micro-plan from `src/planner.py`. The planner takes the total shard count and risk level and returns a short list of storage tiers plus a personal note reminder. That distribution gets captured in the log entry so I can review it later without running the CLI again.

## Reading the log

There's a tiny helper in `src/log_reader.py` that replays the last few entries from `logs/shard_history.log`. Run it like `python -m src.log_reader --limit 5` to see what labels were generated most recently and where those shards were meant to live. It keeps the solo-lab feel by staying offline and textual.

## Validating the log

`src/validator.py` does a quick pass over that same log file and reports any missing timestamp/label/seal shards. I run `python -m src.validator --limit 8` before every commit to make sure the history file still looks human and complete.

## Digest snapshots

`src/digest.py` reads the log again, builds a few bullet points, and can write them to `data/digest_summary.md`. I usually run `python -m src.digest --limit 4 --out data/digest_summary.md` after a session to keep a readable short-form record of the most recent vaults.

## Jotting lab notes

The project keeps a small Markdown log under `data/lab_notes.md` and `src/note_keeper.py` can append entries for me. Running `python -m src.note_keeper "Experimenting with planners tonight"` stamps the current time and saves the entry so I can remember what I was testing in each session.

## Running the tests

Simple assertions live under `tests/`; nothing fancy, just `python -m pytest` or `python -m unittest discover` whenever I feel like a quick check before the next evening session.

## Risk guidance data

Risk levels now draw from `data/risk_guidelines.json`, so every plan includes a small narrative note plus a preferred distribution list. That file lets me keep tweaking the solo workflow without touching the code, and it explains why the CLI is voicing the same teaching line every time.
