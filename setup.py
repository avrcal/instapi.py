from setuptools import setup, find_packages

setup(
    name="instapi.py",
    version="0.2.0",
    author="avrcal',
    description="Instagram API client with event-driven architecture",
    packages=find_packages(),
    install_requires=[
        "instagrapi>=1.20.0",
        "python-dotenv>=1.0.0",
        "aiohttp>=3.8.1"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    python_requires=">=3.8",
    include_package_data=True
)
