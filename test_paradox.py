from microps import js, lua, _core

# Set the lie in the C-Global scope
_core.set_var("global", "logic_bomb", 0)

print("--- The Semantic Paradox ---")
print(f"JS sees logic_bomb as: {js.logic_bomb}")   # Output: 0
print(f"Lua sees logic_bomb as: {lua.logic_bomb}") # Output: 0

print("\n--- The Truth Battle ---")

# JavaScript logic: 0 is Falsy
if js.logic_bomb:
    print("JS Error: 0 should be false")
else:
    print("JS says: 0 is False! (Correct)")

# Lua logic: 0 is Truthy
if lua.logic_bomb:
    print("Lua says: 0 is True! (Correct)")
else:
    print("Lua Error: 0 should be true")

print("\n--- Debug Mode Toggle ---")
js.debug = True
print(f"JS (Debug On): {js.logic_bomb}")

lua.debug = True
print(f"Lua (Debug On): {lua.logic_bomb}")
