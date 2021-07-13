#include <stdio.h>
#include "bread.h"

int stage8_pull() {
  puts("the tray burns you and you drop the pan on the floor, waking up the entire house");
  return -1;
}

int stage8_towel() {
  puts("the flaming loaf sizzles in the sink");
  return 0;
}

stage_t stage8 = {
  10,
  "there's no time to waste",
  "the flaming loaf sets the kitchen on fire, setting off the fire alarm and waking up the entire house",
  2, {
    {"pull the tray out", stage8_pull},
    {"pull the tray out with a towel", stage8_towel},
  },
};
