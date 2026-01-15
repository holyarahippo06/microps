#include "microops.h"
PyObject* micro_is_list(PyObject* a) {
    return PyBool_FromLong(PyList_Check(a));
}
