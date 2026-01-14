from microps import js, lua
import microps._core as _core

# 1. The Type Lie
x = js.Number(10)
y = js.Object()

print(f"JS says type of 10 is: {x.typeof}")     # JS('number')
print(f"JS says type of {{}} is: {y.typeof}")    # JS('object')
print(f"Python would say: {type(x._val)}")      # <class 'float'>

# 2. The Property Deletion
user = js.Object()
user.name = "Hippo"
user.temp_data = "Secret"

print(f"Before delete: {_core.keys(user._val)}")
user.delete("temp_data")
print(f"After delete:  {_core.keys(user._val)}")

# 3. The Obfuscated "Shared Identity"
# Let's make a variable that exists in BOTH languages but looks different
shared_data = _core.obj_new()
_core.set_var("global", "data", shared_data)

# JS sees it as an object with properties
js.data.val = 100
# Lua sees it as a table with keys
print(f"Lua sees data.val: {lua.data['val']}")

# 4. The "Ghost" Variable
# We set a variable that no one can find via globals()
_core.set_var("js", "hidden", "I am a ghost")

def hack_attempt():
    # A standard Python function trying to find the variable
    return "hidden" in globals()

print(f"Is 'hidden' in globals? {hack_attempt()}") # False
print(f"Can JS see 'hidden'? {js.hidden}")         # JS('I am a ghost')
