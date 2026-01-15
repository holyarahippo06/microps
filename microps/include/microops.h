// FILE: microps/include/microops.h
#ifndef MICROOPS_H
#define MICROOPS_H
#include <Python.h>

// ==================== ARITHMETIC ====================
PyObject* micro_add(PyObject* a, PyObject* b);
PyObject* micro_sub(PyObject* a, PyObject* b);
PyObject* micro_mul(PyObject* a, PyObject* b);
PyObject* micro_div(PyObject* a, PyObject* b);
PyObject* micro_mod(PyObject* a, PyObject* b);
PyObject* micro_pow(PyObject* a, PyObject* b);
PyObject* micro_floor_div(PyObject* a, PyObject* b);
PyObject* micro_neg(PyObject* a);
PyObject* micro_abs(PyObject* a);

// Arithmetic Extensions
PyObject* micro_divmod(PyObject* a, PyObject* b);
PyObject* micro_min(PyObject* a, PyObject* b);
PyObject* micro_max(PyObject* a, PyObject* b);
PyObject* micro_clamp(PyObject* val, PyObject* min_val, PyObject* max_val);
PyObject* micro_sign(PyObject* a);

// ==================== COMPARISON ====================
PyObject* micro_eq(PyObject* a, PyObject* b);
PyObject* micro_ne(PyObject* a, PyObject* b);
PyObject* micro_lt(PyObject* a, PyObject* b);
PyObject* micro_le(PyObject* a, PyObject* b);
PyObject* micro_gt(PyObject* a, PyObject* b);
PyObject* micro_ge(PyObject* a, PyObject* b);

// ==================== BITWISE ====================
PyObject* micro_bit_and(PyObject* a, PyObject* b);
PyObject* micro_bit_or(PyObject* a, PyObject* b);
PyObject* micro_bit_xor(PyObject* a, PyObject* b);
PyObject* micro_bit_not(PyObject* a);
PyObject* micro_lshift(PyObject* a, PyObject* b);
PyObject* micro_rshift(PyObject* a, PyObject* b);

// Bitwise Extensions
PyObject* micro_rotl(PyObject* a, PyObject* b);
PyObject* micro_rotr(PyObject* a, PyObject* b);
PyObject* micro_popcount(PyObject* a);

// ==================== LOGICAL ====================
PyObject* micro_not(PyObject* a);
PyObject* micro_truthy(PyObject* a);

// ==================== TYPE CONVERSIONS ====================
PyObject* micro_to_int(PyObject* a);
PyObject* micro_to_float(PyObject* a);
PyObject* micro_to_str(PyObject* a);
PyObject* micro_to_bool(PyObject* a);

// ==================== TYPE INFO ====================
PyObject* micro_len(PyObject* a);
PyObject* micro_type(PyObject* a);

// Type Checking
PyObject* micro_is_int(PyObject* a);
PyObject* micro_is_float(PyObject* a);
PyObject* micro_is_str(PyObject* a);
PyObject* micro_is_list(PyObject* a);
PyObject* micro_is_dict(PyObject* a);
PyObject* micro_is_tuple(PyObject* a);
PyObject* micro_is_bool(PyObject* a);
PyObject* micro_is_none(PyObject* a);
PyObject* micro_is_callable(PyObject* a);

// ==================== OBJECT OPERATIONS ====================
PyObject* micro_obj_new(void);
PyObject* micro_obj_get(PyObject* obj, PyObject* key);
PyObject* micro_obj_set(PyObject* obj, PyObject* key, PyObject* val);
PyObject* micro_del_op(PyObject* obj, PyObject* key);
PyObject* micro_keys(PyObject* a);
PyObject* micro_values(PyObject* dict);

// ==================== LIST OPERATIONS ====================
PyObject* micro_list_new(void);
PyObject* micro_append(PyObject* list, PyObject* item);
PyObject* micro_pop(PyObject* list, PyObject* index);
PyObject* micro_reverse(PyObject* list);
PyObject* micro_insert(PyObject* list, PyObject* index, PyObject* item);
PyObject* micro_extend(PyObject* list, PyObject* iterable);
PyObject* micro_clear(PyObject* container);

// ==================== SEQUENCE OPERATIONS ====================
PyObject* micro_contains(PyObject* container, PyObject* item);
PyObject* micro_slice(PyObject* seq, PyObject* start, PyObject* end);
PyObject* micro_concat(PyObject* a, PyObject* b);
PyObject* micro_find(PyObject* seq, PyObject* item);
PyObject* micro_rfind(PyObject* seq, PyObject* item);
PyObject* micro_swap(PyObject* seq, PyObject* i, PyObject* j);
PyObject* micro_count(PyObject* seq, PyObject* item);
PyObject* micro_is_sorted(PyObject* seq);

// ==================== STRING OPERATIONS ====================
PyObject* micro_str_upper(PyObject* s);
PyObject* micro_str_lower(PyObject* s);
PyObject* micro_str_split(PyObject* s, PyObject* sep);
PyObject* micro_str_join(PyObject* sep, PyObject* iterable);
PyObject* micro_str_replace(PyObject* s, PyObject* old, PyObject* new);

// String Extensions
PyObject* micro_str_startswith(PyObject* s, PyObject* prefix);
PyObject* micro_str_endswith(PyObject* s, PyObject* suffix);
PyObject* micro_str_contains(PyObject* s, PyObject* substring);
PyObject* micro_str_count(PyObject* s, PyObject* substring);
PyObject* micro_str_find(PyObject* s, PyObject* substring);
PyObject* micro_str_rfind(PyObject* s, PyObject* substring);
PyObject* micro_str_strip(PyObject* s);
PyObject* micro_str_lstrip(PyObject* s);
PyObject* micro_str_rstrip(PyObject* s);
PyObject* micro_str_capitalize(PyObject* s);
PyObject* micro_str_title(PyObject* s);
PyObject* micro_str_swapcase(PyObject* s);
PyObject* micro_str_repeat(PyObject* s, PyObject* n);
PyObject* micro_str_pad_left(PyObject* s, PyObject* width, PyObject* fill);
PyObject* micro_str_pad_right(PyObject* s, PyObject* width, PyObject* fill);
PyObject* micro_str_center(PyObject* s, PyObject* width, PyObject* fill);

// ==================== DICTIONARY OPERATIONS ====================
PyObject* micro_dict_merge(PyObject* dict1, PyObject* dict2);
PyObject* micro_dict_update(PyObject* dict, PyObject* other);
PyObject* micro_dict_pop(PyObject* dict, PyObject* key, PyObject* default_val);
PyObject* micro_dict_setdefault(PyObject* dict, PyObject* key, PyObject* default_val);
PyObject* micro_dict_items(PyObject* dict);

// ==================== FUNCTIONAL OPERATIONS ====================
PyObject* micro_map_func(PyObject* func, PyObject* iterable);
PyObject* micro_filter_func(PyObject* func, PyObject* iterable);
PyObject* micro_reduce_func(PyObject* func, PyObject* iterable, PyObject* initial);

// ==================== HASH & IDENTITY ====================
PyObject* micro_hash_val(PyObject* a);
PyObject* micro_id_val(PyObject* a);
PyObject* micro_is_identical(PyObject* a, PyObject* b);

// ==================== SPECIAL OPERATIONS ====================
PyObject* micro_inc_get(PyObject* obj, PyObject* key);

#endif
