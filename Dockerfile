FROM tensorflow/tensorflow:latest-gpu

#FROM tensorflow/tensorflow:2.12.0
FROM python:3.9-alpine3.16
#FROM nvcr.io/nvidia/tensorrt:latest
FROM nvcr.io/nvidia/tensorrt:21.03-py3

#WORKDIR /serve

RUN apt-get update && apt-get install -y python3-venv && rm -rf /var/lib/apt/lists/*
#RUN python3 -m venv /app/venv

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"


#RUN python -m pip install --upgrade --no-cache-dir
#RUN pip install --no-cache-dir --upgrade pip
RUN pip --version

FROM archlinux:latest

# Update and install OpenCV dependencies
RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm base-devel \
                          opencv \
                          cmake \
			  cuda \
                          git \
                          gtk2 \
                          ffmpeg \
                          tbb \
                          python-numpy \
                          libjpeg-turbo \
                          libpng \
                          libtiff \
                          openexr \
                          libwebp \
                          libdc1394 \
			  python \
			  python-pip \
			  python-virtualenv && \
    pacman -Scc --noconfirm


RUN pacman -Syu --noconfirm --needed cuda
#RUN pacman -U cuda-12.3.0-4-x86_64.pkg.tar.zst 
#RUN pacman -S nvidia

#RUN pacman -S nvidia-container-toolkit
#RUN nvidia-smi


# Export CUDA_HOME and LD_LIBRARY_PATH
RUN export CUDA_VISIBLE_DEVICES=0
RUN export CUDA_HOME=/usr/local/cuda
RUN export LD_LIBRARY_PATH="$CUDA_HOME/lib64:$LD_LIBRARY_PATH"


WORKDIR /serve
COPY . . 
#RUN pip install --no-cach-dir --upgrade pip
#RUN pip install --no-cache-dir -r req.txt



RUN python -m venv /app/venv \
    && source /app/venv/bin/activate \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r req.txt

EXPOSE 5000

#CMD ["python", "serve_model.py"]
CMD ["/app/venv/bin/python", "app.py"]

#CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
