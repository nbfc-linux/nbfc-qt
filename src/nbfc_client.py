#!/usr/bin/env python3

import os
import re
import json
import socket
import subprocess
from collections import namedtuple

Sensor = namedtuple('Sensor', ['name', 'description'])

class NbfcClientError(Exception):
    pass

class NbfcClient:
    """
    A client to interact with the NBFC service using Unix sockets.
    """

    def __init__(self):
        """
        Initializes the NbfcClient instance by retrieving necessary file paths.

        Raises:
            NbfcClientError:
                See `call_nbfc` for further information.
        """

        self.socket_file = self.get_compile_time_variable('socket_file')
        self.config_file = self.get_compile_time_variable('config_file')
        self.model_configs_dir = self.get_compile_time_variable('model_configs_dir')
        self.model_configs_dir_mutable = '/var/lib/nbfc/configs'

    # =========================================================================
    # Helper methods
    # =========================================================================

    def call_nbfc(self, args):
        """
        Calls the `nbfc` binary with the given arguments and returns the output.

        Args:
            args (list of str):
                The arguments to pass to the NBFC client.

        Returns:
            str:
                The output (STDOUT) from the client command.

        Raises:
            NbfcClientError:
                - If the `nbfc` binary could not be found.

                - If the client command returns a non-zero exit code.
                  The exception's text is the output written to STDERR.
        """

        command = ['nbfc'] + args

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=False)
        except FileNotFoundError:
            raise NbfcClientError('Could not find the `nbfc` program. Is NBFC-Linux installed?') from e

        if result.returncode != 0:
            raise NbfcClientError(result.stderr.rstrip())

        return result.stdout.rstrip()

    def socket_communicate(self, data):
        """
        Sends a JSON-encoded message to the NBFC service via a Unix socket
        and returns the response.

        Args:
            data (dict):
                The data to send to the NBFC service.

        Returns:
            dict:
                The response from the NBFC service.

        Raises:
            NbfcClientError:
                If the socket file could not be found.

            PermissionError:
                If the socket file could not be opened.

            JSONDecodeError:
                If the received JSON is invalid.

            TypeError:
                If `data` could not be serialized to JSON.
        """

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:

            try:
                sock.connect(self.socket_file)
            except FileNotFoundError:
                raise NbfcClientError(f'Could not find {self.socket_file}. Is the service running?') from None

            message = "%s\nEND" % json.dumps(data)
            sock.sendall(message.encode('utf-8'))

            response = b''
            while True:
                data = sock.recv(1024)
                if not data:
                    break

                response += data

                if b'\nEND' in response:
                    break

            response = response.decode('utf-8')
            response = response.replace('\nEND', '')
            response = json.loads(response)
            return response

    # =========================================================================
    # Methods based on `call_nbfc`
    # =========================================================================

    def get_compile_time_variable(self, variable):
        """
        Retrieves the value of a compile-time variable defined in the NBFC binary.

        Args:
            variable (str):
                The name of the compile-time variable to retrieve.

        Returns:
            str:
                The value assigned to the compile time variable.

        Raises:
            NbfcClientError:
                See `call_nbfc` for further information.
        """
        return self.call_nbfc(['show-variable', variable])

    def get_version(self):
        """
        Return the version of the nbfc client.

        Returns:
            str:
                The version in form of "MAJOR.MINOR.PATCH".

        Raises:
            NbfcClientError:
                See `call_nbfc` for further information.
        """

        output = self.call_nbfc(['--version'])

        match = re.search(r'\d+\.\d+\.\d+', output)

        if not match:
            raise NbfcClientError('Could not extract version')

        return match[0]

    def start(self, readonly=False):
        """
        Starts the NBFC service.

        Args:
            readonly (bool):
                If True, starts the service in read-only mode.

        Raises:
            NbfcClientError:
                See `call_nbfc` for further information.
        """

        args = ['start']

        if readonly:
            args.append('-r')

        self.call_nbfc(args)

    def restart(self, readonly=False):
        """
        Restarts the NBFC service.

        Args:
            readonly (bool):
                If True, starts the service in read-only mode.

        Raises:
            NbfcClientError:
                See `call_nbfc` for further information.
        """

        args = ['restart']

        if readonly:
            args.append('-r')

        self.call_nbfc(args)

    def stop(self):
        """
        Stops the NBFC service.

        Raises:
            NbfcClientError:
                See `call_nbfc` for further information.
        """

        self.call_nbfc(['stop'])

    def get_model_name(self):
        """
        Retrieve the model name of the notebook.

        Returns:
            str:
                The model name of the notebook.

        Raises:
            NbfcClientError:
                See `call_nbfc` for further information.
        """

        return self.call_nbfc(['get-model-name'])

    def list_configs(self):
        """
        List all available model configurations.

        Returns:
            list of str:
                A list of all available model configurations.

        Raises:
            NbfcClientError:
                See `call_nbfc` for further information.
        """

        configs = self.call_nbfc(['config', '-l'])
        configs = configs.strip()

        if configs:
            return configs.split('\n')
        else:
            return []

    def recommended_configs(self):
        """
        List recommended model configurations.

        Returns:
            list of str:
                A list of recommended configurations.

        Raises:
            NbfcClientError:
                See `call_nbfc` for further information.
        Note:
            This returns recommended configurations based solely on comparing
            your model name with configuration file names.
            This recommendation does not imply any further significance or validation
            of the configurations beyond the string matching.
        """

        configs = self.call_nbfc(['config', '-r'])
        configs = configs.strip()

        if configs:
            return configs.split('\n')
        else:
            return []

    def get_available_sensors(self):
        """
        Returns a list of all available sensors.

        Returns:
            list of Sensor:
                A list of all available sensors.

        Raises:
            NbfcClientError:
                See `call_nbfc` for further information.
        """

        sensors = []

        output = self.call_nbfc(['complete-sensors'])

        for line in output.split('\n'):
            parts = line.split('\t', maxsplit=1)

            if len(parts) == 2:
                name, description = parts

                # This is needed for old version of NBFC-Linux where the
                # `complete-sensors` outputs a `none` sensor
                if name == 'none':
                    continue

                sensors.append(Sensor(name, description))

        return sensors

    # =========================================================================
    # Methods based on `socket_communicate`
    # =========================================================================

    def get_status(self):
        """
        Retrieves the status of the NBFC service.

        Returns:
            dict:
                The status information of the NBFC service.

        Raises:
            NbfcClientError:
                If there is an error in the response from the service.
        """

        response = self.socket_communicate({'Command': 'status'})

        if 'Error' in response:
            raise NbfcClientError(response['Error'])

        return response

    def set_fan_speed(self, speed, fan=None):
        """
        Sets the fan speed.

        Args:
            speed (float, int, str):
                The desired fan speed in percent or "auto" for setting
                fan to auto-mode.

            fan (int, optional):
                The fan index to set the speed for. If not given, set the
                speed for all available fans.

        Raises:
            NbfcClientError:
                If there is an error in the response from the service.
        """

        request = {'Command': 'set-fan-speed', 'Speed': speed}

        if fan is not None:
            request['Fan'] = fan

        response = self.socket_communicate(request)

        if 'Error' in response:
            raise NbfcClientError(response['Error'])

    # =========================================================================
    # Methods for accessing / setting the configuration
    # =========================================================================

    def get_service_config(self):
        """
        Retrieves the current service configuration.

        Returns:
            dict:
                The current service configuration.

        Raises:
            PermissionError:
                If the file could not be read due to insufficient permissions.

            IsADirectoryError:
                If the file is a directory.

            JSONDecodeError:
                If the configuration file is not valid JSON.
        """

        try:
            with open(self.config_file, 'r', encoding='UTF-8') as fh:
                return json.load(fh)
        except FileNotFoundError:
            return {}

    def set_service_config(self, config):
        """
        Writes a new configuration to the service config file.

        Args:
            config (dict):
                The configuration data to write.

        Raises:
            PermissionError:
                If the program does not have permission to write to the config file.

            IsADirectoryError:
                If the config file is a directory.

            TypeError:
                If `config` could not be serialized to JSON.
        """

        with open(self.config_file, 'w', encoding='UTF-8') as fh:
            json.dump(config, fh, indent=1)

    def get_model_configuration_file(self):
        """
        Retrieve the file path of the model configuration file.

        Returns:
            str:
                The resolved file path of the model configuration file.

        Raises:
            NbfcClientError:
                If the configuration file could not be resolved.
        """

        config = self.get_service_config()

        if 'SelectedConfigId' not in config:
            raise NbfcClientError('Configuration has no model configuration ("SelectedConfigId") set')

        config_id = config['SelectedConfigId']

        if config_id.startswith('/'):
            return config_id

        model_config_path = os.path.join(self.model_configs_dir_mutable, config_id + '.json')
        if os.path.exists(model_config_path):
            return model_config_path

        model_config_path = os.path.join(self.model_configs_dir, config_id + '.json')
        if os.path.exists(model_config_path):
            return model_config_path

        raise NbfcClientError(f'No configuration file found for SelectedConfigId = "{config_id}"')

    def get_model_configuration(self):
        """
        Return the model configuration.

        Returns:
            dict:
                The model configuration.

        Raises:
            FileNotFoundError:
                If the file could not be found.

            PermissionError:
                If the file could not be read due to insufficient permissions.

            IsADirectoryError:
                If the file is a directory.

            JSONDecodeError:
                If the file contains invalid JSON.
        """

        config_file = self.get_model_configuration_file()

        with open(config_file, 'r', encoding='UTF-8') as fh:
            return json.load(fh)
