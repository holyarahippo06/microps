#include "microops.h"
PyObject* micro_inc_get(PyObject* o, PyObject* k) {
    PyObject* v = PyObject_GetItem(o, k);
    if (!v) { PyErr_Clear(); v = PyLong_FromLong(0); }
    PyObject* one = PyLong_FromLong(1);
    PyObject* inc = PyNumber_Add(v, one);
    PyObject_SetItem(o, k, inc);
    Py_DECREF(one); Py_DECREF(inc);
    return v; // Return old value
}
