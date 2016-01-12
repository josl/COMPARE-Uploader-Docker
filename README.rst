COMPARE/ENGAGE uploader in a Docker container
==========================

This project documents theCOMPARE/ENGAGE uploader running in a Docker container

Installation
=============

If in another platform that is not Linux, like MacOS X or Window, boot2docker should be installed.

Recommended installer can be found [here](http://boot2docker.io) which install Docker and the VM.

For the specific OS:
- [Mac](https://github.com/boot2docker/osx-installer/releases)
- [Windows](https://github.com/boot2docker/windows-installer/releases)

Alternatively, on Mac there is also the possibility to install it through HomeBrew

```bash
brew install boot2docker
brew install docker-compose
```

To start running the VM and the Docker daemon:

```bash
boot2docker init
boot2docker start
# To test that everything worked
boot2docker status
docker version
docker run hello-worldw
```

Usage
=============

```bash
docker-compose build
docker-compose up -d
```
```bash
# Run terminal shell on selected image
docker exec -t -i <imageid> /bin/bash
```
```bash
# Remove all containers
docker rm $(docker ps -a -q)
```
```bash
# Remove all images
docker rmi $(docker images -a -q)
```

Documentation
=============



License
=======

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
