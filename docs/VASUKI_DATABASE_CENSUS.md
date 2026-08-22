# Vasuki Database Census — August 2026

This document records the Termux database census used to identify the current Vasuki data landscape.

## Scope

Candidate roots scanned:

```text
~/vasuki
~/vasuki_core
~/founder
~/Vasuki
~/M-V1-portfolio-
~/downloads/Startup-borardcasting-system
```

Linux/Kali system databases are excluded from Vasuki analysis.

## Database inventory

| Path | Size | Tables | Key status |
|---|---:|---:|---|
| `~/vasuki/vasuki.db` | 70,545,408 B | 107 | Primary candidate |
| `~/founder/founder.db` | 62,914,560 B | 15 | Founder canonical candidate |
| `~/vasuki/db_backup/vasuki.db` | 59,510,784 B | 92 | Historical snapshot |
| `~/vasuki/db_backup/vasuki_day1_founder_os.db` | 54,173,696 B | 64 | Historical snapshot |
| `~/vasuki/db_backup/vasuki_backup_20260624.db` | 34,451,456 B | 26 | Historical snapshot |
| `~/vasuki/db_backup/vasuki_backup.db` | 13,242,368 B | 3 | Early/partial backup |
| `~/vasuki/vasuki_archaeologist/founder/founder.db` | 786,432 B | 46 | Experimental prototype |
| `~/Vasuki/projects/vasuki-memory-engine/founder/founder.db` | 667,648 B | 25 | Project/prototype store |
| `~/founder/founder_inventory.db` | 20,480 B | 1 | Meta-database |
| `~/M-V1-portfolio-/backend/founder.db` | 24,576 B | 3 | Duplicate-schema family |
| `~/vasuki/db_backup/founder.db` | 24,576 B | 3 | Duplicate-schema family |
| `~/vasuki/founder.db` | 24,576 B | 3 | Duplicate-schema family |
| `~/vasuki/portfolio_api/data/portfolio.db` | 28,672 B | 4 | Portfolio DB |
| `~/vasuki/db_backup/portfolio.db` | 28,672 B | 4 | Duplicate portfolio DB |
| `~/Vasuki/projects/JANANI.AI/dev.db` | — | — | Corrupted: malformed image |
| `~/vasuki/termex.db` | 0 B | 0 | Empty |
| `~/Vasuki/projects/vasuki-memory-engine/founder.db` | 0 B | 0 | Empty |
| `~/Vasuki/projects/vasuki-memory-engine/vasuki.db` | 0 B | 0 | Empty |
| `~/vasuki/vasuki_archaeologist/founder.db` | 0 B | 0 | Empty |
| `~/Vasuki/projects/vasuki-memory-engine/vasuki.db` | 0 B | 0 | Empty |
| `~/vasuki/memory/founder.db` | 12,288 B | 1 | Legacy micro-store |
| `~/vasuki/memory/vasuki.db` | 12,288 B | 1 | Legacy micro-store |
| `~/downloads/Startup-borardcasting-system/jan_ai/jan_ai.db` | 69,632 B | 7 | Jan AI application DB |
| `~/downloads/Startup-borardcasting-system/jan_ai_saas.db` | 49,152 B | 5 | Jan AI SaaS DB |

## Primary Vasuki corpus

`~/vasuki/vasuki.db` contains the richest current schema found in the census:

```text
Tables                 107
Files                41,802
Documents                595
Memories              21,474
Entities              48,238
Entity mentions      545,000
Graph                 29,794
Concepts               5,000
Skills                   246
Goals                    664
Decisions               188
Learnings                77
OCR records           3,848
Screenshots               5
Projects_v2              35
Self classes           2,863
Self functions       23,629
Self modules          3,066
SQL references       17,980
Import edges          17,936
System modules        8,395
Applications             972
Commands              5,070
App files             1,183
```

## Founder corpus

`~/founder/founder.db` contains a distinct founder-focused corpus:

```text
Artifacts             41,908
Imports              150,200
Entities              54,436
Memories              17,019
Relationships         18,557
Evidence              16,594
Documents                886
Decisions                159
Projects                 570
Events                     9
Observations              21
Truths                    16
```

## Historical overlap

The following historical databases contain substantial portions of the same large corpus:

- `~/vasuki/db_backup/vasuki.db`
- `~/vasuki/db_backup/vasuki_day1_founder_os.db`
- `~/vasuki/db_backup/vasuki_backup_20260624.db`

They should be treated as snapshots until row-level comparisons establish exact overlap and unique records.

## Schema fingerprints

The three small founder databases share:

```text
cea9fa5ddfd517b7
```

The two portfolio databases share:

```text
bd0824a4eda3217a
```

The two micro-memory databases share:

```text
45c1d091ca7b51fc
```

A schema fingerprint confirms structural similarity, not identical content.

## Corruption

`~/Vasuki/projects/JANANI.AI/dev.db` failed read-only inspection with:

```text
database disk image is malformed
```

This must be handled as a recovery problem rather than as a duplicate-cleanup candidate.

## Cleanup classification

### Keep as canonical

```text
~/vasuki/vasuki.db
~/founder/founder.db
```

### Preserve as archive

```text
~/vasuki/db_backup/vasuki.db
~/vasuki/db_backup/vasuki_day1_founder_os.db
~/vasuki/db_backup/vasuki_backup_20260624.db
~/vasuki/db_backup/vasuki_backup.db
```

### Preserve as experiments until reviewed

```text
~/vasuki/vasuki_archaeologist/founder/founder.db
~/Vasuki/projects/vasuki-memory-engine/founder/founder.db
```

### Verify then consolidate

```text
~/M-V1-portfolio-/backend/founder.db
~/vasuki/db_backup/founder.db
~/vasuki/founder.db

~/vasuki/portfolio_api/data/portfolio.db
~/vasuki/db_backup/portfolio.db

~/vasuki/memory/founder.db
~/vasuki/memory/vasuki.db
```

### Delete only after reference check

```text
zero-byte database files
```

### Keep outside Vasuki cleanup

```text
Kali/Linux/Termux system databases
unrelated third-party application databases
Jan AI project databases
```

## Next required inspection

The next step is to perform:

1. row-level comparison of duplicate-schema databases
2. table-level overlap analysis between Vasuki snapshots
3. source-code reference search for each database path
4. integrity checks on all proposed canonical databases
5. creation of a formal database registry

No destructive operation should occur before these checks.
