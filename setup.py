from setuptools import setup, find_packages

setup(
    name="content_generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'click>=8.1.7',
        'langchain>=0.1.0',
        'python-dotenv>=1.0.0',
        'openai>=1.3.0',
        'tiktoken>=0.5.2',
        'markdown>=3.5.1',
        'pyyaml>=6.0.1',
    ],
    entry_points={
        'console_scripts': [
            'content-generator=content_generator.content_generator:main',
        ],
    },
)
