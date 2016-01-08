from distutils.core import setup

setup(name="quickplots",
      version="1.0.0",
      description="A simple plotting library",
      long_description="A Python plotting library with simplicty and intuition as its primary goals",
      url="https://quickplots.readthedocs.org",
      author="Sam Ireland",
      author_email="sam.ireland.uk@gmail.com",
      classifiers=["Development Status :: 4 - Beta",
                   "Programming Language :: Python :: 3"],
      py_modules=["quickplotss"],
      install_requires=["matplotlib"])
