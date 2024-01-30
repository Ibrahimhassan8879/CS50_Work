// Implements a dictionary's functionality

#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

//Structure node
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

//Global variables
unsigned int hash_total_value;
unsigned int Words_counts;
// TODO: Choose number of buckets in hash table
const unsigned int N_letter = 26;

// Hash table
node *table[N_letter];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    //hashing words
    hash_total_value = hash(word);
    node *word_cursor = table[hash_total_value];

    //while loop for the word_cursor to compare the words in dictionary & text files and return true
    while ( word_cursor != 0)
    {
        if (strcasecmp(word, word_cursor->word) == 0)
        {
            return true;
        }
        word_cursor = word_cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //hashing function
    unsigned long total_letters = 0;
    int word_length = strlen(word);
    for ( int k = 0 ; k < word_length;k++)
    {
        total_letters = tolower(word[k]) + total_letters;
    }
    return total_letters % N_letter;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *Dictionary_file = fopen(dictionary,"r");
    if ( Dictionary_file == NULL)
    {
        printf("Unable to open broken file\n");
        return false;
    }
    char word[LENGTH +1];
    while (fscanf(Dictionary_file, "%s",word) != EOF)
    {
        node *n = malloc(sizeof(node));

        if ( n == NULL)
        {
            return false;
        }
        strcpy(n->word, word);
        hash_total_value = hash(word);
        n-> next = table[hash_total_value];
        table[hash_total_value] = n;
        Words_counts ++;
    }
    fclose(Dictionary_file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (Words_counts > 0)
    {
        return Words_counts;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    //for loop for every letter defined in N
    for ( int j = 0 ; j < N_letter ; j++)
    {
        node *word_cursor = table[j];
        while ( word_cursor)
        {
            node *tmp = word_cursor;
            word_cursor = word_cursor-> next;
            free(tmp);
        }
    }
    return true;
}
