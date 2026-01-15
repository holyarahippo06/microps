# FILE: microps/wrappers/js.py
from .. import _core
from .wrapper import unwrap, get_mm, create_decorator, BaseValue

class JSValue(BaseValue):
    """
    The JavaScript Pretender.
    Maps JS-nouns to C micro-operations.
    """

    @property
    def length(self):
        """JS uses .length as a property, not a method."""
        return JSValue(_core.len(self._val), self._engine)

    def __getattr__(self, n):
        if n.startswith('_'): raise AttributeError(n)
        
        # --- String Methods ---
        if n == 'toUpperCase': return lambda: JSValue(_core.str_upper(self._val), self._engine)
        if n == 'toLowerCase': return lambda: JSValue(_core.str_lower(self._val), self._engine)
        if n == 'split': return lambda sep="": JSValue(_core.str_split(self._val, unwrap(sep)), self._engine)
        if n == 'replace': return lambda old, new: JSValue(_core.str_replace(self._val, unwrap(old), unwrap(new)), self._engine)
        if n == 'charAt': return lambda i: JSValue(_core.obj_get(self._val, unwrap(i)), self._engine)
        if n == 'charCodeAt': return lambda i: JSValue(ord(_core.to_str(_core.obj_get(self._val, unwrap(i)))), self._engine)
        if n == 'concat': return lambda *args: JSValue(_core.str_join("", [self._val] + [unwrap(a) for a in args]), self._engine)
        if n == 'startsWith': return lambda prefix: JSValue(_core.eq(_core.slice(self._val, 0, _core.len(unwrap(prefix))), unwrap(prefix)), self._engine)
        if n == 'endsWith': return lambda suffix: JSValue(_core.eq(_core.slice(self._val, _core.sub(_core.len(self._val), _core.len(unwrap(suffix))), _core.len(self._val)), unwrap(suffix)), self._engine)
        if n == 'trim': return lambda: JSValue(_core.str_replace(_core.str_replace(self._val, " ", ""), "\t", ""), self._engine)
        if n == 'repeat': return lambda times: JSValue(_core.str_join("", [self._val] * unwrap(times)), self._engine)
        if n == 'padStart': return lambda length, fill=" ": JSValue(_core.str_join("", [unwrap(fill)] * (unwrap(length) - _core.len(self._val)) + [self._val]) if _core.len(self._val) < unwrap(length) else self._val, self._engine)
        if n == 'padEnd': return lambda length, fill=" ": JSValue(_core.str_join("", [self._val] + [unwrap(fill)] * (unwrap(length) - _core.len(self._val))) if _core.len(self._val) < unwrap(length) else self._val, self._engine)
        
        # --- Array Methods ---
        if n == 'push': return lambda v: (_core.append(self._val, unwrap(v)), JSValue(_core.len(self._val), self._engine))[1]  # Returns new length
        if n == 'pop': return lambda: JSValue(_core.pop(self._val, JSValue(-1, self._engine)), self._engine)
        if n == 'shift': return lambda: JSValue(_core.pop(self._val, JSValue(0, self._engine)), self._engine)
        if n == 'unshift': return lambda v: (_core.obj_set(self._val, 0, unwrap(v)), JSValue(_core.len(self._val), self._engine))[1]
        if n == 'reverse': return lambda: (_core.reverse(self._val), self)[1]  # Mutates
        if n == 'slice': return lambda start=0, end=None: JSValue(_core.slice(self._val, unwrap(start), unwrap(end) if end is not None else _core.len(self._val)), self._engine)
        if n == 'concat': return lambda *args: JSValue(_core.concat(self._val, _core.concat(*[unwrap(a) for a in args])) if args else self._val, self._engine)
        if n == 'includes': return lambda v: JSValue(_core.contains(self._val, unwrap(v)), self._engine)
        if n == 'indexOf': 
            def find_index(v):
                for i in range(int(unwrap(_core.len(self._val)))):
                    if unwrap(_core.eq(_core.obj_get(self._val, i), unwrap(v))):
                        return JSValue(i, self._engine)
                return JSValue(-1, self._engine)
            return find_index
        if n == 'join': return lambda sep=",": JSValue(_core.str_join(unwrap(sep), self._val), self._engine)
        if n == 'fill': return lambda value, start=0, end=None: self._fill_array(unwrap(value), unwrap(start), unwrap(end))
        if n == 'every': return lambda fn: JSValue(all(unwrap(fn(JSValue(item, self._engine))) for item in self._val), self._engine)
        if n == 'some': return lambda fn: JSValue(any(unwrap(fn(JSValue(item, self._engine))) for item in self._val), self._engine)
        
        # --- Object Methods (JS Object.* exposed as methods) ---
        if n == 'toString': return lambda: JSValue(_core.to_str(self._val), self._engine)
        if n == 'valueOf': return lambda: self  # Returns itself
        
        # --- Number Methods ---
        if n == 'toFixed': return lambda decimals=0: JSValue(f"{unwrap(_core.to_float(self._val)):.{unwrap(decimals)}f}", self._engine)
        if n == 'toPrecision': return lambda precision: JSValue(f"{unwrap(_core.to_float(self._val)):.{unwrap(precision)-1}e}", self._engine)
        if n == 'toExponential': return lambda decimals=2: JSValue(f"{unwrap(_core.to_float(self._val)):.{unwrap(decimals)}e}", self._engine)
        
        # --- Boolean/Type Checks ---
        if n == 'isNaN': return lambda: JSValue(_core.ne(self._val, self._val), self._engine)  # NaN != NaN in JS
        if n == 'isFinite': return lambda: JSValue(not (self._val == float('inf') or self._val == float('-inf')), self._engine)

        return JSValue(_core.obj_get(self._val, n), self._engine)
    
    def _fill_array(self, value, start, end):
        """Helper for Array.fill()"""
        end = end if end is not None else int(unwrap(_core.len(self._val)))
        for i in range(start, end):
            _core.obj_set(self._val, i, value)
        return self

