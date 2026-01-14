from microps import js, lua
import microps._core as _core

# Constructors now work!
val1 = js.Number("50")
val2 = js.Number(10)
print(f"JS 50 + 10: {val1 + val2}")

# String coercion lie
s1 = js.String("Hello ")
print(f"JS String + Num: {s1 + 100}")

# Lua strict number lie
l1 = lua.Number("10")
print(f"Lua 10 + 20: {l1 + 20}")

# Scope Isolation
js.secret = "JS Secret"
lua.secret = "Lua Secret"
_core.set_var("global", "secret", "Global Secret")

print(f"JS sees: {js.secret}")
print(f"Lua sees: {lua.secret}")

# Truthiness Battle
print(f"Lua 0 truthiness: {bool(lua.Number(0))}") # True in Lua
