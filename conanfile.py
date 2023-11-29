from conan import ConanFile
from conan.tools.files import download
from shutil import copytree

from os.path import join

import os
import subprocess
import sys

class CargoConan(ConanFile):
    name = 'cargo'
    settings = 'os', 'arch'

    # This is the rust version that will be installed
    version = '1.74.0'

    package_type = 'application'

    def layout(self):
        pass

    def build(self):
        build_folder = self.build_folder

        download(self, 'https://sh.rustup.rs', join(build_folder, 'rustup-init.sh'))

        env = os.environ.copy()
        env['RUSTUP_INIT_SKIP_PATH_CHECK'] = 'yes'
        env['RUSTUP_HOME'] = join(build_folder, 'rustup')
        env['CARGO_HOME' ] = join(build_folder,  'cargo')

        # Pipe stdout to stderr because the stdout output is read by some tools
        subprocess.run(
            ['sh', 'rustup-init.sh', '-y', '--no-modify-path', '--default-toolchain', self.version],
            stdout=sys.stderr,
            env=env
        )

        os.remove(join(build_folder, 'cargo', 'env'))

        env['PATH'] = join(build_folder, 'cargo', 'bin') + ':' + env['PATH']

        subprocess.run(
            ['rustup', 'default', 'stable'],
            stdout=sys.stderr,
            env=env
        )

    def package(self):
        build_folder = self.build_folder
        package_folder = self.package_folder

        copytree(src=join(build_folder, 'rustup'), dst=join(package_folder, 'rustup'))
        copytree(src=join(build_folder, 'cargo' ), dst=join(package_folder, 'cargo' ))

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs     = []

        self.runenv_info.define_path('RUSTUP_HOME', join(self.package_folder, 'rustup'))
        self.buildenv_info.define_path('RUSTUP_HOME', join(self.package_folder, 'rustup'))

        self.runenv_info.define_path('CARGO_HOME' , join(self.package_folder, 'cargo' ))
        self.buildenv_info.define_path('CARGO_HOME' , join(self.package_folder, 'cargo' ))

        self.runenv.prepend_path('PATH', join(self.package_folder, 'cargo', 'bin'))
        self.buildenv_info.prepend_path('PATH', join(self.package_folder, 'cargo', 'bin'))