int main()  
{  
    CvCapture *capture = NULL;  
    IplImage *frame = NULL;  
    char *AviFileName = "D:\\clock.avi";//视频的目录  
    char *AviSavePath = "D:\\截图\\";//图片保存的位置  
    const int jiange = 2;//间隔两帧保存一次图片  
    capture = cvCaptureFromAVI(AviFileName);  
    cvNamedWindow("AVI player",1);  
    int count_tmp = 0;//计数总帧数  
    char tmpfile[100]={'\0'};  
    while(true)  
    {  
        if(cvGrabFrame(capture))  
        {  
            if (count_tmp % jiange == 0)  
            {  
                frame=cvRetrieveFrame(capture);  
                cvShowImage("AVI player",frame);//显示当前帧  
                sprintf(tmpfile,"%s//%d.jpg",AviSavePath,count_tmp);//使用帧号作为图片名  
                cvSaveImage(tmpfile,frame);  
            }                 
            if(cvWaitKey(10)>=0) //延时  
                break;  
            ++count_tmp;  
        }  
        else  
        {  
            break;  
        }  
    }  
    cvReleaseCapture(&capture);  
    cvDestroyWindow("AVI player");   
    std::cout<<"总帧数" << count_tmp << std::endl;  
    return 0;  
}  
