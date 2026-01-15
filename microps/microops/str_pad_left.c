#include "microops.h"
PyObject* micro_str_pad_left(PyObject* s, PyObject* width, PyObject* fill) {
    if (!PyUnicode_Check(s)) s = PyObject_Str(s);
    if (!PyUnicode_Check(fill)) fill = PyObject_Str(fill);
    PyObject* method = PyUnicode_FromString("rjust");
    PyObject* result = PyObject_CallMethodObjArgs(s, method, width, fill, NULL);
    Py_DECREF(method);
    return result;
}
