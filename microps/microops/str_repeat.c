#include "microops.h"
PyObject* micro_str_repeat(PyObject* s, PyObject* n) {
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    return PySequence_Repeat(s, PyLong_AsSsize_t(n));
}
