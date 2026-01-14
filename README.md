# microps

**Micro Operations** - A Python C extension that brings JavaScript and Lua semantics to Python through low-level C operations.

## 🎯 What is microps?

microps is a unique Python library that implements JavaScript and Lua-like behavior in Python by using C extensions for performance-critical operations. It provides language-specific wrappers that emulate the semantics, type coercion, and quirks of JavaScript and Lua while running in Python.

**The best part?** The architecture is fully modular and extensible. Want to add C, C++, C#, R, Ruby, Rust, Squirrel, Go, PHP, Perl, or any other language's semantics? Just add new micro operations (if needed) and create a new wrapper! Since you're building from source, **you can scale this to emulate virtually any language's behavior.**

## ✨ Features

### Core Operations (C Extension)
All core operations are implemented in C for maximum performance:

- **Arithmetic Operations**: `add`, `sub`, `mul`, `div`, `mod`, `pow`
- **Comparison Operations**: `eq` (equality comparison)
- **Logical Operations**: `not`, `truthy` (truthiness evaluation)
- **Type Conversions**: `to_int`, `to_float`, `to_str`
- **Object Operations**: `obj_new`, `obj_get`, `obj_set`, `del`
- **Utility Operations**: `len`, `type`, `keys`
- **Special Operations**: `inc_get` (increment and get), `haunted_get` (ghost variables)

### Language Wrappers

#### JavaScript Wrapper (`microps.js`)
Emulates JavaScript semantics in Python:
- JavaScript-style type coercion
- Truthy/falsy behavior matching JS rules
- String concatenation with `+` operator
- Property access via dot notation
- Built-in constructors: `Object()`, `Number()`, `String()`
- **Ghost Variables**: Special variables prefixed with `ghost_` that auto-increment on each read

#### Lua Wrapper (`microps.lua`)
Emulates Lua semantics in Python:
- Lua-style truthiness (only `nil` and `false` are falsy)
- Table operations with 1-based indexing support
- Metatable support for operator overloading
- Built-in functions: `Table()`, `setmetatable()`, `Number()`
- **Ghost Variables**: Same haunted behavior as JS wrapper

## 🏗️ Architecture

```
microps/
├── _core.c              # Core C extension with scope management
├── include/
│   └── microops.h       # Header file with operation declarations
├── microops/            # Individual C operation implementations
│   ├── add.c, sub.c, mul.c, div.c, mod.c, pow.c
│   ├── eq.c, not.c, truthy.c
│   ├── to_int.c, to_float.c, to_str.c
│   ├── obj_new.c, obj_get.c, obj_set.c, del.c
│   ├── len.c, type.c, keys.c
│   └── inc_get.c        # Special increment-and-get operation
├── wrappers/
│   ├── js.py            # JavaScript semantics wrapper
│   └── lua.py           # Lua semantics wrapper
└── __init__.py          # Package initialization
```

## 🚀 Installation

### Prerequisites
- Python 3.x with development headers
- GCC or compatible C compiler
- setuptools

### Build from source

```bash
# Clone the repository
git clone https://github.com/holyarahippo06/microps.git
cd microps

# Install in development mode
pip install -e .

# Or build directly
python setup.py build
python setup.py install
```

## 📖 Usage

### JavaScript Wrapper

```python
from microps import js

# Use the decorator to enable JS semantics
@js.decorator
def javascript_function():
    # JavaScript-style type coercion
    result = js.Number(5) + js.String("10")  # "510" (string concatenation)
    
    # Truthy/falsy behavior
    if js.String(""):  # False in JS
        print("Won't print")
    
    if js.Number(0):   # False in JS
        print("Won't print either")
    
    # Object creation and property access
    obj = js.Object()
    obj.name = "microps"
    obj.version = 1.0
    
    return obj.name

result = javascript_function()
print(result)  # Output: microps

# Ghost variables - auto-increment on each read
@js.decorator  
def ghost_example():
    print(js.ghost_counter)  # 0
    print(js.ghost_counter)  # 1
    print(js.ghost_counter)  # 2
    return js.ghost_counter  # 3

ghost_example()
```

### Lua Wrapper

