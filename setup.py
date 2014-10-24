from setuptools import setup, find_packages

try:
   import pypandoc
   description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
   description = ''

setup(name='bai-indexer',
      version='0.1.1',
      description='An index for your BAM Index (BAI)',
      long_description=description,
      author='Dan Vanderkam',
      author_email='danvdk@gmail.com',
      url='https://github.com/danvk/bai-indexer/',
      entry_points={
          'console_scripts': [
              'bai-indexer = bai_indexer:run',
          ],
      },
      packages=find_packages(exclude=['tests*']),
      install_requires=[],
      classifiers=[
          'Environment :: Console',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Healthcare Industry',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Scientific/Engineering :: Bio-Informatics'
      ],
)
