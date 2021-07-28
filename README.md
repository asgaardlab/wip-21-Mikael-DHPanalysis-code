## Docker Image Performance Risk Analysis
This repository contains deployment instructions and configuration files for performance risk analysis approach proposed in the paper titled "Studying the Performance Risks of Upgrading Docker Hub Images: A Case Study of WordPress".
## Config Files
In this folder configuration files for deploying WordPress, MySQL, and Locust are provided. We used Kubernetes as our orchestration platform. 
## Crawler Collected Tags
This compressed file contains all the collected tags for WordPress images. In order to collect the latest Docker image tags there is a need for developing a crawler.
## Load Tester
This code is used to automate the process of deploying different WordPress image tags and measuring the performance metrics during the load test. 
## Data Summary
This excel sheet contains all the image tags that are studied in our paper along with the number of images with specific dependency versions. 
