# FILE: microps/wrappers/php.py
from .. import _core
from .wrapper import unwrap, get_mm, create_decorator, BaseValue

class PHPValue(BaseValue):
    """
    The PHP Pretender.
    Reassembles C micro-ops to enforce PHP Type Juggling and Array nouns.
    """

    def __bool__(self):
        """PHP Truthiness: 0, 0.0, "", "0", empty array, and null are falsy."""
        v = self._val
        if v in (0, 0.0, "", "0", None, False):
            return False
        # Check for empty list/dict via C micro_len
        if int(unwrap(_core.len(v))) == 0:
            return False
        return True

    def __add__(self, o):
        """PHP Addition: Check for Lua metatable first, then force numeric context."""
        # Check if object has Lua __add metamethod
        mm = get_mm(self._val, '__add', self._engine)
        if mm:
            # Metatable functions expect objects with _val attribute
            # PHPValue already has this, so we can pass self directly
            res = mm(self, PHPValue(unwrap(o), self._engine))
            return PHPValue(unwrap(res), self._engine)
        
        # Otherwise, PHP's normal type juggling
        v1 = _core.to_float(self._val)
        v2 = _core.to_float(unwrap(o))
        return PHPValue(_core.add(v1, v2), self._engine)

    def __getattr__(self, n):
        """Maps PHP-style nouns/functions as if they were methods."""
        if n.startswith('_'): raise AttributeError(n)

        # --- String Functions (as methods) ---
        if n == 'strtoupper': return lambda: PHPValue(_core.str_upper(self._val), self._engine)
        if n == 'strtolower': return lambda: PHPValue(_core.str_lower(self._val), self._engine)
        if n == 'strlen': return lambda: PHPValue(_core.len(self._val), self._engine)
        if n == 'str_replace': return lambda old, new: PHPValue(_core.str_replace(self._val, unwrap(old), unwrap(new)), self._engine)
        if n == 'str_repeat': return lambda times: PHPValue(_core.str_join("", [self._val] * unwrap(times)), self._engine)
        if n == 'strrev': return lambda: PHPValue(_core.str_join("", _core.reverse(_core.str_split(self._val, ""))), self._engine)
        if n == 'trim': return lambda: PHPValue(_core.str_replace(_core.str_replace(self._val, " ", ""), "\t", ""), self._engine)
        if n == 'ltrim': return lambda: PHPValue(self._val.lstrip(), self._engine)
        if n == 'rtrim': return lambda: PHPValue(self._val.rstrip(), self._engine)
        if n == 'substr': return lambda start, length=None: PHPValue(_core.slice(self._val, unwrap(start), unwrap(start) + unwrap(length) if length else _core.len(self._val)), self._engine)
        if n == 'str_split_fn': return lambda length=1: PHPValue([self._val[i:i+unwrap(length)] for i in range(0, len(self._val), unwrap(length))], self._engine)
        if n == 'ucfirst': return lambda: PHPValue(_core.str_upper(_core.slice(self._val, 0, 1)) + _core.slice(self._val, 1, _core.len(self._val)), self._engine)
        if n == 'lcfirst': return lambda: PHPValue(_core.str_lower(_core.slice(self._val, 0, 1)) + _core.slice(self._val, 1, _core.len(self._val)), self._engine)
        if n == 'str_pad': return lambda length, pad=" ", type="right": self._str_pad(unwrap(length), unwrap(pad), type)
        
        # --- Array Functions (as methods) ---
        if n == 'count': return lambda: PHPValue(_core.len(self._val), self._engine)
        if n == 'array_push': return lambda v: (_core.append(self._val, unwrap(v)), PHPValue(_core.len(self._val), self._engine))[1]
        if n == 'array_pop': return lambda: PHPValue(_core.pop(self._val, PHPValue(-1, self._engine)), self._engine)
        if n == 'array_shift': return lambda: PHPValue(_core.pop(self._val, PHPValue(0, self._engine)), self._engine)
        if n == 'array_unshift': return lambda v: (_core.obj_set(self._val, 0, unwrap(v)), self)[1]
        if n == 'array_reverse': return lambda: PHPValue(_core.reverse(self._val.copy()), self._engine)
        if n == 'array_slice': return lambda start, length=None: PHPValue(_core.slice(self._val, unwrap(start), unwrap(start) + unwrap(length) if length else _core.len(self._val)), self._engine)
        if n == 'array_merge': return lambda *arrays: PHPValue(_core.concat(self._val, *[unwrap(a) for a in arrays]), self._engine)
        if n == 'in_array': return lambda needle: PHPValue(_core.contains(self._val, unwrap(needle)), self._engine)
        if n == 'array_search': 
            def search(needle):
                for i in range(int(unwrap(_core.len(self._val)))):
                    if unwrap(_core.eq(_core.obj_get(self._val, i), unwrap(needle))):
                        return PHPValue(i, self._engine)
                return PHPValue(False, self._engine)
            return search
        if n == 'array_keys': return lambda: PHPValue(_core.keys(self._val), self._engine)
        if n == 'array_values': return lambda: PHPValue(_core.values(self._val), self._engine)
        if n == 'array_key_exists': return lambda key: PHPValue(_core.ne(_core.obj_get(self._val, unwrap(key)), None), self._engine)
        if n == 'array_sum': return lambda: PHPValue(sum(unwrap(v) for v in self._val), self._engine)
        if n == 'array_product': return lambda: PHPValue(_core.mul(*self._val) if self._val else 1, self._engine)
        if n == 'array_unique': return lambda: PHPValue(list(set(self._val)), self._engine)
        if n == 'array_filter': return lambda fn: PHPValue([v for v in self._val if unwrap(fn(PHPValue(v, self._engine)))], self._engine)
        if n == 'array_map': return lambda fn: PHPValue([unwrap(fn(PHPValue(v, self._engine))) for v in self._val], self._engine)
        if n == 'sort': return lambda: (_core.reverse(self._val) if False else sorted(self._val), self)[1]  # Simplified
        if n == 'rsort': return lambda: (sorted(self._val, reverse=True), self)[1]
        if n == 'is_array': return lambda: PHPValue(isinstance(self._val, (list, dict)), self._engine)
        if n == 'empty': return lambda: PHPValue(_core.eq(_core.len(self._val), 0), self._engine)
        if n == 'isset': return lambda: PHPValue(self._val is not None, self._engine)
        
        # --- Type Conversion Functions ---
        if n == 'intval': return lambda: PHPValue(_core.to_int(self._val), self._engine)
        if n == 'floatval': return lambda: PHPValue(_core.to_float(self._val), self._engine)
        if n == 'strval': return lambda: PHPValue(_core.to_str(self._val), self._engine)
        if n == 'boolval': return lambda: PHPValue(_core.to_bool(self._val), self._engine)
        
        # --- Math Functions ---
        if n == 'abs': return lambda: PHPValue(_core.abs(self._val), self._engine)
        if n == 'floor': return lambda: PHPValue(_core.to_int(self._val), self._engine)
        if n == 'ceil': return lambda: PHPValue(_core.to_int(_core.add(self._val, 0.999999)), self._engine)
        if n == 'round': return lambda precision=0: PHPValue(round(unwrap(_core.to_float(self._val)), unwrap(precision)), self._engine)
        if n == 'pow': return lambda exp: PHPValue(_core.pow(self._val, unwrap(exp)), self._engine)
        if n == 'sqrt': return lambda: PHPValue(_core.pow(self._val, 0.5), self._engine)
        if n == 'max': return lambda *args: PHPValue(max(self._val, *[unwrap(a) for a in args]), self._engine)
        if n == 'min': return lambda *args: PHPValue(min(self._val, *[unwrap(a) for a in args]), self._engine)
        
        # --- Type Checking ---
        if n == 'is_numeric': return lambda: PHPValue(isinstance(self._val, (int, float)), self._engine)
        if n == 'is_string': return lambda: PHPValue(isinstance(self._val, str), self._engine)
        if n == 'is_int': return lambda: PHPValue(isinstance(self._val, int), self._engine)
        if n == 'is_float': return lambda: PHPValue(isinstance(self._val, float), self._engine)
        if n == 'is_bool': return lambda: PHPValue(isinstance(self._val, bool), self._engine)
        if n == 'is_null': return lambda: PHPValue(self._val is None, self._engine)
        if n == 'gettype': return lambda: PHPValue(_core.type(self._val), self._engine)

        # Default: C obj_get
        return PHPValue(_core.obj_get(self._val, n), self._engine)
    
    def _str_pad(self, length, pad, pad_type):
        """Helper for str_pad"""
        current_len = int(unwrap(_core.len(self._val)))
        if current_len >= length:
            return self
        
        pad_len = length - current_len
        padding = unwrap(pad) * (pad_len // len(unwrap(pad)) + 1)
        padding = padding[:pad_len]
        
        if pad_type == "left":
            return PHPValue(padding + self._val, self._engine)
        elif pad_type == "both":
            left_pad = padding[:pad_len // 2]
            right_pad = padding[pad_len // 2:]
            return PHPValue(left_pad + self._val + right_pad, self._engine)
        else:  # right
            return PHPValue(self._val + padding, self._engine)

class PHPEngine:
    def __init__(self):
        self.__dict__['_scope'] = "php"
        self.__dict__['_builtins'] = {
            # --- Global PHP Functions (reassembled from C Verbs) ---
            'array': lambda *items: PHPValue(list(unwrap(i) for i in items) if items else _core.list_new(), self),
            
            # String functions
            'strtoupper': lambda x: PHPValue(_core.str_upper(unwrap(x)), self),
            'strtolower': lambda x: PHPValue(_core.str_lower(unwrap(x)), self),
            'strval': lambda x: PHPValue(_core.to_str(unwrap(x)), self),
            'explode': lambda sep, s: PHPValue(_core.str_split(unwrap(s), unwrap(sep)), self),
            'implode': lambda sep, arr: PHPValue(_core.str_join(unwrap(sep), unwrap(arr)), self),
            'strlen': lambda x: PHPValue(_core.len(unwrap(x)), self),
            'str_replace': lambda old, new, subj: PHPValue(_core.str_replace(unwrap(subj), unwrap(old), unwrap(new)), self),
            'substr': lambda s, start, length=None: PHPValue(_core.slice(unwrap(s), unwrap(start), unwrap(start) + unwrap(length) if length else _core.len(unwrap(s))), self),
            'trim': lambda x: PHPValue(_core.str_replace(_core.str_replace(unwrap(x), " ", ""), "\t", ""), self),
            
            # Numeric functions
            'intval': lambda x: PHPValue(_core.to_int(unwrap(x)), self),
            'floatval': lambda x: PHPValue(_core.to_float(unwrap(x)), self),
            'abs': lambda x: PHPValue(_core.abs(unwrap(x)), self),
            'floor': lambda x: PHPValue(_core.to_int(unwrap(x)), self),
            'ceil': lambda x: PHPValue(_core.to_int(_core.add(unwrap(x), 0.999999)), self),
            'round': lambda x, precision=0: PHPValue(round(unwrap(_core.to_float(x)), unwrap(precision)), self),
            'pow': lambda base, exp: PHPValue(_core.pow(unwrap(base), unwrap(exp)), self),
            'sqrt': lambda x: PHPValue(_core.pow(unwrap(x), 0.5), self),
            'max': lambda *args: PHPValue(max(unwrap(a) for a in args), self),
            'min': lambda *args: PHPValue(min(unwrap(a) for a in args), self),
            
            # Array functions
            'array_push': lambda arr, *items: [_core.append(unwrap(arr), unwrap(i)) for i in items] and PHPValue(_core.len(unwrap(arr)), self),
            'array_pop': lambda arr: PHPValue(_core.pop(unwrap(arr), PHPValue(-1, self)), self),
            'array_shift': lambda arr: PHPValue(_core.pop(unwrap(arr), PHPValue(0, self)), self),
            'array_reverse': lambda arr: PHPValue(_core.reverse(unwrap(arr).copy()), self),
            'array_slice': lambda arr, start, length=None: PHPValue(_core.slice(unwrap(arr), unwrap(start), unwrap(start) + unwrap(length) if length else _core.len(unwrap(arr))), self),
            'array_merge': lambda *arrays: PHPValue(_core.concat(*[unwrap(a) for a in arrays]), self) if arrays else PHPValue(_core.list_new(), self),
            'count': lambda x: PHPValue(_core.len(unwrap(x)), self),
            'in_array': lambda needle, haystack: PHPValue(_core.contains(unwrap(haystack), unwrap(needle)), self),
            'array_keys': lambda arr: PHPValue(_core.keys(unwrap(arr)), self),
            'array_values': lambda arr: PHPValue(_core.values(unwrap(arr)), self),
            'array_sum': lambda arr: PHPValue(sum(unwrap(arr)), self),
            'empty': lambda x: PHPValue(_core.eq(_core.len(unwrap(x)), 0), self),
            'isset': lambda x: PHPValue(unwrap(x) is not None, self),
            
            # Type checking
            'is_array': lambda x: PHPValue(isinstance(unwrap(x), (list, dict)), self),
            'is_numeric': lambda x: PHPValue(isinstance(unwrap(x), (int, float)), self),
            'is_string': lambda x: PHPValue(isinstance(unwrap(x), str), self),
            'is_int': lambda x: PHPValue(isinstance(unwrap(x), int), self),
            'is_float': lambda x: PHPValue(isinstance(unwrap(x), float), self),
            'is_bool': lambda x: PHPValue(isinstance(unwrap(x), bool), self),
            'is_null': lambda x: PHPValue(unwrap(x) is None, self),
            'gettype': lambda x: PHPValue(_core.type(unwrap(x)), self),
            
            # Global Constants
            'TRUE': True,
            'FALSE': False,
            'NULL': None,
            'true': True,
            'false': False,
            'null': None,
            
            # Output
            'echo': lambda *args: print(*(str(unwrap(a)) for a in args), end=""),
            'print': lambda x: print(str(unwrap(x)), end=""),
            'print_r': lambda x: print(f"Array\n(\n{unwrap(x)}\n)"),
            'var_dump': lambda *args: [print(f"{type(unwrap(a)).__name__}({unwrap(a)})") for a in args],
        }
        self.__dict__['decorator'] = create_decorator(self, PHPValue)

    def __getattr__(self, n):
        from .wrapper import lie_lookup
        return PHPValue(lie_lookup(self, None, n), self)
    
    def __setattr__(self, n, v):
        _core.set_var(self._scope, n, unwrap(v))

php = PHPEngine()
