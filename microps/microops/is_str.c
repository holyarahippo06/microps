#include "microops.h"
PyObject* micro_is_str(PyObject* a) {
    return PyBool_FromLong(PyUnicode_Check(a));
}
