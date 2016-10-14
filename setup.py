from setuptools import find_packages
from setuptools import setup

import os

version = open(
    os.path.join("Products", "PloneSurvey", "version.txt")
).read().strip()

description = "Plone Survey is an addon collecting data from people."

longdesc = open("README.rst").read()
longdesc += open(os.path.join("docs", "HISTORY.rst")).read()

setup(
    name='Products.PloneSurvey',
    version=version,
    description=description,
    long_description=longdesc,
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='Plone, Survey',
    author='Michael Davis',
    author_email='m.r.davis@me.com',
    url='http://plone.org/products/plonesurvey',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Products.CMFPlone',
        'z3c.rml<2.6.0',
        'reportlab<3.0',
    ],
    extras_require={
        "test": ["plone.app.testing",
                 "collective.recaptcha", ],
    },
    entry_points="""
    # -*- Entry points: -*-
    """,
)
