#include <stdio.h>
#include "bread.h"

int oven_unplugged = 0;
int alarm_unplugged = 0;
int window_opened = 0;

int stage9_check() {
  return oven_unplugged && alarm_unplugged && window_opened;
}

int stage9_unplug() {
  oven_unplugged = 1;
  puts("the oven shuts off");
  return !stage9_check();
}

int stage9_alarm() {
  alarm_unplugged = 1;
  puts("you put the fire alarm in another room");
  return !stage9_check();
}

int stage9_window() {
  window_opened = 1;
  puts("cold air rushes in");
  return !stage9_check();
}

stage_t stage9 = {
  5,
  "there's smoke in the air",
  "one of the fire alarms in the house triggers, waking up the entire house",
  3, {
    {"unplug the oven", stage9_unplug},
    {"unplug the fire alarm", stage9_alarm},
    {"open the window", stage9_window},
  },
};
