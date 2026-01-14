#include <Python.h>
#include "microops.h"
static PyObject* _scopes = NULL;

static PyObject* set_var(PyObject* self, PyObject* args) {
    const char *s_n, *k; PyObject *v;
    if (!PyArg_ParseTuple(args, "ssO", &s_n, &k, &v)) return NULL;
    PyObject* s = PyDict_GetItemString(_scopes, s_n);
    if (!s) { s = PyDict_New(); PyDict_SetItemString(_scopes, s_n, s); }
    PyDict_SetItemString(s, k, v); Py_RETURN_NONE;
}

static PyObject* get_var(PyObject* self, PyObject* args) {
    const char *s_n, *k; if (!PyArg_ParseTuple(args, "ss", &s_n, &k)) return NULL;
    PyObject* s = PyDict_GetItemString(_scopes, s_n);
    PyObject* v = s ? PyDict_GetItemString(s, k) : NULL;
    if (!v) { PyObject* g = PyDict_GetItemString(_scopes, "global"); v = g ? PyDict_GetItemString(g, k) : NULL; }
    if (v) { Py_INCREF(v); return v; } Py_RETURN_NONE;
}

// Haunted Get: Increments a variable in C memory after reading it
static PyObject* haunted_get(PyObject* self, PyObject* args) {
    const char *s_n, *k; if (!PyArg_ParseTuple(args, "ss", &s_n, &k)) return NULL;
    PyObject* s = PyDict_GetItemString(_scopes, s_n);
    if (!s) { s = PyDict_New(); PyDict_SetItemString(_scopes, s_n, s); }
    PyObject* v = micro_inc_get(s, PyUnicode_FromString(k));
    return v;
}

static PyObject* py_obj_new(PyObject* s, PyObject* a) { return micro_obj_new(); }
static PyObject* py_obj_get(PyObject* s, PyObject* a) { PyObject *o, *k; PyArg_ParseTuple(a, "OO", &o, &k); return micro_obj_get(o, k); }
static PyObject* py_obj_set(PyObject* s, PyObject* a) { PyObject *o, *k, *v; PyArg_ParseTuple(a, "OOO", &o, &k, &v); return micro_obj_set(o, k, v); }
static PyObject* py_del_op(PyObject* s, PyObject* a) { PyObject *o, *k; PyArg_ParseTuple(a, "OO", &o, &k); return micro_del(o, k); }
static PyObject* py_inc_get(PyObject* s, PyObject* a) { PyObject *o, *k; PyArg_ParseTuple(a, "OO", &o, &k); return micro_inc_get(o, k); }

#define B_FUNC(n) static PyObject* py_##n(PyObject* s, PyObject* a){ PyObject *x, *y; if(!PyArg_ParseTuple(a,"OO",&x,&y))return NULL; return micro_##n(x,y); }
#define U_FUNC(n) static PyObject* py_##n(PyObject* s, PyObject* a){ PyObject *x; if(!PyArg_ParseTuple(a,"O",&x))return NULL; return micro_##n(x); }

B_FUNC(add) B_FUNC(sub) B_FUNC(mul) B_FUNC(div) B_FUNC(mod) B_FUNC(pow) B_FUNC(eq)
U_FUNC(not) U_FUNC(truthy) U_FUNC(to_int) U_FUNC(to_float) U_FUNC(to_str) U_FUNC(len) U_FUNC(type) U_FUNC(keys)

static PyMethodDef Methods[] = {
    {"set_var", set_var, METH_VARARGS, NULL}, {"get_var", get_var, METH_VARARGS, NULL},
    {"haunted_get", haunted_get, METH_VARARGS, NULL},
    {"obj_new", py_obj_new, METH_NOARGS, NULL}, {"obj_get", py_obj_get, METH_VARARGS, NULL},
    {"obj_set", py_obj_set, METH_VARARGS, NULL}, {"del_op", py_del_op, METH_VARARGS, NULL},
    {"inc_get", py_inc_get, METH_VARARGS, NULL},
    {"add", py_add, METH_VARARGS, NULL}, {"sub", py_sub, METH_VARARGS, NULL},
    {"mul", py_mul, METH_VARARGS, NULL}, {"div", py_div, METH_VARARGS, NULL},
    {"mod", py_mod, METH_VARARGS, NULL}, {"pow", py_pow, METH_VARARGS, NULL},
    {"eq", py_eq, METH_VARARGS, NULL}, {"not_op", py_not, METH_VARARGS, NULL},
    {"truthy", py_truthy, METH_VARARGS, NULL}, {"to_int", py_to_int, METH_VARARGS, NULL},
    {"to_float", py_to_float, METH_VARARGS, NULL}, {"to_str", py_to_str, METH_VARARGS, NULL},
    {"len", py_len, METH_VARARGS, NULL}, {"type", py_type, METH_VARARGS, NULL},
    {"keys", py_keys, METH_VARARGS, NULL}, {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = { PyModuleDef_HEAD_INIT, "_core", NULL, -1, Methods };
PyMODINIT_FUNC PyInit__core(void) { _scopes = PyDict_New(); Py_INCREF(_scopes); return PyModule_Create(&module); }
