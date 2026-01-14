import microps
from wrappers.js import js
from wrappers.lua import lua

val1 = js.Number(10)   # JS Context
val2 = lua.Number(20)  # Lua Context

# Who wins the semantics battle? 
# If JS is on the left, JS rules apply.
result = val1 + val2 
print(f"Result: {result}")
