from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.scm import Git
from conan.tools.microsoft import is_msvc, msvc_runtime_flag, unix_path
import os

class natsRecipe(ConanFile):
    name = "cnats"
    version = "v3.8.0"

    # Optional metadata
    license = "MIT"
    author = "Jelin (jelin-sh@outlook.com)"
    url = "https://github.com/jelin-sh/conan2-cnats.git"
    description = "C client for NATS, a lightweight & high performance messaging system for cloud native applications."
    topics = ("C", "messaging", "message-bus", "message-queue", "message-library","nats-client")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "no_spin": [True, False],
        "tls": [True, False],
        "tls_force_host_verify": [True, False],
        "tls_use_openssl_1_1_api": [True, False],
    }
    default_options = {
        "shared": False,
        "no_spin": False,
        "tls": True,
        "tls_force_host_verify": True,
        "tls_use_openssl_1_1_api": True,
    }

    generators = "CMakeDeps"    

    def source(self):
        git = Git(self)
        git.clone(url="https://github.com/nats-io/nats.c.git", target=".")
        git.checkout(self.version)    

    def requirements(self):
        self.requires("protobuf-c/1.5.0")
        self.requires("openssl/3.1.3")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["NATS_BUILD_NO_SPIN"] = self.options.no_spin
        tc.variables["NATS_BUILD_WITH_TLS"] = self.options.tls
        tc.variables["NATS_BUILD_TLS_FORCE_HOST_VERIFY"] = self.options.tls_force_host_verify
        tc.variables["NATS_BUILD_TLS_USE_OPENSSL_1_1_API"] = self.options.tls_use_openssl_1_1_api
        tc.variables["CMAKE_MACOSX_RPATH"] = True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):            
        base_path = os.path.join("lib", "cmake", "cnats")     
        self.cpp_info.builddirs.append(base_path)
        self.cpp_info.set_property("cmake_build_modules", [
            os.path.join(base_path, "cnats-config.cmake")
        ])
        
