# FILE: microps/wrappers/lua.py
from .. import _core
from .wrapper import unwrap, get_mm, create_decorator, BaseValue, _GLOBAL_METATABLES

class LuaValue(BaseValue):
    """
    The Lua Pretender.
    Reassembles C micro-ops into Lua's table-based semantics with metatables.
    """
    
    def __bool__(self):
        """Lua truthiness: Only nil and false are falsy."""
        return not (self._val is None or self._val is False)

    def _call_mm(self, name, other=None):
        """Helper to call metamethod if it exists."""
        mm = get_mm(self._val, name, self._engine)
        if mm:
            res = mm(self, other) if other is not None else mm(self)
            return LuaValue(res, self._engine)
        return None

    def __add__(self, o):
        """Lua addition with __add metamethod support."""
        return self._call_mm('__add', o) or LuaValue(_core.add(self._val, unwrap(o)), self._engine)
    
    def __sub__(self, o):
        """Lua subtraction with __sub metamethod support."""
        return self._call_mm('__sub', o) or LuaValue(_core.sub(self._val, unwrap(o)), self._engine)
    
    def __mul__(self, o):
        """Lua multiplication with __mul metamethod support."""
        return self._call_mm('__mul', o) or LuaValue(_core.mul(self._val, unwrap(o)), self._engine)
    
    def __truediv__(self, o):
        """Lua division with __div metamethod support."""
        return self._call_mm('__div', o) or LuaValue(_core.div(self._val, unwrap(o)), self._engine)
    
    def __mod__(self, o):
        """Lua modulo with __mod metamethod support."""
        return self._call_mm('__mod', o) or LuaValue(_core.mod(self._val, unwrap(o)), self._engine)
    
    def __pow__(self, o):
        """Lua power with __pow metamethod support."""
        return self._call_mm('__pow', o) or LuaValue(_core.pow(self._val, unwrap(o)), self._engine)
    
    def __neg__(self):
        """Lua unary minus with __unm metamethod support."""
        return self._call_mm('__unm') or LuaValue(_core.neg(self._val), self._engine)
    
    def __eq__(self, o):
        """Lua equality with __eq metamethod support."""
        mm_result = self._call_mm('__eq', o)
        return bool(unwrap(mm_result)) if mm_result else bool(unwrap(_core.eq(self._val, unwrap(o))))
    
    def __lt__(self, o):
        """Lua less than with __lt metamethod support."""
        mm_result = self._call_mm('__lt', o)
        return bool(unwrap(mm_result)) if mm_result else bool(unwrap(_core.lt(self._val, unwrap(o))))
    
    def __le__(self, o):
        """Lua less or equal with __le metamethod support."""
        mm_result = self._call_mm('__le', o)
        return bool(unwrap(mm_result)) if mm_result else bool(unwrap(_core.le(self._val, unwrap(o))))
    
    def __concat__(self, o):
        """Lua concatenation with __concat metamethod support."""
        return self._call_mm('__concat', o) or LuaValue(_core.str_join("", [_core.to_str(self._val), _core.to_str(unwrap(o))]), self._engine)

    def __getitem__(self, k):
        """Lua table indexing with __index metamethod and 1-based indexing."""
        raw_k = unwrap(k)
        
        # Try direct access first
        val = _core.obj_get(self._val, raw_k)
        
        # Lua 1-based indexing pretension: If it's a numeric key and not found, try k-1
        if val is None and isinstance(raw_k, (int, float)):
            val = _core.obj_get(self._val, raw_k - 1)
        
        # Try __index metamethod if still not found
        if val is None:
            mm = self._call_mm('__index', k)
            if mm:
                return mm
        
        return LuaValue(val, self._engine)

    def __setitem__(self, k, v):
        """Lua table assignment with __newindex metamethod support."""
        mm = get_mm(self._val, '__newindex')
        if mm:
            mm(self, k, v)
        else:
            _core.obj_set(self._val, unwrap(k), unwrap(v))
    
    def __len__(self):
        """Lua length operator with __len metamethod support."""
        mm_result = self._call_mm('__len')
        return int(unwrap(mm_result)) if mm_result else int(unwrap(_core.len(self._val)))
    
    def __call__(self, *args, **kwargs):
        """Lua call with __call metamethod support."""
        mm = get_mm(self._val, '__call', self._engine)
        if mm:
            return LuaValue(mm(self, *args), self._engine)
        
        if callable(self._val):
            u_args = [unwrap(a) for a in args]
            return LuaValue(self._val(*u_args, **kwargs), self._engine)
        return self

