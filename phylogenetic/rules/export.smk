"""
Export Auspice datasets.
"""

rule traits:
    input:
        tree="results/{build}/tree_raw.nwk",
        metadata="results/{build}/metadata.tsv",
    output:
        node_data="results/{build}/traits.json",
    params:
        columns=" ".join(config["traits"]["columns"]),
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
            --columns {params.columns:q} \
            --confidence
        """


rule export:
    input:
        tree="results/{build}/tree_raw.nwk",
        metadata="results/{build}/metadata.tsv",
        nt_muts="results/{build}/nt_muts.json",
        traits="results/{build}/traits.json",
        auspice_config=config["export"]["auspice_config"],
        description=config["export"]["description"],
    output:
        auspice="auspice/by_build/{build}.json",
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
            --node-data {input.nt_muts:q} {input.traits:q} \
            --auspice-config {input.auspice_config:q} \
            --description {input.description:q} \
            --output {output.auspice:q}
        """


rule final_output_name:
    input:
        auspice=lambda wildcards: f"auspice/by_build/{output_to_build[wildcards.output]}.json",
    output:
        auspice="auspice/{output}.json",
    log:
        "logs/final_output_name/{output}.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        cp {input.auspice:q} {output.auspice:q}
        """
