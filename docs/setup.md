# Setup

Create the conda environment:

```bash
conda env create -f environment.yml
conda activate hantavirus-nextstrain
```

Install local checks:

```bash
pre-commit install
```

Confirm the expected tools are available:

```bash
nextstrain version
augur --version
snakemake --version
datasets --version
dataformat --version
```

The local machine used to initialize this repository did not have the Nextstrain runtime or NCBI Datasets CLI on PATH. The environment file is the source of truth for project setup.
