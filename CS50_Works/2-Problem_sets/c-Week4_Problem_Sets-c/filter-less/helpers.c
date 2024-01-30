#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
//Check over image height
    for (int i = 0 ; i < height ; i++)
    {
//Check over image width
        for (int j = 0 ; j < width ; j++)
        {
            int New_grey_pixel = round((image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3.0);

            image[i][j].rgbtBlue = New_grey_pixel;
            image[i][j].rgbtRed = New_grey_pixel;
            image[i][j].rgbtGreen = New_grey_pixel;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{

//Check over image height
    for (int i = 0 ; i < height ; i++)
    {
//Check over image width
        for (int j = 0 ; j < width ; j++)
        {

            int sepia_r = round((0.393 * image[i][j].rgbtRed) + (0.769 * image[i][j].rgbtGreen) + (0.189 * image[i][j].rgbtBlue));
            int sepia_g = round((0.349 * image[i][j].rgbtRed) + (0.686 * image[i][j].rgbtGreen) + (0.168 * image[i][j].rgbtBlue));
            int sepia_b = round((0.272 * image[i][j].rgbtRed) + (0.534 * image[i][j].rgbtGreen) + (0.131 * image[i][j].rgbtBlue));

            if (sepia_r > 0xff)
            {
                sepia_r = 0xff;
            }

            if (sepia_g > 0xff)
            {
                sepia_g = 0xff;
            }

            if (sepia_b > 0xff)
            {
                sepia_b = 0xff;
            }

            image[i][j].rgbtBlue  =   sepia_b;
            image[i][j].rgbtRed   =   sepia_r;
            image[i][j].rgbtGreen =   sepia_g;
        }


    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
//Itrating over the height
    for (int k = 0; k < height; k++)
    {
//Check even width
        if (width % 2 != 0)
        {
            for (int u = 0; u < (width - 1) / 2; u++)
            {
                RGBTRIPLE temp[height][width];
                temp[k][u] = image[k][u];
                image[k][u] = image[k][width - (u + 1)];
                image[k][width - (u + 1)] = temp[k][u];
            }
        }
//Check Odd width
        else if (width % 2 == 0)
        {
            for (int u = 0; u < width / 2; u++)
            {
                RGBTRIPLE temp[height][width];
                temp[k][u] = image[k][u];
                image[k][u] = image[k][width - (u + 1)];
                image[k][width - (u + 1)] = temp[k][u];
            }
        }
    }
    return;
}




// Blur images
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
//Check over image height
    for (int k = 0; k < height; k++)
    {
//Check over image width
        for (int u = 0; u < width; u++)
        {

            float countRed = 0;
            float countGreen = 0;
            float countBlue = 0;
            float counter = 0;

            for (int r = -1; r < 2; r++)
            {
                for (int c = -1; c < 2; c++)
                {
                    if (k + r < 0 || k + r > height - 1)
                    {
                        continue;
                    }

                    if (u + c < 0 || u + c > width - 1)
                    {
                        continue;
                    }

                    countGreen = image[k + r][u + c].rgbtGreen + countGreen ;
                    countRed = image[k + r][u + c].rgbtRed + countRed;
                    countBlue = image[k + r][u + c].rgbtBlue + countBlue;

                    counter++;
                }
            }

            temp[k][u].rgbtBlue = round(countBlue / counter);
            temp[k][u].rgbtGreen = round(countGreen / counter);
            temp[k][u].rgbtRed = round(countRed / counter);
        }
    }

    for (int k = 0; k < height; k++)
    {
        for (int u = 0; u< width; u++)
        {
            image[k][u].rgbtRed = temp[k][u].rgbtRed;
            image[k][u].rgbtGreen = temp[k][u].rgbtGreen;
            image[k][u].rgbtBlue = temp[k][u].rgbtBlue;
        }

    }

    return;
}