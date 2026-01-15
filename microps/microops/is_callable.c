#include "microops.h"
PyObject* micro_is_callable(PyObject* a) {
    return PyBool_FromLong(PyCallable_Check(a));
}
