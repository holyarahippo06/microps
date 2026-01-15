#include "microops.h"
PyObject* micro_is_tuple(PyObject* a) {
    return PyBool_FromLong(PyTuple_Check(a));
}
