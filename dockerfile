
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /workdir

RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    vim \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-setuptools \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade \
    transformers[torch] \
    datasets \
    google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client \
    huggingface-hub
RUN pip install -U accelerate

COPY train2.py .
COPY drive_utils.py .
COPY token.pickle .
COPY dataset/vhdl_dataset.json .
CMD ["python", "train2.py"]
