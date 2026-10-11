import numpy as np
import pytest
import rdata

from bep.paths import EXPORT_FILE
from bep.tables import build_tables

# These run against the real export, which is not in the repository.
pytestmark = pytest.mark.skipif(not EXPORT_FILE.exists(), reason="export not downloaded")

# A small network, used to compare single values against the .rds.
EXAMPLE_NETWORK = "N0025_1"


@pytest.fixture(scope="module")
def export():
    """The parsed .rds, read once for the module."""
    return rdata.read_rds(str(EXPORT_FILE))


@pytest.fixture(scope="module")
def tables(export):
    """The three tables built from the export."""
    return build_tables(export)


def test_every_network_gets_one_row(export, tables):
    assert len(tables["networks"]) == len(export)
    assert tables["networks"]["network_id"].is_unique


def test_edges_cover_every_node_pair(tables):
    networks = tables["networks"].set_index("network_id")
    edge_counts = tables["edges"].groupby("network_id").size()
    expected = networks["nodes"] * (networks["nodes"] - 1) // 2

    assert (edge_counts == expected.loc[edge_counts.index]).all()
    assert (expected == networks["possible_edges"]).all()


def test_edge_values_match_the_matrices(export, tables):
    entry = export[EXAMPLE_NETWORK]
    edges = tables["edges"].query("network_id == @EXAMPLE_NETWORK")
    labels = list(entry["meta"]["correlation_matrix"].coords["dim_0"].values)

    first = edges.iloc[0]
    a, b = labels.index(first["node_a"]), labels.index(first["node_b"])
    correlation = np.asarray(entry["meta"]["correlation_matrix"])[a, b]
    bayes_factor = np.asarray(entry["BGGM_BF"])[a, b]

    assert first["correlation"] == pytest.approx(correlation)
    assert first["bggm_bf"] == pytest.approx(bayes_factor)


def test_category_agrees_with_bayes_factor(tables):
    # Jeffreys' cut-off: BF above 10 is "included".
    edges = tables["edges"]

    assert ((edges["bggm_bf"] > 10) == (edges["bggm_category"] == "included")).all()
