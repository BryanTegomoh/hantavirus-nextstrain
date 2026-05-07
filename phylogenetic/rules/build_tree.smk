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
            --fill-gaps
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
            --method iqtree
        """


rule ancestral:
    input:
        tree="results/{build}/tree_raw.nwk",
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
