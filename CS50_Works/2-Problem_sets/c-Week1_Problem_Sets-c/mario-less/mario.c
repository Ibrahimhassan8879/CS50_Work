#include <stdio.h>
#include "cs50.h"
#include <math.h>

int main(void)

{
    int j;
    do
    {
        j = get_int(" Pryamid Height ?");
        // getting user prymid height//
    }
    while (j < 1 || j > 8);

    if (j >= 1 && j <= 8)

        for (int i = 0 ; i < j ; i++)
        {

            for (int l = j - 1 ; l > i ; l--)

            {

                printf(" ");

            }

            for (int k = -1 ; k < i ; k++)
            {

                printf("#");

            }

            printf("\n");

        }

}