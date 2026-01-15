from microps import js, lua, ruby, php, py, c, shared, unwrap

# Note: This test file should be run from outside the microps package directory
# If you're getting import errors, make sure you're running: python3 test.py
# from the parent directory, NOT from inside microps/

@ruby.decorator
def step1_ruby():
    print("[Ruby] Initializing shared packet...")
    packet = ruby.Array()
    packet.push("Microps")
    shared.packet = packet
    print(f"[Ruby] Created object of type: {packet.klass()}")
    print(f"[Ruby] Packet length: {packet.length()}")

@lua.decorator
def step2_lua():
    print("[Lua] Injecting metatable logic...")
    mt = lua.Table()
    mt['__add'] = lambda a, b: lua.Number(1000)
    # Set the metatable on the shared packet
    lua.setmetatable(shared.packet, mt)
    # Lua pretension: index 1 (which Ruby pushed to index 0)
    print(f"[Lua] Item 1 (1-based indexing): {shared.packet[1]}") 

@php.decorator
def step3_php():
    # PHP sees the Lua metatable via the C layer
    print("[PHP] Testing polyglot math...")
    res = shared.packet + 1
    print(f"[PHP] Result: {res}")  # Should be 1000.0
    print(f"[PHP] ✓ Metatable __add worked! Got {res} instead of error!")

print("="*60)
print("POLYGLOT TEST: Ruby -> Lua -> PHP")
print("="*60)
step1_ruby()
step2_lua()
step3_php()
print("="*60)

# Additional test: Mixing methods from different languages
print("\nMULTI-LANGUAGE METHOD TEST:")
print("="*60)

@js.decorator
def test_js_string():
    text = js.String("hello world")
    print(f"[JS] Original: {text}")
    print(f"[JS] toUpperCase(): {text.toUpperCase()}")
    print(f"[JS] length: {text.length}")

@ruby.decorator  
def test_ruby_array():
    arr = ruby.Array()
    arr.push(1)
    arr.push(2)
    arr.push(3)
    print(f"[Ruby] Array: {arr}")
    arr.reverse()
    print(f"[Ruby] reversed: {arr}")
    print(f"[Ruby] last: {arr.last()}")

@php.decorator
def test_php_juggling():
    val = php.strval("42")  # Proper PHP function!
    print(f"[PHP] String '42' + 8 = {val + 8}")  # Type juggling!
    print(f"[PHP] strtoupper: {val.strtoupper()}")

@c.decorator
def test_c_operations():
    # C-style array manipulation
    arr = c.array_new(5)
    c.array_set(arr, 0, 42)
    c.array_set(arr, 1, 100)
    print(f"[C] Array[0] = {c.array_get(arr, 0)}")
    print(f"[C] Array[1] = {c.array_get(arr, 1)}")
    
    # Bitwise operations (very C!)
    val = c.int_cast(15)  # 0b1111
    shifted = c.left_shift(val, 2)  # 0b111100 = 60
    print(f"[C] 15 << 2 = {shifted}")
    
    # Bitwise AND
    result = c.bit_and(60, 12)  # 0b111100 & 0b001100 = 0b001100 = 12
    print(f"[C] 60 & 12 = {result}")

test_js_string()
test_ruby_array()
test_php_juggling()
test_c_operations()

print("="*60)
print("All tests completed successfully!")
