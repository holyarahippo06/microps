// FILE: microps/_core.c
#include <Python.h>
#include "microops.h"
static PyObject* _scopes = NULL;

// Scope management
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

static PyObject* haunted_get(PyObject* self, PyObject* args) {
    const char *s_n, *k; if (!PyArg_ParseTuple(args, "ss", &s_n, &k)) return NULL;
    PyObject* s = PyDict_GetItemString(_scopes, s_n);
    if (!s) { s = PyDict_New(); PyDict_SetItemString(_scopes, s_n, s); }
    PyObject* v = micro_inc_get(s, PyUnicode_FromString(k));
    return v;
}

// Wrapper macros for cleaner code
#define WRAP_0(name) static PyObject* py_##name(PyObject* s, PyObject* a) { return micro_##name(); }
#define WRAP_1(name) static PyObject* py_##name(PyObject* s, PyObject* a) { PyObject *x; PyArg_ParseTuple(a, "O", &x); return micro_##name(x); }
#define WRAP_2(name) static PyObject* py_##name(PyObject* s, PyObject* a) { PyObject *x, *y; PyArg_ParseTuple(a, "OO", &x, &y); return micro_##name(x, y); }
#define WRAP_3(name) static PyObject* py_##name(PyObject* s, PyObject* a) { PyObject *x, *y, *z; PyArg_ParseTuple(a, "OOO", &x, &y, &z); return micro_##name(x, y, z); }

// Arithmetic
WRAP_2(add) WRAP_2(sub) WRAP_2(mul) WRAP_2(div) WRAP_2(mod) WRAP_2(pow) WRAP_2(floor_div)
WRAP_1(neg) WRAP_1(abs)
WRAP_2(divmod) WRAP_2(min) WRAP_2(max) WRAP_3(clamp) WRAP_1(sign)

// Comparison
WRAP_2(eq) WRAP_2(ne) WRAP_2(lt) WRAP_2(le) WRAP_2(gt) WRAP_2(ge)

// Bitwise
WRAP_2(bit_and) WRAP_2(bit_or) WRAP_2(bit_xor) WRAP_1(bit_not)
WRAP_2(lshift) WRAP_2(rshift) WRAP_2(rotl) WRAP_2(rotr) WRAP_1(popcount)

// Logical
WRAP_1(not) WRAP_1(truthy)

// Type conversions
WRAP_1(to_int) WRAP_1(to_float) WRAP_1(to_str) WRAP_1(to_bool)

// Type info
WRAP_1(len) WRAP_1(type)
WRAP_1(is_int) WRAP_1(is_float) WRAP_1(is_str) WRAP_1(is_list)
WRAP_1(is_dict) WRAP_1(is_tuple) WRAP_1(is_bool) WRAP_1(is_none) WRAP_1(is_callable)

// Object operations
WRAP_0(obj_new) WRAP_2(obj_get) WRAP_3(obj_set) WRAP_2(del_op) WRAP_2(inc_get)
WRAP_1(keys) WRAP_1(values)

// List operations
WRAP_0(list_new) WRAP_2(append) WRAP_2(pop) WRAP_1(reverse)
WRAP_3(insert) WRAP_2(extend) WRAP_1(clear)

// Sequence operations
WRAP_2(contains) WRAP_3(slice) WRAP_2(concat)
WRAP_2(find) WRAP_2(rfind) WRAP_3(swap) WRAP_2(count) WRAP_1(is_sorted)

// String operations
WRAP_1(str_upper) WRAP_1(str_lower) WRAP_2(str_split) WRAP_2(str_join) WRAP_3(str_replace)
WRAP_2(str_startswith) WRAP_2(str_endswith) WRAP_2(str_contains)
WRAP_2(str_count) WRAP_2(str_find) WRAP_2(str_rfind)
WRAP_1(str_strip) WRAP_1(str_lstrip) WRAP_1(str_rstrip)
WRAP_1(str_capitalize) WRAP_1(str_title) WRAP_1(str_swapcase)
WRAP_2(str_repeat) WRAP_3(str_pad_left) WRAP_3(str_pad_right) WRAP_3(str_center)

