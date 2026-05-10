# Hantavirus Nextstrain Workflow

Public working repository for a pan-Orthohantavirus Nextstrain workflow. The primary output is segment-specific maximum-likelihood trees for all publicly available Orthohantavirus sequences from NCBI, with Andes virus clustering naturally within the S tree alongside other New World hantaviruses.

Target taxon: `Orthohantavirus`, NCBI taxon `1980442`. Builds: S, M, and L segment trees. Segments are built independently and not concatenated.

## Rationale

WHO and ECDC describe the May 2026 cruise-ship cluster as Andes hantavirus-related. Andes virus is the only hantavirus with documented person-to-person transmission among close contacts. There is no publicly available phylogenetic tree covering all Orthohantavirus sequences in the context of this outbreak:

- [WHO Disease Outbreak News, 4 May 2026](https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON599)
- [ECDC response, 6 May 2026](https://www.ecdc.europa.eu/en/news-events/cruise-ship-hantavirus-outbreak-ecdc-response-activated)
- [ECDC threat assessment brief, 6 May 2026](https://www.ecdc.europa.eu/sites/default/files/documents/TAB-hantavirus-06052026.pdf)
- [NCBI Taxonomy: Orthohantavirus](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=1980442)
- [ICTV Orthohantavirus genus report](https://ictv.global/report/chapter/hantaviridae/hantaviridae/mammantavirinae/orthohantavirus)

## Repository Layout

```text
config/             Build registry and curated accession lists
data/example/       Tiny non-sensitive example records
docs/               Setup, usage, and interpretation notes
ingest/             NCBI acquisition and metadata curation workflow
phylogenetic/       Augur and Auspice workflow
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

- `ortho_s`: all Orthohantavirus S-segment sequences (primary)
- `ortho_m`: all Orthohantavirus M-segment sequences
- `ortho_l`: all Orthohantavirus L-segment sequences
- `ortho_s_time`: dated S-segment records for exploratory time-resolved analysis
- `ortho_m_time`: dated M-segment records for exploratory time-resolved analysis
- `ortho_l_time`: dated L-segment records for exploratory time-resolved analysis

Output JSON files follow the Nextstrain community naming convention:
`auspice/hantavirus-nextstrain_S.json`, `_M.json`, `_L.json`, and
`_S_time.json`, `_M_time.json`, `_L_time.json`

## Nextstrain Community Build

The public community trees are available at:

```
nextstrain.org/community/BryanTegomoh/hantavirus-nextstrain/S
nextstrain.org/community/BryanTegomoh/hantavirus-nextstrain/M
nextstrain.org/community/BryanTegomoh/hantavirus-nextstrain/L
```

## Data Governance

This repository tracks code, configuration, documentation, accession lists, and tiny example records only. Raw NCBI downloads, private data, unpublished outbreak sequences, intermediate products, logs, caches, and Auspice JSON outputs are ignored by default.

Before pushing, run:

```bash
make validate
git diff --check
```

## Current Status

Active development. Environment setup required before running the full workflow. See [docs/setup.md](docs/setup.md).
