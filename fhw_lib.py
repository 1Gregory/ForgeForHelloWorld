class HWPackage:
    dependencies = []
    name = "-"
    version = (0, 0, 0)
    built = False

    def __init__(self, program, from_mod):
        self.program = program
        self.from_mod = from_mod

    def after_build(self):
        pass

    def more_type_info(self):
        return '{} {} v{}, from modification {}'.format(("built" if self.built else "non_built"),
                                                        self.name, ".".join(map(str, self.version)), self.from_mod)

    def build_me(self):
        for d_pack_name, d_pack_version, preferred_name in self.dependencies:
            setattr(self, preferred_name, self.program.forge.built_packages[d_pack_name])
        self.program.forge.built_packages[self.name] = self
        self.built = True
        self.after_build()


class HWMod:
    def __init__(self, name, version, packages, program):
        self.program = program
        self.name = name
        self.version = version
        self.packages = map(lambda x: x(program, name), packages)
