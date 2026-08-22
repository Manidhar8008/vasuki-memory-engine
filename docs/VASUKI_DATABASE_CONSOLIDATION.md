# Vasuki Database Consolidation Map

## Purpose

This document records the August 2026 census of the SQLite databases found in the Termux environment and defines the proposed canonicalization strategy.

> **Safety rule:** do not delete databases based only on schema similarity. Verify content and code references before destructive cleanup.

## Executive finding

The Termux filesystem contains multiple generations of Vasuki databases, backups, founder stores, experimental stores, project-specific databases, and unrelated Linux/application databases.

The strongest current candidate for the primary Vasuki intelligence database is:

```text
/data/data/com.termux/files/home/vasuki/vasuki.db
```

It has 107 tables and contains the broadest current Vasuki corpus observed in the census.

## Canonical candidates

### Primary Vasuki database — KEEP

```text
~/vasuki/vasuki.db
```

- Size: 70,545,408 bytes
- Tables: 107
- Files: 41,802
- Documents: 595
- Memories: 21,474
- Entities: 48,238
- Entity mentions: 545,000
- Graph: 29,794
- Concepts: 5,000
- Skills: 246
- Self-functions: 23,629
- Self-modules: 3,066
- Self-classes: 2,863
- System modules: 8,395
- SQL references: 17,980
- Import edges: 17,936

This database appears to be the convergence point of several Vasuki architecture generations: filesystem indexing, documents, entities, concepts, memory, graph, founder intelligence, OCR, mobile/system telemetry, and self-analysis.

### Founder database — KEEP SEPARATE

```text
~/founder/founder.db
```

- Size: 62,914,560 bytes
- Tables: 15
- Artifacts: 41,908
- Imports: 150,200
- Entities: 54,436
- Memories: 17,019
- Relationships: 18,557
- Evidence: 16,594
- Documents: 886
- Decisions: 159
- Projects: 570
- Events: 9

This is a distinct founder-centric data model and should remain conceptually separate from the primary Vasuki system database until a formal federation layer exists.

## Historical Vasuki snapshots — ARCHIVE

### 92-table snapshot

```text
~/vasuki/db_backup/vasuki.db
```

Contains the older 92-table architecture with 41,802 files, 595 documents, 21,422 memories, 42,648 entities, 29,794 graph records, and 5,000 concepts.

Classification: historical snapshot.

### Day-1 Founder OS snapshot

```text
~/vasuki/db_backup/vasuki_day1_founder_os.db
```

Contains 64 tables and a large overlap with the older Vasuki corpus.

Classification: historical architecture snapshot.

### June 24 snapshot

```text
~/vasuki/db_backup/vasuki_backup_20260624.db
```

Contains 26 tables with 41,802 files, 595 documents, 44,444 entities, 545,000 entity mentions, 5,000 concepts, 29,794 graph records, 3,848 OCR records, and 165 timeline records.

Classification: historical snapshot.

### Early filesystem backup

```text
~/vasuki/db_backup/vasuki_backup.db
```

Contains only files, documents, and events. It is an early or partial backup.

Classification: early/partial backup.

## Duplicate-schema families

### Founder 3-table family

These share schema fingerprint `cea9fa5ddfd517b7`:

```text
~/M-V1-portfolio-/backend/founder.db
~/vasuki/db_backup/founder.db
~/vasuki/founder.db
```

All have:

- founder_evidence = 0
- founder_questions = 25
- founder_truths = 25

Classification: duplicate-schema family.

Recommended eventual action: verify row-level equality, keep one required copy, archive or remove redundant copies.

### Portfolio 4-table family

These share schema fingerprint `bd0824a4eda3217a`:

```text
~/vasuki/portfolio_api/data/portfolio.db
~/vasuki/db_backup/portfolio.db
```

Both contain the same four-table structure and five `stats` rows.

Classification: duplicate portfolio database family.

## Empty database candidates

The census found zero-byte database files:

