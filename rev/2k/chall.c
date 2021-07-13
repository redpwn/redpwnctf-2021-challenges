#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define SIZE 0x10000

typedef struct {
    int16_t *stack;
    int16_t *mem;
    uint16_t mp;
    uint32_t ip;
    char* prog;
    size_t len;
} state;

typedef enum {
    VM_NOP = 0x00,
    VM_DUP = 0x01,
    VM_DSC = 0x02,
    VM_EXT = 0x03,
    VM_ADD = 0x10,
    VM_SUB = 0x11,
    VM_MUL = 0x12,
    VM_DIV = 0x13,
    VM_MOD = 0x14,
    VM_MMD = 0x15,
    VM_NEQ = 0x16,
    VM_SIG = 0x17,
    VM_INP = 0x20,
    VM_OUT = 0x21,
    VM_LOV = 0x22,
    VM_JMP = 0x30,
    VM_JIZ = 0x31,
    VM_JNZ = 0x32,
    VM_JLT = 0x33,
    VM_JGT = 0x34,
    VM_JLE = 0x35,
    VM_JGE = 0x36,
    VM_STO = 0x40,
    VM_RET = 0x41,
    VM_IMP = 0x50,
    VM_DMP = 0x51,
    VM_IMS = 0x52,
    VM_DMS = 0x53,
} __attribute__((packed)) opcodes;



__attribute__((always_inline)) static inline
void _push(int16_t** const stack, int16_t val) {
	*((*stack)++) = val;
}


__attribute__((always_inline)) static inline
int16_t _pop(int16_t** const stack) {
    return *(--(*stack));
}


__attribute__((always_inline)) static inline
int16_t _peek(int16_t* const stack) {
    return *(stack - 1);
}


int step(state* st) {
    // fprintf(stderr, "instruction: %04x\topcode: %02x\n", st->ip, st->prog[st->ip]);
    // fprintf(stderr, "memat: %08x\n", st->mem[st->mp]);
    if (st->ip > st->len) {
        return 1;
    }
    switch (st->prog[st->ip++]) {
        case VM_NOP:
            break;
        case VM_DUP:
            _push(&st->stack, _peek(st->stack));
            break;
        case VM_DSC:
            _pop(&st->stack);
            break;
        case VM_EXT:
            return _pop(&st->stack);
        case VM_ADD:
            {
                int16_t t1 = _pop(&st->stack);
                int16_t t2 = _pop(&st->stack);
                _push(&st->stack, t1+t2);
                break;
            }
        case VM_SUB:
            {
                int16_t t1 = _pop(&st->stack);
                int16_t t2 = _pop(&st->stack);
                _push(&st->stack, t1-t2);
                break;
            }
        case VM_MUL:
            {
                int16_t t1 = _pop(&st->stack);
                int16_t t2 = _pop(&st->stack);
                _push(&st->stack, t1*t2);
                break;
            }
        case VM_DIV:
            {
                int16_t t1 = _pop(&st->stack);
                int16_t t2 = _pop(&st->stack);
                _push(&st->stack, t1/t2);
                break;
            }
        case VM_MOD:
            {
                int16_t t1 = _pop(&st->stack);
                int16_t t2 = _pop(&st->stack);
                _push(&st->stack, t1%t2);
                break;
            }
        case VM_MMD:
            {
                int16_t m = _pop(&st->stack);
                int16_t t1 = _pop(&st->stack);
                int16_t t2 = _pop(&st->stack);
                _push(&st->stack, (int16_t)(((uint16_t)t1*(uint16_t)t2)%(uint16_t)m));
                break;
            }
        case VM_NEQ:
            {
                int16_t t1 = _pop(&st->stack);
                int16_t t2 = _pop(&st->stack);
                if (t1 == t2) {
                    _push(&st->stack, 1);
                } else {
                    _push(&st->stack, 0);
                }
                break;
            }
        case VM_SIG:
            {
                int16_t n = _pop(&st->stack);
                if (n < 0) {
                    _push(&st->stack, -1);
                } else if (n == 0) {
                    _push(&st->stack, 0);
                } else {
                    _push(&st->stack, 1);
                }
                break;
            }
        case VM_INP:
            {
                int16_t character = (int16_t) getchar();
                _push(&st->stack, character);
                break;
            }
        case VM_OUT:
            {
                int16_t t1 = _pop(&st->stack);
                if (!(0 <= t1 && t1 <= 255)) {
                    return 1;
                }
                printf("%c", t1);
                break;
            }
        case VM_LOV:
            {
                if (st->ip + sizeof(int16_t) >= st->len) {
                    return 1;
                }
                int16_t ld = *(int16_t*)(st->prog + st->ip);
                st->ip += sizeof(int16_t);
                _push(&st->stack, ld);
                break;
            }
        case VM_JMP:
            {
                uint16_t t = abs(_pop(&st->stack));
                st->ip = t;
                break;
            }
        case VM_JIZ:
            {
                uint16_t t = abs(_pop(&st->stack));
                if (_pop(&st->stack) == 0) {
                    st->ip = t;
                }
                break;
            }
        case VM_JNZ:
            {
                uint16_t t = abs(_pop(&st->stack));
                if (_pop(&st->stack) != 0) {
                    st->ip = t;
                }
                break;
            }
        case VM_JLT:
            {
                uint16_t t = abs(_pop(&st->stack));
                if (_pop(&st->stack) < 0) {
                    st->ip = t;
                }
                break;
            }
        case VM_JLE:
            {
                uint16_t t = abs(_pop(&st->stack));
                if (_pop(&st->stack) <= 0) {
                    st->ip = t;
                }
                break;
            }
        case VM_JGT:
            {
                uint16_t t = abs(_pop(&st->stack));
                if (_pop(&st->stack) > 0) {
                    st->ip = t;
                }
                break;
            }
        case VM_JGE:
            {
                uint16_t t = abs(_pop(&st->stack));
                if (_pop(&st->stack) >= 0) {
                    st->ip = t;
                }
                break;
           }
        case VM_STO:
            {
                st->mem[st->mp] = _pop(&st->stack);
                break;
            }
        case VM_RET:
            {
                _push(&st->stack, st->mem[st->mp]);
                break;
            }
        case VM_IMP:
            {
                st->mp += 1;
                st->mp %= SIZE;
                break;
            }
        case VM_DMP:
            {
                st->mp -= 1;
                st->mp %= SIZE;
                break;
            }
        case VM_IMS:
            {
                st->mp += _pop(&st->stack);
                st->mp %= SIZE;
                break;
            }
        case VM_DMS:
            {
                st->mp -= _pop(&st->stack);
                st->mp %= SIZE;
                break;
            }
    }
    return -1;
}

