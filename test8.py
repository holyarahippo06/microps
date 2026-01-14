from microps import lua

print("--- The Observer Effect (Haunted Variables) ---")
lua.ghost_counter = 100
print(f"Touch 1: {lua.ghost_counter}")
print(f"Touch 2: {lua.ghost_counter}")
print(f"Touch 3: {lua.ghost_counter}")

print("\n--- Lua Metatable Magic (Operator Overloading) ---")
my_vec = lua.Table()
my_vec['x'] = 10 

def lua_add_logic(a, b):
    print(" (Metatable Logic Triggered!) ")
    # 'a' is a LuaValue, 'b' is a raw number (or LuaValue)
    # Because of transparency, float(a['x']) just works!
    return float(a['x']) - float(b)

mt = lua.Table()
mt['__add'] = lua_add_logic
lua.setmetatable(my_vec, mt)

# 10 + 5 should trigger the subtract logic -> 5.0
print(f"Result (10 + 5) becomes: {my_vec + 5}")
