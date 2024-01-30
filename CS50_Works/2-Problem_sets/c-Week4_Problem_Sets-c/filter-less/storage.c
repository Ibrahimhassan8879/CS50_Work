#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
for ( int i = 0 ; i < height ; i++)
{
    for ( int j = 0 ; j < width ; j++)
    {
        int New_grey_pixel = round(( image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen )/3);

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


for ( int i = 0 ; i < height ; i++)
{
    for ( int j = 0 ; j < width ; j++)
    {

int sepia_r = round(( 2*image[i][j].rgbtRed) + ( 2*image[i][j].rgbtGreen) + (2*image[i][j].rgbtBlue));
int sepia_g = round(( 0.349*image[i][j].rgbtRed) + ( 0.686*image[i][j].rgbtGreen) + (0.168*image[i][j].rgbtBlue));
int sepia_b = round(( 0.272*image[i][j].rgbtRed) + ( 0.534*image[i][j].rgbtGreen) + (0.131*image[i][j].rgbtBlue));

if ( sepia_r > 0xff)
{
    sepia_r = 0xff;
}

if ( sepia_g > 0xff)
{
   sepia_g = 0xff;
}

if ( sepia_b > 0xff)
{
   sepia_b = 0xff;
}

image[i][j].rgbtBlue  =   sepia_b;
image[i][j].rgbtRed   =   sepia_r;
image[i][j].rgbtGreen =   sepia_g;





    }

    return;
}
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    {
for ( int i = 0 ; i < height ; i++)
{
    for ( int j = 0 ; j < width ; j++)
    {
int left_pixel_r;
int right_pixel_r;
int left_pixel_g;
int right_pixel_g;
int left_pixel_b;
int right_pixel_b;

left_pixel_r  =   image[i][j].rgbtRed;
right_pixel_r =  image[i][width - j].rgbtRed;

left_pixel_g  =   image[i][j].rgbtGreen;
right_pixel_g =  image[i][width - j].rgbtGreen;

left_pixel_b  =   image[i][j].rgbtBlue;
right_pixel_b =  image[i][width - j].rgbtBlue;

        swap ( &left_pixel_r ,  &right_pixel_r );
        swap ( &left_pixel_g ,  &right_pixel_g );
        swap ( &left_pixel_b ,  &right_pixel_b );

    }


    }


}
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
