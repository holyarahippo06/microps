#include "microops.h"
PyObject* micro_slice(PyObject* seq, PyObject* start, PyObject* end) { 
    Py_ssize_t s = PyLong_AsSsize_t(start);
    Py_ssize_t e = PyLong_AsSsize_t(end);
    return PySequence_GetSlice(seq, s, e);
}
