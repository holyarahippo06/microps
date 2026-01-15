# FILE: microps/wrappers/py.py
from .. import _core
from .wrapper import unwrap, get_mm, create_decorator, BaseValue

class PyValue(BaseValue):
    """
    The Python Pretender.
    Maps standard Python method names to C micro-operations.
    """

    def __bool__(self):
        """Python truthiness: Uses C to_bool/truthy logic."""
        return bool(unwrap(_core.truthy(self._val)))

    def __getattr__(self, n):
        """Maps standard Python attributes/methods to C micro-ops."""
        if n.startswith('_'): raise AttributeError(n)

        # --- String Methods ---
        if n == 'upper': return lambda: PyValue(_core.str_upper(self._val), self._engine)
        if n == 'lower': return lambda: PyValue(_core.str_lower(self._val), self._engine)
        if n == 'split': return lambda sep=None: PyValue(_core.str_split(self._val, unwrap(sep)), self._engine)
        if n == 'join': return lambda it: PyValue(_core.str_join(self._val, unwrap(it)), self._engine)
        if n == 'replace': return lambda o, r: PyValue(_core.str_replace(self._val, unwrap(o), unwrap(r)), self._engine)
        if n == 'strip': return lambda: PyValue(_core.str_replace(_core.str_replace(self._val, " ", ""), "\t", ""), self._engine)
        if n == 'lstrip': return lambda: PyValue(self._val.lstrip(), self._engine)
        if n == 'rstrip': return lambda: PyValue(self._val.rstrip(), self._engine)
        if n == 'startswith': return lambda prefix: PyValue(_core.eq(_core.slice(self._val, 0, _core.len(unwrap(prefix))), unwrap(prefix)), self._engine)
        if n == 'endswith': return lambda suffix: PyValue(_core.eq(_core.slice(self._val, _core.sub(_core.len(self._val), _core.len(unwrap(suffix))), _core.len(self._val)), unwrap(suffix)), self._engine)
        if n == 'capitalize': return lambda: PyValue(_core.str_upper(_core.slice(self._val, 0, 1)) + _core.str_lower(_core.slice(self._val, 1, _core.len(self._val))), self._engine)
        if n == 'title': return lambda: PyValue(" ".join(word[0].upper() + word[1:].lower() for word in str(self._val).split()), self._engine)
        if n == 'swapcase': return lambda: PyValue("".join(c.upper() if c.islower() else c.lower() for c in str(self._val)), self._engine)
        if n == 'count': return lambda sub: PyValue(str(self._val).count(str(unwrap(sub))), self._engine)
        if n == 'find': return lambda sub: PyValue(str(self._val).find(str(unwrap(sub))), self._engine)
        if n == 'rfind': return lambda sub: PyValue(str(self._val).rfind(str(unwrap(sub))), self._engine)
        if n == 'index': return lambda sub: PyValue(str(self._val).index(str(unwrap(sub))), self._engine)
        if n == 'isalpha': return lambda: PyValue(str(self._val).isalpha(), self._engine)
        if n == 'isdigit': return lambda: PyValue(str(self._val).isdigit(), self._engine)
        if n == 'isalnum': return lambda: PyValue(str(self._val).isalnum(), self._engine)
        if n == 'isspace': return lambda: PyValue(str(self._val).isspace(), self._engine)
        if n == 'isupper': return lambda: PyValue(str(self._val).isupper(), self._engine)
        if n == 'islower': return lambda: PyValue(str(self._val).islower(), self._engine)
        if n == 'center': return lambda width, fill=" ": PyValue(str(self._val).center(unwrap(width), unwrap(fill)), self._engine)
        if n == 'ljust': return lambda width, fill=" ": PyValue(str(self._val).ljust(unwrap(width), unwrap(fill)), self._engine)
        if n == 'rjust': return lambda width, fill=" ": PyValue(str(self._val).rjust(unwrap(width), unwrap(fill)), self._engine)
        if n == 'zfill': return lambda width: PyValue(str(self._val).zfill(unwrap(width)), self._engine)
        
        # --- List Methods ---
        if n == 'append': return lambda v: _core.append(self._val, unwrap(v))
        if n == 'pop': return lambda i=-1: PyValue(_core.pop(self._val, PyValue(i, self._engine)), self._engine)
        if n == 'reverse': return lambda: _core.reverse(self._val)
        if n == 'extend': return lambda it: [_core.append(self._val, unwrap(i)) for i in unwrap(it)]
        if n == 'insert': return lambda i, v: _core.obj_set(self._val, unwrap(i), unwrap(v))
        if n == 'remove': return lambda v: self._val.remove(unwrap(v))
        if n == 'clear': return lambda: self._val.clear()
        if n == 'index': return lambda v: PyValue(self._val.index(unwrap(v)), self._engine)
        if n == 'count': return lambda v: PyValue(self._val.count(unwrap(v)), self._engine)
        if n == 'sort': return lambda key=None, reverse=False: self._val.sort(key=key, reverse=unwrap(reverse))
        if n == 'copy': return lambda: PyValue(self._val.copy(), self._engine)
        
        # --- Dict Methods ---
        if n == 'keys': return lambda: PyValue(_core.keys(self._val), self._engine)
        if n == 'values': return lambda: PyValue(_core.values(self._val), self._engine)
        if n == 'items': return lambda: PyValue(list(self._val.items()), self._engine)
        if n == 'get': return lambda k, d=None: PyValue(_core.obj_get(self._val, unwrap(k)) or d, self._engine)
        if n == 'pop': return lambda k, d=None: PyValue(_core.del_op(self._val, unwrap(k)) or d, self._engine)
        if n == 'popitem': return lambda: PyValue(self._val.popitem(), self._engine)
        if n == 'clear': return lambda: self._val.clear()
        if n == 'update': return lambda other: self._val.update(unwrap(other))
        if n == 'setdefault': return lambda k, d=None: PyValue(self._val.setdefault(unwrap(k), unwrap(d)), self._engine)
        
        # --- Set Methods (if dict-like) ---
        if n == 'add': return lambda v: self._val.add(unwrap(v)) if hasattr(self._val, 'add') else None
        if n == 'discard': return lambda v: self._val.discard(unwrap(v)) if hasattr(self._val, 'discard') else None
        if n == 'union': return lambda other: PyValue(self._val.union(unwrap(other)), self._engine)
        if n == 'intersection': return lambda other: PyValue(self._val.intersection(unwrap(other)), self._engine)
        if n == 'difference': return lambda other: PyValue(self._val.difference(unwrap(other)), self._engine)
        if n == 'symmetric_difference': return lambda other: PyValue(self._val.symmetric_difference(unwrap(other)), self._engine)
        if n == 'issubset': return lambda other: PyValue(self._val.issubset(unwrap(other)), self._engine)
        if n == 'issuperset': return lambda other: PyValue(self._val.issuperset(unwrap(other)), self._engine)
        if n == 'isdisjoint': return lambda other: PyValue(self._val.isdisjoint(unwrap(other)), self._engine)

        # Default: C obj_get
        return PyValue(_core.obj_get(self._val, n), self._engine)