// Dictionary operations
WRAP_2(dict_merge) WRAP_2(dict_update) WRAP_3(dict_pop)
WRAP_3(dict_setdefault) WRAP_1(dict_items)

// Functional operations
WRAP_2(map_func) WRAP_2(filter_func) WRAP_3(reduce_func)

// Hash & Identity
WRAP_1(hash_val) WRAP_1(id_val) WRAP_2(is_identical)

static PyMethodDef Methods[] = {
    // Scope management
    {"set_var", set_var, METH_VARARGS, NULL}, 
    {"get_var", get_var, METH_VARARGS, NULL},
    {"haunted_get", haunted_get, METH_VARARGS, NULL},
    
    // Arithmetic
    {"add", py_add, METH_VARARGS, NULL}, 
    {"sub", py_sub, METH_VARARGS, NULL},
    {"mul", py_mul, METH_VARARGS, NULL}, 
    {"div", py_div, METH_VARARGS, NULL},
    {"mod", py_mod, METH_VARARGS, NULL}, 
    {"pow", py_pow, METH_VARARGS, NULL},
    {"floor_div", py_floor_div, METH_VARARGS, NULL},
    {"neg", py_neg, METH_VARARGS, NULL},
    {"abs", py_abs, METH_VARARGS, NULL},
    {"divmod", py_divmod, METH_VARARGS, NULL},
    {"min", py_min, METH_VARARGS, NULL},
    {"max", py_max, METH_VARARGS, NULL},
    {"clamp", py_clamp, METH_VARARGS, NULL},
    {"sign", py_sign, METH_VARARGS, NULL},
    
    // Comparison
    {"eq", py_eq, METH_VARARGS, NULL},
    {"ne", py_ne, METH_VARARGS, NULL},
    {"lt", py_lt, METH_VARARGS, NULL},
    {"le", py_le, METH_VARARGS, NULL},
    {"gt", py_gt, METH_VARARGS, NULL},
    {"ge", py_ge, METH_VARARGS, NULL},
    
    // Bitwise
    {"bit_and", py_bit_and, METH_VARARGS, NULL},
    {"bit_or", py_bit_or, METH_VARARGS, NULL},
    {"bit_xor", py_bit_xor, METH_VARARGS, NULL},
    {"bit_not", py_bit_not, METH_VARARGS, NULL},
    {"lshift", py_lshift, METH_VARARGS, NULL},
    {"rshift", py_rshift, METH_VARARGS, NULL},
    {"rotl", py_rotl, METH_VARARGS, NULL},
    {"rotr", py_rotr, METH_VARARGS, NULL},
    {"popcount", py_popcount, METH_VARARGS, NULL},
    
    // Logical
    {"not_op", py_not, METH_VARARGS, NULL},
    {"truthy", py_truthy, METH_VARARGS, NULL},
    
    // Type conversions
    {"to_int", py_to_int, METH_VARARGS, NULL},
    {"to_float", py_to_float, METH_VARARGS, NULL}, 
    {"to_str", py_to_str, METH_VARARGS, NULL},
    {"to_bool", py_to_bool, METH_VARARGS, NULL},
    
    // Type info & checking
    {"len", py_len, METH_VARARGS, NULL}, 
    {"type", py_type, METH_VARARGS, NULL},
    {"is_int", py_is_int, METH_VARARGS, NULL},
    {"is_float", py_is_float, METH_VARARGS, NULL},
    {"is_str", py_is_str, METH_VARARGS, NULL},
    {"is_list", py_is_list, METH_VARARGS, NULL},
    {"is_dict", py_is_dict, METH_VARARGS, NULL},
    {"is_tuple", py_is_tuple, METH_VARARGS, NULL},
    {"is_bool", py_is_bool, METH_VARARGS, NULL},
    {"is_none", py_is_none, METH_VARARGS, NULL},
    {"is_callable", py_is_callable, METH_VARARGS, NULL},
    
    // Object operations
    {"obj_new", py_obj_new, METH_NOARGS, NULL}, 
    {"obj_get", py_obj_get, METH_VARARGS, NULL},
    {"obj_set", py_obj_set, METH_VARARGS, NULL}, 
    {"del_op", py_del_op, METH_VARARGS, NULL},
    {"inc_get", py_inc_get, METH_VARARGS, NULL},
    {"keys", py_keys, METH_VARARGS, NULL},
    {"values", py_values, METH_VARARGS, NULL},
    
    // List operations
    {"list_new", py_list_new, METH_NOARGS, NULL},
    {"append", py_append, METH_VARARGS, NULL},
    {"pop", py_pop, METH_VARARGS, NULL},
    {"reverse", py_reverse, METH_VARARGS, NULL},
    {"insert", py_insert, METH_VARARGS, NULL},
    {"extend", py_extend, METH_VARARGS, NULL},
    {"clear", py_clear, METH_VARARGS, NULL},
    
    // Sequence operations
    {"contains", py_contains, METH_VARARGS, NULL},
    {"slice", py_slice, METH_VARARGS, NULL},
    {"concat", py_concat, METH_VARARGS, NULL},
    {"find", py_find, METH_VARARGS, NULL},
    {"rfind", py_rfind, METH_VARARGS, NULL},
    {"swap", py_swap, METH_VARARGS, NULL},
    {"count", py_count, METH_VARARGS, NULL},
    {"is_sorted", py_is_sorted, METH_VARARGS, NULL},
    
    // String operations
    {"str_upper", py_str_upper, METH_VARARGS, NULL},
    {"str_lower", py_str_lower, METH_VARARGS, NULL},
    {"str_split", py_str_split, METH_VARARGS, NULL},
    {"str_join", py_str_join, METH_VARARGS, NULL},
    {"str_replace", py_str_replace, METH_VARARGS, NULL},
    {"str_startswith", py_str_startswith, METH_VARARGS, NULL},
    {"str_endswith", py_str_endswith, METH_VARARGS, NULL},
    {"str_contains", py_str_contains, METH_VARARGS, NULL},
    {"str_count", py_str_count, METH_VARARGS, NULL},
    {"str_find", py_str_find, METH_VARARGS, NULL},
    {"str_rfind", py_str_rfind, METH_VARARGS, NULL},
    {"str_strip", py_str_strip, METH_VARARGS, NULL},
    {"str_lstrip", py_str_lstrip, METH_VARARGS, NULL},
    {"str_rstrip", py_str_rstrip, METH_VARARGS, NULL},
    {"str_capitalize", py_str_capitalize, METH_VARARGS, NULL},
    {"str_title", py_str_title, METH_VARARGS, NULL},
    {"str_swapcase", py_str_swapcase, METH_VARARGS, NULL},
    {"str_repeat", py_str_repeat, METH_VARARGS, NULL},
    {"str_pad_left", py_str_pad_left, METH_VARARGS, NULL},
    {"str_pad_right", py_str_pad_right, METH_VARARGS, NULL},
    {"str_center", py_str_center, METH_VARARGS, NULL},
    
    // Dictionary operations
    {"dict_merge", py_dict_merge, METH_VARARGS, NULL},
    {"dict_update", py_dict_update, METH_VARARGS, NULL},
    {"dict_pop", py_dict_pop, METH_VARARGS, NULL},
    {"dict_setdefault", py_dict_setdefault, METH_VARARGS, NULL},
    {"dict_items", py_dict_items, METH_VARARGS, NULL},
    
    // Functional operations
    {"map_func", py_map_func, METH_VARARGS, NULL},
    {"filter_func", py_filter_func, METH_VARARGS, NULL},
    {"reduce_func", py_reduce_func, METH_VARARGS, NULL},
    
    // Hash & Identity
    {"hash_val", py_hash_val, METH_VARARGS, NULL},
    {"id_val", py_id_val, METH_VARARGS, NULL},
    {"is_identical", py_is_identical, METH_VARARGS, NULL},
    
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = { PyModuleDef_HEAD_INIT, "_core", NULL, -1, Methods };
PyMODINIT_FUNC PyInit__core(void) { _scopes = PyDict_New(); Py_INCREF(_scopes); return PyModule_Create(&module); }