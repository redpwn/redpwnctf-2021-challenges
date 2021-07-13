#include <stdio.h>
#include "bread.h"

int stage4_kitchen() {
  puts("brother is still awake, and sees you making bread");
  return -1;
}

int stage4_basement() {
  puts("you bring a bottle of oil and a tray");
  return 0;
}

stage_t stage4 = {
  30,
  "it is time to finish the dough",
  "you've shuffled around too long, mom wakes up and sees you making bread",
  2, {
    {"work in the kitchen", stage4_kitchen},
    {"work in the basement", stage4_basement},
  },
};
