#include "microops.h"
PyObject* micro_str_count(PyObject* s, PyObject* substring) {
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    if (!PyUnicode_Check(substring)) substring = PyObject_Str(substring);
    Py_ssize_t count = PyUnicode_Count(s, substring, 0, PY_SSIZE_T_MAX);
    return PyLong_FromSsize_t(count);
}
