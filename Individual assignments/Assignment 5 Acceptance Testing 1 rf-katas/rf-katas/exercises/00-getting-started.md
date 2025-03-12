# Getting started

In these exercises, we are going to start with a short introduction followed by exercises where you can apply
what you've learned. The exercises are designed to be done in order, so make sure you complete each exercise before
moving on to the next one. Additionally, each of the exercises comes with a simple script that you can run to verify
your solution.

## Terminology

In this section, you will see a lot of Python, operating system and Robot Framework related jargon
which might be confusing to some. So before you go further, let's clarify some terminology that is
used frequently in this ecosystem.

- _pip_ - Python package manager, this is a tool that is needed to install Robot Framework and needed test libraries
- _shell_ - The shell is the command interpreter in an operating system such as Unix or GNU/Linux, it is a program that executes other programs
- _bat / batch file / cmd_ - A batch file is a script file in DOS, OS/2 and Microsoft Windows. It consists of a series of commands to be executed by the command-line interpreter, stored in a plain text file.
- _robot_ - The command line tool that allows the user to run Robot Framework test cases and tasks
- _test suite_ - A Robot file that contains test cases
- _keyword_ - a component, similar to a function in programming, that robot uses to execute steps
- _arguments_ - Values that are given to keywords. Also known as parameters.

## Install Robot Framework

After completing last week's assingment, you should have a working Python environment with Robot Framework, SeleniumLibrary, and a webdriver installed.

You can install any additional requirements for this exercise by running `pip install -r requirements.txt` from the root of this project.

NOTE: If you are working on your own machine, activate the Python environment you created last week before proceeding. When executing the tests and verification scripts from command line or terminal, make sure you are in the same window, where you activated the Python environment.

## Start server

In order to run the exercises in this training, you need to start the demo app. You can start the server
by running `python3 server/server.py` in your terminal/command prompt. Your terminal or command prompt is
now occupied with running the server, which means you need to open another terminal/command prompt to run
your tests.

After the server has started it will be running in http://localhost:7272.

## Verify installation

Verify setup by running:

- in Windows: run command `python verify.py 00`
- in macOS/Linux: run command `python3 verify.py 00`

This should take a few seconds. If the output of the script ends with `Setup in perfect condition!`
we're good to go.

Otherwise, check the output and fix the missing packages.
