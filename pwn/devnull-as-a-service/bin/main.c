#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

const char *title = "    __  _             __           _ _ \n"
                    "   / /_| | _____   __/ / __  _   _| | |\n"
                    "  / / _` |/ _ \\ \\ / / / '_ \\| | | | | |\n"
                    " / / (_| |  __/\\ V / /| | | | |_| | | |\n"
                    "/_/ \\__,_|\\___| \\_/_/ |_| |_|\\__,_|_|_|\n"
                    "        as a service                   \n";

typedef struct
{
    char data[96];
    char id[32];
} Packet;

int input(char *buf)
{
    fgets(buf, sizeof(Packet), stdin);
    buf[strcspn(buf, "\n")] = 0;
    return 0;
}

int fetch_data(Packet *p)
{
    puts("Send data:");
    input(p->data);
    puts("Customer ID:");
    input(p->id);
    return 0;
}

int main()
{
    Packet p;

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts(title);
    fetch_data(&p);
    puts("Thank, you processing now!");
    memset(&p, 0, sizeof(Packet));

    if (close(STDOUT_FILENO) != 0 || close(STDERR_FILENO) != 0)
        _exit(EXIT_FAILURE);
    return 0;
}
