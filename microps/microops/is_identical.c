#include "microops.h"
PyObject* micro_is_identical(PyObject* a, PyObject* b) {
    return PyBool_FromLong(a == b);
}
