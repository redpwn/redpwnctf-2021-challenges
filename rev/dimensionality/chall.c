#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include "chall.h"


typedef struct {
	uint8_t s[0x100];
	uint8_t i;
	uint8_t j;
} rc4_state_t;

void rc4_init(rc4_state_t* state, const void* keybuf, size_t keylen) {
	const uint8_t* keybuf_ = keybuf;
	for (int i = 0; i < 0x100; ++i) {
		state->s[i] = i;
	}
	uint8_t j = 0;
	for (int i = 0; i < 0x100; ++i) {
		uint8_t vi = state->s[i];
		j += vi + keybuf_[i % keylen];
		state->s[i] = state->s[j];
		state->s[j] = vi;
	}
    state->i = state->j = 0;
}

uint8_t rc4_byte(rc4_state_t* state) {
	state->i += 1;
	uint8_t vi = state->s[state->i];
	state->j += vi;
	uint8_t vj = state->s[state->i] = state->s[state->j];
	state->s[state->j] = vi;
	return state->s[(vi + vj) & 0xff];
}

// flag{star_/_so_bright_/_car_/_site_-ppsu}
uint8_t flag_crypt[] = {0x93, 0x8a, 0x88, 0xce, 0x73, 0x81, 0xf0, 0x73, 0x8a, 0x7b, 0x42, 0xea, 0xb4, 0x8c, 0x47, 0x35, 0xcf, 0x0e, 0xc6, 0xdc, 0xef, 0x05, 0xc7, 0x0d, 0x31, 0x1b, 0x74, 0x42, 0xa8, 0xc0, 0x27, 0x4e, 0x9e, 0x01, 0xc0, 0xca, 0x72, 0x27, 0xe3, 0xfb, 0x9a};

int main() {
    char input[29];
    fgets(input, sizeof(input), stdin);
    if (!check_flag(input)) {
        puts(":(");
        return 1;
    }
    puts(":)");
    rc4_state_t st;
    rc4_init(&st, input, sizeof(input) - 1);
    for (uint8_t i = 0; i < sizeof(flag_crypt); i++) {
        flag_crypt[i] ^= rc4_byte(&st);
    }
    fwrite(flag_crypt, 1, sizeof(flag_crypt), stdout);
    putchar('\n');
    return 0;
}

bool check_flag(char string[]) {
    int p;
    for (int i = 0; i < size*size*size; i++) {
        if (maze[i] == 2) {
            p = i;
            break;
        }
    }
    int direc = size*size;
    int i = 0;
    while (string[i]) {
        switch (string[i]) {
            case 'u':
                direc = -size;
                break;
            case 'd':
                direc = size;
                break;
            case 'f':
                direc = size*size;
                break;
            case 'b':
                direc = -(size*size);
                break;
            case 'r':
                direc = 1;
                break;
            case 'l':
                direc = -1;
                break;
        }
        p += direc;
        if (p < 0 || p > size*size*size) {
            return false;
        }
        if (maze[p] == 0) {
            return false;
        }
        ++i;
    }
    if (maze[p] == 3) {
        return true;
    }
    return false;
}
