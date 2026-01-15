#include "microops.h"
PyObject* micro_is_dict(PyObject* a) {
    return PyBool_FromLong(PyDict_Check(a));
}
