# Zone Adjacency Pipeline Usage

This document covers setup and usage for:

- `zones/generate_adj_grid.py`
- `zones/visualise_adj_map.py`
- `zones/run_pipeline.py`

## What it does

- Builds a taxi-zone adjacency matrix using **rook contiguity** (shared edges only, no corner-only links).
- Adds extra adjacency links for bridge/tunnel-connected zones from a NYC road GraphML.
- Optionally keeps disconnected zones (islands) in CSV and map output.

## Required files

- Zone shapefile (default):
  - `zones/data/taxi_zones/taxi_zones.shp`
- Road graph GraphML:
  - Pass explicitly with `--graphml /path/to/newyork.graphml`, or
  - Put file at `zones/data/newyork.graphml`
  - If missing, script attempts Kaggle download via `kagglehub`.

## Quick start

Run full pipeline (matrix + map):

```bash
python zones/run_pipeline.py
```


## Include islands

To keep zero-adjacency zones in both outputs:

```bash
python zones/run_pipeline.py --include-islands 
```

Without `--include-islands`, disconnected zones are removed from the adjacency matrix and the map data subset.


## CLI parameters

### `run_pipeline.py`

```text
--zones           Path to zone shapefile
                  default: zones/data/taxi_zones/taxi_zones.shp
--adjacency-out   Output adjacency CSV path
                  default: zones/data/taxi_zones_adjacency_matrix.csv
--map-out         Output adjacency map PNG path
                  default: zones/data/taxi_zones_adjacency_map.png
--graphml         Optional GraphML path; if omitted, local/Kaggle resolution is used
--include-islands Keep zero-degree zones in CSV and map
```

### `generate_adj_grid.py`

```text
--zones           Path to zone shapefile
--adjacency-out   Output adjacency CSV path
--graphml         Optional GraphML path
--include-islands Keep zero-degree zones in adjacency CSV
```

### `visualise_adj_map.py`

```text
--zones           Path to zone shapefile
--adjacency       Input adjacency CSV path
--output          Output PNG path
--include-islands Ensure all zones are shown (reindexes missing zones to 0 links)
```

## Outputs

- Adjacency matrix CSV:
  - default: `zones/data/taxi_zones_adjacency_matrix.csv`
  - square matrix indexed by `LocationID` with `0/1` connectivity.
- Visualization PNG:
  - default: `zones/data/taxi_zones_adjacency_map.png`
  - zone polygons + red line segments for adjacency edges.

## Notes

- Contiguity is `Rook`: edge-sharing only.
- Bridge/tunnel links are added after geometric adjacency.
- Warnings about disconnected components/islands from `libpysal` are expected and not fatal.

## Troubleshooting

- `No such file or directory: ...taxi_zones.shp`
  - Pass the correct path with `--zones`.
- `Could not fetch GraphML from Kaggle...`
  - Provide `--graphml /path/to/newyork.graphml` or place file at `src/zones/data/newyork.graphml`.
- `ModuleNotFoundError` for geospatial libs
  - Run `make setup` (or `uv sync`) and use `uv run ...` or the repo `.venv`.
