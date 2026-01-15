#include "microops.h"
PyObject* micro_is_int(PyObject* a) {
    return PyBool_FromLong(PyLong_Check(a));
}
