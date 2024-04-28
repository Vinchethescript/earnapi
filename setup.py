from setuptools import setup, find_packages
import os
import re

packages = find_packages()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

with open(
    os.path.join(os.path.dirname(__file__), packages[0], "__init__.py"),
    "r",
    encoding="utf-8",
) as f:
    kwargs = {
        var.strip("_"): val
        for var, val in re.findall(
            r'^(__\w+__)\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
        )
    }
    kwargs["author_email"] = kwargs.pop("email", "")

# Setting up
setup(
    name="earnapi",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=packages,
    python_requires=">=3.7",
    install_requires=["aiohttp"],
    keywords=[
        "python",
        "earnapi",
        "python earnapp api",
        "python earnapp api wrapper",
        "earnapp api wrapper",
        "earnapp",
        "passive income",
        "earnapp api",
        "earnapp dashboard",
        "requests",
        "python earnapp",
    ],
    **kwargs
)
