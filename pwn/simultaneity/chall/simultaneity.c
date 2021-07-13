#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>

int main() {
	int64_t tmp;

	setvbuf(stdout, NULL, _IONBF, 0);

	puts("how big?");
	scanf("%ld", &tmp);
	size_t* buf = malloc(tmp);
	printf("you are here: %p\n", buf);
	puts("how far?");
	scanf("%ld", &tmp);
	puts("what?");
	scanf("%zu", buf + tmp);

	_exit(0);
}
