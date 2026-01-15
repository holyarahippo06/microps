#include "microops.h"
PyObject* micro_str_contains(PyObject* s, PyObject* substring) {
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    if (!PyUnicode_Check(substring)) substring = PyObject_Str(substring);
    int result = PyUnicode_Contains(s, substring);
    if (result < 0) return NULL;
    return PyBool_FromLong(result);
}
