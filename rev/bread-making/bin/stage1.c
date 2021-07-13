#include <stdio.h>
#include "bread.h"

int flour_added = 0;
int yeast_added = 0;
int salt_added = 0;
int water_added = 0;

int stage1_check() {
  return flour_added && yeast_added && salt_added && water_added;
}

int stage1_flour() {
  flour_added = 1;
  puts("flour has been added");
  return !stage1_check();
}

int stage1_yeast() {
  yeast_added = 1;
  puts("yeast has been added");
  return !stage1_check();
}

int stage1_salt() {
  salt_added = 1;
  puts("salt has been added");
  return !stage1_check();
}

int stage1_water() {
  water_added = 1;
  puts("water has been added");
  return !stage1_check();
}

stage_t stage1 = {
  30,
  "add ingredients to the bowl",
  "we don't have that ingredient at home!",
  4, {
    {"add flour", stage1_flour},
    {"add yeast", stage1_yeast},
    {"add salt", stage1_salt},
    {"add water", stage1_water},
  },
};
