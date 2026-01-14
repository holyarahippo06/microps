#!/bin/bash

# 1. Folders
mkdir -p microps/microops microps/include microps/wrappers

# 2. Updated Header (Added Len and Objects)
cat <<EOF > microps/include/microops.h
#ifndef MICROOPS_H
#define MICROOPS_H
#include <Python.h>

// Arithmetic & Bitwise (Previous ones)
PyObject* micro_add(PyObject* a, PyObject* b);
PyObject* micro_sub(PyObject* a, PyObject* b);
PyObject* micro_mul(PyObject* a, PyObject* b);
PyObject* micro_div(PyObject* a, PyObject* b);
PyObject* micro_mod(PyObject* a, PyObject* b);
PyObject* micro_pow(PyObject* a, PyObject* b);
PyObject* micro_eq(PyObject* a, PyObject* b);
PyObject* micro_not(PyObject* a);
PyObject* micro_truthy(PyObject* a);
PyObject* micro_to_int(PyObject* a);
PyObject* micro_to_float(PyObject* a);
PyObject* micro_to_str(PyObject* a);

// --- NEW MICRO-OPS ---
PyObject* micro_len(PyObject* a);
PyObject* micro_obj_new(void);
PyObject* micro_obj_get(PyObject* obj, PyObject* key);
PyObject* micro_obj_set(PyObject* obj, PyObject* key, PyObject* val);
#endif
EOF

# 3. Generate New C Files
gen_bin() { echo -e "#include \"microops.h\"\nPyObject* micro_$1(PyObject* a, PyObject* b) { return $2; }" > "microps/microops/$1.c"; }
gen_una() { echo -e "#include \"microops.h\"\nPyObject* micro_$1(PyObject* a) { return $2; }" > "microps/microops/$1.c"; }

# Basic Ops
gen_bin "add" "PyNumber_Add(a, b)"; gen_bin "sub" "PyNumber_Subtract(a, b)"
gen_bin "mul" "PyNumber_Multiply(a, b)"; gen_bin "div" "PyNumber_TrueDivide(a, b)"
gen_bin "mod" "PyNumber_Remainder(a, b)"; gen_bin "pow" "PyNumber_Power(a, b, Py_None)"
gen_bin "eq" "PyObject_RichCompare(a, b, Py_EQ)"
gen_una "not" "PyBool_FromLong(!PyObject_IsTrue(a))"
gen_una "truthy" "PyBool_FromLong(PyObject_IsTrue(a))"
gen_una "to_int" "PyNumber_Long(a)"; gen_una "to_float" "PyNumber_Float(a)"
gen_una "to_str" "PyObject_Str(a)"

# New Ops Implementation
gen_una "len" "PyLong_FromSsize_t(PyObject_Size(a))"

cat <<EOF > microps/microops/obj_new.c
#include "microops.h"
PyObject* micro_obj_new(void) { return PyDict_New(); }
EOF

cat <<EOF > microps/microops/obj_get.c
#include "microops.h"
PyObject* micro_obj_get(PyObject* obj, PyObject* key) {
    PyObject* res = PyObject_GetItem(obj, key);
    if (!res) { PyErr_Clear(); Py_RETURN_NONE; }
    return res;
}
EOF

cat <<EOF > microps/microops/obj_set.c
#include "microops.h"
PyObject* micro_obj_set(PyObject* obj, PyObject* key, PyObject* val) {
    PyObject_SetItem(obj, key, val);
    Py_RETURN_NONE;
}
EOF

# 4. Update Core Engine (_core.c)
cat <<EOF > microps/_core.c
#include <Python.h>
#include "microops.h"
static PyObject* _scopes = NULL;

static PyObject* set_var(PyObject* self, PyObject* args) {
    const char *scope_n, *key; PyObject *v;
    if (!PyArg_ParseTuple(args, "ssO", &scope_n, &key, &v)) return NULL;
    PyObject* s = PyDict_GetItemString(_scopes, scope_n);
    if (!s) { s = PyDict_New(); PyDict_SetItemString(_scopes, scope_n, s); }
    PyDict_SetItemString(s, key, v); Py_RETURN_NONE;
}

static PyObject* get_var(PyObject* self, PyObject* args) {
    const char *scope_n, *key;
    if (!PyArg_ParseTuple(args, "ss", &scope_n, &key)) return NULL;
    PyObject* s = PyDict_GetItemString(_scopes, scope_n);
    PyObject* v = s ? PyDict_GetItemString(s, key) : NULL;
    if (!v) { PyObject* g = PyDict_GetItemString(_scopes, "global"); v = g ? PyDict_GetItemString(g, key) : NULL; }
    if (v) { Py_INCREF(v); return v; } Py_RETURN_NONE;
}

static PyObject* py_obj_new(PyObject* s, PyObject* a) { return micro_obj_new(); }
static PyObject* py_obj_get(PyObject* s, PyObject* a) { PyObject *o, *k; PyArg_ParseTuple(a, "OO", &o, &k); return micro_obj_get(o, k); }
static PyObject* py_obj_set(PyObject* s, PyObject* a) { PyObject *o, *k, *v; PyArg_ParseTuple(a, "OOO", &o, &k, &v); return micro_obj_set(o, k, v); }
static PyObject* py_len(PyObject* s, PyObject* a) { PyObject *o; PyArg_ParseTuple(a, "O", &o); return micro_len(o); }

