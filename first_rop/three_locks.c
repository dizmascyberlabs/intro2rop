#include <stdio.h>
// global variables
FILE *fp; // file pointer
char buffer[255]; //buffer to hold flag data

void lock1(int key){
        if (key == 5){
                fp = fopen("flag.txt", "r");
                printf("Lock 1 unlocked!\n");
        }
        else {
                printf("Sorry, lock 1 was not opened.");
        }
        return;
}

void lock2(int key1, int key2){
        if (key1 == 42 && key2 == 1776) {
                fgets(buffer, 255, fp);
                printf("Lock 2 unlocked!\n");
        }
        else {
                printf("Sorry, lock 2 was not opened.");
        }
        return;
}

void lock3() {
        printf("Lock 3 is a gimmie. If you get the other 2, this should work.\nHere is you flag
(hopefully):\n");
        printf("%s\n", buffer);
}

void start(){
        char name[24];
        gets(name);
//      lock1(5);
//      lock2(42, 1776);
//      lock3();
        return;
}

int main() {
        printf("We need to unlock 3 locks to print the flag!\n");
        start();
        return 0;
}
