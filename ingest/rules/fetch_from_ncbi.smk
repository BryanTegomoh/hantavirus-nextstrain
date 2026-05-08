"""
Fetch public records from NCBI Datasets and convert to TSV + FASTA.

The downloaded zip and extracted directory are intentionally ignored by git.
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


rule extract_ncbi_dataset:
    input:
        dataset_package="data/ncbi_dataset.zip",
    output:
        sequences="data/sequences.fasta",
        data_report="data/ncbi_dataset/data/data_report.jsonl",
    log:
        "logs/extract_ncbi_dataset.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        unzip -o {input.dataset_package:q} -d data/
        cp data/ncbi_dataset/data/genomic.fna {output.sequences:q}
        """


rule convert_ncbi_metadata:
    input:
        data_report="data/ncbi_dataset/data/data_report.jsonl",
    output:
        raw_metadata="data/raw_metadata.tsv",
    params:
        fields=",".join(config["ncbi_datasets_fields"]),
    log:
        "logs/convert_ncbi_metadata.txt"
    shell:
        r"""
        exec &> >(tee {log:q})
        dataformat tsv virus-genome \
            --inputfile {input.data_report:q} \
            --fields {params.fields:q} \
            > {output.raw_metadata:q}
        """
