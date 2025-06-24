"""NPB data source implementations."""

# Source registry for plugin discovery
_sources = {}

def register_source(name: str):
    """Decorator to register a data source."""
    def decorator(cls):
        _sources[name] = cls
        return cls
    return decorator

def get_source(name: str):
    """Get a registered data source by name."""
    return _sources.get(name)

def list_sources():
    """List all registered data sources."""
    return list(_sources.keys())

# Import sources to register them
try:
    from . import npb_official
except Exception:
    pass

try:
    from . import baseball_ref
except Exception:
    pass

try:
    from . import fangraphs
except Exception:
    pass