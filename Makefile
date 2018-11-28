before_install:
	if [ $$TEST = "yes" ]; then \
		pip install --upgrade tox \
		echo 'repo_token: '$$COVERALLS_REPO_TOKEN > .coveralls.yml \
    tox \
    rm .coveralls.yml; \
  fi

install:
	if [ $$LOCAL = "yes" ]; then \
		pip install . ; \
	fi

before_script:
	if [ $$LOCAL = "yes" ]; then \
		qemu-composer --help; \
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
