# Project-1: Scalable Image Processing System

![image](https://github.com/user-attachments/assets/2fc02da1-3091-4b37-a96a-daefc42e6e56)


A cloud-native image processing application built on AWS that enables asynchronous image processing at scale. The system leverages a microservices architecture with seamless auto-scaling capabilities.

## Architecture

- **Web Tier**: Frontend controller service that handles client requests and responses
- **Message Queue Layer**: Utilizes Amazon SQS for reliable message handling with separate request and response queues
- **Processing Layer**: Auto-scaling application tier for image processing
- **Storage Layer**: Amazon S3 buckets for persistent storage of original images and processed results

## Key Features

- Asynchronous processing to handle high-volume image operations
- Automatic scaling based on processing demand
- Fault-tolerant design with message queuing
- Decoupled architecture for improved maintainability and scalability
- Persistent storage for both input and processed images

## Tech Stack

- AWS Services: S3, SQS, Auto Scaling
- Web Controller for client interaction
- Containerized application tier for processing

# Project-2: Serverless Video Analysis Pipeline

![image](https://github.com/user-attachments/assets/8fa65f27-6ef2-4d31-9416-4e08299321c6)


A serverless video processing and analysis system built on AWS Lambda that automates video frame extraction and analysis. This pipeline demonstrates modern event-driven architecture for efficient video processing.

## Architecture

- **Input Layer**: S3 bucket for receiving uploaded video content
- **Processing Stage 1**: Lambda function for video frame extraction and splitting
- **Intermediate Storage**: S3 bucket for storing extracted video frames
- **Processing Stage 2**: Lambda function for object detection and analysis
- **Output Layer**: S3 bucket for storing analysis results and metadata

## Key Features

- Fully serverless architecture using AWS Lambda
- Event-driven processing pipeline
- Automated frame extraction from video content
- Scene analysis capabilities
- Cost-effective - pay only for actual processing time
- Scalable design that handles videos of any size

## Tech Stack

- AWS Lambda for serverless compute
- Amazon S3 for video and frame storage
- AWS SDK for service integration
- Python/OpenCV for video processing
- Serverless framework for deployment

## Benefits

- No infrastructure management required
- Automatic scaling based on demand
- Cost optimization through serverless architecture
- Modular design for easy feature additions
