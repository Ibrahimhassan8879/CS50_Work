#include <stdio.h>
#include "cs50.h"
#include "stdint.h"
#include "stdlib.h"

//Define the byte data type
typedef uint8_t BYTE;

//Main function
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *Recovered_file = NULL;
    BYTE buffer[512];
    FILE *Recovery_file = fopen(argv[1], "r");
    char filename[8] = {0};
    int jpeg = 0;

//Check the recovery file
    if (Recovery_file == NULL)
    {
        printf("Empty File\n");
        return 2;
    }

//Read every 512 BYTE of the file
    while (fread(buffer, sizeof(BYTE), 512, Recovery_file) == 512)
    {
//Found jpeg header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
//Check if the previous file if still opened
            if (Recovered_file != NULL)
            {
                fclose(Recovered_file);
            }
//Open new file
            sprintf(filename, "%0.03d.jpg", jpeg++);
            Recovered_file = fopen(filename, "w");

        }

//Write on new file
        if (Recovered_file != NULL)
        {
            fwrite(buffer, sizeof(BYTE), 512, Recovered_file);
        }

    }

//Closing the last file
    if (Recovered_file != NULL)
    {
        fclose(Recovered_file);
    }

    fclose(Recovery_file);
    return 0;
}
