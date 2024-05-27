.ONESHELL:
SHELL = /bin/bash
.PHONY: help clean environment kernel jupyter install data
CONDA_ENV_DIR = $(shell conda info --base)/envs/tuw_education_notebooks
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate


help:
	@echo "make clean"
	@echo " clean all jupyter checkpoints"
	@echo "make manifest"
	@echo " lock dependencies of conda environment"
	@echo "make environment"
	@echo " create a conda environment"
	@echo "make kernel"
	@echo " make ipykernel based on conda lock file"
	@echo "make jupyter"
	@echo " launch JupyterLab server"
	@echo "make data"
	@echo " get example data"

clean:
	rm --force --recursive .ipynb_checkpoints/

$(CONDA_ENV_DIR):
	if ! { conda env list | grep 'tuw_education_notebooks'; } >/dev/null 2>&1; then
		@echo "creating new base tuw_education_notebooks conda environment..."
		conda create -y -c conda-forge -n tuw_education_notebooks python=3.10 pip mamba
	fi;
	$(CONDA_ACTIVATE) tuw_education_notebooks

environment: $(CONDA_ENV_DIR)
	@echo -e "conda environment is ready. To activate use:\n\tconda activate tuw_education_notebooks"

publish: environment
	$(CONDA_ACTIVATE) tuw_education_notebooks
	mamba env export --from-history | grep -ve "^prefix:" -ve "jupyterlab"  > environment.yml

kernel: environment
	$(CONDA_ACTIVATE) tuw_education_notebooks
	pip install --upgrade pip setuptools wheel
	pip install ./
	python -m ipykernel install --user --name tuw_education_notebooks
	@echo -e "conda jupyter kernel is ready."

jupyter: kernel
	$(CONDA_ACTIVATE) tuw_education_notebooks
	mamba install -c conda-forge jupyterlab
	jupyter lab .

install:
	$(CONDA_ACTIVATE) tuw_education_notebooks
	pip install --upgrade pip setuptools wheel
	pip install -e ./

data:
	wget -q -P ./data  https://cloud.geo.tuwien.ac.at/s/HxHCM4mqD3qRoEw/download/cd_ssm.zip
	cd data && unzip -n cd_ssm.zip && rm cd_ssm.zip