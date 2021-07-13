#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/mman.h>
#include <unistd.h>
#include <seccomp.h>

#define HEAD "\x48\xB8\x37\x13\x37\x13\x37\x13\x37\x13\x48\xBB\x37\x13\x37\x13\x37\x13\x37\x13\x48\xB9\x37\x13\x37\x13\x37\x13\x37\x13\x48\xBA\x37\x13\x37\x13\x37\x13\x37\x13\x48\xBC\x37\x13\x37\x13\x37\x13\x37\x13\x48\xBD\x37\x13\x37\x13\x37\x13\x37\x13\x48\xBE\x37\x13\x37\x13\x37\x13\x37\x13\x48\xBF\x37\x13\x37\x13\x37\x13\x37\x13\x49\xB8\x37\x13\x37\x13\x37\x13\x37\x13\x49\xB9\x37\x13\x37\x13\x37\x13\x37\x13\x49\xBA\x37\x13\x37\x13\x37\x13\x37\x13\x49\xBB\x37\x13\x37\x13\x37\x13\x37\x13\x49\xBC\x37\x13\x37\x13\x37\x13\x37\x13\x49\xBD\x37\x13\x37\x13\x37\x13\x37\x13\x49\xBE\x37\x13\x37\x13\x37\x13\x37\x13\x49\xBF\x37\x13\x37\x13\x37\x13\x37\x13"

int parse(char *str, unsigned long *result) {
  unsigned long val = 0;
  char *end;
  val = strtoul(str, &end, 10);
  if (str == end || errno == ERANGE || *end != 0)
    return -1;
  *result = val;
  return 0;
}

int seccomp() {
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL);
  int ret = 0;
  if (ctx != NULL) {
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    ret |= seccomp_load(ctx);
  }
  seccomp_release(ctx);
  if (ctx == NULL || ret)
    return -1;
  return 0;
}

void __attribute__((always_inline)) static inline die(char *msg) {
  puts(msg);
  _exit(EXIT_FAILURE);
}

void __attribute__((always_inline)) static inline golf_die() {
  die(
    "The character limit is either missing or invalid. "
    "Please pass an integer [50, 1000] as the first argument.\n"
    "If you are running this on the remote server, please contact an admin."
  );
}

int main(int argc, char *argv[]) {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  unsigned long limit;
  if (argc < 2 || parse(argv[1], &limit) == -1 || limit < 50 || limit > 1000) golf_die();
  printf("the current limit is %lu characters\n", limit);

  unsigned char *buf = mmap((void *)(0x420691337000), 0x1000,
    PROT_EXEC | PROT_READ | PROT_WRITE,
    MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
  if (buf == MAP_FAILED) die("could not mmap!");

  memcpy(buf, HEAD, sizeof(HEAD));
  unsigned char *cod = buf + sizeof(HEAD) - 1;

  puts("input:");
  if (fread(cod, 1, limit, stdin) != limit) die("could not read!");
  for (size_t i = 0; i < limit; i++)
    if (cod[i] > 5) cod[i] = 0;

  if (seccomp() == -1) die("could not seccomp!");

  ((void (*)()) buf)();
  _exit(EXIT_SUCCESS);
}