class PyEngine:
    def __init__(self):
        self.__dict__['_scope'] = "py"
        self.__dict__['_builtins'] = {
            # --- Python Nouns reassembled from C Verbs ---
            'len': lambda x: PyValue(_core.len(unwrap(x)), self),
            'str': lambda x: PyValue(_core.to_str(unwrap(x)), self),
            'int': lambda x: PyValue(_core.to_int(unwrap(x)), self),
            'float': lambda x: PyValue(_core.to_float(unwrap(x)), self),
            'bool': lambda x: PyValue(_core.to_bool(unwrap(x)), self),
            'abs': lambda x: PyValue(_core.abs(unwrap(x)), self),
            'type': lambda x: PyValue(_core.type(unwrap(x)), self),
            'pow': lambda x, y: PyValue(_core.pow(unwrap(x), unwrap(y)), self),
            'min': lambda *args: PyValue(min(unwrap(a) for a in args), self),
            'max': lambda *args: PyValue(max(unwrap(a) for a in args), self),
            'sum': lambda it: PyValue(sum(unwrap(i) for i in unwrap(it)), self),
            'round': lambda x, n=0: PyValue(round(unwrap(x), unwrap(n)), self),
            
            # Constructors
            'list': lambda iterable=None: PyValue(_core.list_new() if iterable is None else list(unwrap(i) for i in unwrap(iterable)), self),
            'dict': lambda **kwargs: PyValue(_core.obj_new() if not kwargs else {k: unwrap(v) for k, v in kwargs.items()}, self),
            'set': lambda iterable=None: PyValue(set() if iterable is None else set(unwrap(i) for i in unwrap(iterable)), self),
            'tuple': lambda iterable=None: PyValue(tuple() if iterable is None else tuple(unwrap(i) for i in unwrap(iterable)), self),
            'range': lambda *args: PyValue(list(range(*[unwrap(a) for a in args])), self),
            
            # Logic
            'any': lambda x: any(unwrap(i) for i in unwrap(x)),
            'all': lambda x: all(unwrap(i) for i in unwrap(x)),
            'enumerate': lambda it: PyValue(list(enumerate(unwrap(it))), self),
            'zip': lambda *its: PyValue(list(zip(*[unwrap(i) for i in its])), self),
            'map': lambda fn, it: PyValue(list(map(lambda x: unwrap(fn(PyValue(x, self))), unwrap(it))), self),
            'filter': lambda fn, it: PyValue(list(filter(lambda x: unwrap(fn(PyValue(x, self))), unwrap(it))), self),
            'sorted': lambda it, key=None, reverse=False: PyValue(sorted(unwrap(it), key=key, reverse=unwrap(reverse)), self),
            'reversed': lambda it: PyValue(list(reversed(unwrap(it))), self),
            
            # Comparison operations using C micro-ops
            'eq': lambda a, b: PyValue(_core.eq(unwrap(a), unwrap(b)), self),
            'ne': lambda a, b: PyValue(_core.ne(unwrap(a), unwrap(b)), self),
            'lt': lambda a, b: PyValue(_core.lt(unwrap(a), unwrap(b)), self),
            'le': lambda a, b: PyValue(_core.le(unwrap(a), unwrap(b)), self),
            'gt': lambda a, b: PyValue(_core.gt(unwrap(a), unwrap(b)), self),
            'ge': lambda a, b: PyValue(_core.ge(unwrap(a), unwrap(b)), self),
            
            # Bitwise operations using C micro-ops
            'bit_and': lambda a, b: PyValue(_core.bit_and(unwrap(a), unwrap(b)), self),
            'bit_or': lambda a, b: PyValue(_core.bit_or(unwrap(a), unwrap(b)), self),
            'bit_xor': lambda a, b: PyValue(_core.bit_xor(unwrap(a), unwrap(b)), self),
            'bit_not': lambda a: PyValue(_core.bit_not(unwrap(a)), self),
            'lshift': lambda a, b: PyValue(_core.lshift(unwrap(a), unwrap(b)), self),
            'rshift': lambda a, b: PyValue(_core.rshift(unwrap(a), unwrap(b)), self),
            
            # Print (uses C to_str for consistency)
            'print': lambda *args: print(*(str(unwrap(a)) for a in args))
        }
        self.__dict__['decorator'] = create_decorator(self, PyValue)

    def __getattr__(self, n):
        from .wrapper import lie_lookup
        return PyValue(lie_lookup(self, None, n), self)
    
    def __setattr__(self, n, v):
        _core.set_var(self._scope, n, unwrap(v))

py = PyEngine()
