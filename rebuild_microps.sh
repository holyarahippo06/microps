#!/bin/bash

# 1. Setup Folders
mkdir -p microops
mkdir -p include
rm -rf microops/*.c

echo "Generating Micro-ops..."

# Helper function to generate C files
# Usage: gen_op <filename> <C-Expression/Function>
gen_op() {
    cat <<EOF > "microops/$1.c"
#include "microops.h"
PyObject* micro_$1(PyObject* a, PyObject* b) {
    return $2;
}
EOF
}

# Helper for unary ops
gen_unary() {
    cat <<EOF > "microops/$1.c"
#include "microops.h"
PyObject* micro_$1(PyObject* a) {
    return $2;
}
EOF
}

# --- ARITHMETIC ---
gen_op "add" "PyNumber_Add(a, b)"
gen_op "sub" "PyNumber_Subtract(a, b)"
gen_op "mul" "PyNumber_Multiply(a, b)"
gen_op "div" "PyNumber_TrueDivide(a, b)"
gen_op "mod" "PyNumber_Remainder(a, b)"
gen_op "pow" "PyNumber_Power(a, b, Py_None)"

# --- BITWISE ---
gen_op "and" "PyNumber_And(a, b)"
gen_op "or"  "PyNumber_Or(a, b)"
gen_op "xor" "PyNumber_Xor(a, b)"
gen_op "shl" "PyNumber_Lshift(a, b)"
gen_op "shr" "PyNumber_Rshift(a, b)"

# --- COMPARISON ---
gen_op "eq"  "PyObject_RichCompare(a, b, Py_EQ)"
gen_op "neq" "PyObject_RichCompare(a, b, Py_NE)"
gen_op "lt"  "PyObject_RichCompare(a, b, Py_LT)"
gen_op "lte" "PyObject_RichCompare(a, b, Py_LE)"
gen_op "gt"  "PyObject_RichCompare(a, b, Py_GT)"
gen_op "gte" "PyObject_RichCompare(a, b, Py_GE)"

# --- UNARY ---
gen_unary "neg"    "PyNumber_Negative(a)"
gen_unary "pos"    "PyNumber_Positive(a)"
gen_unary "inv"    "PyNumber_Invert(a)"
gen_unary "not"    "PyBool_FromLong(!PyObject_IsTrue(a))"
gen_unary "truthy" "PyBool_FromLong(PyObject_IsTrue(a))"

# --- TYPES ---
gen_unary "to_int"   "PyNumber_Long(a)"
gen_unary "to_float" "PyNumber_Float(a)"
gen_unary "to_str"   "PyObject_Str(a)"

# 2. Generate Header
echo "Generating include/microops.h..."
cat <<EOF > include/microops.h
#ifndef MICROOPS_H
#define MICROOPS_H
#include <Python.h>

// Binary
PyObject* micro_add(PyObject* a, PyObject* b);
PyObject* micro_sub(PyObject* a, PyObject* b);
PyObject* micro_mul(PyObject* a, PyObject* b);
PyObject* micro_div(PyObject* a, PyObject* b);
PyObject* micro_mod(PyObject* a, PyObject* b);
PyObject* micro_pow(PyObject* a, PyObject* b);
PyObject* micro_and(PyObject* a, PyObject* b);
PyObject* micro_or(PyObject* a, PyObject* b);
PyObject* micro_xor(PyObject* a, PyObject* b);
PyObject* micro_shl(PyObject* a, PyObject* b);
PyObject* micro_shr(PyObject* a, PyObject* b);
PyObject* micro_eq(PyObject* a, PyObject* b);
PyObject* micro_neq(PyObject* a, PyObject* b);
PyObject* micro_lt(PyObject* a, PyObject* b);
PyObject* micro_lte(PyObject* a, PyObject* b);
PyObject* micro_gt(PyObject* a, PyObject* b);
PyObject* micro_gte(PyObject* a, PyObject* b);

// Unary
PyObject* micro_neg(PyObject* a);
PyObject* micro_pos(PyObject* a);
PyObject* micro_inv(PyObject* a);
PyObject* micro_not(PyObject* a);
PyObject* micro_truthy(PyObject* a);
PyObject* micro_to_int(PyObject* a);
PyObject* micro_to_float(PyObject* a);
PyObject* micro_to_str(PyObject* a);

#endif
EOF

# 3. Generate the Python Glue (microps.c)
echo "Generating microps.c..."
cat <<EOF > microps.c
#include <Python.h>
#include "microops.h"

static PyObject* _scopes = NULL;

// Scope Management: set_var(scope, key, val)
static PyObject* set_var(PyObject* self, PyObject* args) {
    const char *scope_name, *key;
    PyObject *val;
    if (!PyArg_ParseTuple(args, "ssO", &scope_name, &key, &val)) return NULL;

    PyObject* scope_dict = PyDict_GetItemString(_scopes, scope_name);
    if (!scope_dict) {
        scope_dict = PyDict_New();
        PyDict_SetItemString(_scopes, scope_name, scope_dict);
    }
    PyDict_SetItemString(scope_dict, key, val);
    Py_RETURN_NONE;
}

// Scope Management: get_var(scope, key) -> checks scope then global
static PyObject* get_var(PyObject* self, PyObject* args) {
    const char *scope_name, *key;
    if (!PyArg_ParseTuple(args, "ss", &scope_name, &key)) return NULL;

    // 1. Try language-specific scope
    PyObject* scope_dict = PyDict_GetItemString(_scopes, scope_name);
    if (scope_dict) {
        PyObject* val = PyDict_GetItemString(scope_dict, key);
        if (val) { Py_INCREF(val); return val; }
    }

    // 2. Fallback to global scope
    PyObject* global_dict = PyDict_GetItemString(_scopes, "global");
    if (global_dict) {
        PyObject* val = PyDict_GetItemString(global_dict, key);
        if (val) { Py_INCREF(val); return val; }
    }

    Py_RETURN_NONE;
}

// Macro-like generation for Python-exposed methods
#define BIN_FUNC(name) \\
static PyObject* py_##name(PyObject* self, PyObject* args) { \\
    PyObject *a, *b; \\
    if (!PyArg_ParseTuple(args, "OO", &a, &b)) return NULL; \\
    return micro_##name(a, b); \\
}

#define UNARY_FUNC(name) \\
static PyObject* py_##name(PyObject* self, PyObject* args) { \\
    PyObject *a; \\
    if (!PyArg_ParseTuple(args, "O", &a)) return NULL; \\
    return micro_##name(a); \\
}

BIN_FUNC(add) BIN_FUNC(sub) BIN_FUNC(mul) BIN_FUNC(div) BIN_FUNC(mod) BIN_FUNC(pow)
BIN_FUNC(and) BIN_FUNC(or) BIN_FUNC(xor) BIN_FUNC(shl) BIN_FUNC(shr)
BIN_FUNC(eq) BIN_FUNC(neq) BIN_FUNC(lt) BIN_FUNC(lte) BIN_FUNC(gt) BIN_FUNC(gte)
UNARY_FUNC(neg) UNARY_FUNC(pos) UNARY_FUNC(inv) UNARY_FUNC(not) UNARY_FUNC(truthy)
UNARY_FUNC(to_int) UNARY_FUNC(to_float) UNARY_FUNC(to_str)

static PyMethodDef MicropsMethods[] = {
    {"set_var", set_var, METH_VARARGS, "Set variable in scope"},
    {"get_var", get_var, METH_VARARGS, "Get variable (scope or global)"},
    {"add", py_add, METH_VARARGS, NULL}, {"sub", py_sub, METH_VARARGS, NULL},
    {"mul", py_mul, METH_VARARGS, NULL}, {"div", py_div, METH_VARARGS, NULL},
    {"mod", py_mod, METH_VARARGS, NULL}, {"pow", py_pow, METH_VARARGS, NULL},
    {"and_op", py_and, METH_VARARGS, NULL}, {"or_op", py_or, METH_VARARGS, NULL},
    {"xor_op", py_xor, METH_VARARGS, NULL}, {"shl", py_shl, METH_VARARGS, NULL},
    {"shr", py_shr, METH_VARARGS, NULL}, {"eq", py_eq, METH_VARARGS, NULL},
    {"neq", py_neq, METH_VARARGS, NULL}, {"lt", py_lt, METH_VARARGS, NULL},
    {"lte", py_lte, METH_VARARGS, NULL}, {"gt", py_gt, METH_VARARGS, NULL},
    {"gte", py_gte, METH_VARARGS, NULL}, {"neg", py_neg, METH_VARARGS, NULL},
    {"pos", py_pos, METH_VARARGS, NULL}, {"inv", py_inv, METH_VARARGS, NULL},
    {"not_op", py_not, METH_VARARGS, NULL}, {"truthy", py_truthy, METH_VARARGS, NULL},
    {"to_int", py_to_int, METH_VARARGS, NULL}, {"to_float", py_to_float, METH_VARARGS, NULL},
    {"to_str", py_to_str, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef micropsmodule = {
    PyModuleDef_HEAD_INIT, "microps", NULL, -1, MicropsMethods
};

PyMODINIT_FUNC PyInit_microps(void) {
    _scopes = PyDict_New();
    Py_INCREF(_scopes);
    return PyModule_Create(&micropsmodule);
}
EOF

echo "Done! Run 'python setup.py build_ext --inplace' to compile."
