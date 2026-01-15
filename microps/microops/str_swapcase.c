#include "microops.h"
PyObject* micro_str_swapcase(PyObject* s) {
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    PyObject* method = PyUnicode_FromString("swapcase");
    PyObject* result = PyObject_CallMethodObjArgs(s, method, NULL);
    Py_DECREF(method);
    return result;
}
