# FILE: microps/wrappers/c.py
from .. import _core
from .wrapper import unwrap, get_mm, create_decorator, BaseValue

class CValue(BaseValue):
    """
    The C Pretender.
    Reassembles C micro-ops into C's explicit, pointer-oriented style.
    Everything is explicit, nothing is hidden.
    """
    
    def __bool__(self):
        """C truthiness: 0 is false, everything else is true."""
        return unwrap(self._val) != 0

    def __getattr__(self, n):
        """Maps C-style operations to micro-operations."""
        if n.startswith('_'): raise AttributeError(n)
        
        # No method syntax in C - everything is a function or operator
        # But we'll provide some helpers for array/string manipulation
        
        # Array-like access helpers
        if n == 'at': return lambda i: CValue(_core.obj_get(self._val, unwrap(i)), self._engine)
        if n == 'set_at': return lambda i, v: _core.obj_set(self._val, unwrap(i), unwrap(v))
        
        # String manipulation (C-style)
        if n == 'chr_at': return lambda i: CValue(ord(str(self._val)[unwrap(i)]), self._engine)
        if n == 'str_len': return lambda: CValue(_core.len(self._val), self._engine)
        
        # Bitwise helpers (these are operators in C, but we expose as methods)
        if n == 'band': return lambda other: CValue(_core.bit_and(self._val, unwrap(other)), self._engine)
        if n == 'bor': return lambda other: CValue(_core.bit_or(self._val, unwrap(other)), self._engine)
        if n == 'bxor': return lambda other: CValue(_core.bit_xor(self._val, unwrap(other)), self._engine)
        if n == 'bnot': return lambda: CValue(_core.bit_not(self._val), self._engine)
        if n == 'lshift': return lambda other: CValue(_core.lshift(self._val, unwrap(other)), self._engine)
        if n == 'rshift': return lambda other: CValue(_core.rshift(self._val, unwrap(other)), self._engine)

        # Default to C structure member access
        return CValue(_core.obj_get(self._val, n), self._engine)
    
    # Override arithmetic to be more explicit (C-style)
    def __add__(self, o):
        """C addition - explicit numeric promotion."""
        return CValue(_core.add(self._val, unwrap(o)), self._engine)
    
    def __sub__(self, o):
        """C subtraction - can simulate pointer arithmetic."""
        return CValue(_core.sub(self._val, unwrap(o)), self._engine)

