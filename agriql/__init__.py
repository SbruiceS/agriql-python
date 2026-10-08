"""AgriQL client. Queries run in the AgriQL engine through its C ABI or its port."""

from agriql.connection import connect
from agriql.result import Result

__all__ = ["connect", "Result"]
__version__ = "3.10.1"
