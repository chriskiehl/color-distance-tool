import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chriskiehl",
    version="0.0.1",
    author="Chris Kiehl",
    author_email="audionautic@gmail.com",
    description="A weirdly hyper-specific tool for selecting arbitrary colors from the screen and comparing them in various color spaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chriskiehl/color-distance-tool",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        "Topic :: Multimedia :: Graphics :: Capture"
    ],
    python_requires='>=3.6',
)