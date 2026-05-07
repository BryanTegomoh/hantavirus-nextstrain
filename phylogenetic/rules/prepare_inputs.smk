"""
Prepare metadata and sequences for tree construction.
"""

def build_config(wildcards):
    return config["builds"][wildcards.build]


rule prepare_inputs:
    input:
        metadata=lambda wildcards: build_config(wildcards)["input_metadata"],
        sequences=lambda wildcards: build_config(wildcards)["input_sequences"],
    output:
        metadata="results/{build}/metadata.tsv",
        sequences="results/{build}/sequences.fasta",
    log:
        "logs/{build}/prepare_inputs.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        cp {input.metadata:q} {output.metadata:q}
        cp {input.sequences:q} {output.sequences:q}
        python ../scripts/validate_metadata.py \
            --metadata {output.metadata:q} \
            --sequences {output.sequences:q}
        """
