#include <stdio.h>
#include "bread.h"

int window_closed = 0;
int alarm_replaced = 0;

int stage11_window() {
  window_closed = 1;
  puts("the window is closed");
  return 1;
}

int stage11_alarm() {
  alarm_replaced = 1;
  puts("the fire alarm is replaced");
  return 1;
}

int stage11_brush() {
  puts("you sleep very well");
  return 0;
}

stage_t stage11 = {
  30,
  "time to go to sleep",
  "you've taken too long and fall asleep",
  3, {
    {"close the window", stage11_window},
    {"replace the fire alarm", stage11_alarm},
    {"brush teeth and go to bed", stage11_brush},
  },
};
