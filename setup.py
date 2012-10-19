try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_desc=open('README.rst','r').read()

setup(name="pyclj",
      version="0.2.0",
      author="Sun Ning",
      author_email="sunng@about.me",
      description="clojure literal reader and writer for python",
      long_description=long_desc,
      url="http://github.com/sunng87/pyclj",
      install_requires=["pyRFC3339"],
      license='mit',
      py_modules=['clj'],
      classifiers=['Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Topic :: Software Development',
            'Programming Language :: Python',
            'Operating System :: OS Independent']
    )
