#include <stdlib.h>
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <opencv2/imgproc/imgproc.hpp>
#include <fstream>
#include <sstream>
#include <string>
#include <stdio.h>
#include <iostream> 

using namespace cv;
using namespace std;

bool selectObject = false;
bool drawing_selection = false;
Rect selection;
Mat frame;
int k = 0;

void draw_selection(Mat &image, Rect car_rect )
{
		rectangle( 	image,
					Point(car_rect.x, car_rect.y),
					Point(car_rect.x+car_rect.width,car_rect.y+car_rect.height),
                    Scalar(0x00,0x00,0xff)
                 	);
}
static void onMouse( int event, int x, int y, int, void* )
{
    switch( event ){
		case CV_EVENT_MOUSEMOVE:
			if( drawing_selection )
			{
				selection.width = x-selection.x;
				selection.height = y-selection.y;
			}
			break;

		case CV_EVENT_LBUTTONDOWN:
			drawing_selection = true;
			selection = Rect(x, y, 0, 0);
			break;

		case CV_EVENT_LBUTTONUP:
			drawing_selection = false;
			if( selection.width < 0 )
			{
				selection.x += selection.width;
				selection.width *= -1;
			}

			if( selection.height < 0 )
			{
				selection.y += selection.height;
				selection.height *= -1;
			}
			draw_selection(frame, selection);
			k = 1;
			break;
	}
}


int main(int argc, char** argv)
{
	VideoCapture cap(argv[1]);/*"/home/mahdi/Videos/robotic/test_video.avi"*/
	int framenum = 0;
	
	Mat temp;

	// string output_file = "final_sharifcup_tags.txt";
	// ofstream output(output_file.c_str());
	ofstream output(argv[2]);

	string name = "selection Example__";
	selection = Rect(-1, -1, 0, 0);
	namedWindow(name);

	for(;;)
	{
		cap >> frame;
        if( frame.empty() )
            break;
        framenum++;
        temp = frame.clone();
        imshow(name, frame);

        setMouseCallback( name, onMouse, 0);

        while( 1 )
        {

			frame.copyTo(temp);
			if( drawing_selection /*|| true*/ )
				draw_selection(temp, selection);

			if (k == 1)
			{
				k = 0;

				output << framenum << ","
				<< selection.x << "," 
				<< selection.y << ","
				<< selection.x + selection.width <<","
				<< selection.y + selection.height << endl;
				
				std::cout << framenum << " "
				<< selection.x << " " 
				<< selection.y << " "
				<< selection.x + selection.width <<" "
				<< selection.y + selection.height << endl;
			}

			imshow(name, temp);

			if( waitKey( 1 ) == 'f' )
			{
				std::cout << "New Frame: " << framenum << endl;
				break;
			}
			
		}
	}

	return 0;
}