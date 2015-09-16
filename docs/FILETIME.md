# FILETIME structure

The FILETIME structure is a 64-bit value representing the number of 100-nanosecond intervals since January 1, 1601.

```
typedef struct \_FILETIME { // ft
  DWORD dwLowDateTime;
  DWORD dwHighDateTime;
} FILETIME;
```

## Members

dwLowDateTime - Specifies the low-order 32 bits of the file time.
dwHighDateTime - Specifies the high-order 32 bits of the file time.

## Remarks

It is not recommended that you add and subtract values from the FILETIME structure to obtain relative times. Instead, you should:

* Copy the resulting FILETIME structure to a LARGE\_INTEGER structure.
* Use normal 64-bit arithmetic on the LARGE\_INTEGER value.
