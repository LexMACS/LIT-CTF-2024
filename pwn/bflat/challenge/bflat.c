#include <stdio.h>
#include <stdlib.h>

int cmp_int(const void *a, const void *b)
{
    int arg1 = *(const int*)a;
    int arg2 = *(const int*)b;

    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

int cmp_int_rev(const void *a, const void *b){
  return cmp_int(b, a);
}

const int (*cmps[2])() = {cmp_int, cmp_int_rev};

int main(){
  setbuf(stdin, 0);
  setbuf(stdout, 0);

  int n, type;
  int *a;

  puts("How to raise a boring vuln (flat).\n");

  puts("How many ints?");
  scanf("%d", &n);

  a = malloc(n * sizeof(int));

  puts("Input ints (separate by space):");
  for(int i = 0; i < n; i++) scanf("%d", &a[i]);

  puts("Input sort type (1 = forward, 2 = reverse):");
  scanf("%d", &type);

  qsort(a, n, sizeof(int), cmps[type - 1]);

  puts("Sorted array:");
  for(int i = 0; i < n; i++) printf("%d ", a[i]);
  puts("\n");

  puts("Bye.");

  return 0;
}
