import sys

from src.infra import network as _network

sys.modules[__name__] = _network
