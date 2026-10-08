"""Connections. A file path uses the C ABI. agriql:// uses the server port."""

import socket

from agriql._ffi import load
from agriql.result import Result

_lib = None


def connect(target=":memory:"):
    if str(target).startswith("agriql://"):
        return PortConnection(str(target))
    return EngineConnection(str(target))


class EngineConnection:
    def __init__(self, path):
        global _lib
        if _lib is None:
            _lib = load()
        self._lib = _lib
        self._db = ctypes_open(self._lib, path)

    def query(self, sql):
        result = self._lib.agriql_execute(self._db, sql.encode())
        if not result:
            raise RuntimeError(_error(self._lib))
        status = self._lib.agriql_result_status(result)
        raw = self._lib.agriql_result_text(result)
        text = raw.decode() if raw else ""
        self._lib.agriql_free_result(result)
        if status != 0:
            raise RuntimeError(text or _error(self._lib))
        return Result(text)

    def close(self):
        if self._db:
            self._lib.agriql_close(self._db)
            self._db = None

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


class PortConnection:
    def __init__(self, url):
        raw = url.replace("agriql://", "", 1)
        database = None
        if "/" in raw:
            raw, database = raw.split("/", 1)
        host, port = raw.rsplit(":", 1)
        self.host = host
        self.port = int(port)
        self.database = database

    def query(self, sql):
        sock = socket.create_connection((self.host, self.port), timeout=5)
        try:
            payload = ""
            if self.database:
                payload += f"USE DATABASE {self.database};\n"
            payload += sql.strip() + "\n.quit\n"
            sock.sendall(payload.encode())
            data = b""
            while True:
                chunk = sock.recv(65536)
                if not chunk:
                    break
                data += chunk
        finally:
            sock.close()
        if not data:
            raise ConnectionError(f"agriql://{self.host}:{self.port} closed without a reply")
        return Result(data.decode())

    def close(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None


def ctypes_open(lib, path):
    import ctypes

    out = ctypes.c_void_p()
    encoded = None if path in ("", ":memory:") else path.encode()
    status = lib.agriql_open(encoded, ctypes.byref(out))
    if status != 0 or not out.value:
        raise RuntimeError(_error(lib))
    return out.value


def _error(lib):
    raw = lib.agriql_thread_error()
    if not raw:
        return "AGRIQL-2701: the engine returned no message"
    return raw.decode()
