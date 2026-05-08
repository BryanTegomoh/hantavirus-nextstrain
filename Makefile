PYTHON ?= python3

.PHONY: help setup validate validate-example ingest-example ingest build copy-auspice view clean

help:
	@printf "Targets:\n"
	@printf "  setup            Create the conda environment from environment.yml\n"
	@printf "  validate         Run local metadata and repository safety checks\n"
	@printf "  ingest-example   Run deterministic segment assignment on example data\n"
	@printf "  ingest           Run the Nextstrain ingest workflow\n"
	@printf "  build            Run the Nextstrain phylogenetic workflow\n"
	@printf "  copy-auspice     Copy final Auspice JSONs to root auspice/ for community build\n"
	@printf "  view             Open local Auspice datasets with Nextstrain\n"
	@printf "  clean            Remove workflow outputs and local caches\n"

setup:
	conda env create -f environment.yml

validate: validate-example
	$(PYTHON) scripts/check_repository_safety.py .

validate-example:
	$(PYTHON) scripts/validate_metadata.py \
		--metadata data/example/metadata.tsv \
		--sequences data/example/sequences.fasta

ingest-example:
	$(PYTHON) scripts/assign_segments.py \
		--metadata data/example/raw_metadata.tsv \
		--sequences data/example/raw_sequences.fasta \
		--output-metadata data/example/metadata.tsv \
		--output-sequences data/example/sequences.fasta

ingest:
	cd ingest && snakemake --cores all

build:
	cd phylogenetic && snakemake --cores all
	$(MAKE) copy-auspice

copy-auspice:
	mkdir -p auspice
	cp phylogenetic/auspice/ortho_s.json auspice/hantavirus-nextstrain_S.json 2>/dev/null || true
	cp phylogenetic/auspice/ortho_m.json auspice/hantavirus-nextstrain_M.json 2>/dev/null || true
	cp phylogenetic/auspice/ortho_l.json auspice/hantavirus-nextstrain_L.json 2>/dev/null || true

view:
	auspice view --datasetDir auspice

clean:
	rm -rf .snakemake ingest/.snakemake phylogenetic/.snakemake \
		scripts/__pycache__ ingest/results ingest/data ingest/logs ingest/benchmarks \
		phylogenetic/results phylogenetic/auspice phylogenetic/logs \
		phylogenetic/benchmarks auspice
