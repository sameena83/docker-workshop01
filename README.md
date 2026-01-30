# docker-workshop01
workshop codespaces

dOCKER- WAY TO SEPERATE WHAT YOU HAVE IN YOUR HOST MACHINE
ISOLATED CONTAINER FROM SYSTEM

>docker run hello-world 

DISPLAYS HELLO FROM DOCKER

>docker run ubuntu
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
a3629ac5b9f4: Pull complete 
Digest: sha256:cd1dba651b3080c3686ecf4e3c4220f026b521fb76978881737d24f200828b2b
Status: Downloaded newer image for ubuntu:latest
>ls
README.md
>docker  run -it ubuntu (This will go inside ubuntu)
root@243a205c2dbe:/# ls
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr

WHATEVER WE DO HERE IS ISOLATED FROM HOST MACHINE

we dont have python here, 

root@243a205c2dbe:/# apt update

DO as follows

root@243a205c2dbe:/# apt install python3
EXIT THE DOCKER AND CHECK IF PYTHON IS EXISTING IN NEW CONTAINER
root@243a205c2dbe:/# exit 
exit
>docker run -it ubuntu
root@dae5c0987a72:/# python -V
bash: python: command not found
root@dae5c0987a72:/# 
IT IS STATELESS. WHEN WE EXIT CONTAINER AND RUN THE IMAGE WE ARE BACK TO ZERO
HOW TO PRESERVE STATE? THAT WE WILL DISCUSS LATER

create another docker image called python

docker run -it python:3.13.11
Unable to find image 'python:3.13.11' locally
3.13.11: Pulling from library/python
2ca1bfae7ba8: Pull complete 
82e18c5e1c15: Extracting  25.61MB/25.61MB
be442a7e0d6f: Download complete 
26d823e3848f: Download complete 
ca4b54413202: Download complete 
b6513238a015: Download complete 
9b57076d00d4: Download complete 

PYTHON IMAGE IS CREATED

docker run -it python:3.13.11-slim. (lighter version of python)

SO if we want the entrypoint bash and want the python image we give the following command as follows
docker run -it --entrypoint=bash python:3.13.11-slim
root@b9026a6f0e88:/# ls
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr

root@b9026a6f0e88:/# python -V
Python 3.13.11
root@b9026a6f0e88:/# 

FILE CREATE IN DOCKER

root@b9026a6f0e88:/# echo 123 > file
root@b9026a6f0e88:/# ls
bin   dev  file  lib    media  opt   root  sbin  sys  usr
boot  etc  home  lib64  mnt    proc  run   srv   tmp  var
root@b9026a6f0e88:/# 

STATELESS, BUT A VERSION OF CONTAINER IS SAVED SOMEWHERE
USE COMMAND BELOW

docker ps -a
CONTAINER ID   IMAGE                 COMMAND       CREATED          STATUS                        PORTS     NAMES
b9026a6f0e88   python:3.13.11-slim   "bash"        2 minutes ago    Exited (127) 11 seconds ago             naughty_bohr
6b1e1cd326dc   python:3.13.11        "python3"     5 minutes ago    Exited (0) 3 minutes ago                reverent_nightingale
dae5c0987a72   ubuntu                "/bin/bash"   9 minutes ago    Exited (127) 6 minutes ago              admiring_ramanujan
243a205c2dbe   ubuntu                "/bin/bash"   14 minutes ago   Exited (0) 9 minutes ago                great_grothendieck
cccf1e6b1fa7   ubuntu                "/bin/bash"   14 minutes ago   Exited (0) 14 minutes ago               recursing_mclaren
a4480528cfa1   hello-world           "/hello"      16 minutes ago   Exited (0) 16 minutes ago               suspicious_morse
>
>docker ps -aq TO GET ONLY ID
b9026a6f0e88
6b1e1cd326dc
dae5c0987a72
243a205c2dbe
cccf1e6b1fa7
a4480528cfa1

>docker rm `docker ps -aq` TO REMOVE ALL DOCKER
b9026a6f0e88
6b1e1cd326dc
dae5c0987a72
243a205c2dbe
cccf1e6b1fa7
a4480528cfa1
 CHECK WHETHER WE REMOVED ALL CONTAINERS AS FOLLOWS
docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES


>ls
README.md
>mkdir test
>cd test/
>touch file1.txt file2.txt file3.txt
>echo "hello from file1" > file1.txt
>ls
file1.txt  file2.txt  file3.txt
>catt file1.txt
bash: catt: command not found
>cat file1.txt
hello from file1
>cat ./file1.txt
hello from file1
>ls
file1.txt  file2.txt  file3.txt  script.py
>python script.py
  File "/workspaces/docker-workshop01/test/script.py", line 1
    cst ./file1.
         ^
SyntaxError: invalid syntax

create script.py
writs a short program
whatever in the current directory should be available inside the container. This is achieved by volums mapping

