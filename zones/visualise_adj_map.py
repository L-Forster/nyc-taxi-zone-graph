import argparse
from pathlib import Path

import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zones", default="zones/data/taxi_zones/taxi_zones.shp")
    parser.add_argument("--adjacency", default="zones/data/taxi_zones_adjacency_matrix.csv")
    parser.add_argument("--output", default="zones/data/taxi_zones_adjacency_map.png")
    parser.add_argument("--include-islands", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    zones = gpd.read_file(args.zones).sort_values("LocationID")
    adjacency = pd.read_csv(args.adjacency, index_col=0)
    adjacency.index = adjacency.index.astype(int)
    adjacency.columns = adjacency.columns.astype(int)

    if args.include_islands:
        all_zone_ids = sorted(zones["LocationID"].astype(int).tolist())
        adjacency = adjacency.reindex(index=all_zone_ids, columns=all_zone_ids, fill_value=0).astype(int)
        zones = zones.set_index("LocationID").loc[all_zone_ids].reset_index()
    else:
        zones = zones[zones["LocationID"].isin(adjacency.index)].copy()
        zones = zones.set_index("LocationID").loc[sorted(adjacency.index)].reset_index()

    anchors = zones.set_index("LocationID").geometry.representative_point()
    segments = []

    for source_zone in adjacency.index:
        for target_zone in adjacency.columns:
            if target_zone <= source_zone or adjacency.loc[source_zone, target_zone] != 1:
                continue
            source_point = anchors.loc[source_zone]
            target_point = anchors.loc[target_zone]
            segments.append([(source_point.x, source_point.y), (target_point.x, target_point.y)])

    fig, ax = plt.subplots(figsize=(14, 14))
    zones.plot(ax=ax, facecolor="#f2efe8", edgecolor="#555555", linewidth=0.35)
    ax.add_collection(LineCollection(segments, colors="#c0392b", linewidths=0.35, alpha=0.18))

    ax.set_axis_off()
    ax.set_title("NYC Taxi Zone Adjacency", fontsize=16)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
