#include "microops.h"
PyObject* micro_clamp(PyObject* val, PyObject* min_val, PyObject* max_val) {
    PyObject* result = val;
    if (PyObject_RichCompareBool(val, min_val, Py_LT)) result = min_val;
    else if (PyObject_RichCompareBool(val, max_val, Py_GT)) result = max_val;
    Py_INCREF(result);
    return result;
}
