#include <cs50.h>
#include <stdio.h>

int main(void)
{
  int n = 0;

    do
    {
        n = get_int("height: ");
    }
    while (n < 1 || n > 8);

    for (int i = 0; i < n; i++)
    {
        for (int j = n - i; j > 1; j--)
        {
            printf(" ");
        }
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }

    return 0;
}