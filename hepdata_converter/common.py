class Option(object):
    def __init__(self, name, shortversion=None, type=str, default=None, variable_mapping=None, required=True, help='', auto_help=True):
        self.name = name
        self.help = help
        self.required = required
        self.auto_help = auto_help
        self.shortversion = shortversion
        self.variable_mapping = variable_mapping or self.name
        self.default = default
        self.type = type
        if self.type is bool:
            self.action = 'store_const'
        else:
            self.action = 'store'

    def attach_to_parser(self, parser):
        args = ['--'+self.name]
        if self.shortversion:
            args.append('-'+self.shortversion)

        kwargs = {
            'default': self.default,
            'help': self.help,
            'required': self.required,
            'action': self.action
        }
        if self.type == bool:
            kwargs['const'] = True

        parser.add_argument(*args, **kwargs)

class OptionInitMixin(object):
    """This mixin requires a class to have specified options dictionary as
    class variable

    """
    def __init__(self, options):
        self.options_values = {}
        for option in options:
            if option in self.__class__.options:
                self.options_values[self.__class__.options[option].variable_mapping] = options[option]

        # add default values
        for key, option in self.__class__.options.items():
            if key not in options:
                self.options_values[self.__class__.options[key].variable_mapping] = option.default

    @classmethod
    def register_cli_options(cls, parser):
        for option in cls.options:
            cls.options[option].attach_to_parser(parser)

    def __getattr__(self, attr_name):
        if attr_name in self.options_values:
            return self.options_values[attr_name]
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, attr_name))

    def __dir__(self):
        _dir = dir(super(OptionInitMixin, self))
        _dir += [option.variable_mapping for key, option in self.__class__.options.items()]
        return _dir
