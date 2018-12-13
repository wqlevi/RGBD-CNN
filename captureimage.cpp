**********************************************************************
#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv.hpp>
#include <iostream>
#include <vector>
#include <stdio.h>
 
 
using namespace cv;
using namespace std;
 
 
int process(VideoCapture& capture)
{
	int n = 0;
	char filename[200];
	string window_name = "video | q or esc to quit";
 
	std::cout << "按下【Space】空格键可以截图" << std::endl;
	std::cout <<"【Esc】和【q】键 - 退出程序"  << endl;
 
	namedWindow(window_name, CV_WINDOW_KEEPRATIO); //resizable window;
	cv::Mat frame;
	for (;;)
	{
		capture >> frame;
		if (frame.empty())break;
 
		cv::Mat gray;
		cv::cvtColor(frame, gray, COLOR_RGB2GRAY);
 
		std::vector<string> codes;
		cv::Mat corners;
		cv::imshow(window_name, frame);
 
		char key = (char)waitKey(1); 
 
		switch (key)
		{
		case 'q':
		case 'Q':
		case 27:                                                 //[1]escape key
			return 0;
		case ' ':                                                //[2]Save an image
			sprintf(filename, "D:\\OpenCvDemo\\VideoScreen\\VideoScreen\\screenImg\\%.3d.png", n++);
			imwrite(filename, frame);
			cout << "\n\t>保存了 " << filename << "文件到工程目录下" << endl;
			break;
		default:
			break;
		}
	}
	return 0;
}
int main(int argc,char** argv)
{
 
	VideoCapture capture("D:\\MSR_original\\MSR_original\\Img\\03.mpeg"); //从文件载入视频
	//VideoCapture capture(0); //从摄像头载入视频
	if (!capture.isOpened())
	{
		std::cerr << "Failed to open a video device or video file!\n" << endl;
		return 1;
	}
 
	return process(capture);
}
