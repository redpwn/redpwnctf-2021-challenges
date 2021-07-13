#include <stdio.h>
#include "bread.h"

int stage7_upstairs() {
  puts("the kitchen catches fire, setting off the fire alarm and waking up the entire house");
  return -1;
}

int stage7_watch() {
  puts("the bread has risen, touching the top of the oven and catching fire");
  return 0;
}

stage_t stage7 = {
  10,
  "45 minutes is an awfully long time",
  "you've moved around too much and mom wakes up, seeing you bake bread",
  2, {
    {"return upstairs", stage7_upstairs},
    {"watch the bread bake", stage7_watch},
  },
};
