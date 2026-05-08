"""
Build segment-specific maximum-likelihood trees.
"""

rule align:
    input:
        sequences="results/{build}/sequences.fasta",
    output:
        alignment="results/{build}/aligned.fasta",
    log:
        "logs/{build}/align.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        augur align \
            --sequences {input.sequences:q} \
            --output {output.alignment:q} \
            --fill-gaps \
            --nthreads auto
        """


rule tree:
    input:
        alignment="results/{build}/aligned.fasta",
    output:
        tree="results/{build}/tree_raw.nwk",
    log:
        "logs/{build}/tree.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        augur tree \
            --alignment {input.alignment:q} \
            --output {output.tree:q} \
            --method iqtree \
            --nthreads auto \
            --tree-builder-args "--seqtype DNA"
        """


rule refine:
    input:
        tree="results/{build}/tree_raw.nwk",
        alignment="results/{build}/aligned.fasta",
        metadata="results/{build}/metadata.tsv",
    output:
        tree="results/{build}/tree.nwk",
        node_data="results/{build}/branch_lengths.json",
    params:
        strain_id_field=config["strain_id_field"],
    log:
        "logs/{build}/refine.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        augur refine \
            --tree {input.tree:q} \
            --alignment {input.alignment:q} \
            --metadata {input.metadata:q} \
            --metadata-id-columns {params.strain_id_field:q} \
            --output-tree {output.tree:q} \
            --output-node-data {output.node_data:q} \
            --keep-root
        """


rule ancestral:
    input:
        tree="results/{build}/tree.nwk",
        alignment="results/{build}/aligned.fasta",
    output:
        node_data="results/{build}/nt_muts.json",
    log:
        "logs/{build}/ancestral.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        augur ancestral \
            --tree {input.tree:q} \
            --alignment {input.alignment:q} \
            --output-node-data {output.node_data:q}
        """
