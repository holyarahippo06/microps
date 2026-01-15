#include "microops.h"
PyObject* micro_str_startswith(PyObject* s, PyObject* prefix) {
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    if (!PyUnicode_Check(prefix)) prefix = PyObject_Str(prefix);
    int result = PyUnicode_Tailmatch(s, prefix, 0, PY_SSIZE_T_MAX, -1);
    return PyBool_FromLong(result == 1);
}
