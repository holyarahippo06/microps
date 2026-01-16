# FILE: microps/wrappers/wrapper.py
from .. import _core, unwrap
from types import FunctionType
import builtins

# Global metatable registry shared across all engines
_GLOBAL_METATABLES = {}

def get_mm(obj_raw, name, engine=None):
    """Finds Lua-style metamethods in raw C-dictionaries or global registry."""
    # First try: object is a dict with _mt key
    if isinstance(obj_raw, dict):
        mt = obj_raw.get('_mt')
        if mt and isinstance(mt, dict):
            return mt.get(name)
    
    # Second try: check global metatable registry (for lists, etc.)
    obj_id = id(obj_raw)
    mt = _GLOBAL_METATABLES.get(obj_id)
    if mt and isinstance(mt, dict):
        return mt.get(name)
    
    return None

class BaseValue:
    def __init__(self, v, engine):
        self.__dict__['_val'] = unwrap(v)
        self.__dict__['_engine'] = engine

    # --- Reassembling Arithmetic from C ---
    def __add__(self, o):
        left = self._val
        right = unwrap(o)
        # If either operand is a string, concatenate as strings (JS-like)
        if isinstance(left, str) or isinstance(right, str):
            return self.__class__(str(left) + str(right), self._engine)
        # Attempt to convert to float otherwise
        for idx, val in enumerate([left, right]):
            if isinstance(val, str):
                try:
                    if idx == 0:
                        left = float(left)
                    else:
                        right = float(right)
                except ValueError:
                    pass
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return self.__class__(_core.add(left, right), self._engine)
        raise TypeError(f"Cannot add {type(left).__name__} and {type(right).__name__}")

    def __sub__(self, o): return self.__class__(_core.sub(self._val, unwrap(o)), self._engine)
    def __mul__(self, o): return self.__class__(_core.mul(self._val, unwrap(o)), self._engine)
    def __truediv__(self, o): return self.__class__(_core.div(self._val, unwrap(o)), self._engine)
    def __mod__(self, o): return self.__class__(_core.mod(self._val, unwrap(o)), self._engine)
    def __pow__(self, o): return self.__class__(_core.pow(self._val, unwrap(o)), self._engine)
    
    # --- Reassembling Bitwise/Logic ---
    def __or__(self, o):
        if callable(o): return o(self) # Pipe
        return self.__class__(_core.bit_or(self._val, unwrap(o)), self._engine)
    def __and__(self, o): return self.__class__(_core.bit_and(self._val, unwrap(o)), self._engine)

    # --- Reassembling Container Ops ---
    def __getitem__(self, k): 
        return self.__class__(_core.obj_get(self._val, unwrap(k)), self._engine)
    def __setitem__(self, k, v): 
        _core.obj_set(self._val, unwrap(k), unwrap(v))
    def __len__(self): 
        return int(unwrap(_core.len(self._val)))

    def __call__(self, *args, **kwargs):
        if callable(self._val):
            u_args = [unwrap(a) for a in args]
            return self.__class__(self._val(*u_args, **kwargs), self._engine)
        return self

    def __repr__(self): return str(self._val)

def lie_lookup(engine, func, key):
    if key.startswith('_'): raise AttributeError(key)
    if key.startswith('ghost_'): return _core.haunted_get(engine._scope, key)
    
    v = _core.get_var(engine._scope, key)
    if v is not None: return v
    if key in engine._builtins: return engine._builtins[key]
    v = _core.get_var("global", key)
    if v is not None: return v

    if func and key in func.__globals__: return func.__globals__[key]
    if hasattr(builtins, key): return getattr(builtins, key)
    raise NameError(f"[{engine._scope}] Variable '{key}' not found.")

def create_decorator(engine, value_class):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Local import to break circularity
            from .. import SharedBridge
            class Scope(dict):
                def __getitem__(self, k):
                    if k == 'shared': return SharedBridge(engine, value_class)
                    val = lie_lookup(engine, func, k)
                    if hasattr(val, '_scope'): return val
                    return val if callable(val) else value_class(val, engine)
                def __setitem__(self, k, v): _core.set_var(engine._scope, k, unwrap(v))
                def __contains__(self, k): return True
            
            new_func = FunctionType(func.__code__, Scope(), func.__name__, 
                                    func.__defaults__, func.__closure__)
            w_args = [value_class(a, engine) for a in args]
            return value_class(new_func(*w_args, **kwargs), engine)
        return wrapper
    return decorator
