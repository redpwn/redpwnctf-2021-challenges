#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>

#include "bread.h"

stage_t *stages[] = {
  &stage1,
  &stage2,
  &stage3,
  &stage4,
  &stage5,
  &stage6,
  &stage7,
  &stage8,
  &stage9,
  &stage10,
  &stage11,
};

size_t stage_idx;

void fail() {
  puts(stages[stage_idx]->fail);
  exit(EXIT_FAILURE);
}

void handler(int num) {
  fail();
}

size_t get_idx() {
  char buf[128];
  if (fgets(buf, sizeof buf, stdin) == NULL) fail();
  buf[strcspn(buf, "\n")] = 0;
  for (size_t i = 0; i < stages[stage_idx]->num_options; i++) {
    if (!strcmp(buf, stages[stage_idx]->options[i].input)) {
      return i;
    }
  }
  fail();
}

void success() {
  puts("mom doesn't suspect a thing, but asks about some white dots on the bathroom floor");
  char buf[128];
  FILE *f = fopen("flag.txt", "r");
  if (f != NULL && fgets(buf, sizeof buf, f) != NULL) {
    puts(buf);
  } else {
    puts("couldn't open/read flag file, contact an admin if running on server");
  }
}

int main() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  signal(SIGALRM, handler);
  stage_idx = 0;
  while (stage_idx < 11) {
    alarm(stages[stage_idx]->timeout);
    puts(stages[stage_idx]->intro);
    while (1) {
      size_t option = get_idx();
      int res = stages[stage_idx]->options[option].handler();
      if (res == -1) fail();
      if (!res) {
        stage_idx++;
        break;
      }
    }
    puts("");
  }
  alarm(0);
  puts("it's the next morning");
  if (!sink_washed) puts("mom finds flour in the sink and accuses you of making bread");
  else if (!counters_cleaned) puts("mom finds flour on the counter and accuses you of making bread");
  else if (!bread_flushed) puts("mom finds burnt bread on the counter and accuses you of making bread");
  else if (!window_closed) puts("mom finds the window opened and accuses you of making bread");
  else if (!alarm_replaced) puts("mom finds the fire alarm in the laundry room and accuses you of making bread");
  else success();
}
