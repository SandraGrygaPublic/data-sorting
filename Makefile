#!make

DOCKER_IMAGE_NAME='sort_algorytm:0.0.0'
DOCKER_RAM_MEMORY='5m'
CHANK_MAX_SIZE_MB='3'
DOCKER_CPUS='4'
TEST_FILE_SIZE_MB='10'
SHARED_DATA_DIR_NAME='docker_shared_data'

venv:
	@ echo " PREPARE ENV ===============================================\n"
	scripts/prepare-env.sh 'app/file_generator' 'app/sorting_script'

install_required_packages: venv
	@ echo " INSTALL PACKAGES ==========================================\n"
	. ./venv/bin/activate && scripts/install-required-packages.sh 'app'

run_tests: install_required_packages
	@ echo " RUN TESTS =================================================\n"
	. ./venv/bin/activate && scripts/run-tests.sh

install_app: venv
	@ echo " INSTALL APPLICATION =======================================\n"
	. ./venv/bin/activate && cd app && python setup.py install

build_docker:
	@ echo " BUILD DOCKER ==============================================\n"
	docker build -f Dockerfile -t $(DOCKER_IMAGE_NAME) .

test_code_in_docker: build_docker
	@ echo " RUN DOCKER ================================================\n"
	docker run --memory=$(DOCKER_RAM_MEMORY) --cpus=$(DOCKER_CPUS) sort_algorytm:0.0.0 $(TEST_FILE_SIZE_MB) $(CHANK_MAX_SIZE_MB)
