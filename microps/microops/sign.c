#include "microops.h"
PyObject* micro_sign(PyObject* a) {
    PyObject* zero = PyLong_FromLong(0);
    int cmp_gt = PyObject_RichCompareBool(a, zero, Py_GT);
    int cmp_lt = PyObject_RichCompareBool(a, zero, Py_LT);
    Py_DECREF(zero);
    return PyLong_FromLong(cmp_gt ? 1 : (cmp_lt ? -1 : 0));
}
