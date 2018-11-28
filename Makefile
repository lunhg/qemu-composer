before_install:
	if [ $$TEST = "yes" ]; then \
		pip install --upgrade tox; \
	fi

requirements:
	if [ $$TEST = "yes" ] || [ $$LOCAL = "yes" ];  then \
		pip install -r requirements.txt; \
	fi

install:
	if [ $$TEST = "yes" ] || [ $$LOCAL = "yes" ] || [ $$PIP = "yes" ];  then \
		pip install -e .; \
	fi

before_script:
	if [ $$TEST = "yes" ] || [ $$LOCAL = "yes" ] || [$$PIP = "yes" ]; then \
		qemu-composer --version \
		qemu-composer --help;	\
  fi

script:
	if [ $$LOCAL = "yes" ]; then \
		qemu-composer --prefix $$QEMU_PREFIX \
                  --file $$QEMU_FILE \
                  --group $$QEMU_GROUP \
                  --gid $$QEMU_GID \
                  --uid $$QEMU_UID \
                  build; \
	fi

after_script:
	if [ $$LOCAL = "yes" ]; then \
		docker-compose \
			--file $$DOCKER_COMPOSE_FILE up \
      --build \
      -d; \
	fi

after_success:
	if [ $$PIP = "yes" ]; then \
		python setup.py register --show-response \
														 --list-classifiers \
														 --strict \
		python setup.py sdist --show-response \
		python setup.py upload -- show-response; \
  fi
	if [ $$HUB = "yes" ]; then \
		docker login --username $$HUB_USERNAME \
								 --password $$HUB_PWD \
		docker-compose --file $$DOCKER_COMPOSE_FILE push; \
	fi

test:
	if [ $$TEST = "yes" ]; then \
		py.test --cov=qemu_composer tests/ --verbose; \
	fi

coveralls:
	if [ $$COVER = "yes" ]; then \
		COVERALLS_REPO_TOKEN=$$COVERALLS_REPO_TOKEN coveralls; \
	fi

tox:
	if [ $$TEST = "yes" ]; then tox; fi