```python
from microps import lua

# Use the decorator to enable Lua semantics
@lua.decorator
def lua_function():
    # Lua-style truthiness (only nil and false are falsy)
    if lua.Number(0):  # True in Lua! (0 is truthy)
        print("This prints!")
    
    # Table operations
    t = lua.Table()
    t[1] = "first"   # Lua uses 1-based indexing
    t[2] = "second"
    t["key"] = "value"
    
    return t[1]

result = lua_function()
print(result)  # Output: first

# Metatable support
@lua.decorator
def metatable_example():
    t = lua.Table()
    mt = lua.Table()
    
    # Define custom addition behavior
    mt['__add'] = lambda a, b: lua.Number(100)
    lua.setmetatable(t, mt)
    
    result = t + t  # Uses metatable's __add
    return result   # 100

metatable_example()

# Ghost variables work in Lua too
@lua.decorator
def lua_ghost():
    print(lua.ghost_x)  # 0
    print(lua.ghost_x)  # 1
    print(lua.ghost_x)  # 2
    
lua_ghost()
```

### Direct C Operations

You can also use the C operations directly:

```python
from microps import _core

# Create objects and perform operations
a = 5
b = 10

result = _core.add(a, b)      # 15
result = _core.mul(a, b)      # 50
result = _core.to_str(a)      # "5"

# Object operations
obj = _core.obj_new()
_core.obj_set(obj, "key", "value")
value = _core.obj_get(obj, "key")
```

## 🎭 Special Features

### Ghost Variables (Haunted Get)

Ghost variables are a unique feature where reading a variable automatically increments it in C memory:

```python
from microps import js

@js.decorator
def counter_without_state():
    # No explicit counter variable needed!
    print(f"Call #{js.ghost_count}")  # Increments each time
    print(f"Call #{js.ghost_count}")
    print(f"Call #{js.ghost_count}")
    
counter_without_state()
# Output:
# Call #0
# Call #1
# Call #2
```

This is implemented in C through the `haunted_get` function which:
1. Reads the current value from C memory
2. Increments it
3. Returns the old value

### Scope Management

Each wrapper (JS and Lua) has its own isolated scope managed in C memory:
- Variables set in JS don't affect Lua and vice versa
- Global scope fallback for undefined variables
- Efficient C-level storage without Python dictionary overhead

### Debug Mode

Enable debug mode to see the internal wrapped values:

```python
from microps import js

js.debug = True

@js.decorator
def debug_example():
    x = js.Number(42)
    print(x)  # Output: JS(42.0) instead of just 42.0

debug_example()
```

## 🔧 How It Works

### The Magic of Scope Lies

microps uses a clever technique called "scope lying" to intercept variable access:

1. When you use `@js.decorator` or `@lua.decorator`, it wraps your function
2. It creates a custom dictionary-like object that intercepts `__getitem__` and `__setitem__`
3. Variable reads/writes are redirected to C memory instead of Python's namespace
4. This allows implementing language-specific behaviors at the C level

```python
# When you write:
@js.decorator
def my_func():
    x = 5  # Stored in C memory
    return x  # Retrieved from C memory

# microps rewrites the function's globals dict to use custom C-backed storage
```

### Modular & Extensible Architecture

The true power of microps lies in its modularity:

**Core C Operations** → **Language Wrappers** → **Any Language Semantics You Want**

Each component is independent:
- **Micro Operations**: Atomic C functions for basic operations (`add`, `sub`, type conversions, etc.)
- **Wrappers**: Python files that define language-specific behavior using those operations
- **Extensibility**: Add new operations or wrappers without touching existing code

Want to add Ruby semantics? Create `wrappers/ruby.py` and implement Ruby's truthiness, string interpolation, and symbol handling. Need PHP's type juggling? Make `wrappers/php.py` and go wild with loose comparisons. The C operations are already there - you just define how to use them!

**This means the community can contribute wrappers for ANY language** without needing to modify the core C extension. It's like a language playground where Python becomes a universal host.

## 🎪 Use Cases

- **Educational**: Learn how different languages handle type coercion and semantics
- **Polyglot Programming**: Write Python code with JS, Lua, or ANY language's semantics
- **Language Experimentation**: Test how a language feature would work before implementing it in a real compiler
- **Performance Testing**: Compare Python vs C-backed operations
- **Language Research**: Experiment with language design concepts
- **Community-Driven Language Library**: Build a comprehensive collection of language semantic wrappers
- **Teaching Tool**: Show students the differences between language behaviors side-by-side
- **Prototyping**: Quickly prototype new language features without building a full parser/interpreter
- **Code Golf**: Abuse ghost variables for stateful behavior without explicit state
- **Fun**: Because why not make Python behave like ANY language? 🎉

