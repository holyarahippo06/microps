#include "microops.h"
PyObject* micro_is_bool(PyObject* a) {
    return PyBool_FromLong(PyBool_Check(a));
}
