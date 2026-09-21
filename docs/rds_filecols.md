# Network-specific .rds files
> Taken directly from the [ReBayesed Project](https://uvasobe.shinyapps.io/ReBayesed/)

For each network or each collection of networks, users can download the aggregated data. In case of one network, users will download one .rds file with the following information, and for a set of networks users will obtain an .rds file which contains a list with all respective network specific elements. For each network, users will have the following data: the name of list element is highlighted in blue, the R-object type is indicated in parentheses, and the respective meaning of the element is added after the colon.

- **p (integer)** = Number of nodes in the network
- **n_edges (integer)** = number of possible edges in the network
- **meta (list)** = list that contains several meta-data information about the network
    - **networkID (character)** = project-assigned ID for the particular network. Can be used to link to other project data files.
    - **paperID (character)** = project-assigned ID for the particular paper. Can be used to link to other project data files.
    - **citation (character)** = Citation for the paper that the network was published in
    - **data_link (character)** = if available, link to the public repository holding the raw data
    - **model (character)** = type of model that was fit to the data, either GGM for continuous data or Ising for binary data
    - **network_subtype (character)** = if there are several networks in one paper, it encodes how the respective network is different from the original network (first network shown in the publication); e.g., could be a `different population` to indicate a network that differs from the `original` network by being fit to a different sample or `different variables` to indicate a network that differs based on the nodes that are included in the network
    - **topic (character)** = overarching research topic of the publication. Can be one of the following: Clinical, Social, Personality, Work- and Organizational, Diagnostics, Public Health, Education, Other
    - **subtopic (character)** = More specific research topic of the article which was assigned after screening the articles. It usually is the phenomenon mentioned in the title or research question of the article. At least one subtopic but can also be more than one subtopic separated with a semi-colon. e.g., Depression, Narcissism, Rumination
    - **questionnaires (character)** = the name(s) or abbreviation(s) of the questionnaire, if an established questionnaire was used. If several established questionnaires were used, they were separated with a semi-colon
    - **variable_names (character)** = Names or abbreviations of the nodes as provided in the original publication separated with a semi-colon
    - **type_of_variables (character)** = The nature of the variables that were included in the network. Can be one of the following: continuous, binary, mixed. If the type of variables were “mixed”, they needed to have no categorical variables
    - **sample_type (character)** = The type of sample on which the network was fitted, which can be one of the following: population, clinical, and mixed. Population indicates general population samples, clinical indicates a sample with a diagnosed disorder, and mixed indicates a mix of general population and clinical samples
    - **sample_size (integer)** = the number of individuals included in the sample to which the network was fit
    - **number_nodes (integer)** = number of nodes in the network
    - **variable_means (vector)** = mean of the variables
    - **variable_standard_deviations (vector)** = standard deviation of the variables
    - **covariance_matrix (matrix)** = covariance matrix of the dataset, obtained with the R function cov(na.omit(data))
    - **correlation_matrix (matrix)** = correlation matrix of the dataset, obtained with the R function cor(na.omit(data))
    - **partialcorrelation_matrix (matrix)** = partial correlation matrix of the dataset, obtained with the R function ppcor::pcor(na.omit(data))
- **modSelect_parameters (matrix)** = parameter estimates of the network edges obtained with the frequentist modeling “ggmModSelect”. Fit obtained with bo**otnet::estimateNetwork(data, default** = “ggmModSelect”). Bootnet version: 1.5.3
- **modSelect_n_inc (integer)** = number of edges determined to be included when fitting the network with “ggmModSelect”
- **modSelect_n_exc (integer)** = number of edges determined to be excluded when fitting the network with “ggmModSelect”
- **EBIC_parameters (matrix)** = parameter estimates of the network edges obtained with the frequentist modeling “EBICglasso”. Fit obtained with bo**otnet::estimateNetwork(data, default** = “EBICglasso”). Bootnet version: 1.5.3
- **EBIC_n_inc (integer)** = number of edges determined to be included when fitting the network with “EBICglasso”
- **EBIC_n_exc (integer)** = number of edges determined to be excluded when fitting the network with “EBICglasso”
- **BGGM_parameters (matrix)** = parameter estimates of the network edges obtained with the Bayesian modeling as implemented in “BGGM”. Fit obtained wi**th easybgm::easybgm(data = data, type = "continuous", save = F, package = "BGGM", prior_sd = sqrt(1/8) , iter** = 10000). easybgm version: 0.1.2
- **BGGM_inc_probs (matrix)** = edge-specific posterior inclusion probability obtained with “BGGM”.
- **BGGM_BF (matrix)** = edge-specific inclusion Bayes factor obtained with “BGGM”.
- **BGGM_category (matrix)** = edge-specific categorization of the Bayes factor obtained with “BGGM” following the criteria by Jeffreys (1961): excluded, weak excluded, inconclusive, weak included, and included.
- **BGGM_color (matrix)** = self-assigned coloring to the edge-specific inclusion categorization used in the network edge evidence plots: dark yellow, light yellow, grey, light blue, dark blue.
- **BGGM2_parameters (matrix)** = parameter estimates of the network edges obtained with the Bayesian modeling as implemented in “BGGM”. Fit obtained wi**th easybgm::easybgm(data = data, type = "continuous", save = F, package = "BGGM", prior_sd = sqrt(1/24) , iter** = 10000). easybgm version: 0.1.2
- **BGGM2_inc_probs (matrix)** = edge-specific posterior inclusion probability obtained with “BGGM”.
- **BGGM2_BF (matrix)** = edge-specific inclusion Bayes factor obtained with “BGGM”.
- **BGGM2_category (matrix)** = edge-specific categorization of the Bayes factor obtained with “BGGM” following the criteria by Jeffreys (1961): excluded, weak excluded, inconclusive, weak included, and included.
- **BGGM2_color (matrix)** = self-assigned coloring to the edge-specific inclusion categorization used in the network edge evidence plots: dark yellow, light yellow, grey, light blue, dark blue.
- **BGGM3_parameters (matrix)** = parameter estimates of the network edges obtained with the Bayesian modeling as implemented in “BGGM”. Fit obtained wi**th easybgm::easybgm(data = data, type = "continuous", save = F, package = "BGGM", prior_sd = sqrt(1/16) , iter** = 10000). easybgm version: 0.1.2
- **BGGM3_inc_probs (matrix)** = edge-specific posterior inclusion probability obtained with “BGGM”.
- **BGGM3_BF (matrix)** = edge-specific inclusion Bayes factor obtained with “BGGM”.
- **BGGM3_category (matrix)** = edge-specific categorization of the Bayes factor obtained with “BGGM” following the criteria by Jeffreys (1961): excluded, weak excluded, inconclusive, weak included, and included.
- **BGGM3_color (matrix)** = self-assigned coloring to the edge-specific inclusion categorization used in the network edge evidence plots: dark yellow, light yellow, grey, light blue, dark blue.