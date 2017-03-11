from setuptools import setup
import io


req_file = open('requirements.txt')
reqs = req_file.read().strip().split('\n')

with io.open('README.md', encoding='utf-8') as f:
    README = f.read()

setup_args = {
    'description': 'Flask Cloudant Interface',
    'long_description': README,
    'include_package_data': True,
    'install_requires': reqs,
    'name': 'flask-cloudant',
    'version': '0.0.1.dev',
    'author': 'porthunt',
    'author_email': 'jportela.gomez@gmail.com',
    'url': 'https://github.com/porthunt/flask-cloudant',
    'packages': ['flask_cloudant'],
    'classifiers': [
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development :: Libraries :: Python Module',
          'Operating System :: OS Independent',
          'Development Status :: 1 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5'
      ]
}

setup(**setup_args)
