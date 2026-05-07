# Workflow

The project has two stages.

## Ingest

The ingest stage acquires public NCBI records, normalizes metadata, assigns segments, and writes segment-specific FASTA and metadata files.

```bash
nextstrain build ingest
```

The first target is Andes virus, `Orthohantavirus andesense`, NCBI taxon `1980456`.

## Phylogenetic

The phylogenetic stage consumes curated segment-specific metadata and sequences, then builds Auspice datasets.

```bash
nextstrain build phylogenetic
nextstrain view phylogenetic
```

Initial build order:

1. `andes_s`
2. `andes_m`
3. `andes_l`
4. `context_s`

TreeTime should only be enabled after date precision and temporal signal checks pass on real data.