### Potential Language Wrappers to Build

The community could create wrappers for:
- **C/C++**: Pointer semantics, manual memory "management", undefined behavior emulation
- **Ruby**: Symbol handling, everything is an object, monkey patching
- **PHP**: Type juggling, array/object duality, the infamous `==` operator
- **Rust**: Ownership semantics (checked at runtime), borrow checker simulation
- **Go**: Goroutine-like behavior, multiple return values, nil semantics
- **R**: Vectorized operations, NA handling, data frame semantics
- **Perl**: TMTOWTDI (There's More Than One Way To Do It), special variables
- **Squirrel**: Game scripting semantics, table inheritance
- **And literally any other language!**

Since you're building from source, **the only limit is your imagination!**

## 📊 Performance

Core operations are implemented in C for optimal performance:
- Direct Python C API calls
- Minimal Python overhead
- Efficient scope management in C memory
- No intermediate Python objects for primitive operations

## 🤔 Why?

Because we can. And because understanding how different languages implement their semantics at a low level is fascinating. This project demonstrates:

- How to write Python C extensions
- Language semantic differences (JS vs Lua vs Python)
- Custom scope management
- Type coercion strategies
- The dark arts of `FunctionType` manipulation

## ⚠️ Warnings
- Ghost variables are cursed (that's the point)
- Type coercion rules might surprise you
- Your coworkers might question your sanity

## 🐛 Known Issues / Limitations

- Ghost variables persist across function calls in the same wrapper
- Limited error handling for edge cases
- Not all JS/Lua semantics are implemented (yet)
- No actual JS/Lua VM - just semantic emulation
- The scope lying technique may break with certain Python introspection tools

## 🤝 Contributing

Contributions are **highly encouraged**! The modular design makes it easy to contribute:

### Ways to Contribute

1. **Add New Language Wrappers** (Easiest!)
   - Create a new file in `wrappers/`
   - Implement the language's semantics using existing C operations
   - No C knowledge required if operations already exist!
   - Examples: Ruby, PHP, C#, Go, Rust semantics

2. **Add New Micro Operations** (Intermediate)
   - Add new `.c` files in `microops/`
   - Declare in `microops.h`
   - Expose in `_core.c`
   - Useful for operations specific to certain languages

3. **Improve Existing Wrappers** (Any level)
   - Make JS/Lua semantics more accurate
   - Add missing features
   - Fix edge cases

4. **Documentation & Examples** (Any level)
   - Add example scripts
   - Write tutorials
   - Document language quirks

5. **Testing & Bug Fixes**
   - Report issues
   - Add test cases
   - Fix bugs

### Getting Started with Contributing

Want to add a new language? Here's a template:

```python
# wrappers/yourlang.py
from .. import _core
from types import FunctionType

def unwrap(x):
    return x._val if hasattr(x, '_val') else x

class YourLangValue:
    def __init__(self, v, engine):
        self.__dict__['_val'] = v
        self.__dict__['_engine'] = engine
    
    # Implement language-specific behavior here!
    def __bool__(self):
        # Your language's truthiness rules
        pass
    
    def __add__(self, o):
        # Your language's addition semantics
        pass
    
    # ... etc

class YourLangEngine:
    def __init__(self):
        self.__dict__['_scope'] = "yourlang"
        self.__dict__['debug'] = False
    
    def decorator(self, func):
        # Standard decorator pattern (copy from js.py or lua.py)
        pass
    
    # ... etc

yourlang = YourLangEngine()
```

Then in `__init__.py`, add:
```python
from .wrappers.yourlang import yourlang
```

**That's it!** You've added a new language to microps!

### Building a Language Wrapper Community

The vision is to have a **comprehensive library of language semantic wrappers** that anyone can use to:
- Learn language differences
- Test code behavior across languages
- Experiment with language design
- Have fun with polyglot programming

**Every language wrapper added makes microps more valuable for the entire community!**

## 🙏 Acknowledgments

Created with a deep appreciation for:
- Language design quirks
- The Python C API
- Cursed programming techniques
- The beauty of low-level operations

## 📞 Contact

- GitHub: [@holyarahippo06](https://github.com/holyarahippo06)
- Issues: [GitHub Issues](https://github.com/holyarahippo06/microps/issues)

---

**Remember**: Just because you *can* make Python behave like JavaScript doesn't mean you *should*. But it's fun to try! 🎪
