try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="pyclj",
      version="0.1.1",
      author="Sun Ning",
      author_email="sunng@about.me",
      description="clojure literal reader and writer for python",
      url="http://github.com/sunng87/pyclj",
      license='mit',
      classifiers=['Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Topic :: Software Development',
            'Programming Language :: Python',
            'Operating System :: OS Independent']
    )
