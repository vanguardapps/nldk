import argparse
import regex as re
from basic_object import get_basic_object


class CLIMenu(object):
    def __init__(self):
        # Disable default `-h`/`--help` behavior for `argparse.ArgumentParser`
        self._parser = argparse.ArgumentParser(add_help=False)
        self._options = {}
        self._all_parameters = set()

        # Having disabled `--help` default beahvior, we must define our own `--help` argument now.
        self._all_parameters.add("help")
        self._parser.add_argument(f"--help", action="store_true")

        # Support the `--languages-supported` flag by default
        self._all_parameters.add("languages_supported")
        self._parser.add_argument(f"--languages_supported", action="store_true")

    def add_primary_flag(
        self,
        flag=None,
        help=None,
        callback=None,
        get_languages_supported=None,
        required_params=None,
        optional_params=None,
    ):
        """
        Adds an option `--<flag>` to the `CommandLineMenu` instance. If the option is encountered, all of
        the parameters from `required_params` and `optional_params` will be concatenated and passed from the
        user's input to `callback`. `required_params` will be validated to ensure their presence (more specific
        validations must be performed inside of `callback`)

        @param flag (str):                          Indicates the primary option flag as a string. For instance, if the primary
                                                    option is `--convert_to_csv`, you would pass `flag="convert_to_csv"`.
                                                    NOTE: Any non-alphanumeric character in flag will be coerced to an underscore.

        @param help (str):                          The string text to be displayed next to the primary utility flag when `--help` is
                                                    passed to the application.

        @param callback (function):                 The callback function that will be invoked if the user passes `--<flag>` when
                                                    executing the script. Using the `--convert_to_csv` example, this may be a callback
                                                    `convert_to_csv(in_filename, out_filename)` (note all hyphens `-` will be converted
                                                    to underscores `_` for the purpose of variable names passed to callbacks). Callback
                                                    is responsible for accepting all arguments listed in the union of `required_params`
                                                    and `optional_params` as keyword arguments. NOTE: All parameters will have to be cast
                                                    to desired type from `str`.

        @param get_languages_supported (function):  A callback function called with all required and optional params of the chosen main
                                                    utility that must return the list of languages (lowercase full name) that support
                                                    all of the specified required and optional parameters. If the chosen main utility has
                                                    any default values for parameters, those should be used accordingly to make the
                                                    determination of whether a language is supported or not. The goal is to make it so
                                                    invoking the `--languages_supported` flag will show the exact list of languages supported
                                                    by the feature flags if the same flags were used to actually invoke the utility.

        @param required_params (Dict):              A dict where the keys are the names of the required parameters and the values are the
                                                    help text to be displayed next to that parameter when user passes `--help`. The string
                                                    `(bool)` may be appended to the end of any key (parameter name) to indicate that it is
                                                    a true/false flag as opposed to a parameter that expects a value. For instance
                                                    `is_collated(bool)` would specify a parameter `--is_collated` that is intended to be
                                                    used as a true/false flag. Leaving `(bool)` off implies that the parameter will be used
                                                    to capture a value. Required params are always validated to ensure they are present.
                                                    NOTE: Any non-alphanumeric character in required_params will be coerced to an underscore.

        @param optional_params (Dict):              A dict where the keys are the names of the optional parameters and the values are the
                                                    help text to be displayed next to that parameter when user passes `--help`. The string
                                                    `(bool)` may be appended to the end of any key (parameter name) to indicate that it is
                                                    a true/false flag as opposed to a parameter that expects a value. For instance
                                                    `is_collated(bool)` would specify a parameter `--is_collated` that is intended to be
                                                    used as a true/false flag. Leaving `(bool)` off implies that the parameter will be used
                                                    to capture a value. NOTE: Any non-alphanumeric character in any key of `required_params`
                                                    will be coerced to an underscore `_`.

        """

        if flag is None:
            raise ValueError("Missing required parameter `flag`")

        if flag in self._all_parameters:
            raise ValueError(
                f"Flag `--{flag}` has already been added as an option. Cannot add the same option twice."
            )

        if callback is None:
            raise ValueError("Missing required parameter `callback`")

        if get_languages_supported is None:
            raise ValueError("Missing required parameter `get_languages_supported`")

        if not (required_params or optional_params):
            raise ValueError(
                "Must specify one or both: `required_params` and/or `optional_params`"
            )

        # Sanitize primary flag to only allow alphanumeric characters and underscores
        flag = re.sub("[^0-9a-zA-Z]+", "_", flag)

        # Provide a default help text
        help = help if help else f"TODO: write `help` text for the `--{flag}` flag"

        # Add this primary utility flag to the parser
        self._parser.add_argument(f"--{flag}", action="store_true", help=help)

        if required_params:
            # 1. Strip required params
            required_params = {
                key.strip(): value for key, value in required_params.items()
            }
            # 2. Acknowledge required params intended to be boolean flags
            required_param_is_boolean = {
                key: True for key in required_params.keys() if key.endswith("(bool)")
            }
            # 3. Remove "(bool)" out if it appears
            required_params = {
                key.replace("(bool)", ""): value
                for key, value in required_params.items()
            }
            # 4. Sanitize required parameter names to only allow alphanumeric characters and underscores
            required_params = {
                re.sub("[^0-9a-zA-Z]+", "_", key): value
                for key, value in required_params.items()
            }
            # Add all required params as either boolean or value-capturing
            for param_name in required_params.keys():
                if param_name not in self._all_parameters:
                    self._all_parameters.add(param_name)
                    self._parser.add_argument(
                        f"--{param_name}",
                        action="store_true"
                        if required_param_is_boolean.get(param_name, None)
                        else None,
                    )

        if optional_params:
            # 1. Strip optional params
            optional_params = {
                key.strip(): value for key, value in optional_params.items()
            }

            # 2. Acknowledge optional params intended to be boolean flags
            optional_param_is_boolean = {
                key.replace("(bool)", ""): True
                for key in optional_params.keys()
                if key.endswith("(bool)")
            }

            # 3. Remove "(bool)" out if it appears
            optional_params = {
                key.replace("(bool)", ""): value
                for key, value in optional_params.items()
            }

            # 4. Sanitize optional parameter names to only allow alphanumeric characters and underscores
            optional_params = {
                re.sub("[^0-9a-zA-Z]+", "_", key): value
                for key, value in optional_params.items()
            }

            # Add all optional params as either boolean or value-capturing
            for param_name in optional_params.keys():
                if param_name not in self._all_parameters:
                    self._all_parameters.add(param_name)
                    self._parser.add_argument(
                        f"--{param_name}",
                        action="store_true"
                        if optional_param_is_boolean.get(param_name, None)
                        else None,
                    )

        if required_params and optional_params:
            # Validate that there is no overlap between `required_params` and `optional_params`
            overlapping_params = set(required_params.keys()) & set(
                optional_params.keys()
            )
            if overlapping_params:
                raise ValueError(
                    f"Parameters [`--{'`, `--'.join(overlapping_params)}] are inclued in both `required_params` and `optional_params`. "
                    + "There should be no overlap between `required_params` and `optional_params`."
                )

        # Add the parameter attributes to our dict of options
        self._options[flag] = get_basic_object()  # Creates a basic object
        self._options[flag].callback = callback
        self._options[flag].required_params = required_params
        self._options[flag].optional_params = optional_params
        self._options[flag].help = help
        self._options[flag].get_languages_supported = get_languages_supported

    def execute(self):
        if not self._options:
            raise ValueError(
                "Cannot execute `CommandLineMenu` because no options have been added"
            )

        args = self._parser.parse_args()

        primary_flags = self._options.keys()
        user_selection = None

        for flag in primary_flags:
            if getattr(args, flag, None):
                if user_selection:
                    raise ValueError("Only one primary flag may be selected at a time!")
                user_selection = flag

        help_flag = True if getattr(args, "help") else False

        if not user_selection:
            if help_flag:
                # Display general help output for all primary utility flags
                output = (
                    "\nUse one of the following primary flags. Use a primary flag in combination"
                    + " with `--help` to view help information specific to that flag:\n"
                )
                output += (
                    "--help: Display help for either the whole application (without a primary option) or for the "
                    + "primary option indicated by the feature flag (ie `--clean_content_file`).\n"
                )
                output += (
                    "--languages_supported: Display a list of languages that are supported for the features indicated for the "
                    + "primary utility selected (list of strings, lowercase, full language names).\n"
                )
                for flag, option in self._options.items():
                    output += f"--{flag}: {option.help}\n"
                print(output + "\n")
                return
            else:
                # If no `--help` flag was sent, throw an error as a selection from primary flags is required
                raise ValueError(
                    f"At least one primary utility must be passed. Should be one of [`--help`, `--{'`, `--'.join(primary_flags)}]"
                )

        callback = self._options[user_selection].callback
        required_params = self._options[user_selection].required_params
        optional_params = self._options[user_selection].optional_params
        get_languages_supported = self._options[user_selection].get_languages_supported
        user_selection_help = self._options[user_selection].help

        if help_flag:
            # Display help related to the selected primary flag
            output = f"\nHelp for `--{user_selection}`: {user_selection_help}\n\n"

            if required_params:
                output += "Required parameters:\n"
                for flag, help in required_params.items():
                    output += f"--{flag}: {help}\n"
            if optional_params:
                output += "\nOptional parameters:\n"
                for flag, help in optional_params.items():
                    output += f"--{flag}: {help}\n"
            print(output)
            return

        # Only using parameter keys from here onward, so converting to keys-only lists
        required_params = required_params.keys() if required_params else None
        optional_params = optional_params.keys() if optional_params else None

        # Dict to hold all parameters for the action being executed
        params = {}

        missing_required_params = []
        if required_params:
            # Store required parameters (check for missing)
            for name in required_params:
                value = getattr(args, name, None)
                if value:
                    params[name] = value
                else:
                    missing_required_params.append(name)

        if optional_params:
            # Store optional parameters
            for name in optional_params:
                value = getattr(args, name, None)
                if value:
                    params[name] = value

        # Check to see if the `--languages-supported` was specified
        if getattr(args, "languages_supported", None):
            language_support_output = f"\nLanguages supported for `--{user_selection}` using your parameters:\n\n"
            languages_list = get_languages_supported(**params)
            if languages_list:
                language_support_output += f"{languages_list}"
            else:
                language_support_output += "No languages are suppported for the specified utility and parameters."
            print(language_support_output + "\n")
            return
        else:
            # Check for missing required parameters
            if len(missing_required_params) > 0:
                raise ValueError(
                    f"Missing required parameters `--{'`, `--'.join(missing_required_params)}"
                )

            # Execute callback with params dict converted to keyword arguments
            callback(**params)
