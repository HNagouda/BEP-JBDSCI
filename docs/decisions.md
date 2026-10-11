# Decisions

Every choice that shapes the data or the analysis, with the date and why. The working
notes behind each one are in `data/cleaning_notes.md`.

## 2026-10-11: drop `N0423_2`

The app export has 294 networks and the paper says 293. The OSF copy of the results is our export minus
`N0423_2`. `N0423_2` is labelled "Subset of variables", but it has the same 67 nodes as
`N0423_1` with n = 829 instead of 840, so it's almost a duplicate of another network.
Dropping it matches the authors' own copy of the results.

#! NOTE[research] : Not sure which 293 networks the paper used, OSF has no script for N0986_1

## 2026-10-11: a node's name is its matrix label

There were three options: the matrix label, the name in the publication, or the column
name from the cleaning script. I wanted the cleaning script's name, and it turns out that
is the matrix label. Each script ends with `colnames(data) = c(...)`, and those names are
the matrix labels, in the same order (checked on `N0029_1`). The raw columns before that
rename are item codes like `RRS_6`, which say even less.

The `variable_names` field in the metadata sheet is not used for node names. It's often
in a different order from the matrix, so it can't be paired with the labels by position.

#! NOTE[research] : None of these names line up across studies. The sleep item alone is `Sleep`, `SLEEP`,
`sleep_problems` or `I have trouble sleeping at night` depending on the network, and some
networks only have item codes (`D-1` to `D-9` in `N0759_1`). So comparing depression
networks (BEP-6) will need a hand-made table that maps each label to a shared symptom name.
The details are in `data/cleaning_notes.md`, under "Do the variable names match the matrix
labels?".

#! NOTE[research] : Map depression labels to DSM-5 symptoms or to scale items?
