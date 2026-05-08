"""
Curate NCBI records into segment-specific metadata and FASTA files.
"""

rule curate_segment:
    input:
        metadata="data/raw_metadata.tsv",
        sequences="data/sequences.fasta",
    output:
        metadata="results/{build}/metadata.tsv",
        sequences="results/{build}/sequences.fasta",
    params:
        segment=lambda wildcards: config["builds"][wildcards.build]["segment"],
    log:
        "logs/{build}/curate_segment.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        python ../scripts/assign_segments.py \
            --metadata {input.metadata:q} \
            --sequences {input.sequences:q} \
            --filter-segment {params.segment:q} \
            --output-metadata {output.metadata:q} \
            --output-sequences {output.sequences:q}
        python ../scripts/validate_metadata.py \
            --metadata {output.metadata:q} \
            --sequences {output.sequences:q}
        """
