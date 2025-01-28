from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req:
        content = req.read()
        requirements = content.split('\n')
    return requirements


setup(
    name='chat_deepseek_api',
    version='0.1.1',
    packages=find_packages(),
    install_requires=read_requirements(),
    description='An unofficial Python API wrapper for chat.deepseek.com',
)