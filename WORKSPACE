workspace(
    name = "t2engine"
)

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

http_archive(
    name = "bazel_federation",
    url = "https://github.com/bazelbuild/bazel-federation/releases/download/0.0.1/bazel_federation-0.0.1.tar.gz",
    sha256 = "506dfbfd74ade486ac077113f48d16835fdf6e343e1d4741552b450cfc2efb53",
)

git_repository(
    name = "rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    # NOT VALID: Replace with actual Git commit SHA.
    commit = "cd552725122fdfe06a72864e21a92b5093a1857d",
)

load("@bazel_federation//:repositories.bzl", "rules_python_deps")

rules_python_deps()
load("@bazel_federation//setup:rules_python.bzl",  "rules_python_setup")
rules_python_setup(use_pip=True)

# Setup python requirements
load("@rules_python//python:pip.bzl", "pip3_import")

pip3_import(
   name = "testing_deps",
   requirements = "//:requirements.txt",
)

# Load the central repo's install function from its `//:requirements.bzl` file,
# and call it.
load("@testing_deps//:requirements.bzl", "pip_install")
pip_install()
