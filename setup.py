from setuptools import setup, find_packages

packages = find_packages(exclude=['human-eval', 'media','root','scripts'])

# Read the requirements file and extract package names
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='safuraireflexion',
      version='0.0.1',
      description="python library to apply reflexion algorithm",
      long_description="",
      author="Matheus Sasso",
      author_email="sasso@safurai.com",
      license='MIT',
      packages=packages,
      install_requires=install_requires
)