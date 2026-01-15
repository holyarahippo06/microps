#include "microops.h"
PyObject* micro_rfind(PyObject* seq, PyObject* item) {
    Py_ssize_t size = PySequence_Size(seq);
    for (Py_ssize_t i = size - 1; i >= 0; i--) {
        PyObject* elem = PySequence_GetItem(seq, i);
        int cmp = PyObject_RichCompareBool(elem, item, Py_EQ);
        Py_DECREF(elem);
        if (cmp == 1) return PyLong_FromSsize_t(i);
        if (cmp < 0) return NULL;
    }
    return PyLong_FromLong(-1);
}
