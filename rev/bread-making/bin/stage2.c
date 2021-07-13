#include <stdio.h>
#include "bread.h"

int stage2_counter() {
  puts("mom comes home and finds the bowl");
  return -1;
}

int stage2_bookshelf() {
  puts("mom comes home and brings you food, then sees the bowl");
  return -1;
}

int stage2_box() {
  puts("the box is nice and warm");
  return 0;
}

stage_t stage2 = {
  30,
  "the ingredients are added and stirred into a lumpy dough",
  "mom comes home before you find a place to put the bowl",
  3, {
    {"leave the bowl on the counter", stage2_counter},
    {"put the bowl on the bookshelf", stage2_bookshelf},
    {"hide the bowl inside a box", stage2_box},
  },
};
