# HPC Instructions

There are 2 ways to access the HPC: the first is by SSH-ing from your terminal to the remote cluster, the second is using CARC OnDemand.

- SSH to the Discovery Cluster: Please read the following [guide](https://www.carc.usc.edu/user-information/user-guides/hpc-basics/getting-started-discovery)
- OnDemand: Please read the following [guide](https://www.carc.usc.edu/user-information/user-guides/hpc-basics/getting-started-ondemand)

In both cases, you will have to either be connected to the USC network or use
the [USC VPN](https://www.carc.usc.edu/user-information/user-guides/hpc-basics/anyconnect-vpn-setup)
to connect to the cluster.
Once you are able to access the terminal on the cluster using whichever method
you prefer, continue reading.

**Note: It is important to be familiar with how to use the shell for each case, and also how to transfer files.**

In the rest of the document I will assume the following convention:

- In code blocks, lines that start with `$` are shell commands. Copy the text after the `$`.
- In code blocks, lines that start with `#` are either outputs or comments.
- Output code in `<...>` are placeholders. In output lines that start with `#`, this just refers to text we don't necessarily care about.

## Initial Setup

Before you can run the experiments, you will have to setup the environment for the HPC. These instructions only need to be run once. 

### Python/Anaconda setup

Run the following in the shell:

```shell
$ module purge
$ module load conda
$ conda init bash
$ conda config --set auto_activate_base false # This will prevent the base environment from being loaded
$ source ~/.bashrc
```

This will load the [Anaconda](https://docs.conda.io/en/latest/) module. So, you will have to create your own environment:

```shell
$ conda activate base
$ conda create -n carla python=3.8 conda -c conda-forge
```

This will create the `carla` environment with Python 3.8. To use this environment, run:

```shell
$ conda activate carla
```

To verify that you have the correct environment loaded, make sure the command line prompt begins with `(carla)` and the following commands output correctly:

```shell
$ python --version
# Python 3.8.<*>
$ which python
# ~/.conda/envs/carla/bin/python
```

Now we make the conda executable in the `carla` environment the default so it can be found by the Singularity container. If the `condabin` directory doesn't have the `conda` executable, it may be at `~/.conda/envs/carla/bin/conda` instead.  

```shell
$ ~/.conda/envs/carla/condabin/conda init bash
$ source ~/.bashrc
```

### Code transfer

First, get the template for the project:

```shell
$ cd ~
$ cp /project/jdeshmuk_786/csci513-miniproject1b.zip .
$ unzip csci513-miniproject1b.zip
```

This will create a `csci513-miniproject1b` directory in the home directory.
Use the file transfer methods described in the linked guides above to update
the files in this directory with your code.

### Carla and Python setup

We are going to be using [`singularity`](https://docs.sylabs.io/guides/3.7/user-guide/index.html) to run CARLA within a container.

Now, this following command is the one you will use every time you want to
acquire a compute "node" with a GPU:

```shell
$ salloc --time=2:00:00 --cpus-per-task=8 --mem=32GB --account=jdeshmuk_786 --partition=gpu --gres=gpu:1
# salloc: Granted job allocation <job id>
# salloc: Waiting for resource configuration
# salloc: Nodes <node-name> are ready for job
```

Run the command `nvidia-smi` to ensure the GPU drivers were loaded properly. 
Run the above so that we can setup the Python library for Carla.
Once you're allocated a node (based on the output above), you will run the following:

```shell
$ module load conda
$ source ~/.bash_profile
```

Make sure that the `carla` environment is loaded before continuing.
Now, launch the singularity container:

```shell
$ singularity exec --nv /project/jdeshmuk_786/carla_0.9.12.sif bash
```

When you run this, your prompt should change to `Singularity>`. Then, run:

```
$ source ~/.bashrc
$ conda activate carla # The prompt should change to show that the env is activated
$ pip install -U carla==0.9.12
```

This will install the required Python library. Now, you will have to make sure the project in `~/csci513-miniproject1b` is found by Python:

```
$ cd ~/csci513-miniproject1b
$ python3 -m pip install -U -e .
```

Now, we will try to run Carla and verify that it works.
Run the following while still inside the Singularity container:

```shell
$ cd /home/carla/ # This will change directories to the specified one
$ bash ./CarlaUE4.sh -nosound -vulkan -RenderOffScreen & # The & is required
# chmod: changing permissions of '/home/carla/CarlaUE4/Binaries/Linux/CarlaUE4-Linux-Shipping': Read-only file system
# 4.26.2-0+++UE4+Release-4.26 522 0
# Disabling core dumps.
# sh: 1: xdg-user-dir: not found
# Hit ENTER here and the prompt will reappear. If it doesnt, make sure that you put in the &
$ cd PythonAPI/util
$ python3 test_connection.py
# CARLA 0.9.12 connected at 127.0.0.1:2000.
```

If you don't see the last output, then there is an issue.

**Note: To exit from the Singularity container and/or the allocated job node, simply run the command `exit`.**

You can exit the container and the job node now (you will have to run `exit` twice: once for the container, once for the job node).

## Running the experiment

Once your environment is setup, the process to run the experiments is a little simpler. After accessing HPC, first get a job allocation using `salloc`:

```shell
$ salloc --time=2:00:00 --cpus-per-task=8 --mem=32GB --account=jdeshmuk_786 --partition=gpu --gres=gpu:1
# salloc: Granted job allocation <job id>
# salloc: Waiting for resource configuration
# salloc: Nodes <node-name> are ready for job
```

Once you're allocated a node (based on the output above), you will run the following:

```shell
$ module load conda
$ source ~/.bash_profile
$ singularity exec --nv /project/jdeshmuk_786/carla_0.9.12.sif bash # You will get into the singularity container
$ source ~/.bashrc
$ conda activate carla $ Your prompt should change to show that the env was activated
$ bash /home/carla/CarlaUE4.sh -nosound -vulkan -RenderOffScreen & # This will launch Carla. Remember to hit ENTER after seeing the desired output to get the prompt back.
$ cd ~/csci513-miniproject1b
```

Now, you should be able to run your simulations and evaluate your designs as
described in the README file (follow the instructions after the simulator has
been started).
