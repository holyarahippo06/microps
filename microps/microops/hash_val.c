#include "microops.h"
PyObject* micro_hash_val(PyObject* a) {
    Py_hash_t hash = PyObject_Hash(a);
    if (hash == -1 && PyErr_Occurred()) return NULL;
    return PyLong_FromSsize_t(hash);
}
