FROM python:3

# Prevents Python from writing .pyc (bytecode) files.
# Having up-to-date code and lighter size
# On the other hand having lower performance
ENV PYTHONDONTWRITEBYTECODE=1

# This variable, however, doesn't affect the Python interpreter itself but how its output is handled.
# Setting PYTHONUNBUFFERED=1 forces unbuffered output for standard output (stdout) and standard error (stderr) for Python processes within the container.
# Here's what unbuffered output means:=
#   Normal behavior (without the variable): Python buffers its output before sending it to stdout/stderr.
#     This means it collects some data before flushing it to the terminal or log file.
#     This buffering can be beneficial for performance in some cases.
#   Unbuffered output (with the variable): Python sends each character or line of output immediately to stdout/stderr without buffering. This results in:
#     Real-time output: You'll see the output of your Python scripts or programs as they are generated, character by character, instead of waiting for a buffer to flush.
#     Possible performance overhead: While you see output faster, sending each character individually can be slightly less efficient than sending larger chunks of data.
# Essentially, this setting prioritizes real-time visibility of Python output over potential performance gains from buffering.
# It's often recommended for interactive use, debugging, or situations where you need to see the output immediately.
# However, in production environments where performance is critical, removing this setting might be considered.
ENV PYTHONUNBUFFERED=1

# If /app doesn't exist it'll be created
COPY . /app

# working directory (default is /.)
# commands like COPY, RUN, and CMD will operate relative to the specified /app directory
WORKDIR /app

RUN pip install -r requirements/dev.txt
    

EXPOSE 8000

# Command to be excuted when the app runs
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
