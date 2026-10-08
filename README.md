# agriql

Python client for the AgriQL engine. `import agriql` does not start a second database.

```python
import agriql

db = agriql.connect("farm.aqdb")
result = db.query("SELECT plant_id, soil_moisture FROM agriculture.soil")
result.to_records()
```

`to_pandas()`, `to_polars()`, and `to_arrow()` import those libraries only when called. Arrow IPC is not produced by the engine. `to_arrow()` builds a `pyarrow` table from the result grid.

## Install

`libagriql_ffi` must already be on the library path. Build it from [AgriQL](https://github.com/SbruiceS/AgriQL):

```bash
git clone https://github.com/SbruiceS/AgriQL.git
cd AgriQL
cargo build -p agriql-ffi --release
sudo cp target/release/libagriql_ffi.so /usr/local/lib
sudo ldconfig
```

Then:

```bash
pip install git+https://github.com/SbruiceS/agriql-python.git
pip install "agriql[pandas] @ git+https://github.com/SbruiceS/agriql-python.git"
```

If the library is not in a default directory, set `AGRIQL_FFI` to the full path of `libagriql_ffi.so`.

`agriql.connect("agriql://127.0.0.1:5471/farm")` uses the server port instead of the library. This package is not published on PyPI.
