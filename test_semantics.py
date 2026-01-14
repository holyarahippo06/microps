from wrappers.js import js
from wrappers.lua import lua
import microps

# 1. Test Isolated Variables with shared global
microps.set_var("global", "API_KEY", "SECRET_99")
js.user = "Hippo"
lua.user = "Zebra"

print(f"JS User: {js.user} (Has API: {js.API_KEY})")
print(f"Lua User: {lua.user} (Has API: {lua.API_KEY})")

# 2. Test JS Semantics ("1" + 1 = "11")
@js.decorator
def js_logic(a, b):
    return a + b

print("\n--- JS SEMANTICS ---")
print(f"JS '1' + 1 = {js_logic('1', 1)}") 

# 3. Test Lua Semantics ("1" + 1 = 2)
# (Manual wrapping for variety)
a_lua = lua.Number_as_string = "1"
b_lua = 1
print("\n--- LUA SEMANTICS ---")
print(f"Lua '1' + 1 = {lua.Number_as_string + b_lua}")

# 4. Test Truthiness
empty_list = []

print("\n--- TRUTHINESS BATTLE ---")
# In Python, empty list is False
print(f"Python: {bool(empty_list)}") 

# In JS, empty list is True
js_list = js.my_list = empty_list
print(f"JS: {bool(js.my_list)}")

# In Lua, even 0 is True
lua_zero = lua.zero = 0
print(f"Lua: 0 is {bool(lua.zero)}")

class SchrodingerVar:
    def __repr__(self):
        # When Python tries to print it, it checks JS first, then Lua
        js_val = microps.get_var("js", "secret")
        lua_val = microps.get_var("lua", "secret")
        return f"[JS sees: {js_val} | Lua sees: {lua_val}]"

    def __add__(self, other):
        # This is where it gets evil.
        # If we are 'adding' in a JS context, use JS rules.
        # We can detect context by checking who is asking!
        import inspect
        frame = inspect.currentframe().f_back
        module_name = frame.f_globals.get('__name__', '')
        
        if 'js' in module_name:
            return js.Value(microps.add(microps.to_str("JS-Side: "), microps.to_str(other)))
        else:
            return lua.Value(microps.add(1000, other))

X = SchrodingerVar()
