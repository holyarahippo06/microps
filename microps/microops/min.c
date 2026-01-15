#include "microops.h"
PyObject* micro_min(PyObject* a, PyObject* b) {
    int cmp = PyObject_RichCompareBool(a, b, Py_LT);
    if (cmp < 0) return NULL;
    Py_INCREF(cmp ? a : b);
    return cmp ? a : b;
}