int file_size(FILE *f, size_t *size) {
    long off = ftell(f);
    if (off == -1) return -1;
    if (fseek(f, 0, SEEK_END) == -1) return -1;
    long len = ftell(f);
    if (len == -1) return -1;
    if (fseek(f, off, SEEK_SET) == -1) return -1;
    *size = (size_t) len;
    return 0;
}

__attribute__((always_inline)) static inline
void die() {
    puts("If you are running this on the remote server, please contact an admin.");
    exit(EXIT_FAILURE);
}

int main() {
    setbuf(stdout, NULL);

    int16_t* stack = calloc(0x800, sizeof(int16_t));
    int16_t* fstack = stack;
    int16_t mem[SIZE];

    size_t len = 0;
    char *prog = NULL;

    FILE *f = fopen("prog.bin", "rb");
    if (f == NULL) {
        puts("Couldn't open program.");
        die();
    }
    if (file_size(f, &len) == -1 || (prog = calloc(len, sizeof(char))) == NULL || fread(prog, sizeof(char), len, f) != len) {
        puts("Couldn't read program.");
        die();
    }
    fclose(f);

    state st = {
        .stack = stack,
        .mem = mem,
        .mp = 0,
        .ip = 0,
        .prog = prog,
        .len = len,
    };
    int val = -1;
    while (val == -1) {
        val = step(&st);
    }
    free(fstack);
    free(prog);
    if (val == 0) {
        FILE *f;
        f = fopen("flag.txt", "r");
        if (f == NULL) {
            puts("Couldn't open flag file.");
            die();
        }
        char flag[128];
        if (fgets(flag, sizeof(flag), f) == NULL) {
            puts("Couldn't read flag file.");
            die();
        }
        fclose(f);
        puts(flag);
    }
    return val;
}