class LuaEngine:
    def __init__(self):
        self.__dict__['_scope'] = "lua"
        self.__dict__['_builtins'] = {
            # --- Core Lua Functions ---
            'Table': lambda: LuaValue(_core.obj_new(), self),
            'Number': lambda x: LuaValue(_core.to_float(unwrap(x)), self),
            'String': lambda x: LuaValue(_core.to_str(unwrap(x)), self),
            
            # --- Metatable Functions ---
            'setmetatable': self._setmetatable,
            'getmetatable': self._getmetatable,
            
            # --- Type Functions ---
            'type': lambda x: LuaValue(_core.type(unwrap(x)), self),
            'tonumber': lambda x: LuaValue(_core.to_float(unwrap(x)), self),
            'tostring': lambda x: LuaValue(_core.to_str(unwrap(x)), self),
            
            # --- Table Library ---
            'table': {
                'insert': lambda t, pos_or_val, val=None: (
                    _core.append(unwrap(t), unwrap(pos_or_val)) if val is None 
                    else _core.obj_set(unwrap(t), unwrap(pos_or_val), unwrap(val))
                ),
                'remove': lambda t, pos=None: LuaValue(
                    _core.pop(unwrap(t), LuaValue(-1 if pos is None else unwrap(pos) - 1, self)), 
                    self
                ),
                'concat': lambda t, sep="", i=1, j=None: LuaValue(
                    _core.str_join(unwrap(sep), _core.slice(unwrap(t), unwrap(i) - 1, unwrap(j) if j else _core.len(unwrap(t)))),
                    self
                ),
                'sort': lambda t, comp=None: unwrap(t).sort(key=comp) if comp else unwrap(t).sort(),
                'unpack': lambda t, i=1, j=None: [LuaValue(v, self) for v in _core.slice(unwrap(t), unwrap(i) - 1, unwrap(j) if j else _core.len(unwrap(t)))],
                'pack': lambda *args: LuaValue(list(unwrap(a) for a in args), self),
                'maxn': lambda t: LuaValue(max((k for k in unwrap(t).keys() if isinstance(k, (int, float))), default=0), self),
            },
            
            # --- String Library ---
            'string': {
                'upper': lambda s: LuaValue(_core.str_upper(unwrap(s)), self),
                'lower': lambda s: LuaValue(_core.str_lower(unwrap(s)), self),
                'len': lambda s: LuaValue(_core.len(unwrap(s)), self),
                'sub': lambda s, i, j=None: LuaValue(_core.slice(unwrap(s), unwrap(i) - 1, unwrap(j) if j else _core.len(unwrap(s))), self),
                'rep': lambda s, n: LuaValue(_core.str_join("", [unwrap(s)] * unwrap(n)), self),
                'reverse': lambda s: LuaValue(_core.str_join("", _core.reverse(_core.str_split(unwrap(s), ""))), self),
                'byte': lambda s, i=1: LuaValue(ord(str(unwrap(s))[unwrap(i) - 1]), self),
                'char': lambda *args: LuaValue(_core.str_join("", [chr(unwrap(a)) for a in args]), self),
                'find': lambda s, pattern, init=1: LuaValue(str(unwrap(s)).find(str(unwrap(pattern)), unwrap(init) - 1) + 1, self),
                'gsub': lambda s, pattern, repl, n=None: LuaValue(_core.str_replace(unwrap(s), unwrap(pattern), unwrap(repl)), self),
                'gmatch': lambda s, pattern: iter(str(unwrap(s)).split(str(unwrap(pattern)))),
                'match': lambda s, pattern, init=1: LuaValue(str(unwrap(s))[unwrap(init) - 1:].split(str(unwrap(pattern)))[0] if unwrap(pattern) in str(unwrap(s)) else None, self),
                'format': lambda fmt, *args: LuaValue(str(unwrap(fmt)) % tuple(unwrap(a) for a in args), self),
            },
            
            # --- Math Library ---
            'math': {
                'abs': lambda x: LuaValue(_core.abs(unwrap(x)), self),
                'floor': lambda x: LuaValue(_core.to_int(unwrap(x)), self),
                'ceil': lambda x: LuaValue(_core.to_int(_core.add(unwrap(x), 0.999999)), self),
                'sqrt': lambda x: LuaValue(_core.pow(unwrap(x), 0.5), self),
                'pow': lambda x, y: LuaValue(_core.pow(unwrap(x), unwrap(y)), self),
                'max': lambda *args: LuaValue(max(unwrap(a) for a in args), self),
                'min': lambda *args: LuaValue(min(unwrap(a) for a in args), self),
                'mod': lambda x, y: LuaValue(_core.mod(unwrap(x), unwrap(y)), self),
                'fmod': lambda x, y: LuaValue(_core.mod(unwrap(x), unwrap(y)), self),
                'huge': float('inf'),
                'pi': 3.141592653589793,
            },
            
            # --- Basic Functions ---
            'assert': lambda cond, msg=None: None if unwrap(cond) else (_ for _ in ()).throw(AssertionError(unwrap(msg) if msg else "assertion failed")),
            'error': lambda msg: (_ for _ in ()).throw(RuntimeError(unwrap(msg))),
            'print': lambda *args: print(*(str(unwrap(a)) for a in args)),
            'ipairs': lambda t: enumerate(unwrap(t), start=1),
            'pairs': lambda t: iter(unwrap(t).items()),
            'next': lambda t, k=None: next(iter(unwrap(t).items())),
            'rawget': lambda t, k: LuaValue(_core.obj_get(unwrap(t), unwrap(k)), self),
            'rawset': lambda t, k, v: _core.obj_set(unwrap(t), unwrap(k), unwrap(v)),
            'rawlen': lambda t: LuaValue(_core.len(unwrap(t)), self),
            'select': lambda index, *args: args[unwrap(index) - 1:] if isinstance(unwrap(index), int) else LuaValue(len(args), self),
            
            # --- Lua Constants ---
            'nil': None,
            'true': True,
            'false': False,
            '_VERSION': "Microps Lua 5.4",
        }
        self.__dict__['decorator'] = create_decorator(self, LuaValue)
    
    def _setmetatable(self, t, m):
        """Set metatable - handles both dicts and lists using global registry."""
        obj = unwrap(t)
        mt = unwrap(m)
        
        if isinstance(obj, dict):
            # Dicts can store metatables directly
            _core.obj_set(obj, '_mt', mt)
        else:
            # Lists and other objects: store in global metatable registry
            obj_id = id(obj)
            _GLOBAL_METATABLES[obj_id] = mt
        
        return t
    
    def _getmetatable(self, t):
        """Get metatable - handles both dicts and lists using global registry."""
        obj = unwrap(t)
        
        if isinstance(obj, dict):
            return LuaValue(_core.obj_get(obj, '_mt'), self)
        else:
            obj_id = id(obj)
            return LuaValue(_GLOBAL_METATABLES.get(obj_id), self)

    def __getattr__(self, n):
        from .wrapper import lie_lookup
        return LuaValue(lie_lookup(self, None, n), self)
    
    def __setattr__(self, n, v):
        _core.set_var(self._scope, n, unwrap(v))

lua = LuaEngine()
