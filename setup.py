from setuptools import setup, find_packages


def read_requirements(filename="requirements.txt"):
    "Read the requirements"
    with open(filename) as f:
        return [line.strip() for line in f \
                if line.strip() and \
                line[0].strip() != '#' and \
                not line.startswith('-e ')]


def get_version(filename='gnuplot_data/version.py', name='VERSION'):
    "Get the version"
    with open(filename) as f:
        s = f.read()
        d = {}
        exec(s, d)
        return d[name]


setup(
    name='python-gnuplot-data',
    version='0.3.0',
    author='Dave Gabrielson',
    author_email='Dave.Gabrielson@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['setuptools',],
)
