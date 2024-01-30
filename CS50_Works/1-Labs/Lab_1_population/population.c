#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int k;
    do
    {
        k = get_int("Start size: \n");
    }
    while (k < 9);

    // TODO: Prompt for end size
    int i;
    do
    {
        i = get_int("End size: \n");
    }
    while (i < k);

    // TODO: Calculate number of years until we reach threshold
    int years = 0;
    while (k < i)
    {
        k = k + (k / 3) - (k / 4);
        years++;
    }
    // TODO: Print number of years
    printf("Years: %d\n", years);
}
