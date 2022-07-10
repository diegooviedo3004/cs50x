#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO:
    int vi = 0; //vi
    do //retorna si es menor a 9
    {
        vi = get_int("Valor incial: ");
    }
    while (vi < 9);

    // TODO:

    int vf = 0; //vf
    do //retorna si es negativo
    {
        vf = get_int("Valor Final: ");
    }
    while (vi > vf);

    // TODO: Calculate number of years until we reach threshold



    int y= 0;

    if(vi == vf){
        y = 0;
        vi = vi + (vi / 3) - (vi / 4);
    }
    else{
        do{
            vi = vi + (vi / 3) - (vi / 4);
            y++;
        }while(vi < vf);
    }




    // TODO: Print number of years

    printf("Years: %i",y);

    return 0;
}