# Setup

## Install conda

```bash
brew install miniforge
```

Restart your terminal so conda is on PATH, then create the project environment:

```bash
conda env create -f environment.yml
conda activate hantavirus-nextstrain
```

Confirm the expected tools are available:

```bash
augur --version
snakemake --version
datasets --version
dataformat --version
```

## Run the workflow

Ingest all Orthohantavirus sequences from NCBI:

```bash
make ingest
```

Build phylogenetic trees:

```bash
make build
```

View locally in Auspice:

```bash
make view
```

Copy final JSONs to root auspice/ for Nextstrain community build:

```bash
make copy-auspice
```

## Notes

- No Docker or Nextstrain CLI runtime required. The Makefile runs snakemake directly.
- Activate the conda environment before running any make target.
- Raw NCBI downloads and intermediate results are gitignored. Only final Auspice JSONs in root `auspice/` are committed.