```text
~/vasuki/termex.db
~/Vasuki/projects/vasuki-memory-engine/founder.db
~/Vasuki/projects/vasuki-memory-engine/vasuki.db
~/vasuki/vasuki_archaeologist/founder.db
```

Classification: empty/non-database placeholders.

These are deletion candidates only after confirming that no code or configuration references them.

## Experimental / prototype databases

### Archaeologist founder store

```text
~/vasuki/vasuki_archaeologist/founder/founder.db
```

- Size: 786,432 bytes
- Tables: 46
- Contains experimental systems such as attention state, consciousness state, identity graphs, lake events, lessons_v2, memories_v2, goals, and search index.

Classification: experimental architecture prototype.

### Memory-engine founder store

```text
~/Vasuki/projects/vasuki-memory-engine/founder/founder.db
```

- Size: 667,648 bytes
- Tables: 25
- Contains devices, doctor agents, founder artifacts/content, founder entities/memory, project evidence, room entities/topology, and vision.

Classification: project/prototype database.

## Corrupted database

### JANANI.AI

```text
~/Vasuki/projects/JANANI.AI/dev.db
```

The census returned:

```text
database disk image is malformed
```

Classification: corrupted project database.

Do not use it as a Vasuki source of truth. Before deleting it, inspect project backups or attempt controlled recovery.

## Project-specific databases

These should remain outside the Vasuki memory core:

```text
~/downloads/Startup-borardcasting-system/jan_ai/jan_ai.db
~/downloads/Startup-borardcasting-system/jan_ai_saas.db
```

They are application databases for Jan AI and Jan AI SaaS rather than Vasuki's central intelligence substrate.

## Meta-database

```text
~/founder/founder_inventory.db
```

Contains `source_databases = 28`.

Classification: database inventory/meta-database.

Recommended future role: a formal Vasuki Database Registry describing database path, purpose, generation, owner, schema fingerprint, health, and canonical/archive status.

## Unrelated databases — DO NOT TOUCH

Exclude Kali/Linux/Termux/system/application databases such as:

```text
~/downloads/tabby/ee/tabby-db/schema.sqlite
~/kali-arm64/etc/alternatives/regulatory.db
~/kali-arm64/var/cache/man/*
~/kali-arm64/var/lib/wtmpdb/wtmp.db
~/kali-arm64/usr/share/nmap/scripts/script.db
~/kali-arm64/usr/share/nmap/nselib/data/mgroupnames.db
```

These are not part of the Vasuki intelligence corpus.

## Target state

```text
~/vasuki/
├── db/
│   ├── vasuki_primary.db
│   └── founder_primary.db
├── archive/
│   ├── vasuki_92_tables.db
│   ├── vasuki_day1_founder_os.db
│   ├── vasuki_backup_20260624.db
│   └── vasuki_files_events_backup.db
├── projects/
│   ├── jan_ai.db
│   └── jan_ai_saas.db
└── registry/
    └── database_inventory.db
```

The exact filenames and migration paths are implementation choices; the important constraint is to establish clear canonical, archive, experimental, and project boundaries.

## Cleanup sequence

```text
CONTENT COMPARISON
        ↓
REFERENCE ANALYSIS
        ↓
DUPLICATE CONFIRMATION
        ↓
CANONICALIZATION
        ↓
ARCHIVE
        ↓
DELETION
```

The next technical operation is therefore not destructive cleanup. It is row-level comparison plus source-code/reference analysis.

## Final recommendation

### Primary

```text
~/vasuki/vasuki.db
```

### Founder

```text
~/founder/founder.db
```

### Archive

```text
~/vasuki/db_backup/*
```

### Experimental

```text
~/vasuki/vasuki_archaeologist/founder/founder.db
~/Vasuki/projects/vasuki-memory-engine/founder/founder.db
```

### Delete candidates after verification

- zero-byte databases
- verified duplicate databases
- unused legacy micro-stores

### Never mix into Vasuki cleanup

- Kali/Linux/Termux system databases
- unrelated third-party application databases
