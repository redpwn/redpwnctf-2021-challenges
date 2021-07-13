#include <stdio.h>
#include "bread.h"

int stage5_oven() {
  puts("the oven makes too much noise, waking up the entire house");
  return -1;
}

int stage5_toaster() {
  puts("the oven glows a soft red-orange");
  return 0;
}

stage_t stage5 = {
  30,
  "the dough is done, and needs to be baked",
  "the dough wants to be baked",
  2, {
    {"preheat the oven", stage5_oven},
    {"preheat the toaster oven", stage5_toaster},
  },
};
