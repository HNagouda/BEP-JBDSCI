# Cleaning notes

## Do we actually have all the data?

The [ReBayesed repo](https://github.com/KarolineHuth/ReBayesed) repo also has a metadata sheet, 
`inst/extdata/metadata.xlsx`, and that one lists 346 networks across 152 papers. 
This is 52 more than the 294 networks in the manual export. Where do the other 52 go? Looking at their model type:

- 30 are Ising networks (binary data)
- 13 are MGM networks (mixed graphical models)
- 9 are GGMs whose cleaning was still marked "in process"

The paper only fits GGMs, so none of these were ever analysed and therefore won't be using them.

## 294 or 293 Networks?

The paper says it reanalysed 293 networks, but the export has 294. The OSF copy of the results
has 293 networks. It's identical to the manual export except that `N0423_2` is missing from it.

So is `N0423_2` the extra one? 
- the OSF also has one cleaning script per network, and there is a script for `N0423_2`. 
- However, The network without a script is `N0986_1`.

- `N0423_2` looks odd as well. It's labelled "Subset of variables", but it has the
same 67 nodes as `N0423_1`, with n = 829 instead of 840. That looks more like a subset of
the sample, and its cleaning script doesn't explain it. 
  - will be dropping this network (also described in ADRs)

## Do the variable names match the matrix labels?

The EDA already found that they often don't. After building the tables
(`uv run python -m bep.tables`), I compared the correlation matrix labels with the
`variable_names` string, as-is:

- 26 networks match exactly
- 234 have the same number of names, but the names differ
- 34 have a different number of names

which name do we show for a node - the matrix 
label, the name from the publication, or the raw column name from the cleaning script?
The depression networks need names that can be compared across studies.

Before picking, I looked at where the matrix labels come from. In
`N0029_1_datacleaning.R` the script ends with
`colnames(data) = c("COP4", "res1", "swl3", "res2", "PTG3", "COP1", "swl5", ...`, and
those are exactly the matrix labels, in the same order. So the matrix label already is the
name from the cleaning script. The raw column names before that rename are item codes
like `RRS_6`, which don't mention many values.

Then I looked closer at the 234 "different names". Of the 260 networks with the same count:

- 26 match exactly, in order
- 35 more have the same names, just in a different order
- 4 more match after ignoring case and whitespace

So most of the gap to the EDA's 233 is ordering. That also means `variable_names` is not in
matrix order, and `bep.tables` pairs it with the labels by position. In `N0025_1` that
puts `metadata_name = "unmotiv"` on the node labelled `feel`.

None of the three names lines up across studies (`swl1` in one paper, `"P1,
Delusions"` in another). The same symptom needs the same name in every network 
for a reliable comparison.

So comparing across studies would potentially need a hand-made mapping table that maps 
each label to a shared name. There are two options for that shared name:

- use DSM-5 symptoms, the nine depression criteria (depressed mood, loss of interest, sleep,
  fatigue, ...). Items from PHQ-9, BDI and CES-D can all be mapped onto them, so most
  networks become comparable, but two BDI items about sadness would both become
  "depressed mood".
- Scale items, keeping each questionnaire's own items. It's exact, but only networks that
  used the same questionnaire can be compared.

#! NOTE[research] : going to ask Don about this

## What's in the cleaning scripts?

The scripts are in `data/osf/03_Data_Extraction_Cleaning/03_02_NetworkCleaningScripts/`,
one per network, named like `N0025_1_datacleaning.R`. Opening a few, they all follow the
same template from the project's cleaning protocol, with six numbered steps:

1. Is the data fully anonymised?
2. Is the data a data frame in wide format?
3. Does each column represent a node in the original network?
4. Does anything need recoding or sum scoring?
5. Are all rows complete, or is missing data handled as the authors described?
6. Save with the correct name.

There's also the project's metadata sheet,
`data/osf/03_Data_Extraction_Cleaning/03_03_MetaData/Meta-Data_OSF.csv`, which has a
"Type of recoding" and a "Missing data ?" column per network, and a link to the raw data
where it's public. (NOTE: uses encoding latin-1)
