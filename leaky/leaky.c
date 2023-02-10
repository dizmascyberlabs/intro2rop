#include <dlfcn.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void start() {
  printf("Use me to read flag.txt!\n");

  char buf[32];
  memset(buf, 0, sizeof(buf));
  read(0, buf, 256);
}

void leaky(){
        void *self = dlopen(NULL, RTLD_NOW);
        printf("printf() location: %p leak!\n", dlsym(self, "printf"));
}

int main()
{
  start();

  return 0;
}