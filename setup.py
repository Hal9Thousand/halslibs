from setuptools import setup, find_packages

setup(
    name='halslibs', 
    version='0.0.1',
    author='Hal Thornton', 
    author_email='halbrianthornton@gmail.com',
    url='https://github.com/Hal9Thousand/halslibs',
    description='Python Libraries for Common Tasks',
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    license="MIT",
    license_files=["LICENSE.txt"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True, 
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: Other/Proprietary License',
    ],
    python_requires='>=3.10.12',
    install_requires=[],
)