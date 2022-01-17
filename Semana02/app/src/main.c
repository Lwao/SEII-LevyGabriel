/**
 * @file main.c
 * @brief 
 *
 * @author Levy Gabriel da S. G.
 * @date January 17 2022
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "foo.h"
#include "bar.h"

int main(int argc,char* argv[])
{
    if(argc==4)
    {
        int op1 = strtol(argv[2], NULL, 10); // STRING,ENDPOINTER,BASE
        int op2 = strtol(argv[3], NULL, 10); // STRING,ENDPOINTER,BASE
        if(strcmp(argv[1],"-sum")==0)
        {
            printf("Result: %d\n\n", sum(op1, op2));
            return 0;
        } 
        else if(strcmp(argv[1],"-sub")==0)
        {
            printf("Result: %d\n\n", sub(op1, op2));
            return 0;    
        } 
        else {printf("Invalid operation!\n\n");}
    } else if(argc>4){printf("Too much arguments!\n\n");}
    else{printf("Not enough arguments!\n\n");}
    return 0;
}