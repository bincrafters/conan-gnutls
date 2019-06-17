# -*- coding: utf-8 -*-
import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment
from conans.errors import ConanInvalidConfiguration


class GnuTLSConan(ConanFile):
    name = "gnutls"
    version = "3.6.8"
    url = "https://github.com/bincrafters/conan-gnutls"
    homepage = "https://www.gnutls.org"
    description = "A secure communications library implementing the SSL, TLS and DTLS protocols and technologies around them"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "LGPL-2.1"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}
    requires = ("nettle/3.4.1@bincrafters/stable", "gmp/6.1.2@bincrafters/stable")
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def configure(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            raise ConanInvalidConfiguration("The GnuTLS package cannot be deployed on Visual Studio.")
        del self.settings.compiler.libcxx

    def source(self):
        sha256 = "aa81944e5635de981171772857e72be231a7e0f559ae0292d2737de475383e83"
        source_url = "https://www.gnupg.org/ftp/gcrypt/gnutls"
        tools.get("{}/v3.6/gnutls-{}.tar.xz".format(source_url, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self)
            configure_args = ["--disable-tests"]
            if self.options.shared:
                configure_args.extend(["--enable-shared", "--disable-static"])
            else:
                configure_args.extend(["--disable-shared", "--enable-static"])
            self._autotools.configure(args=configure_args, configure_dir=self._source_subfolder)
        return self._autotools

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        autotools = self._configure_autotools()
        autotools.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
