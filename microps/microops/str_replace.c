#include "microops.h"
PyObject* micro_str_replace(PyObject* s, PyObject* old, PyObject* new) { 
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    PyObject* method = PyUnicode_FromString("replace");
    PyObject* result = PyObject_CallMethodObjArgs(s, method, old, new, NULL);
    Py_DECREF(method);
    return result;
}
