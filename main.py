import os
import sys
import fhw_lib
from colorama import Fore


class Forge:
    def __init__(self, program):
        self.program = program
        self.installed_packages = {}
        self.building_progress = {}
        self.built_packages = {}
        self.ban = ["__pycache__"]

    @staticmethod
    def get_dirs(path_to_parent_dir):
        unfiltered = os.listdir(path_to_parent_dir)
        dirs = filter(lambda name: os.path.isdir(os.path.join(path_to_parent_dir, name)), unfiltered)
        return dirs

    @staticmethod
    def load_mod(mode_dir_name):
        mod_dir_path = os.path.join("./mods", mode_dir_name)
        with open(os.path.join(mod_dir_path, "info.txt")) as f:
            mod_info = f.read()
        mod_main_func = getattr(__import__("mods." + mode_dir_name + ".main", fromlist=["reg"]), "reg")
        return mod_main_func, mod_info

    def read_installed_mods(self):
        mod_dirs = self.get_dirs("./mods")
        mod_dirs = filter(lambda mod_dir: not(mod_dir in self.ban), mod_dirs)
        installed_mods = map(lambda mod_dir: self.load_mod(mod_dir)[0](self.program), mod_dirs)
        return installed_mods

    def generate_packages_list(self, installed_mods):
        for installed_mod in installed_mods:
            for installed_pack in installed_mod.packages:
                self.installed_packages[installed_pack.name] = installed_pack
                self.building_progress[installed_pack.name] = 0

    def build_using_top_sort(self):
        # 0 - absolutely new; 1 - in new chain; 2 - ready
        def dfs(v):
            if self.building_progress[v] == 0:
                self.building_progress[v] = 1
            elif self.building_progress[v] == 1:
                return True, [v]

            for u in self.installed_packages[v].dependencies:
                res = dfs(u[0])
                if hasattr(res, "__getitem__") and [0]:
                    res[1].append(v)
                    if res[1][0] == v:
                        print(Fore.RED + "HW Forge: could not build all packages")
                        print("This part of chain of dependencies is a cycle:")
                        for impossible_to_build_pack in res[1][::-1]:
                            print(self.installed_packages[impossible_to_build_pack].more_type_info)
                        print(Fore.RESET)
                        sys.exit(1)
            self.installed_packages[v].build_me()
            self.building_progress[v] = 2

        for pack_name in self.installed_packages.keys():
            if self.building_progress[pack_name] == 0:
                dfs(pack_name)

    # Hello world Forge main function
    def prepare(self):
        self.generate_packages_list(self.read_installed_mods())
        self.build_using_top_sort()


class Main:
    def __init__(self):
        self.version = (1, 0, 2)
        self.hello_world = "Hello, world!"
        self.writing_hello_word = True
        self.using_forge = True
        self.forge = Forge(self)

    # Hello, world
    def write_hello_world(self):
        sys.stdout.write(self.hello_world)

    def main(self):
        if self.using_forge:
            self.forge.prepare()
        if self.writing_hello_word:
            self.write_hello_world()


if __name__ == '__main__':
    Main().main()
