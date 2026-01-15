#include "microops.h"
PyObject* micro_str_join(PyObject* sep, PyObject* iterable) { 
    if (!PyUnicode_Check(sep)) sep = PyObject_Str(sep);
    PyObject* method = PyUnicode_FromString("join");
    PyObject* result = PyObject_CallMethodObjArgs(sep, method, iterable, NULL);
    Py_DECREF(method);
    return result;
}
