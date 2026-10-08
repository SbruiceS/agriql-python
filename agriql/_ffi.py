"""ctypes bindings for libagriql_ffi. The library owns the engine."""

import ctypes
import os
from pathlib import Path


def load():
    requested = os.environ.get("AGRIQL_FFI")
    names = [
        requested,
        "libagriql_ffi.so",
        "libagriql_ffi.dylib",
        "agriql_ffi.dll",
    ]
    roots = [
        Path.cwd(),
        Path(__file__).resolve().parents[3] / "target" / "debug",
        Path(__file__).resolve().parents[3] / "target" / "release",
    ]
    candidates = []
    for name in names:
        if not name:
            continue
        path = Path(name)
        if path.is_file():
            candidates.append(path)
        for root in roots:
            found = root / name
            if found.is_file():
                candidates.append(found)
    if not candidates:
        raise FileNotFoundError(
            "libagriql_ffi was not found. Build it with `cargo build -p agriql-ffi` "
            "or set AGRIQL_FFI to the library path."
        )
    chosen = max(candidates, key=lambda path: path.stat().st_mtime)
    lib = ctypes.CDLL(str(chosen))
    lib.agriql_open.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]
    lib.agriql_open.restype = ctypes.c_int
    lib.agriql_close.argtypes = [ctypes.c_void_p]
    lib.agriql_close.restype = ctypes.c_int
    lib.agriql_execute.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    lib.agriql_execute.restype = ctypes.c_void_p
    lib.agriql_result_text.argtypes = [ctypes.c_void_p]
    lib.agriql_result_text.restype = ctypes.c_char_p
    lib.agriql_result_status.argtypes = [ctypes.c_void_p]
    lib.agriql_result_status.restype = ctypes.c_int
    lib.agriql_free_result.argtypes = [ctypes.c_void_p]
    lib.agriql_thread_error.argtypes = []
    lib.agriql_thread_error.restype = ctypes.c_char_p
    return lib
