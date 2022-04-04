
from setuptools import setup

setup(
    name="ctt",
    packages=["ctt"],
    include_package_data=True,
    install_requires=[
        "pandas",
        "jupyter",
        "google-api-python-client",
        "google_auth_oauthlib",
        "pyyaml"
    ]
)