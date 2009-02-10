from setuptools import setup, find_packages
import os

version = '1.3.0'

setup(name='Products.PloneSurvey',
      version=version,
      description="Plone Survey is a simple product written to collect data from people - feedback on a course, simple data collection etc.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Plone, Survey',
      author='Seb Bacon',
      author_email='',
      url='http://plone.org/products/plone-survey',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
