from fhw_lib import HWPackage, HWMod


class IntToHelloWordConverter(HWPackage):
    def __init__(self, program, from_mod):
        super().__init__(program, from_mod)
        self.program = program
        self.name = "int-to-hello-world-converter"
        self.version = (0, 1, 0)
        self.arr = [self.program.hello_world, "Hello world!", "Hello world"]

    def convert(self, x):
        return self.arr[x]


class VariationInput(HWPackage):
    def __init__(self, program, from_mod):
        super().__init__(program, from_mod)
        self.dependencies = [("int-to-hello-world-converter", (0, 1, 0), "int_to_hw_convert_pack")]
        self.program = program
        self.name = "hw-variation-input"
        self.version = (0, 1, 0)
        self.prompt = ">"

        self.int_to_hw_convert_pack = None

    def print(self):
        var = int(input(self.prompt))
        hw = self.int_to_hw_convert_pack.convert(var)
        print(hw)

    def after_build(self):
        # Removing default hello world printing
        # self.program.writing_hello_word = False
        self.program.write_hello_world = self.print


def reg(program):
    packages = [IntToHelloWordConverter, VariationInput]
    return HWMod("hello-world-variations", (0, 1, 1), packages, program)
