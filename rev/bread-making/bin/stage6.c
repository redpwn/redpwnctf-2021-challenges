#include <stdio.h>
#include "bread.h"

int stage6_oven() {
  puts("the timer makes too much noise, waking up the entire house");
  return -1;
}

int stage6_phone() {
  puts("the timer ticks down");
  return 0;
}

stage_t stage6 = {
  10,
  "the bread is in the oven, and bakes for 45 minutes",
  "you've forgotten how long the bread bakes",
  2, {
    {"use the oven timer", stage6_oven},
    {"set a timer on your phone", stage6_phone},
  },
};
