from .. import _core
from types import FunctionType

def unwrap(x):
    if hasattr(x, '_val'): return x._val
    return x

class JSValue:
    def __init__(self, v, engine):
        self.__dict__['_val'] = v
        self.__dict__['_engine'] = engine
    
    def __bool__(self):
        v = unwrap(self._val)
        if v == 0 or v == "" or v is None or v is False: return False
        return True

    def __call__(self, *args, **kwargs):
        raw = unwrap(self._val)
        if callable(raw):
            res = raw(*args, **kwargs)
            return JSValue(unwrap(res), self._engine)
        return self

    def __add__(self, o):
        o = unwrap(o); s = unwrap(self)
        if isinstance(s, str) or isinstance(o, str):
            return JSValue(_core.add(_core.to_str(s), _core.to_str(o)), self._engine)
        return JSValue(_core.add(_core.to_float(s), _core.to_float(o)), self._engine)

    def __getattr__(self, n):
        if n == 'length': return JSValue(_core.len(self._val), self._engine)
        return JSValue(_core.obj_get(self._val, n), self._engine)

    def __setattr__(self, n, v):
        if n == '_val': self.__dict__['_val'] = v
        else: _core.obj_set(self._val, n, unwrap(v))

    def __repr__(self):
        if self._engine.debug: return f"JS({repr(self._val)})"
        return str(self._val)
    def __str__(self): return self.__repr__()

class JSEngine:
    def __init__(self):
        self.__dict__['debug'] = False
        self.__dict__['_scope'] = "js"
        self.__dict__['_builtins'] = {
            'Object': lambda: JSValue(_core.obj_new(), self),
            'Number': lambda x: JSValue(_core.to_float(unwrap(x)), self),
            'String': lambda x: JSValue(_core.to_str(unwrap(x)), self)
        }

    def decorator(self, func):
        def wrapper(*args, **kwargs):
            class JS_Scope_Lie(dict):
                def __getitem__(k_self, key):
                    if key.startswith('ghost_'): return JSValue(_core.haunted_get(self._scope, key), self)
                    v = _core.get_var(self._scope, key)
                    if v is not None: return JSValue(v, self)
                    if key in self._builtins: return self._builtins[key]
                    return func.__globals__[key]
                def __setitem__(k_self, key, value): _core.set_var(self._scope, key, unwrap(value))
                def __contains__(k_self, key): return True

            lie = JS_Scope_Lie()
            # This line re-binds the function to our C-memory scope
            new_func = FunctionType(func.__code__, lie, func.__name__, func.__defaults__, func.__closure__)
            res = new_func(*[JSValue(unwrap(a), self) for a in args], **kwargs)
            return JSValue(unwrap(res), self)
        return wrapper

    def __getattr__(self, n):
        if n in self._builtins: return self._builtins[n]
        if hasattr(self.__class__, n): return getattr(self, n)
        if n.startswith('ghost_'): return JSValue(_core.haunted_get(self._scope, n), self)
        v = _core.get_var(self._scope, n)
        return JSValue(v, self) if v is not None else JSValue(None, self)

    def __setattr__(self, n, v):
        if n == 'debug': self.__dict__['debug'] = v
        else: _core.set_var(self._scope, n, unwrap(v))

js = JSEngine()
