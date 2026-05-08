"""
Export Auspice datasets.
"""

rule traits:
    input:
        tree="results/{build}/tree.nwk",
        metadata="results/{build}/metadata.tsv",
    output:
        node_data="results/{build}/traits.json",
    params:
        columns=config["traits"]["columns"],
        strain_id_field=config["strain_id_field"],
    log:
        "logs/{build}/traits.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        augur traits \
            --tree {input.tree:q} \
            --metadata {input.metadata:q} \
            --metadata-id-columns {params.strain_id_field:q} \
            --output-node-data {output.node_data:q} \
            --columns {params.columns} \
            --confidence
        """


rule export:
    input:
        tree="results/{build}/tree.nwk",
        metadata="results/{build}/metadata.tsv",
        branch_lengths="results/{build}/branch_lengths.json",
        nt_muts="results/{build}/nt_muts.json",
        traits="results/{build}/traits.json",
        auspice_config=config["export"]["auspice_config"],
        description=config["export"]["description"],
    output:
        auspice="auspice/{build}.json",
    params:
        strain_id_field=config["strain_id_field"],
    log:
        "logs/{build}/export.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        augur export v2 \
            --tree {input.tree:q} \
            --metadata {input.metadata:q} \
            --metadata-id-columns {params.strain_id_field:q} \
            --node-data {input.branch_lengths:q} {input.nt_muts:q} {input.traits:q} \
            --auspice-config {input.auspice_config:q} \
            --description {input.description:q} \
            --output {output.auspice:q}
        """
