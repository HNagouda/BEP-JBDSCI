import numpy as np
import pandas as pd
import rdata

from bep.paths import EXPORT_FILE, TABLES_DIR

TABLE_NAMES = ["networks", "variables", "edges"]


# * ====================================================================
# * === utils
# * ====================================================================


def _to_scalar(value):
    if value is None:
        return None
    else:
        return np.asarray(value).flat[0]


def _text(value):
    value = _to_scalar(value)

    return None if value is None else str(value)


def _year_to_float(value):
    """'2021.0' -> 2021."""
    
    value = _text(value)

    return None if value is None else int(float(value))


def _labels(entry):

    matrix = entry["meta"]["correlation_matrix"]

    return [str(label) for label in matrix.coords["dim_0"].values]


def _upper(matrix, rows, columns):
    """Upper-triangle values of a matrix, or NaN when the fit is missing."""
    
    if matrix is None:
        return np.full(len(rows), np.nan)
    else:
        return np.asarray(matrix, dtype=float)[rows, columns]


def _upper_category(flat, size, rows, columns):
    # The category matrices arrive flattened in R's column-major order.
    return np.asarray(flat).reshape(size, size, order="F")[rows, columns]


# * ====================================================================
# * === tables
# * ====================================================================


def network_row(network_id, entry):
    meta = entry["meta"]

    return {
        "network_id": network_id,
        "paper_id": _text(meta["paperID"]),
        "citation": _text(meta["citation"]),
        "authors": _text(meta["authors"]),
        "year": _year_to_float(meta["year"]),
        "doi": _text(meta["doi"]),
        "data_link": _text(meta["data_link"]),
        "model": _text(meta["model"]),
        "network_subtype": _text(meta["network_subtype"]),
        "topic": _text(meta["topic"]),
        "subtopic": _text(meta["subtopic"]),
        "questionnaires": _text(meta["questionnaires"]),
        "variable_names": _text(meta["variable_names"]),
        "type_of_variables": _text(meta["type_of_variables"]),
        "sample_type": _text(meta["sample_type"]),
        "sample_size": int(_to_scalar(meta["sample_size"])),
        "nodes": int(_to_scalar(entry["p"])),
        "possible_edges": int(_to_scalar(entry["n_edges"])),
        # Six networks have no ggmModSelect fit.
        "modselect_included": _to_scalar(entry.get("modSelect_n_inc")),
        "ebic_included": _to_scalar(entry["EBIC_n_inc"]),
    }


def variable_rows(network_id, entry):
    labels = _labels(entry)
    means = np.asarray(entry["meta"]["variable_means"], dtype=float)
    standard_deviations = np.asarray(entry["meta"]["variable_standard_deviations"], dtype=float)

    return [
        {
            "network_id": network_id,
            "position": position,
            "label": label,
            "mean": means[position],
            "standard_deviation": standard_deviations[position],
        }
        for position, label in enumerate(labels)
    ]


def edge_rows(network_id, entry):
    meta = entry["meta"]
    labels = _labels(entry)
    size = len(labels)
    rows, columns = np.triu_indices(size, k=1)

    return pd.DataFrame(
        {
            "network_id": network_id,
            "node_a": np.asarray(labels)[rows],
            "node_b": np.asarray(labels)[columns],
            "correlation": _upper(meta["correlation_matrix"], rows, columns),
            "partial_correlation": _upper(meta["partialcorrelation_matrix"], rows, columns),
            "covariance": _upper(meta["covariance_matrix"], rows, columns),
            "modselect_estimate": _upper(entry.get("modSelect_parameters"), rows, columns),
            "ebic_estimate": _upper(entry["EBIC_parameters"], rows, columns),
            "bggm_estimate": _upper(entry["BGGM_parameters"], rows, columns),
            "bggm_inclusion_probability": _upper(entry["BGGM_inc_probs"], rows, columns),
            "bggm_bf": _upper(entry["BGGM_BF"], rows, columns),
            "bggm_category": _upper_category(entry["BGGM_category"], size, rows, columns),
            "bggm2_estimate": _upper(entry["BGGM2_parameters"], rows, columns),
            "bggm2_inclusion_probability": _upper(entry["BGGM2_inc_probs"], rows, columns),
            "bggm2_bf": _upper(entry["BGGM2_BF"], rows, columns),
            "bggm2_category": _upper_category(entry["BGGM2_category"], size, rows, columns),
            "bggm3_estimate": _upper(entry["BGGM3_parameters"], rows, columns),
            "bggm3_inclusion_probability": _upper(entry["BGGM3_inc_probs"], rows, columns),
            "bggm3_bf": _upper(entry["BGGM3_BF"], rows, columns),
            "bggm3_category": _upper_category(entry["BGGM3_category"], size, rows, columns),
        }
    )


def build_tables(export):
    """The parsed .rds -> {'networks': ..., 'variables': ..., 'edges': ...}."""
    networks = []
    variables = []
    edges = []

    for network_id, entry in export.items():
        networks.append(network_row(str(network_id), entry))
        variables.extend(variable_rows(str(network_id), entry))
        edges.append(edge_rows(str(network_id), entry))

    return {
        "networks": pd.DataFrame(networks),
        "variables": pd.DataFrame(variables),
        "edges": pd.concat(edges, ignore_index=True),
    }


def read_table(name):
    if name not in TABLE_NAMES:
        raise ValueError(f"table must be one of {TABLE_NAMES}, got {name!r}")
    else:
        return pd.read_parquet(TABLES_DIR / f"{name}.parquet")


if __name__ == "__main__":
    tables = build_tables(rdata.read_rds(str(EXPORT_FILE)))
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    for name, table in tables.items():
        table.to_parquet(TABLES_DIR / f"{name}.parquet", index=False)
        print(f"{name}: {len(table)} rows")