>cd ..
>ls
README.md  test
>pwd
/workspaces/docker-workshop01
>cd test
>ls
file1.txt  file2.txt  file3.txt  script.py
>echo $(pwd)/test
/workspaces/docker-workshop01/test/test
>cd ..
>echo $(pwd)/test
/workspaces/docker-workshop01/test


>docker run -it \
    --rm \
    -v $(pwd)/test:/app/test \
    --entrypoint=bash \
    python:3.13.11-slim

    IT maps the absolute path of the test folder to the folder called app and the foldet test

root@59f04d9ec5f7:/# ls
app  boot  etc   lib    media  opt   root  sbin  sys  usr
bin  dev   home  lib64  mnt    proc  run   srv   tmp  var
root@59f04d9ec5f7:/# cd app
root@59f04d9ec5f7:/app# ls
test
root@59f04d9ec5f7:/app# 

root@59f04d9ec5f7:/# cd /app/test
ls -la
cat file1.txt
python list_files.py
total 16
drwxrwxrwx+ 2 1000 1000 4096 Jan 28 21:37 .
drwxr-xr-x  3 root root 4096 Jan 28 21:56 ..
-rw-rw-rw-  1 1000 1000   17 Jan 28 21:35 file1.txt
-rw-rw-rw-  1 1000 1000    0 Jan 28 21:35 file2.txt
-rw-rw-rw-  1 1000 1000    0 Jan 28 21:35 file3.txt
-rw-rw-rw-  1 1000 1000  375 Jan 28 21:51 script.py
hello from file1
python: can't open file '/app/test/list_files.py': [Errno 2] No such file or directory
root@59f04d9ec5f7:/app/test# 
now we actually do is to build a csv file and put it inside the postgres for analysis
For that built a folder calles pipeline and another file called pipeline.py
This data pipeline built some input and produce some output.
 Typically this pipelines are parameterized to provide parameter to our pipeline.

 >ls
README.md  pipeline  test
>cd pipeline
>python pipeline.py
hello pipeline
>

This is how we can parameterize our pipeline
import sys

print("Arguements:", sys.argv)
month=int(sys.argv[1])
print(f'The month is,month={month}')

Results below:
python pipeline.py 12
Arguements: ['pipeline.py', '12']
The month is,month=12

Completed program

import sys
import pandas as pd
print("Arguements:", sys.argv)
month=int(sys.argv[1])
print(f'The month is,month={month}')
df=pd.DataFrame({'day':[1,2],'num_passengers':[3,4]})
df['month']=month
print(df.head())

Install extension: for python
we use parquet, so install pyarrow


import sys
import pandas as pd
print("Arguements:", sys.argv)
month=int(sys.argv[1])
print(f'The month is,month={month}')
df=pd.DataFrame({'day':[1,2],'num_passengers':[3,4]})
df['month']=month
df.to_parquet(f"output_{month}.parquet")
print(df.head())


>pip install pyarrow

We installed pyarrow on local machine, may be we do not want it in the local machine, so we need to install it in virtual environment and the python also we can have inside this virtual environment
Python we have on virtual environment is diffenet from python we have on container
We want to install it in virtual environment and not inside the host machine
So we have 3 different environment , virtual , local and docker container
Each virtual environment can have whatever dependencies they need. This way we isolate one project from another. For this we use a tool called UV

uv init is the Python project initializer.
uv will:

Create a project structure

Sets up a basic Python project layout

Create a pyproject.tomlpwd


This becomes the single source of truth for:

dependencies

Python version

project metadata

Initialize uv’s dependency management

uv will manage installs, locking, and virtual environments from here on

Optionally create a virtual environment

Depending on flags / config, uv can manage this automatically:

Start from 

>pip install uv
>uv init --python 3.13

The result is as follows. In the vertual environment we want python 3.13 so we we did as above

>which python
/home/codespace/.python/current/bin/python
>python -V
Python 3.12.1
This is the version of python we have in system
But if we execute the same command in virtual environment by using command below
>uv run python -V

>uv run python -V
Using CPython 3.13.11
Creating virtual environment at: .venv
Python 3.13.11

Inside uv we have a different python : Python 3.13.11

>uv run which python
/workspaces/docker-workshop01/pipeline/.venv/bin/python
>
Inisde the uv we need to create two dependencies
> uv add pandas pyarrow
and you can see the dependencies insid the 
Go to search > Show and Run command select python interpretter
Find > select interpretter path 
.venv/bin/python

RUN THE FOLLOWING TO RUN THE FILE pipeline.py using uv

>uv run python pipeline.py 12
Arguements: ['pipeline.py', '12']
The month is,month=12
   day  num_passengers  month
0    1               3     12
1    2               4     12
> Once run, just check the file side it produce a file named output_12.parquet

Next update gitignore and put in gitignore
*.parquet to ingore all the file with parquet extension
That is inside the gitignore of the folder and not the gitignore of the .venv