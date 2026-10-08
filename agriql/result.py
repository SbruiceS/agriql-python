"""A query result is a grid from the engine. pandas, Polars, and Arrow are optional views."""


class Result:
    def __init__(self, text):
        self.text = text

    def to_records(self):
        lines = [line for line in self.text.splitlines() if line]
        if len(lines) < 2 or "\t" not in lines[0]:
            return [{"text": line} for line in lines]
        header = lines[0].split("\t")
        return [dict(zip(header, line.split("\t"))) for line in lines[1:]]

    def to_pandas(self):
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError("pandas is not installed. Use pip install 'agriql[pandas]'.") from exc
        return pd.DataFrame(self.to_records())

    def to_polars(self):
        try:
            import polars as pl
        except ImportError as exc:
            raise ImportError("polars is not installed. Use pip install 'agriql[polars]'.") from exc
        return pl.DataFrame(self.to_records())

    def to_arrow(self):
        try:
            import pyarrow as pa
        except ImportError as exc:
            raise ImportError(
                "pyarrow is not installed. The engine does not emit Arrow IPC yet. "
                "Use pip install 'agriql[arrow]' to build a table from the result grid."
            ) from exc
        return pa.Table.from_pylist(self.to_records())
