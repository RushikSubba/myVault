import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='myVault',
    version='0.1',
    descrption='Python password manager',
    long_description=long_description,
    author='Subba Rushik',
    author_email='rushiksubba99@gmail.com',
    url='https://github.com/RushikSubba/myVault',
    license='MIT',
    packages=['myVault', 'myVault.models'],
    package_dir={'myVault': 'src'},
    install_requires=['bcrypt==3.1.6', 'pycryptodome==3.8.2', 'SQLAlchemy==1.3.4'],
    classifiers=[
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
    ],

)