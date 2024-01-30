#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

//Function Prototype
char rotate(char letter, int key);

//Main Function
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        char k = argv[1][i];
        if (!isdigit(k))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    if (roundf(atoi(argv[1])) != atoi(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 4;
    }

    int key = atoi(argv[1]);
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0 ; i < strlen(plaintext) ; i++)
    {
        char letter = plaintext[i];
        rotate(letter, key);
        char p = rotate(letter, key);
        printf("%c", p);
    }
    printf("\n");
    return 0;
}

char rotate(char letter, int key)
{
    if (letter >= 'A' &&  letter <= 'Z')
    {
        char letter_r = ((letter - 65 + key) % 26) + 65;
        return letter_r;
    }
    else if (letter >= 'a' && letter <= 'z')
    {
        char letter_r = ((letter - 97 + key) % 26) + 97;
        return letter_r;
    }
    char letter_r = letter;
    return letter_r;
    return 0;
}

