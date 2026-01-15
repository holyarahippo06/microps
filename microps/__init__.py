# FILE: microps/__init__.py
from . import _core

def unwrap(x):
    """Deep unwrap to get raw Python/C objects."""
    while hasattr(x, '__dict__') and '_val' in x.__dict__:
        x = x.__dict__['_val']
    return x

class SharedBridge:
    """Bridge to the global polyglot scope."""
    def __init__(self, engine=None, value_class=None):
        self.__dict__['_engine'] = engine
        self.__dict__['_value_class'] = value_class

    def __getattr__(self, n):
        v = _core.get_var("global", n)
        if self._value_class and v is not None:
            return self._value_class(v, self._engine)
        return v
    
    def __setattr__(self, n, v):
        _core.set_var("global", n, unwrap(v))

shared = SharedBridge()

# Import wrapper utilities before language wrappers
from .wrappers.wrapper import BaseValue, get_mm, create_decorator, lie_lookup

# Late imports to prevent circular dependency issues
from .wrappers.ruby import ruby, RubyValue, RubyEngine
from .wrappers.js import js, JSValue, JSEngine
from .wrappers.lua import lua, LuaValue, LuaEngine
from .wrappers.php import php, PHPValue, PHPEngine
from .wrappers.py import py, PyValue, PyEngine
from .wrappers.c import c, CValue, CEngine

__all__ = [
    # Core
    '_core', 
    'unwrap', 
    'shared',
    
    # Language engines
    'js', 'lua', 'ruby', 'php', 'py', 'c',
    
    # Value classes (for advanced usage)
    'JSValue', 'LuaValue', 'RubyValue', 'PHPValue', 'PyValue', 'CValue',
    
    # Engine classes (for advanced usage)
    'JSEngine', 'LuaEngine', 'RubyEngine', 'PHPEngine', 'PyEngine', 'CEngine',
    
    # Wrapper utilities (for creating new language wrappers)
    'BaseValue', 'get_mm', 'create_decorator', 'lie_lookup'
]
