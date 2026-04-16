# Parallel_computing
# OpenMP Prime Number Generator

**Course:** Parallel Computing

## Overview

This program generates all prime numbers in the range `[M, N]` using multithreaded parallelism with OpenMP. It reports the count of primes found, the time taken for the parallel computation, and writes the primes to an output file.

## Algorithm

For each integer `x` in `[M, N]`:
- Check divisibility by every integer from `2` to `floor(sqrt(x))`
- If no divisor is found, `x` is prime
- **Early-exit optimization:** stop checking as soon as a divisor is found

The outer loop is parallelized across `t` threads using `schedule(dynamic)` to handle load imbalance (larger numbers require more divisor checks).

## Compilation

```bash
gcc -Wall -O3 -std=c99 -fopenmp -o genprimes genprimes.c -lm
