# Phylogenetic Workflow

This workflow will produce segment-specific Auspice datasets for Andes virus and a lower-density Orthohantavirus S context tree.

Run from the repository root:

```bash
nextstrain build phylogenetic
nextstrain view phylogenetic
```

The initial implementation validates inputs and provides the Augur rule structure. Full tree construction requires curated references in `phylogenetic/defaults/references/`.
