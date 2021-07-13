#include <stdio.h>
#include "bread.h"

int stage3_two() {
  puts("the dough has risen, but mom is still awake");
  return -1;
}

int stage3_three() {
  puts("the dough has risen");
  return 0;
}

stage_t stage3 = {
  30,
  "the bread needs to rise",
  "the dough has been forgotten, making an awful smell the next morning",
  2, {
    {"wait 2 hours", stage3_two},
    {"wait 3 hours", stage3_three},
  },
};
