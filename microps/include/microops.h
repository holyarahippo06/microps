#ifndef MICROOPS_H
#define MICROOPS_H
#include <Python.h>

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
PyObject* micro_len(PyObject* a);
PyObject* micro_type(PyObject* a);
PyObject* micro_keys(PyObject* a);
PyObject* micro_obj_new(void);
PyObject* micro_obj_get(PyObject* obj, PyObject* key);
PyObject* micro_obj_set(PyObject* obj, PyObject* key, PyObject* val);
PyObject* micro_del(PyObject* obj, PyObject* key);
PyObject* micro_inc_get(PyObject* obj, PyObject* key);
#endif
