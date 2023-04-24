from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "ORM for postgres"
LONG_DESCRIPTION = """
A package that allows to use orm for serverless lambda so we can open and close connection and
it will never cost money """

# Setting up
setup(
    name="poster",
    version=VERSION,
    author="Ichego (Mohamed Salah)",
    author_email="<emohamed250@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["psycopg2"],
    keywords=["python", "orm", "postgres"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)