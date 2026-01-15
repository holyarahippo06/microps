#include "microops.h"
PyObject* micro_bit_not(PyObject* a) { 
    return PyNumber_Invert(a); 
}
