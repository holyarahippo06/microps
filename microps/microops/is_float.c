#include "microops.h"
PyObject* micro_is_float(PyObject* a) {
    return PyBool_FromLong(PyFloat_Check(a));
}
