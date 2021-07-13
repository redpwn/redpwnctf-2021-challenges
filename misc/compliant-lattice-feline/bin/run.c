#include <stdio.h>

int main() {
  FILE *f = fopen("flag.txt", "r");
  char flag[64];
  if (f == NULL) {
    puts("Could not open flag file! Please contact an admin.");
    return 1;
  }
  if (fgets(flag, sizeof(flag), f) == NULL) {
    puts("Could not read flag file! Please contact an admin.");
    return 1;
  }
  fclose(f);
  printf("%s", flag);
}