#define B_FUNC(n) static PyObject* py_##n(PyObject* s, PyObject* a){ PyObject *x, *y; if(!PyArg_ParseTuple(a,"OO",&x,&y))return NULL; return micro_##n(x,y); }
#define U_FUNC(n) static PyObject* py_##n(PyObject* s, PyObject* a){ PyObject *x; if(!PyArg_ParseTuple(a,"O",&x))return NULL; return micro_##n(x); }

B_FUNC(add) B_FUNC(sub) B_FUNC(mul) B_FUNC(div) B_FUNC(mod) B_FUNC(pow) B_FUNC(eq)
U_FUNC(not) U_FUNC(truthy) U_FUNC(to_int) U_FUNC(to_float) U_FUNC(to_str)

static PyMethodDef Methods[] = {
    {"set_var", set_var, METH_VARARGS, NULL}, {"get_var", get_var, METH_VARARGS, NULL},
    {"add", py_add, METH_VARARGS, NULL}, {"sub", py_sub, METH_VARARGS, NULL},
    {"mul", py_mul, METH_VARARGS, NULL}, {"div", py_div, METH_VARARGS, NULL},
    {"mod", py_mod, METH_VARARGS, NULL}, {"pow", py_pow, METH_VARARGS, NULL},
    {"eq", py_eq, METH_VARARGS, NULL}, {"not_op", py_not, METH_VARARGS, NULL},
    {"truthy", py_truthy, METH_VARARGS, NULL}, {"to_int", py_to_int, METH_VARARGS, NULL},
    {"to_float", py_to_float, METH_VARARGS, NULL}, {"to_str", py_to_str, METH_VARARGS, NULL},
    {"len", py_len, METH_VARARGS, NULL}, {"obj_new", py_obj_new, METH_VARARGS, NULL},
    {"obj_get", py_obj_get, METH_VARARGS, NULL}, {"obj_set", py_obj_set, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = { PyModuleDef_HEAD_INIT, "_core", NULL, -1, Methods };
PyMODINIT_FUNC PyInit__core(void) { _scopes = PyDict_New(); Py_INCREF(_scopes); return PyModule_Create(&module); }
EOF

# 5. Generate Improved JS Wrapper
cat <<EOF > microps/wrappers/js.py
from .. import _core

def unwrap(x):
    # This allows JS to consume Lua values or JS values natively
    if hasattr(x, '_val'): return x._val
    return x

class JSValue:
    def __init__(self, value):
        self.__dict__['_val'] = value
    
    def __add__(self, other):
        o = unwrap(other)
        s = unwrap(self)
        if isinstance(s, str) or isinstance(o, str):
            return JSValue(_core.add(_core.to_str(s), _core.to_str(o)))
        return JSValue(_core.add(_core.to_float(s), _core.to_float(o)))

    def __getattr__(self, name):
        # The 'length' logic
        if name == 'length':
            return JSValue(_core.len(self._val))
        # Handle 'obj.prop' syntax using C micro-ops
        return JSValue(_core.obj_get(self._val, name))

    def __setattr__(self, name, value):
        # Handle 'obj.prop = x' syntax using C micro-ops
        _core.obj_set(self._val, name, unwrap(value))

    def __repr__(self): return f"JS({repr(self._val)})"

class JSEngine:
    def __init__(self):
        self.__dict__['_scope'] = "js"
        self.__dict__['Object'] = lambda: JSValue(_core.obj_new())
        self.__dict__['String'] = lambda x: JSValue(_core.to_str(unwrap(x)))
    def __getattr__(self, name):
        if name in self.__dict__: return self.__dict__[name]
        v = _core.get_var(self._scope, name)
        return JSValue(v) if v is not None else JSValue(None)
    def __setattr__(self, name, value):
        _core.set_var(self._scope, name, unwrap(value))

js = JSEngine()
EOF

# 6. Generate Improved Lua Wrapper
cat <<EOF > microps/wrappers/lua.py
from .. import _core
def unwrap(x):
    return x._val if hasattr(x, '_val') else x

class LuaValue:
    def __init__(self, value):
        self.__dict__['_val'] = value
    
    # Lua uses tab["key"] for properties
    def __getitem__(self, key):
        return LuaValue(_core.obj_get(self._val, unwrap(key)))
    
    def __setitem__(self, key, value):
        _core.obj_set(self._val, unwrap(key), unwrap(value))

    def __add__(self, other):
        return LuaValue(_core.add(_core.to_float(self._val), _core.to_float(unwrap(other))))
        
    def __repr__(self): return f"Lua({repr(self._val)})"

class LuaEngine:
    def __init__(self):
        self.__dict__['_scope'] = "lua"
        self.__dict__['Table'] = lambda: LuaValue(_core.obj_new())
    def __getattr__(self, name):
        v = _core.get_var(self._scope, name)
        return LuaValue(v) if v is not None else LuaValue(None)
    def __setattr__(self, name, value):
        _core.set_var(self._scope, name, unwrap(value))

lua = LuaEngine()
EOF

# 7. Rest of files
cat <<EOF > microps/__init__.py
from . import _core
from .wrappers.js import js
from .wrappers.lua import lua
EOF

# setup.py remains mostly the same
cat <<EOF > setup.py
from setuptools import setup, Extension, find_packages
import os
sources = ['microps/_core.c']
for f in os.listdir('microps/microops'):
    if f.endswith('.c'): sources.append(os.path.join('microps/microops', f))
setup(
    name='microps',
    version='1.1',
    packages=find_packages(),
    ext_modules=[Extension('microps._core', sources=sources, include_dirs=['microps/include'])],
)
EOF

echo "Project regenerated with Objects and Len!"
