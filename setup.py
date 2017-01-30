from setuptools import setup

setup(
 name="quickplots",
 version="2.1.0",
 description="A simple plotting library",
 long_description="A Python plotting library with simplicty and intuition as its primary goals",
 url="https://quickplots.readthedocs.io",
 author="Sam Ireland",
 author_email="mail@samireland.com",
 license="MIT",
 classifiers=[
  "Development Status :: 4 - Beta",
  "Intended Audience :: Science/Research",
  "License :: OSI Approved :: MIT License",
  "Topic :: Scientific/Engineering :: Visualization",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.0",
  "Programming Language :: Python :: 3.1",
  "Programming Language :: Python :: 3.2",
  "Programming Language :: Python :: 3.3",
  "Programming Language :: Python :: 3.4",
  "Programming Language :: Python :: 3.5",
 ],
 keywords="charts graphs data",
 packages=["quickplots"],
 install_requires=["omnicanvas"]
)
