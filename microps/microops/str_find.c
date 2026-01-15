#include "microops.h"
PyObject* micro_str_find(PyObject* s, PyObject* substring) {
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    if (!PyUnicode_Check(substring)) substring = PyObject_Str(substring);
    Py_ssize_t pos = PyUnicode_Find(s, substring, 0, PY_SSIZE_T_MAX, 1);
    return PyLong_FromSsize_t(pos);
}
