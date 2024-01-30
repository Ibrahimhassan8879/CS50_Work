#include <cs50.h>
#include <stdio.h>
#include "string.h"
#include "ctype.h"
#include<math.h>

//Functions Prototypes
float count_sentences(string plain_text, int Y);
float count_words(string plain_text, int Y);
float count_letters(string plain_text, int Y);

//Main Function

int main(void)
{
    string plain_text = get_string("Text : ");
    int Y = strlen(plain_text);

    float u = count_letters(plain_text, Y);
    float o = count_words(plain_text, Y);
    float p = count_sentences(plain_text, Y);
    float L = u * 100 / o;
    float S = p * 100 / o;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    printf("letters %f words %f sentence %f", count_letters(plain_text, Y), count_words(plain_text, Y), count_sentences(plain_text, Y));
    int Grade = round(index);
    if (Grade > 16)
    {
        printf("Grade 16+\n");
        return 0;
    }
    else if (Grade < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }
    else
    {
        printf("Grade %i\n", Grade);
        return 0;
    }


}

//Calculate Letters
float count_letters(string plain_text, int Y)
{
    int letters = 0;
    for (int i = 0 ; i < Y ; i++)
    {
        if (islower(plain_text[i]) != 0)
        {
            letters++;
        }
        else if (isupper(plain_text[i]) != 0)
        {
            letters++;
        }

    }
    return letters;
}

//Calculate Words
float count_words(string plain_text, int Y)
{
    int words = 1;
    char space = ' ';
    for (int i = 0 ; i < Y ; i++)
    {
        if (space == plain_text[i])
        {
            words++;
        }
    }
    return words;
}

//Calculate Sentences
float count_sentences(string plain_text, int Y)
{
    int sentence = 0;
    for (int i = 0 ; i < Y ; i++)
    {
        if (plain_text[i] == '!' || plain_text[i] == '?' || plain_text[i] == '.')
        {
            sentence++;
        }
    }
    return sentence;
}