#include "microops.h"
PyObject* micro_divmod(PyObject* a, PyObject* b) {
    PyObject* div = PyNumber_FloorDivide(a, b);
    PyObject* mod = PyNumber_Remainder(a, b);
    PyObject* result = PyTuple_Pack(2, div, mod);
    Py_DECREF(div);
    Py_DECREF(mod);
    return result;
}
