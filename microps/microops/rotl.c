#include "microops.h"
PyObject* micro_rotl(PyObject* a, PyObject* b) {
    long val = PyLong_AsLong(a);
    long shift = PyLong_AsLong(b);
    long bits = sizeof(long) * 8;
    shift = shift % bits;
    long result = (val << shift) | (val >> (bits - shift));
    return PyLong_FromLong(result);
}
