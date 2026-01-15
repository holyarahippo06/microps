#include "microops.h"
PyObject* micro_is_sorted(PyObject* seq) {
    Py_ssize_t size = PySequence_Size(seq);
    if (size <= 1) return PyBool_FromLong(1);
    for (Py_ssize_t i = 0; i < size - 1; i++) {
        PyObject* a = PySequence_GetItem(seq, i);
        PyObject* b = PySequence_GetItem(seq, i + 1);
        int cmp = PyObject_RichCompareBool(a, b, Py_GT);
        Py_DECREF(a);
        Py_DECREF(b);
        if (cmp < 0) return NULL;
        if (cmp) return PyBool_FromLong(0);
    }
    return PyBool_FromLong(1);
}
