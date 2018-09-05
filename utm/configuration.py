# -*- coding: utf-8 -*-
#
# License:          This module is released under the terms of the LICENSE file
#                   contained within this applications INSTALL directory

"""
    A configuration helper that accepts either INI files or preferably YAML files.

    Provides ``merge`` functionality of objects which allows us to maintain a ``config.global.ini``
    within our source tree and under SCM which acts as a template and contains nothing sensitive;
    whilst maintaining a ``config.local.ini`` within our source tree but **not** under SCM which
    *does* contain sensitive information (usernames/passwords/etc...).

    Assuming we have these two config files and they look like::

        (virtual) C:\>more config.global.ini
        [section]
        k1 =
        k2 =

        (virtual) C:\>more config.local.ini
        [section]
        k1 = secret
        k2 = values

    We can merge the local values into the global (template) with ease

    e.g::

        >>> from nsa.utils.configuration import Configuration
        >>> config = Configuration.load("config.global.ini")# load the global (template) config
        >>> print config
        {
          "section": {
            "k2": "",
            "k1": ""
          }
        }
        >>> lc = Configuration.load("config.local.ini")     # Load the local config
        >>> config << lc                                    # Merge local into global
        >>> print config
        {
          "section": {
            "k2": "values",
            "k1": "secret"
          }
        }


    .. note: Keys which are present in the local file which are not defined in the global file
                will be automatically added

"""

# -- Coding Conventions
#    http://www.python.org/dev/peps/pep-0008/   -   Use the Python style guide
#    http://sphinx.pocoo.org/rest.html          -   Use Restructured Text for docstrings

# -- Public Imports
import os, pkg_resources, ConfigParser
import yaml, json

# -- Private Imports

# -- Globals

# -- Exception classes

# -- Functions

# -- Classes
class Configuration(dict):

    def __init__(self, dictionary):
        super(Configuration, self).__init__()
        for k, v in dictionary.iteritems():
            if isinstance(v, dict):
                cls = object.__getattribute__(self, "__class__")    # Resolve real cls
                v = cls(v)
            self[k] = v

    def __hasattr__(self, k):
        if hasattr(self, k):
            return True
        return False

    def __getattribute__(self, k):
        # Try return values from dictionary first via dot notation
        # On failure check allow normal attribute access
        try:
            return self[k]
        except KeyError, e:
            raise AttributeError(e) # Re-raise something sensible

    def __setattr__(self, k, v):
        # Allow updates to the dictionaries only
        self[k] = v

    def __dir__(self):
        """ Returns a list of configuration keys
        """
        return [k for k in self]

    def __gt__(self, filename):
        """ Saves current configuration instance to file

            :param filename:    Filename
        """
        with open(filename, "w") as fh:
            fh.write(str(self))

    def __lshift__(self, configuration):
        """ Merges the configuration to the right of the operator into that on the left.

            :param configuration:   An configuration instance of the same type as the current
        """
        # Proxy for merging RHS config into LHS config
        # i.e. ``LHS << RHS``
        __class__ = cls = object.__getattribute__(self, "__class__")
        if not isinstance(configuration, __class__):
            raise TypeError(
                "Cannot merge configurations of different types %s, %s" % (type(self), type(configuration))
        )
        for k in configuration:
            v = configuration[k]
            if k not in self:
                self[k] = v
            elif isinstance(v, __class__):
                self[k] << v
            else:
                self[k] = v

    def __str__(self):
        raise NotImplementedError(
            "Subclass must provide implementation which returns current state as string"
        )

    def __call__(self):
        raise NotImplementedError(
            "Subclass must provide implementation which returns current state as dict"
        )

    @classmethod
    def load(cls, filename):
        """ Factory method to load the relevant configuration

            :param filename:    Filename to load
        """
        ext = os.path.splitext(filename)[1][1:]
        for c in cls.__subclasses__():
            if c.__implements__ == ext:
                return c.load(filename)
        raise NotImplementedError("No parser for file type '.%s'" % ext)

    @classmethod
    def validate(cls, filename):
        """ Validates a configuration

            :param filename:    Filename to validate
        """
        try:
            cls.load(filename)
        except IOError, e:
            raise
        except Exception, e:
            raise ValueError("Invalid configuration file")

    @staticmethod
    def resolve(pkg, name="config.local."):
        """ Resolves a local configuration from outside site-packages; in summary, it traverses
            toward the root of the directory looking for the configuration file

            :param pkg:     Current package name
            :param name:    Config file name to look for (Default: 'config.local.')
        """
        current = os.getcwd()
        location =  pkg_resources.require(pkg)[0].location
        os.chdir(location)

        parts = location.split(os.path.sep)
        parts.reverse() # tail first
        for part in parts:
            for listing in os.listdir("."):

                if name in listing:
                    found = os.path.abspath(listing)
                    os.chdir(current)   # Return ~home
                    return found
            else:
                os.chdir("..")
        os.chdir(current)
        raise Exception("Configuration not found")


class YAMLConfiguration(Configuration):

    __implements__ = "yaml"     # http://www.yaml.org/faq.html for file ext naming

    def __str__(self):
        # Serialize back to YAML for display or saving to file
        return yaml.dump(self, default_flow_style=False)

    def __call__(self):
        # Translates :class:`YAMLConfiguration` instances back into dictionaries to support serialization
        d = {}
        for k in self:
            v = self[k]
            if isinstance(v, YAMLConfiguration):
                v = v()
            d[k] = v
        return d

    @classmethod
    def load(cls, filename):
        """
        """
        with open(filename) as fh:
            d = yaml.load(fh.read()) or {}      # If file is empty
            return cls(d)

    @staticmethod
    def _represent_config(dumper, data):
        # Required to serialize data
        return dumper.represent_mapping(u'tag:yaml.org,2002:map', data())
yaml.add_representer(YAMLConfiguration, YAMLConfiguration._represent_config)


class INIConfiguration(Configuration):

    __implements__ = "ini"

    def __str__(self):
        # Serialize back to JSON for display or saving to file
        return json.dumps(self(), indent=2)

    def __call__(self):
        # Translates :class:`INIConfiguration` instances back into dictionaries to support serialization
        d = {}
        for k in self:
            v = self[k]
            if isinstance(v, INIConfiguration):
                v = v()
            d[k] = v
        return d

    @classmethod
    def load(cls, filename):
        """
        """
        def cast(v):
            for type_ in [int, float]:
                try:
                    return type_(v)
                except ValueError:
                    pass    # Allow to continue; if not one of types we fall through to next tests
            tm = {"true": True, "false": False, "none": None, "null": None}
            if v.lower() in tm.keys():
                return tm[v.lower()]
            return v

        if not os.path.exists(filename):
            raise IOError("No such file %s" % filename)
        parser = ConfigParser.RawConfigParser()
        parser.read(filename)
        d = {}
        # Create the configurations
        for k in parser.sections():
            sd = d[k] = {}
            for opt in parser.options(k):
                sd[opt] = cast(parser.get(k, opt))
        return cls(d)

# -- Main
