#!/usr/bin/env python3

"""
Wrapper for docker-py low-level client API.
Allow creating container and using it within `with` statement.
"""

# Imports

import docker


# Classes

class Container:
    """
    Class to represent docker container and expose simple API to it.
    """

    def __init__(self, image, command, environment=None):
        """
        Create the container. Not the same as `docker run`, need to be started after the creation.

        :param image: the image to run
        :type image: STRING
        :param command: the command to be run in the container
        :type command: STRING or LIST
        :param environment: A dictionary or a list of strings in the following format {"TEST": "123"} or ["TEST=123"].
        :type environment: DICT or LIST
        :param mount: absolute path to file to mount
        :type mount: STRING
        """
        self.client = docker.APIClient()
        self.pull(image)
        self.id = None
        self.run(image, command, environment)

    def __enter__(self):
        """
        Start the container and make a `with` context.
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Stop the container and clean up.
        """
        self.stop()
        self.remove()

    def put(self, real_path, container_path):
        with open(real_path, "rb") as bin:
            data = bin.read()
            self.client.put_archive(self.id, container_path, data)

    def run(self, image, command, environment=None):
        """
        Do real work of __init__.
        """
        result = self.client.create_container(
            image,
            command=command,
            detach=True,
            environment=environment,
        )
        self.id = result['Id']

    def exec(self, command):
        """
        Execute the command inside container cid

        :param str command: String representation of bash command

        :return: Returns a generator of output of the result of running bash command in bytes
        :rtype: iter
        """
        exe = self.client.exec_create(container=self.id, cmd=command)
        exe_start = self.client.exec_start(exec_id=exe, stream=True)

        return iter(exe_start)  # as iterator

    def inspect(self):
        """
        :return: Description of the container ans its status
        :rtype: DICT
        """
        return self.client.inspect_container(self.id)

    def start(self):
        """
        Start the container.
        """
        return self.client.start(self.id)

    def stop(self):
        """
        Stop the container.
        """
        return self.client.stop(self.id)

    def logs(self):
        """
        :return: Returns a stream of the STDOUT and STDERR
        :rtype: iter
        """
        return self.client.attach(self.id,
                                  stdout=True,
                                  stderr=True,
                                  stream=True,  # as iterator
                                  logs=False)

    def kill(self):
        """
        Kill the container.
        """
        return self.client.kill(self.id)

    def remove(self):
        """
        Remove the container and associated volumes.
        """
        return self.client.remove_container(self.id, v=True)

    def pull(self, image):
        """
        Pull image
        :param image: the image to pull
        :type image: STRING
        """
        self.client.pull(image)
