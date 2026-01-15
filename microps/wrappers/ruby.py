# FILE: microps/wrappers/ruby.py
from .. import _core
from .wrapper import unwrap, get_mm, create_decorator, BaseValue

class RubyValue(BaseValue):
    """
    The Ruby Pretender.
    Reassembles C micro-ops into Ruby's 'Everything is an Object' style.
    """
    
    def __bool__(self):
        """Ruby truthiness: Only nil and false are falsy."""
        return not (self._val is None or self._val is False)

    def __getattr__(self, n):
        """Maps Ruby nouns to C micro-operations."""
        if n.startswith('_'): raise AttributeError(n)
        
        # --- Type/Meta Nouns ---
        if n == 'klass': return lambda: RubyValue(_core.type(self._val), self._engine)
        if n == 'inspect': return lambda: RubyValue(_core.to_str(self._val), self._engine)
        
        # --- Array Nouns (using list micro-ops) ---
        if n in ('length', 'size', 'count'): return lambda: RubyValue(_core.len(self._val), self._engine)
        if n == 'push': return lambda v: (_core.append(self._val, unwrap(v)), self)[1]  # Returns self
        if n == 'pop': return lambda: RubyValue(_core.pop(self._val, RubyValue(-1, self._engine)), self._engine)
        if n == 'shift': return lambda: RubyValue(_core.pop(self._val, RubyValue(0, self._engine)), self._engine)
        if n == 'unshift': return lambda v: (_core.obj_set(self._val, 0, unwrap(v)), self)[1]  # Add to front
        if n == 'reverse': return lambda: (_core.reverse(self._val), self)[1]  # Mutates and returns self
        if n == 'reverse!': return lambda: (_core.reverse(self._val), self)[1]  # Ruby bang method
        if n == 'include?': return lambda v: RubyValue(_core.contains(self._val, unwrap(v)), self._engine)
        if n == 'empty?': return lambda: RubyValue(_core.eq(_core.len(self._val), 0), self._engine)
        if n == 'first': return lambda: RubyValue(_core.obj_get(self._val, 0), self._engine)
        if n == 'last': return lambda: RubyValue(_core.obj_get(self._val, _core.sub(_core.len(self._val), 1)), self._engine)
        if n == 'concat': return lambda other: RubyValue(_core.concat(self._val, unwrap(other)), self._engine)
        if n == 'slice': return lambda start, length: RubyValue(_core.slice(self._val, unwrap(start), _core.add(unwrap(start), unwrap(length))), self._engine)
        
        # --- String Nouns ---
        if n == 'upcase': return lambda: RubyValue(_core.str_upper(self._val), self._engine)
        if n == 'upcase!': return lambda: RubyValue(_core.str_upper(self._val), self._engine)
        if n == 'downcase': return lambda: RubyValue(_core.str_lower(self._val), self._engine)
        if n == 'downcase!': return lambda: RubyValue(_core.str_lower(self._val), self._engine)
        if n == 'split': return lambda sep=" ": RubyValue(_core.str_split(self._val, unwrap(sep)), self._engine)
        if n == 'gsub': return lambda old, new: RubyValue(_core.str_replace(self._val, unwrap(old), unwrap(new)), self._engine)
        if n == 'strip': return lambda: RubyValue(_core.str_replace(_core.str_replace(self._val, " ", ""), "\t", ""), self._engine)
        if n == 'chars': return lambda: RubyValue(_core.str_split(self._val, ""), self._engine)
        if n == 'reverse': return lambda: RubyValue(_core.str_join("", _core.reverse(_core.str_split(self._val, ""))), self._engine)
        if n == 'start_with?': return lambda prefix: RubyValue(_core.eq(_core.slice(self._val, 0, _core.len(unwrap(prefix))), unwrap(prefix)), self._engine)
        if n == 'end_with?': return lambda suffix: RubyValue(_core.eq(_core.slice(self._val, _core.sub(_core.len(self._val), _core.len(unwrap(suffix))), _core.len(self._val)), unwrap(suffix)), self._engine)
        
        # --- Numeric Nouns ---
        if n == 'abs': return lambda: RubyValue(_core.abs(self._val), self._engine)
        if n == 'to_i': return lambda: RubyValue(_core.to_int(self._val), self._engine)
        if n == 'to_f': return lambda: RubyValue(_core.to_float(self._val), self._engine)
        if n == 'to_s': return lambda: RubyValue(_core.to_str(self._val), self._engine)
        if n == 'negative?': return lambda: RubyValue(_core.lt(self._val, 0), self._engine)
        if n == 'positive?': return lambda: RubyValue(_core.gt(self._val, 0), self._engine)
        if n == 'zero?': return lambda: RubyValue(_core.eq(self._val, 0), self._engine)
        if n == 'even?': return lambda: RubyValue(_core.eq(_core.mod(self._val, 2), 0), self._engine)
        if n == 'odd?': return lambda: RubyValue(_core.ne(_core.mod(self._val, 2), 0), self._engine)
        if n == 'floor': return lambda: RubyValue(_core.to_int(self._val), self._engine)
        if n == 'ceil': return lambda: RubyValue(_core.to_int(_core.add(self._val, 0.999999)), self._engine)
        if n == 'round': return lambda: RubyValue(_core.to_int(_core.add(self._val, 0.5)), self._engine)
        
        # --- Hash/Object Nouns ---
        if n == 'keys': return lambda: RubyValue(_core.keys(self._val), self._engine)
        if n == 'values': return lambda: RubyValue(_core.values(self._val), self._engine)
        if n == 'delete': return lambda k: RubyValue(_core.del_op(self._val, unwrap(k)), self._engine)
        if n == 'has_key?': return lambda k: RubyValue(_core.ne(_core.obj_get(self._val, unwrap(k)), None), self._engine)
        if n == 'has_value?': return lambda v: RubyValue(_core.contains(_core.values(self._val), unwrap(v)), self._engine)
        if n == 'merge': return lambda other: RubyValue({**self._val, **unwrap(other)}, self._engine)
        
        # --- Comparison Nouns (Ruby style) ---
        if n == 'eql?': return lambda other: RubyValue(_core.eq(self._val, unwrap(other)), self._engine)
        if n == 'equal?': return lambda other: RubyValue(self._val is unwrap(other), self._engine)
        
        # --- Boolean/Logic Nouns ---
        if n == 'nil?': return lambda: RubyValue(self._val is None, self._engine)

        # Default to C dictionary lookup
        return RubyValue(_core.obj_get(self._val, n), self._engine)

class RubyEngine:
    def __init__(self):
        self.__dict__['_scope'] = "ruby"
        self.__dict__['_builtins'] = {
            'Array': lambda: RubyValue(_core.list_new(), self),
            'Hash': lambda: RubyValue(_core.obj_new(), self),
            'String': lambda x: RubyValue(_core.to_str(unwrap(x)), self),
            'Integer': lambda x: RubyValue(_core.to_int(unwrap(x)), self),
            'Float': lambda x: RubyValue(_core.to_float(unwrap(x)), self),
            'puts': lambda *args: print(*(str(unwrap(a)) for a in args)),
            'print': lambda *args: print(*(str(unwrap(a)) for a in args), end=""),
            'p': lambda *args: print(*(repr(unwrap(a)) for a in args)),
            'nil': None,
            'true': True,
            'false': False,
        }
        self.__dict__['decorator'] = create_decorator(self, RubyValue)

    def __getattr__(self, n):
        from .wrapper import lie_lookup
        return RubyValue(lie_lookup(self, None, n), self)
    
    def __setattr__(self, n, v):
        _core.set_var(self._scope, n, unwrap(v))

ruby = RubyEngine()
