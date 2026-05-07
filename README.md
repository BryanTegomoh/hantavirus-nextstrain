# Hantavirus Nextstrain Workflow

Private working repository for an Andes-first, context-aware Nextstrain workflow for hantavirus genomic surveillance.

The v1 target is `Orthohantavirus andesense` (Andes virus), NCBI taxon `1980456`. The first analytic surface is segment-specific Andes S, M, and L trees, followed by a low-density Orthohantavirus S context tree. The workflow does not concatenate S, M, and L segments in v1.

## Rationale

WHO and ECDC describe the May 2026 cruise-ship cluster as Andes hantavirus-related and note that Andes virus is the hantavirus with documented person-to-person transmission among close contacts:

- [WHO Disease Outbreak News, 4 May 2026](https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON599)
- [ECDC response, 6 May 2026](https://www.ecdc.europa.eu/en/news-events/cruise-ship-hantavirus-outbreak-ecdc-response-activated)
- [ECDC threat assessment brief, 6 May 2026](https://www.ecdc.europa.eu/sites/default/files/documents/TAB-hantavirus-06052026.pdf)

NCBI lists `Orthohantavirus andesense` as taxon `1980456`, with equivalent names including Andes virus and Andes hantavirus:

- [NCBI Taxonomy: Orthohantavirus andesense](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=1980456)

ICTV describes Orthohantavirus genomes as tri-segmented negative-sense RNA, with S, M, and L segments. Segment-specific trees are therefore the default analytic unit:

- [ICTV Orthohantavirus genus report](https://ictv.global/report/chapter/hantaviridae/hantaviridae/mammantavirinae/orthohantavirus)

## Repository Layout

```text
config/             Build registry and curated accession lists
data/example/       Tiny non-sensitive example records
docs/               Setup, usage, and interpretation notes
ingest/             NCBI acquisition and metadata curation workflow
phylogenetic/       Augur and Auspice workflow skeleton
scripts/            Local validation and curation helpers
```

## Quickstart

Create the runtime environment:

```bash
conda env create -f environment.yml
conda activate hantavirus-nextstrain
```

Run local validation:

```bash
make validate
```

Run the example segment assignment:

```bash
make ingest-example
```

Run the full workflows once the Nextstrain runtime and NCBI tooling are available:

```bash
make ingest
make build
make view
```

## Build Registry

The canonical build list lives in [config/builds.yaml](config/builds.yaml):

- `andes_s`
- `andes_m`
- `andes_l`
- `context_s`

## Data Governance

This repository is designed to track code, configuration, documentation, accession lists, and tiny example records only. Raw NCBI downloads, private data, unpublished outbreak sequences, intermediate products, logs, caches, and Auspice JSON outputs are ignored by default.

Before pushing, run:

```bash
make validate
git diff --check
```

## Current Status

This is a scaffolded research workflow. It is not an operational CDC, WHO, or public-health production system.
