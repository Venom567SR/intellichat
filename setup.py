from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    requirements = []
    try:
        with open('requirements.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('-e'):
                    requirements.append(line)
    except FileNotFoundError:
        print("requirements.txt file not found. Make sure it exists!")
    return requirements

setup(
    name="intellisupport",
    version="0.1.0",
    description="Intelligent Customer Support Agent",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=get_requirements(),
)
