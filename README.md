![GitHub repo size](https://img.shields.io/github/repo-size/EriqueSouza/Thermographic-Image)
![GitHub](https://img.shields.io/github/license/EriqueSouza/Thermographic-Image)
![GitHub language count](https://img.shields.io/github/languages/count/EriqueSouza/Thermographic-Image)
![GitHub top language](https://img.shields.io/github/languages/top/EriqueSouza/Thermographic-Image)

# How to classify a thermography image with computer vision

In this project, I try to identify how hot a Formula 1 tire is using a thermal camera.

## Concepts

Thermographic cameras detect radiation in the long-infrared range of the electromagnetic spectrum. Any object with a temperature above absolute zero can emit infrared radiation and we can see it without visible lighting using a thermographic camera. Using this technique, we can detect equipment anomalies before they break.

## Development

I took a video of a lap given by the driver Paul Di Resta in Monza (link below). The team placed a thermographic camera to monitor how his tires are in good temperature to get more grip. 

[![Di Resta lap with Thermographic camera](http://img.youtube.com/vi/bmy4FcMHF7w/0.jpg)](http://www.youtube.com/watch?v=bmy4FcMHF7w "Di Resta Lap")

The hotter the tire, the better its grip. So, based on the color, we can try to define how the tires are warmer. I defined two regions of interest in tires and tracked these ROIs. I calculated histograms on each frame to define how hot or cold the tires are. You can see it in the image below.

![Image With ROIs](https://github.com/EriqueSouza/Thermographic-Image/blob/master/Image.png)

## Built With

[OpenCV](https://opencv.org/) - Library to help develop computer vision applications.
[Numpy](https://numpy.org/) - The fundamental package for scientific computing with Python.

## Author

  •	[Erique Souza](https://github.com/EriqueSouza) 
