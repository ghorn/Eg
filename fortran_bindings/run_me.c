
#include <stdio.h>

#include "blah.h"

int main(){
  int x = 3;
  int y;
  blah_(&x, &y);
  printf("x: %d, y: %d\n", x, y);
  return 0;
}
