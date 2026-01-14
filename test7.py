from microps import js, _core

# 1. Array Indexing (JS Style)
my_arr = js.Array(10, 20, "Chaos")
print(f"Array Index 2: {my_arr[2]}") # JS('Chaos')

# 2. The Observer Effect (Atomic Increment in C)
# We use the C core to set a "Trap" variable
_core.set_var("js", "counter", 0)

@js.decorator
def watch_me():
    # Every time this function runs, 'counter' is read.
    # We'll make our C_Global_Lie use inc_get instead of get_var for counter.
    return counter

# Let's see it change without us doing anything in Python
print(f"Read 1: {js.counter}") 
print(f"Read 2: {js.counter}") 

# 3. Inheritance Chains in C
proto = js.Object()
proto.power = "Over 9000"

warrior = js.Object()
warrior.__proto__ = proto

@js.decorator
def check_power():
    return warrior.power

print(f"Inherited Power: {check_power()}") # JS('Over 9000')
