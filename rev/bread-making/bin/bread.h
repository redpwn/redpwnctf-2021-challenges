#ifndef INCLUDE_BREAD_H
#define INCLUDE_BREAD_H

typedef struct {
  char *input;
  int (*handler)();
} option_t;

typedef struct {
  unsigned int timeout;
  char *intro;
  char *fail;
  size_t num_options;
  option_t options[];
} stage_t;

extern stage_t stage1;
extern stage_t stage2;
extern stage_t stage3;
extern stage_t stage4;
extern stage_t stage5;
extern stage_t stage6;
extern stage_t stage7;
extern stage_t stage8;
extern stage_t stage9;
extern stage_t stage10;
extern stage_t stage11;

extern int sink_washed;
extern int counters_cleaned;
extern int bread_flushed;
extern int window_closed;
extern int alarm_replaced;

#endif
