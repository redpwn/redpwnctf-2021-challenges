#include <stdio.h>
#include "bread.h"

int sink_washed = 0;
int counters_cleaned = 0;
int bread_flushed = 0;

int stage10_sink() {
  sink_washed = 1;
  puts("the sink is cleaned");
  return 1;
}

int stage10_counters() {
  counters_cleaned = 1;
  puts("the counters are cleaned");
  return 1;
}

int stage10_flush() {
  bread_flushed = 1;
  puts("the half-baked bread is disposed of");
  return 1;
}

int stage10_sleep() {
  puts("everything appears to be okay");
  return 0;
}

stage_t stage10 = {
  30,
  "the kitchen is a mess",
  "you've taken too long and fall asleep",
  4, {
    {"wash the sink", stage10_sink},
    {"clean the counters", stage10_counters},
    {"flush the bread down the toilet", stage10_flush},
    {"get ready to sleep", stage10_sleep},
  },
};
