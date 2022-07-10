// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;
int countWord = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    /*node *cursor = table[N]
    while(cursor != NULL)
    {
        cursor = cursor->siguiente;
    }*/

    int hashNum = hash(word);
    // create cursor variable
    node *cursor = table[hashNum];

    while (cursor != NULL)
    {
        //check if the words are the same
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        // otherwise move cursor to the next node
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    /*int suma = 0;
    for(int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }
    return (sum % N);*/

    /*int hash =toupper(word[0]) - 'A';*/

    //return hash % N;
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODOr
    /*FILE *file = fopen(dictionary, "r'");
    if (file == NULL)
    {
    return false;
    }

    char word[LENGTH + 1];
    while (fscanf(file, "word") != EQF)
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }

        strcpy(n->word, word);
        nex_node->next - NULL;

        int index = hash(word);
        if(table[index] == NULL);
        {
            table[index = new_node];
        }
        else
        {
            new_node->next = table[index];
            table[index] = new_node;
        }
    }*/

    FILE *DictFile = fopen(dictionary, "r");

    if (DictFile == NULL)
    {
        return false;
    }

    //fscanf(file, '%s', word)
    char str[LENGTH + 1];
    while (fscanf(DictFile, "%s", str) != EOF)
    {
        // se crea un nuevo nodo para word
        // usasr malloc
        node *temp = malloc(sizeof(node));

        // check if return value is NULL
        if (temp == NULL)
        {
            return false;
        }
        //copy word into node using strcpy
        strcpy(temp->word, str);

        //use la funcion de hash
        int hashNum = hash(str);

        //check if the head is pointing to NULL
        if (table[hashNum] == NULL)
        {
            // point temp to NULL
            temp->next = NULL;
        }
        else
        {
            // otherwise, point temp to the first node of the limked list
            temp->next = table[hashNum];
        }
        // point the header to temp
        table[hashNum] = temp;

        countWord += 1;
    }
    //close the file
    fclose(DictFile);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return countWord;
}

void freenode(node *n)
{
    if (n->next != NULL)
    {
        freenode(n->next);
    }
    free(n);
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            freenode(table[i]);
        }
    }
    return true;
}
