import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Setting up
setuptools.setup(
    name="earnapi",
    version="1.0.5",
    author="Vinche.zsh",
    author_email="vincysuper07@gmail.com",
    description="Asynchronous EarnApp API wrapper written in Python.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=["earnapi"],
    python_requires=">=3.7",
    install_requires=["aiohttp"],
    url="https://github.com/Vincydotzsh/earnapi",
    project_urls={
        "Bug Tracker": "https://github.com/Vincydotzsh/earnapi/issues",
    },
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
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
