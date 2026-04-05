# NYC Taxi Zone Graph
This project provides a bridge-aware adjacency graph for NYC TLC taxi zones. It exports a ready-to-use adjacency matrix and map for demand forecasting, graph ML, simulation, and spatial feature engineering. Unlike plain polygon-neighbor methods, it can add bridge and tunnel links using the NYC road network.

Builds an adjacency graph for NYC taxi zones using:
- polygon edge-sharing (rook contiguity), and
- extra bridge/tunnel links from a NYC road GraphML network.

The pipeline produces:
- `zones/data/taxi_zones_adjacency_matrix.csv`
- `zones/data/taxi_zones_adjacency_map.png`

## Repository Structure

- `zones/generate_adj_grid.py`: builds adjacency matrix CSV.
- `zones/visualise_adj_map.py`: draws adjacency map PNG from CSV.
- `zones/run_pipeline.py`: runs both steps.
- `zones/data/taxi_zones/`: input taxi zone shapefile.
- `utils/utils.py`: CRS helper utilities.

## Requirements

- Python 3.10+
- GEOS/GDAL/PROJ-compatible environment for GeoPandas stack

Install Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Start

Run full pipeline:

```bash
python zones/run_pipeline.py
```

Include disconnected islands in outputs:

```bash
python zones/run_pipeline.py --include-islands
```

## CLI Options

`zones/run_pipeline.py`

- `--zones` (default: `zones/data/taxi_zones/taxi_zones.shp`)
- `--adjacency-out` (default: `zones/data/taxi_zones_adjacency_matrix.csv`)
- `--map-out` (default: `zones/data/taxi_zones_adjacency_map.png`)
- `--graphml` optional GraphML path
- `--include-islands` keep zero-degree zones

`zones/generate_adj_grid.py`

- `--zones`
- `--adjacency-out`
- `--graphml`
- `--include-islands`

`zones/visualise_adj_map.py`

- `--zones`
- `--adjacency`
- `--output`
- `--include-islands`

## GraphML Source

For bridge/tunnel enrichment, the script resolves GraphML in this order:
1. path passed via `--graphml`
2. local file at `zones/data/newyork.graphml`
3. Kaggle download via `kagglehub` (`crailtap/street-network-of-new-york-in-graphml`)

If Kaggle download is unavailable, pass `--graphml` explicitly.

<img width="800"  alt="taxi_zones_adjacency_map" src="https://github.com/user-attachments/assets/6dc9a640-ae69-4524-86e5-70c5880dc0ed" />



## Notes

- Contiguity uses rook adjacency (shared boundary edge only).
- Island/disconnected-zone warnings from `libpysal` are expected.
- Output directory is created automatically if missing.

## License

MIT License (see [LICENSE](LICENSE)).
