FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# Default: RTX A6000. Override for other GPUs, including builds without a GPU.
ARG TORCH_CUDA_ARCH_LIST="8.6"
ARG MAX_JOBS=4
ENV TORCH_CUDA_ARCH_LIST=${TORCH_CUDA_ARCH_LIST} \
    MAX_JOBS=${MAX_JOBS} \
    CUDA_HOME=/usr/local/cuda \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# COLMAP and ImageMagick support convert.py; build SIBR viewers separately.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates wget git build-essential ninja-build colmap imagemagick \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q \
    https://repo.anaconda.com/miniconda/Miniconda3-py39_24.1.2-0-Linux-x86_64.sh \
    -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /opt/conda \
    && rm /tmp/miniconda.sh

# Direct environment PATH works for both Compose commands and interactive shells.
ENV PATH=/opt/conda/envs/fsgs/bin:/opt/conda/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/opt/conda/envs/fsgs/lib/python3.9/site-packages/torch/lib:/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

RUN /opt/conda/bin/conda create -n fsgs python=3.9 -y \
    && /opt/conda/bin/conda clean -afy

RUN python -m pip install --upgrade pip wheel ninja "setuptools==69.5.1" \
    && python -m pip install \
        torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 \
        --index-url https://download.pytorch.org/whl/cu118 \
    && python -m pip install \
        "numpy<2" "plyfile<1.1" pillow tqdm \
        "opencv-python-headless<4.12" joblib tensorboard

# Initialize recursive submodules before building these CUDA extensions.
COPY submodules/simple-knn /tmp/simple-knn
COPY submodules/diff-gaussian-rasterization /tmp/diff-gaussian-rasterization
COPY submodules/fused-ssim /tmp/fused-ssim
RUN python -m pip install --no-build-isolation \
        /tmp/simple-knn /tmp/diff-gaussian-rasterization /tmp/fused-ssim \
    && python -c "import torch; from simple_knn._C import distCUDA2; import diff_gaussian_rasterization; from fused_ssim import fused_ssim" \
    && rm -rf /tmp/simple-knn /tmp/diff-gaussian-rasterization /tmp/fused-ssim

# Provide an X11/OpenGL display for the packaged COLMAP in headless containers.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        xvfb xauth libgl1-mesa-dri libglx-mesa0 mesa-utils \
    && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:99 \
    QT_QPA_PLATFORM=xcb \
    LIBGL_ALWAYS_SOFTWARE=1

WORKDIR /workspace/fsgs
COPY . .

ENTRYPOINT ["xvfb-run", "--server-num=99", "--server-args=-screen 0 1280x1024x24 -nolisten tcp"]
CMD ["/bin/bash"]
