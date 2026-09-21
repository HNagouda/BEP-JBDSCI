# BEP: causal discovery in psychological networks

Bachelor end project, Data Science. How much causal structure can be recovered from the
cross-sectional psychometric datasets in
[ReBayesed](https://github.com/KarolineHuth/ReBayesed) (Huth et al., 2026)?

## Getting the data

The data is not in this repository, because it is someone else's. Download it yourself
from the [ReBayesed app](https://uvasobe.shinyapps.io/ReBayesed/):

1. Open the "Individual Studies" tab.
2. Click "Select/Deselect Filtered" to select every network.
3. Click "Download selected network results as RDS".
4. Put the file in `data/Individual_Studies/`.

That gives one `.rds` holding all 294 networks, named after the day you downloaded it.
Mine is `filtered-network-data-2026-09-21.rds`, and the exploration below reads that
filename, so change it there if yours differs. Every field in the file is documented in
`docs/rds_filecols.md`.

## Setup

Dependencies are managed with uv.

    uv sync

## Exploratory analysis

`src/eda/exploration.ipynb` is a first pass over the export: how big the corpus is, what
it measures, how much sample each network had per parameter, and how much evidence
stands behind an edge. Open it in an editor and run the cells against the project
environment; `uv sync` installs the kernel it needs.

Research notes, reading and reference PDFs live in the Obsidian vault at
`~/Documents/Obsidian/BEP`, not here.
