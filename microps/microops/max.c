#include "microops.h"
PyObject* micro_max(PyObject* a, PyObject* b) {
    int cmp = PyObject_RichCompareBool(a, b, Py_GT);
    if (cmp < 0) return NULL;
    Py_INCREF(cmp ? a : b);
    return cmp ? a : b;
}
