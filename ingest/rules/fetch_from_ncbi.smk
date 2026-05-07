"""
Fetch public records from NCBI Datasets.

The fetched package is intentionally ignored by git.
"""

rule fetch_ncbi_dataset_package:
    params:
        ncbi_taxon_id=config["ncbi_taxon_id"],
    output:
        dataset_package="data/ncbi_dataset.zip",
    retries: 5
    log:
        "logs/fetch_ncbi_dataset_package.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        datasets download virus genome taxon {params.ncbi_taxon_id:q} \
            --no-progressbar \
            --filename {output.dataset_package:q}
        """
