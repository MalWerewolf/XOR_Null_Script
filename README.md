Null Preserve and Byte Match Preserving XOR Script
============
### To Do:
* Cleanup global variables
* Change to argparse
* Add functionality to use a file as an XOR key
* SUCCESS

### Description:

This python script can take an "XORed" (file or string) and will XOR it with a user-defined XOR Key (single-byte or multi-byte).
Currently the only output is a file.

----

### Options:

There are MANY ways this script will apply the XOR key: You can specify the HEX offset to start and stop at.

When it runs into:

* NULL byte "00" 
OR when
* Byte is equal to the XOR key byte 
You can specify it to either:
* XOR the byte "normally". 
* Skip byte (without key byte changing) 
* Skip byte (incrementing key byte by 1) '''Could be modified to increment by a certain number''' 
* Skip byte (decrementing key byte by 1) '''Could be modified to decrement by a certain number'''

----

### Background:

I'm in no way a good programmer, so please leave some tips/feedback on how to cleanup, optimize, or streamline this code (it's greatly appreciated).

To leave feedback, or for additional information please go here: http://malwerewolf.com/2013/09/xor-script-skips-null-bytes-00/