class JSEngine:
    def __init__(self):
        self.__dict__['_scope'] = "js"
        self.__dict__['_builtins'] = {
            'Object': {
                'keys': lambda o: JSValue(_core.keys(unwrap(o)), self),
                'values': lambda o: JSValue(_core.values(unwrap(o)), self),
                'create': lambda: JSValue(_core.obj_new(), self),
            },
            'Array': lambda *items: JSValue(list(unwrap(i) for i in items) if items else _core.list_new(), self),
            'String': lambda x: JSValue(_core.to_str(unwrap(x)), self),
            'Number': lambda x: JSValue(_core.to_float(unwrap(x)), self),
            'Boolean': lambda x: JSValue(_core.to_bool(unwrap(x)), self),
            'parseInt': lambda x: JSValue(_core.to_int(unwrap(x)), self),
            'parseFloat': lambda x: JSValue(_core.to_float(unwrap(x)), self),
            'isNaN': lambda x: JSValue(_core.ne(unwrap(x), unwrap(x)), self),
            'isFinite': lambda x: JSValue(not (unwrap(x) == float('inf') or unwrap(x) == float('-inf')), self),
            'Math': {
                'abs': lambda x: JSValue(_core.abs(unwrap(x)), self),
                'floor': lambda x: JSValue(_core.to_int(unwrap(x)), self),
                'ceil': lambda x: JSValue(_core.to_int(_core.add(unwrap(x), 0.999999)), self),
                'round': lambda x: JSValue(_core.to_int(_core.add(unwrap(x), 0.5)), self),
                'pow': lambda x, y: JSValue(_core.pow(unwrap(x), unwrap(y)), self),
                'max': lambda *args: JSValue(max(unwrap(a) for a in args), self),
                'min': lambda *args: JSValue(min(unwrap(a) for a in args), self),
            },
            'console': {
                'log': lambda *args: print(*(str(unwrap(a)) for a in args)),
                'error': lambda *args: print("ERROR:", *(str(unwrap(a)) for a in args)),
                'warn': lambda *args: print("WARN:", *(str(unwrap(a)) for a in args)),
            },
            'undefined': None,
            'null': None,
            'true': True,
            'false': False,
            'NaN': float('nan'),
            'Infinity': float('inf'),
        }
        self.__dict__['decorator'] = create_decorator(self, JSValue)

    def __getattr__(self, n):
        from .wrapper import lie_lookup
        return JSValue(lie_lookup(self, None, n), self)

js = JSEngine()
