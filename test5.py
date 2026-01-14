from microps import js

parent = js.Object()
parent.species = "Hippo"

child = js.Object()
child.__proto__ = parent # Set the prototype in C memory

print(child.species) # JS('Hippo') <- Inherited through the lie!
