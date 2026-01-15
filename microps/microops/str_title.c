#include "microops.h"
PyObject* micro_str_title(PyObject* s) {
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    PyObject* method = PyUnicode_FromString("title");
    PyObject* result = PyObject_CallMethodObjArgs(s, method, NULL);
    Py_DECREF(method);
    return result;
}
