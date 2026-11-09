# BEP: causal discovery in psychological networks

Bachelor end project, Data Science. How much causal structure can be recovered from the
cross-sectional psychometric datasets in the 
[ReBayesed project](https://github.com/KarolineHuth/ReBayesed) (Huth et al., 2026)?

## Setup

Dependencies are managed with uv.

    uv sync


## Getting the data

The data is not in this repository, because it belongs to the Rebayesed project. Can be manually downloaded from the [ReBayesed app](https://uvasobe.shinyapps.io/ReBayesed/):

1. Open the "Individual Studies" tab.
2. Click "Select/Deselect Filtered" to select every network.
3. Click "Download selected network results as RDS".
4. Put the file in `data/Individual_Studies/`.
5. Please cite the ReBayesed project in your works.

That gives one `.rds` holding all 294 networks, named after the day you downloaded it.
Mine is `filtered-network-data-2026-09-21.rds`, and the exploration below reads that
filename, so change it there if yours differs. Every field in the file is documented in
`docs/rds_filecols.md`.

Check the `Data Preparation` section below for additional data preprocessing



## Data Preparation

Split into two steps - `data/` folder is gitignored

1. The first step downloads files from the paper's [OSF project](https://osf.io/n8r9g/) into `data/osf/`. The `.rds` from "Getting the data" is still a manual download. The OSF files are:
   - one R cleaning script per network
   - the metadata sheet
   - the author's own copy of the results
 - The scripts show which raw columns and recodings sit behind each correlation matrix. And `cleaning_notes.md` contains notes on what needs fixing.

2. The second step reads the `.rds` once and writes three parquet tables to `data/tables/`:
   - `networks` (one row per network, its metadata)
   - `variables` (one row per node, with its matrix label, mean and SD)
   - `edges` (one row per node pair, with the correlation, partial correlation and every fit's estimate and Bayes factor)

To run, please use the following commands:
```
    uv run python -m bep.download_osf
    uv run python -m bep.tables
```

## Exploratory analysis

`src/eda/exploration.ipynb` is a first pass over the export: how big the corpus is, what
it measures, how much sample each network had per parameter, and how much evidence
stands behind an edge. Open it in an editor and run the cells against the project
environment; `uv sync` installs the kernel it needs.

Research notes, reading and reference PDFs live in the Obsidian vault at
`~/Documents/Obsidian/BEP`, not here.

## Research Question 1 - To what extent is the number of observations per edge parameter associated with the proportion of edges that can be oriented?

Excluding N0423_2, `R/rq1.R` selects one network per paper using seed `2026`, runs PC on the 126 primary
networks, then runs the other 167 separately. 

R packages are managed with renv. From the repository root:

```sh
Rscript -e 'renv::restore()'
Rscript R/rq1.R
uv run python -m bep.rq1
```

Used R to fit the graphs and export csvs to analyze in python. 

The main settings are alpha 0.01, `gaussCItest`, stable skeleton and relaxed
orientation. 

The additional networks are a descriptive sensitivity check, not independent
replications. 

The sensitivity checks run at alpha 0.001 and 0.05 and repeat alpha 0.01 with
three shuffled variable orders (seeds 2027–2029):

```sh
Rscript R/rq1_sensitivity.R
uv run python -m bep.rq1_sensitivity
```

They save separate CSVs under `outputs/pcalg/rq1/sensitivity/`
