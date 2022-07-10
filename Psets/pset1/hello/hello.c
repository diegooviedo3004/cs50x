#include<stdio.h>
#include<cs50.h>

int main(void)
{
    string name = get_string("cual es tu nombre?: ");
    printf("hello %s \n",name);
}