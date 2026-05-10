"""
Prepare metadata and sequences for tree construction.
"""

def build_config(wildcards):
    return config["builds"][wildcards.build]


def date_precisions(wildcards):
    return ",".join(build_config(wildcards).get("date_precisions", []))


rule prepare_inputs:
    input:
        metadata=lambda wildcards: build_config(wildcards)["input_metadata"],
        sequences=lambda wildcards: build_config(wildcards)["input_sequences"],
    output:
        metadata="results/{build}/metadata.tsv",
        sequences="results/{build}/sequences.fasta",
    params:
        tree_mode=lambda wildcards: build_config(wildcards).get("tree_mode", "ml"),
        date_precisions=date_precisions,
    log:
        "logs/{build}/prepare_inputs.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        if [ {params.tree_mode:q} = timetree ]; then
            python ../scripts/filter_temporal_records.py \
                --metadata {input.metadata:q} \
                --sequences {input.sequences:q} \
                --output-metadata {output.metadata:q} \
                --output-sequences {output.sequences:q} \
                --date-precisions {params.date_precisions:q}
        else
            cp {input.metadata:q} {output.metadata:q}
            cp {input.sequences:q} {output.sequences:q}
        fi
        python ../scripts/validate_metadata.py \
            --metadata {output.metadata:q} \
            --sequences {output.sequences:q}
        """
