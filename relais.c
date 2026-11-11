#include <stdio.h>
#include <string.h>
int main(void) {
    char l[8192];
    if (!fgets(l, sizeof l, stdin)) return 1;
    l[strcspn(l, "\r\n")] = 0;
    char *t = strchr(l, '\t');
    if (!t) return 1;
    *t = 0;
    printf("%s\t%s>C\n", l, t + 1);
    return 0;
}
