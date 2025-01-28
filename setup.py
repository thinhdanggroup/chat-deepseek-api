from setuptools import setup, find_packages

def read_long_description():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name='chat_deepseek_api',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'certifi>=2024.12.14',
        'charset-normalizer>=3.4.1',
        'idna>=3.10',
        'python-dotenv>=1.0.1',
        'requests>=2.32.0',
        'urllib3>=2.2.0',
        'PyJWT>=2.4.0',
        'aiofiles>=23.2.0',
        'aiohttp>=3.9.2',
        'pydantic'
    ],
    description='An unofficial Python API wrapper for chat.deepseek.com',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    author='Thinh Dang',
    url='https://github.com/thinhdanggroup/chat-deepseek-api',
    license_files=('LICENSE',),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)
