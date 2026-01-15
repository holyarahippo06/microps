#include "microops.h"
PyObject* micro_count(PyObject* seq, PyObject* item) {
    Py_ssize_t size = PySequence_Size(seq);
    Py_ssize_t count = 0;
    for (Py_ssize_t i = 0; i < size; i++) {
        PyObject* elem = PySequence_GetItem(seq, i);
        int cmp = PyObject_RichCompareBool(elem, item, Py_EQ);
        Py_DECREF(elem);
        if (cmp == 1) count++;
        if (cmp < 0) return NULL;
    }
    return PyLong_FromSsize_t(count);
}
