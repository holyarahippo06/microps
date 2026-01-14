from microps import js, lua, _core

# 1. Setup a haunted variable in C
# (Requires the 'haunted_get' logic from previous TURN's C code)
_core.set_var("lua", "ghost_val", 10)

@lua.decorator
def lua_side(x):
    # 'ghost_val' is retrieved from C memory. 
    # Because of the LuaEngine logic, it's haunted.
    # It will return 10, then increment to 11 in C.
    return x + ghost_val 

@js.decorator
def js_side(x):
    # JavaScript calling Lua logic!
    return lua_side(x)

print("--- Polyglot Execution ---")
# 5 (Input) + 10 (Ghost) = 15
print(f"First run: {js_side(5)}") 

# Now the ghost has grown to 11 in C
# 5 (Input) + 11 (Ghost) = 16
print(f"Second run: {js_side(5)}")
