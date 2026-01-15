#include "microops.h"
PyObject* micro_str_endswith(PyObject* s, PyObject* suffix) {
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    if (!PyUnicode_Check(suffix)) suffix = PyObject_Str(suffix);
    int result = PyUnicode_Tailmatch(s, suffix, 0, PY_SSIZE_T_MAX, 1);
    return PyBool_FromLong(result == 1);
}
