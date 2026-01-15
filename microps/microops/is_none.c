#include "microops.h"
PyObject* micro_is_none(PyObject* a) {
    return PyBool_FromLong(a == Py_None);
}
