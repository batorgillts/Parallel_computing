#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

int main(int argc, char *argv[])
{
    if (argc != 4) {
        printf("Usage: ./genprimes M N t\n");
        return 1;
    }

    long M = atol(argv[1]);
    long N = atol(argv[2]);
    int  t = atoi(argv[3]);

    long range = N - M + 1;

    /* Allocate a flat boolean array: is_prime[i] == 1  =>  (M + i) is prime */
    int *is_prime = (int *)calloc(range, sizeof(int));
    if (!is_prime) {
        printf("Error allocating memory\n");
        return 1;
    }

    double tstart = 0.0, ttaken;

    tstart = omp_get_wtime();

    /* --- parallel prime-generation section -------------------------------- */
    #pragma omp parallel num_threads(t)
    {
        #pragma omp for schedule(dynamic)
        for (long x = M; x <= N; x++) {
            int prime = 1;
            long sq = (long)floor(sqrt((double)x));
            for (long d = 2; d <= sq; d++) {
                if (x % d == 0) {
                    prime = 0;
                    break;          /* early-exit optimisation */
                }
            }
            is_prime[x - M] = prime;
        }
        #pragma omp barrier         /* explicit barrier as required */
    }
    /* ---------------------------------------------------------------------- */

    ttaken = omp_get_wtime() - tstart;

    /* Count primes */
    long count = 0;
    for (long i = 0; i < range; i++)
        if (is_prime[i]) count++;

    printf("The number of prime numbers found from %ld to %ld is %ld\n", M, N, count);
    printf("Time taken for the main part: %lf seconds\n", ttaken);

    /* Write N.txt — primes in ascending order, one per line */
    char filename[64];
    snprintf(filename, sizeof(filename), "%ld.txt", N);
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        printf("Error opening output file %s\n", filename);
        free(is_prime);
        return 1;
    }
    for (long i = 0; i < range; i++)
        if (is_prime[i])
            fprintf(fp, "%ld\n", M + i);
    fclose(fp);

    free(is_prime);
    return 0;
}
