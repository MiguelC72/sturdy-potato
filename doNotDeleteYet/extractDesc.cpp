#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/xfeatures2d/nonfree.hpp>
//#include <opencv2/persistence.hpp>

using namespace std;
using namespace cv;

int main()
{
	Ptr<Feature2D> f2d = xfeatures2d::SIFT::create();

	//Mat train = imread("kboxNano.jpg"), train_g;
	//open images and read into a matrix
	Mat laptop = imread("laptop.jpg"), laptop_g;
	Mat notebook = imread("notebook.png"), notebook_g;
	Mat pencil = imread("pencil.jpg"), pencil_g;
	Mat printer = imread("printer.jpg"), printer_g;

	//convert images to gray scale
	if(!laptop.empty())
	{
		cvtColor(laptop, laptop_g, CV_BGR2GRAY);
	}
	else
	{
		cout << "laptop image is empty" << endl;
	}

	if(!notebook.empty())
	{
		cvtColor(notebook, notebook_g, CV_BGR2GRAY);
	}
	else
	{
		cout << "notebook image is empty" << endl;
	}

	if(!pencil.empty())
	{
		cvtColor(pencil, pencil_g, CV_BGR2GRAY);
	}
	else
	{
		cout << "pencil image is empty" << endl;
	}
	
	if(!printer.empty())
	{
		cvtColor(printer, printer_g, CV_BGR2GRAY);
	}
	else
	{
		cout << "printer image is empty" << endl;
	}

	//create STL vectors and matrices to hold keypoints and feature descriptors
	vector<KeyPoint> laptop_kp, notebook_kp, pencil_kp, printer_kp;
	Mat laptop_desc, notebook_desc, pencil_desc, printer_desc;

	//detect SIFT keypoint and extract descriptors in the images
	f2d->detect(laptop_g, laptop_kp);
	f2d->compute(laptop_g, laptop_kp, laptop_desc);

	f2d->detect(notebook_g, notebook_kp);
	f2d->compute(notebook_g, notebook_kp, notebook_desc);

	f2d->detect(pencil_g, pencil_kp);
	f2d->compute(pencil_g, pencil_kp, pencil_desc);

	f2d->detect(printer_g, printer_kp);
	f2d->compute(printer_g, printer_kp, printer_desc);

	cout << "Laptop desc matrix" << endl << laptop_desc << endl << endl;

	//write feature descriptors to files
	FileStorage fs1("laptop.xml", FileStorage::WRITE);
	write(fs1, "laptop_desc", laptop_desc);

	FileStorage fs2("notebook.xml", FileStorage::WRITE);
	write(fs2, "notebook_desc", notebook_desc);

	FileStorage fs3("pencil.xml", FileStorage::WRITE);
	write(fs3, "pencil_desc", pencil_desc);

	FileStorage fs4("printer.xml", FileStorage::WRITE);
	write(fs4, "printer_desc", printer_desc);
	
	//close fs objects
	fs1.release();
	fs2.release();
	fs3.release();
	fs4.release();
}
