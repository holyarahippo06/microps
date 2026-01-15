#include "microops.h"
PyObject* micro_str_rstrip(PyObject* s) {
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    PyObject* method = PyUnicode_FromString("rstrip");
    PyObject* result = PyObject_CallMethodObjArgs(s, method, NULL);
    Py_DECREF(method);
    return result;
}
