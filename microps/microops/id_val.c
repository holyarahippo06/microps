#include "microops.h"
PyObject* micro_id_val(PyObject* a) {
    return PyLong_FromVoidPtr(a);
}
