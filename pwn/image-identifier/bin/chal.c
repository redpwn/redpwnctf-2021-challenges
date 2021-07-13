#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <stdint.h>


char bmpHead[] = {0x42, 0x4d};
char pngHead[] = {137, 80, 78, 71, 13, 10, 26, 10};

char end[] = {0x49, 0x45, 0x4e, 0x44};

int ended = 0;

int offset = 0;

struct validations
{
    int (*header)(char *, int);
    char *(*chunk)(char *, int);
    char *(*footer)(char *);
};

uint32_t crc_table[256];

void make_crc_table()
{
    uint32_t c;

    for (int n = 0; n < 256; n++)
    {
        c = (uint8_t)n;
        for (int k = 0; k < 8; k++)
        {
            if ((c & 1) == 1)
                c = 0xedb88320 ^ (c >> 1);
            else
                c = c >> 1;
        }
        crc_table[n] = c;
    }
}

uint32_t update_crc(char *buf, int bufLen)
{
    uint32_t c = 0xffffffff;
    for (int n = 0; n < bufLen; n++)
    {
        c = crc_table[(c ^ *buf) & 0xff] ^ (c >> 8);
        buf++;
    }
    return c ^ 0xffffffff;
}

int bmpHeadValidate(char *f, int size)
{
    int fsize = f[3] | (f[4] << 8) | (f[5] << 16) | (f[6] << 24);
    if (size != fsize)
    {
        puts("invalid size!");
        exit(1);
    }
}

char *bmpChunkValidate(char *f, int invert)
{
    puts("to be implemented");
    exit(1);
}

int pngHeadValidate(char *f, int size)
{
    f += 8;
    offset += 8;
    int fsize = f[3];
    if (fsize != 0x0d)
    {
        puts("bad header");
        return 1;
    }
    f += 4;
    offset += 4;
    uint32_t checksum = update_crc(f, fsize + 4);
    f += fsize + 4;
    offset += fsize + 8;
    uint32_t check = (f[3] & 0xff) | ((f[2] & 0xff) << 8) | ((f[1] & 0xff) << 16) | ((f[0] & 0xff) << 24);
    if (checksum != check)
    {
        puts("invalid checksum!");
        return 1;
    }
    return 0;
}

char *pngChunkValidate(char *f, int invert)
{
    uint32_t len = (f[3] & 0xff) | ((f[2] & 0xff) << 8) | ((f[1] & 0xff) << 16) | ((f[0] & 0xff) << 24);
    len += 4;
    f += 4;
    if (memcmp(f, end, 4) == 0)
    {
        ended = 1;
        return ((char *)f - 4);
    }
    if (invert == 1)
    {
        f += 4;
        for (int i = 0; i < len - 4; i++)
        {
            f[i] = ~f[i];
        }
        f -= 4;
        int x = update_crc(f, len);
        f += len;
        *(uint16_t *)(f) = (uint16_t)x;
        return ((char *)f + 4);
    }
    int checksum = update_crc(f, len);
    f += len;
    uint32_t check = (f[3] & 0xff) | ((f[2] & 0xff) << 8) | ((f[1] & 0xff) << 16) | ((f[0] & 0xff) << 24);
    if (check != checksum)
    {
        puts("bad chunk");
    }
    return ((char *)f + 4);
}

char *pngFooterValidate(char *f)
{
    uint32_t len = (f[3] & 0xff) | ((f[2] & 0xff) << 8) | ((f[1] & 0xff) << 16) | ((f[0] & 0xff) << 24);
    f += 4;
    len += 4;
    int checksum = update_crc(f, len);
    f += len;
    uint32_t check = (f[3] & 0xff) | ((f[2] & 0xff) << 8) | ((f[1] & 0xff) << 16) | ((f[0] & 0xff) << 24);
    if (check != checksum)
    {
        puts("bad chunk");
        exit(1);
    }
    return ((char *)f + 4);
}

char *bmpFooterValidate(char *f)
{
    puts("to be implemented");
    exit(1);
}

int validateHeader(char *head)
{
    if (memcmp(head, bmpHead, 2) == 0)
    {
        return 1;
    }
    else if (memcmp(head, pngHead, 8) == 0)
    {
        return 2;
    }
    return 0;
}

int win()
{
    system("/bin/sh");
}

int main(void)
{
      setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);
    puts("welcome to the image identifier service\n");
    puts("How large is your file?\n");
    int len;
    if (scanf("%d", &len) != 1)
    {
        puts("invalid file size");
    }
    char *f = malloc(len);
    struct validations *handler;
    getchar();
    handler = malloc(sizeof(struct validations));
    puts("please send your image here:\n");
    fread(f, len, 1, stdin);
    int type = validateHeader(f);
    switch (type)
    {
    case 1:
        handler->header = bmpHeadValidate;
        handler->chunk = bmpChunkValidate;
        handler->footer = bmpFooterValidate;
        break;

    case 2:
        handler->header = pngHeadValidate;
        handler->chunk = pngChunkValidate;
        handler->footer = pngFooterValidate;
        break;

    default:
        puts("unidentifiable format");
        exit(1);
    }

    make_crc_table();
    if (handler->header(f, len) == 0)
    {
        puts("valid header, processing chunks");
    }
    else
    {
        exit(1);
    }
    f += offset;
    char yes;
    int invert = 0;
    puts("do you want to invert the colors?");
    if (scanf("%c", &yes) == 1)
    {
        if (yes == 'y')
        {
            invert = 1;
        }
    }
    while (ended == 0 && ((long)f) < ((long)handler))
    {
        f = handler->chunk(f, invert);
    }
    handler->footer(f);
    puts("congrats this is a great picture");
}
