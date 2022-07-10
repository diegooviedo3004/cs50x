

#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>


//representa el byte a byte
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr,"holi");
        return 1;
    }

    //se abre el archivo
    FILE *file = fopen(argv[1], "r");

    //si no encuentra el archivo pues F
    if (file == NULL)
    {
        //aqui el habia puesto argv[1] pero mandaba error,lo quite y todo bien xD
        fprintf(stderr, "no abrio F");
        return 2;
    }

    //puntero de salida
    FILE* outptr = NULL;

    //tamaño de la memory card
    BYTE buffer[512];

    //variable contadora asies c:
    int imagen = 0;

    //cadena para contener nombres de archivos// //nom file ;u
    char nomfile[8] = {0};

    //lee la memory card
    while(fread(buffer, sizeof(BYTE)*512,1,file))
    {
        //las primeras 3 bytes de un jpeg
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3]&0xf0)==0xe0)
        {
            //si es diferente de null significa que encontró algo
            if(outptr != NULL)
            {
                fclose(outptr);
            }

            sprintf(nomfile,"%03d.jpg",imagen++);

            //se abre otro para la siguiente imagen

            outptr = fopen(nomfile,"w");
        }
        //si no encuentra mas sigue
        if(outptr != NULL)
        {
            fwrite(buffer,sizeof(BYTE)*512,1,outptr);
        }
    }

    //cerramos
    if(outptr != NULL)
    {
        fclose(outptr);
    }


    //cerramos y a mimir
    fclose(file);

    return 0;
}