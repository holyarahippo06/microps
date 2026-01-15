#include "microops.h"
PyObject* micro_popcount(PyObject* a) {
    unsigned long val = PyLong_AsUnsignedLong(a);
    int count = 0;
    while (val) {
        count += val & 1;
        val >>= 1;
    }
    return PyLong_FromLong(count);
}