class CEngine:
    def __init__(self):
        self.__dict__['_scope'] = "c"
        self.__dict__['_builtins'] = {
            # --- Type Constructors (C casts) ---
            'int_cast': lambda x: CValue(_core.to_int(unwrap(x)), self),
            'float_cast': lambda x: CValue(_core.to_float(unwrap(x)), self),
            'char_cast': lambda x: CValue(_core.to_int(unwrap(x)) & 0xFF, self),  # Mask to 8 bits
            'long_cast': lambda x: CValue(_core.to_int(unwrap(x)), self),
            'double_cast': lambda x: CValue(_core.to_float(unwrap(x)), self),
            
            # --- Array Operations ---
            'array_new': lambda size: CValue([0] * unwrap(size), self),
            'array_get': lambda arr, idx: CValue(_core.obj_get(unwrap(arr), unwrap(idx)), self),
            'array_set': lambda arr, idx, val: _core.obj_set(unwrap(arr), unwrap(idx), unwrap(val)),
            
            # --- String Operations (C-style: char arrays) ---
            'strlen': lambda s: CValue(_core.len(unwrap(s)), self),
            'strcpy': lambda dest, src: _core.obj_set(unwrap(dest), 0, unwrap(src)),  # Simplified
            'strcat': lambda dest, src: CValue(_core.concat(unwrap(dest), unwrap(src)), self),
            'strcmp': lambda s1, s2: CValue(_core.eq(unwrap(s1), unwrap(s2)), self),
            'strchr': lambda s, c: CValue(str(unwrap(s)).find(chr(unwrap(c))), self),
            'strstr': lambda haystack, needle: CValue(str(unwrap(haystack)).find(str(unwrap(needle))), self),
            
            # --- Math Operations (C standard library) ---
            'abs': lambda x: CValue(_core.abs(unwrap(x)), self),
            'fabs': lambda x: CValue(_core.abs(unwrap(x)), self),
            'floor': lambda x: CValue(_core.to_int(unwrap(x)), self),
            'ceil': lambda x: CValue(_core.to_int(_core.add(unwrap(x), 0.999999)), self),
            'pow': lambda x, y: CValue(_core.pow(unwrap(x), unwrap(y)), self),
            'sqrt': lambda x: CValue(_core.pow(unwrap(x), 0.5), self),
            
            # --- Bitwise Operations (operators in C) ---
            'bit_and': lambda a, b: CValue(_core.bit_and(unwrap(a), unwrap(b)), self),
            'bit_or': lambda a, b: CValue(_core.bit_or(unwrap(a), unwrap(b)), self),
            'bit_xor': lambda a, b: CValue(_core.bit_xor(unwrap(a), unwrap(b)), self),
            'bit_not': lambda a: CValue(_core.bit_not(unwrap(a)), self),
            'left_shift': lambda a, b: CValue(_core.lshift(unwrap(a), unwrap(b)), self),
            'right_shift': lambda a, b: CValue(_core.rshift(unwrap(a), unwrap(b)), self),
            
            # --- Comparison Operations ---
            'eq': lambda a, b: CValue(_core.eq(unwrap(a), unwrap(b)), self),
            'ne': lambda a, b: CValue(_core.ne(unwrap(a), unwrap(b)), self),
            'lt': lambda a, b: CValue(_core.lt(unwrap(a), unwrap(b)), self),
            'le': lambda a, b: CValue(_core.le(unwrap(a), unwrap(b)), self),
            'gt': lambda a, b: CValue(_core.gt(unwrap(a), unwrap(b)), self),
            'ge': lambda a, b: CValue(_core.ge(unwrap(a), unwrap(b)), self),
            
            # --- Logical Operations ---
            'not_op': lambda a: CValue(_core.not_op(unwrap(a)), self),
            'truthy': lambda a: CValue(_core.truthy(unwrap(a)), self),
            
            # --- Memory Operations (simulated) ---
            'malloc': lambda size: CValue([0] * unwrap(size), self),  # Returns "pointer" (list)
            'calloc': lambda num, size: CValue([0] * (unwrap(num) * unwrap(size)), self),
            'free': lambda ptr: None,  # No-op in Python (GC handles it)
            'memset': lambda ptr, val, size: [_core.obj_set(unwrap(ptr), i, unwrap(val)) for i in range(unwrap(size))],
            'memcpy': lambda dest, src, size: [_core.obj_set(unwrap(dest), i, _core.obj_get(unwrap(src), i)) for i in range(unwrap(size))],
            
            # --- Struct Operations (using dicts) ---
            'struct_new': lambda: CValue(_core.obj_new(), self),
            'struct_get': lambda s, field: CValue(_core.obj_get(unwrap(s), unwrap(field)), self),
            'struct_set': lambda s, field, val: _core.obj_set(unwrap(s), unwrap(field), unwrap(val)),
            
            # --- I/O Operations ---
            'printf': lambda fmt, *args: print(str(unwrap(fmt)) % tuple(unwrap(a) for a in args)),
            'puts': lambda s: print(str(unwrap(s))),
            'putchar': lambda c: print(chr(unwrap(c)), end=''),
            'getchar': lambda: CValue(ord(input()[0]) if True else -1, self),
            
            # --- Constants ---
            'NULL': None,
            'TRUE': 1,
            'FALSE': 0,
            'EOF': -1,
            
            # --- Limits (from limits.h) ---
            'INT_MAX': 2147483647,
            'INT_MIN': -2147483648,
            'CHAR_MAX': 127,
            'CHAR_MIN': -128,
            'UCHAR_MAX': 255,
            'SHRT_MAX': 32767,
            'SHRT_MIN': -32768,
            'LONG_MAX': 9223372036854775807,
            'LONG_MIN': -9223372036854775808,
        }
        self.__dict__['decorator'] = create_decorator(self, CValue)

    def __getattr__(self, n):
        from .wrapper import lie_lookup
        return CValue(lie_lookup(self, None, n), self)
    
    def __setattr__(self, n, v):
        _core.set_var(self._scope, n, unwrap(v))

c = CEngine()
