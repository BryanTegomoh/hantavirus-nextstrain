# Data Governance

Commit code, documentation, configuration, accession lists, and tiny example records.

Do not commit:

- Private or unpublished sequences
- Raw NCBI downloads
- Patient-level data
- PHI-like fields
- Credentials or API keys
- Intermediate workflow products
- Auspice JSON outputs from sensitive analyses

Ignored paths include `data/raw/`, `data/private/`, `ingest/results/`, `phylogenetic/results/`, and `phylogenetic/auspice/`.

Run before pushing:

```bash
make validate
git diff --check
```
