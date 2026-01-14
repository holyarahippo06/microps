from microps import js

js.x = 10 # Set in C

@js.decorator
def secret_sauce(y):
    # 'x' is not defined in this function! 
    # Usually, this would throw a NameError.
    # But because of our decorator, it looks in C-memory.
    return x + y

print(secret_sauce(5)) # JS(15.0)
