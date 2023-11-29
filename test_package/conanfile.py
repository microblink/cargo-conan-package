from conan import ConanFile

class CargoTestPackageConan(ConanFile):
    generators = "VirtualBuildEnv"
    test_type  = "explicit"

    def layout(self):
        # do not care
        self.folders.generators = 'build'

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def test(self):
        self.run("rustup --version")
        self.run("cargo --version")

    def build(self):
        pass