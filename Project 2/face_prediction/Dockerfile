# Defining global args
ARG FUNCTION_DIR="/home/app/"
ARG RUNTIME_VERSION="3.8"

# Using a smaller base image
FROM python:${RUNTIME_VERSION}-slim AS base

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Installing Python packages
RUN python -m pip install --upgrade pip

# Installing Lambda Runtime Interface Client for Python
RUN pip install awslambdaric

# Installing PyTorch and Torchvision without CUDA
RUN pip install --no-cache-dir \
    torch==1.9.0+cpu -f https://download.pytorch.org/whl/torch_stable.html \
    torchvision==0.10.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Copying the local facenet_pytorch folder
COPY facenet_pytorch ${FUNCTION_DIR}/facenet_pytorch
COPY face-recognition-code.py .

# Installing facenet_pytorch from the local copy
RUN pip install --no-cache-dir ./facenet_pytorch

# Copying the requirements file and install additional Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying function code
COPY handler.py .

# Adding Lambda Runtime Interface Emulator for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie

# Setting up the entry script
COPY entry.sh /
RUN chmod 755 /entry.sh

# Setting the CMD to your handler
ENTRYPOINT ["/entry.sh"]
CMD ["handler.handler"]