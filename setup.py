import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='zhtools',
    version='0.3.0',
    author='zhyipeng',
    author_email='zhyipeng@outlook.com',
    description='Some simple tool methods like cache, exporter and so on.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zhyipeng/zhtools',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': ['zhtools=zhtools.cli:execute_from_command_line'],
    }
)
