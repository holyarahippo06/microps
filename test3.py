from microps import js, lua

# 1. Fix the "Nesting" Bug
# JS Logic now "unwraps" Lua values automatically
print("--- Cross-Language Concatenation ---")
val_js = js.String("The answer is: ")
val_lua = lua.Table() # Just for fun, let's use a number
val_lua = 42 
print(val_js + val_lua) # Result: JS('The answer is: 42.0') (No more Lua(42.0) inside!)

# 2. Test the Length Property
print("\n--- Length Property ---")
msg = js.String("Hello World")
print(f"Message: {msg}, Length: {msg.length}") # JS(11)

# 3. Test the Universal Object (JS Object vs Lua Table)
print("\n--- Universal Object Shared Memory ---")
# Create a shared object in C memory
shared_obj = js.Object()

# JS sets a property like an object
shared_obj.username = "Hippo"

# Wrap that same C object in a LuaValue
shared_tab = lua.Table()
shared_tab._val = shared_obj._val 

# Lua reads it like a table
print(f"Lua reads property 'username': {shared_tab['username']}") # Lua('Hippo')

# Lua modifies it
shared_tab["status"] = "Coding"

# JS reads it back as an attribute
print(f"JS reads property 'status': {shared_obj.status}") # JS('Coding')
