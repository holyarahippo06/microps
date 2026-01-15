#include "microops.h"
PyObject* micro_swap(PyObject* seq, PyObject* i, PyObject* j) {
    Py_ssize_t idx_i = PyLong_AsSsize_t(i);
    Py_ssize_t idx_j = PyLong_AsSsize_t(j);
    PyObject* val_i = PySequence_GetItem(seq, idx_i);
    PyObject* val_j = PySequence_GetItem(seq, idx_j);
    PySequence_SetItem(seq, idx_i, val_j);
    PySequence_SetItem(seq, idx_j, val_i);
    Py_DECREF(val_i);
    Py_DECREF(val_j);
    Py_RETURN_NONE;
}
