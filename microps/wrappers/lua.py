from .. import _core
from types import FunctionType

def unwrap(x):
    return x._val if hasattr(x, '_val') else x

class LuaValue:
    def __init__(self, v, engine):
        self.__dict__['_val'] = v
        self.__dict__['_engine'] = engine
        self.__dict__['metatable'] = None
    
    def __bool__(self):
        v = unwrap(self._val)
        if v is None or v is False: return False
        return True

    def __call__(self, *args, **kwargs):
        raw = unwrap(self._val)
        if callable(raw):
            res = raw(*args, **kwargs)
            return LuaValue(unwrap(res), self._engine)
        return self

    def __add__(self, o):
        if self.metatable and '__add' in self.metatable:
            return self.metatable['__add'](self, o)
        return LuaValue(_core.add(_core.to_float(self._val), _core.to_float(unwrap(o))), self._engine)
        
    def __getitem__(self, k): return LuaValue(_core.obj_get(self._val, unwrap(k)), self._engine)
    def __setitem__(self, k, v): _core.obj_set(self._val, unwrap(k), unwrap(v))
    def __repr__(self):
        if self._engine.debug: return f"Lua({repr(self._val)})"
        return str(self._val)
    def __str__(self): return self.__repr__()

class LuaEngine:
    def __init__(self):
        self.__dict__['debug'] = False
        self.__dict__['_scope'] = "lua"
        self.__dict__['_builtins'] = {
            'Table': lambda: LuaValue(_core.obj_new(), self), 
            'setmetatable': lambda t, m: setattr(t, 'metatable', m) or t,
            'Number': lambda x: LuaValue(_core.to_float(unwrap(x)), self)
        }

    def decorator(self, func):
        def wrapper(*args, **kwargs):
            class Lua_Scope_Lie(dict):
                def __getitem__(k_self, key):
                    if key.startswith('ghost_'): return LuaValue(_core.haunted_get(self._scope, key), self)
                    v = _core.get_var(self._scope, key)
                    if v is not None: return LuaValue(v, self)
                    if key in self._builtins: return self._builtins[key]
                    return func.__globals__[key]
                def __setitem__(k_self, key, value): _core.set_var(self._scope, key, unwrap(value))
                def __contains__(k_self, key): return True

            lie = Lua_Scope_Lie()
            new_func = FunctionType(func.__code__, lie, func.__name__, func.__defaults__, func.__closure__)
            res = new_func(*[LuaValue(unwrap(a), self) for a in args], **kwargs)
            return LuaValue(unwrap(res), self)
        return wrapper

    def __getattr__(self, n):
        if n in self._builtins: return self._builtins[n]
        if hasattr(self.__class__, n): return getattr(self, n)
        if n.startswith('ghost_'): return LuaValue(_core.haunted_get(self._scope, n), self)
        v = _core.get_var(self._scope, n)
        return LuaValue(v, self) if v is not None else LuaValue(None, self)

    def __setattr__(self, n, v):
        if n == 'debug': self.__dict__['debug'] = v
        else: _core.set_var(self._scope, n, unwrap(v))

lua = LuaEngine()
