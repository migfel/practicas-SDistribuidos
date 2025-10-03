// client.c
#include <stdio.h>
#include <stdlib.h>
#include "rand.h"

static void rand_prog_1(const char *host, long seed, int iters)
{
    CLIENT *clnt = clnt_create(host, RAND_PROG, RAND_VERS, "udp");
    if (!clnt) { clnt_pcreateerror(host); exit(1); }

    if (inicializa_random_1(&seed, clnt) == (void *)NULL) {
        clnt_perror(clnt, "call failed (inicializa_random_1)");
        clnt_destroy(clnt);
        exit(1);
    }
    printf("Semilla inicializada: %ld\n", seed);

    for (int i = 0; i < iters; i++) {
        double *r = obtiene_siguiente_random_1(NULL, clnt); // sin argumentos
        if (!r) {
            clnt_perror(clnt, "call failed (obtiene_siguiente_random_1)");
            clnt_destroy(clnt);
            exit(1);
        }
        printf("Iter %2d: %f\n", i+1, *r);
    }

    clnt_destroy(clnt);
}

int main(int argc, char *argv[])
{
    if (argc < 4) {
        fprintf(stderr, "Uso: %s <host> <seed> <iters>\n", argv[0]);
        return 1;
    }
    const char *host = argv[1];
    long seed = strtol(argv[2], NULL, 10);
    int iters = atoi(argv[3]);
    if (iters <= 0) iters = 1;

    rand_prog_1(host, seed, iters);
    return 0;
}

