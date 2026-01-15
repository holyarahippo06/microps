#include "microops.h"
PyObject* micro_str_split(PyObject* s, PyObject* sep) { 
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    PyObject* method = PyUnicode_FromString("split");
    PyObject* result = PyObject_CallMethodObjArgs(s, method, sep, NULL);
    Py_DECREF(method);
    return result;
}
