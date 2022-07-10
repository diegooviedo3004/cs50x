#include<stdio.h>
#include<stdlib.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>
#include<strings.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        int n = strlen(argv[1]);
        int i = 0;

        //ciclo para que detecte solo letras

        for (int l = 0; l < n; l++)
        {
            if (!isdigit(argv[1][l]))
            {
                printf("xd");
                return 1;
            }
        }
        int k = atoi(argv[1]);

        //texto en string(podia haber sido char creo) por si acaso xd

        string text = get_string("plain text: ");
        printf("ciphertext: ");
        int t = strlen(text);

        //Formulas uwu con ciclo para que detecte mayusculas y minusculas

        for (int l = 0; l < t; l++)
        {
            if (isupper(text[l]))
            {
                //may
                printf("%c", (((text[l] - 'A') + k) % 26) + 'A');
            }
            else if (islower(text[l]))
            {
                //min
                printf("%c", (((text[l] - 'a') + k) % 26) + 'a');
            }
            else
            {
                //por si no es ninguno
                printf("%c", text[l]);
            }
        }
    }
    else
    {
        printf("xd");
        return 1;
    }

    //salida
    printf("\n");
    return 0;
}