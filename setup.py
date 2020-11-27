#!/usr/bin/env python3
from setuptools import setup


PLUGIN_ENTRY_POINT = 'nyumaya_ww_plug=mycroft_wake_word_plugin_nyumaya:NyumayaWakeWordPlugin'
setup(
    name='mycroft_wake_word_plugin_nyumaya',
    version='0.1',
    description='Nyumaya wake word plugin for mycroft',
    url='https://github.com/OpenJarbas/mycroft_wake_word_plugin_nyumaya',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['mycroft_wake_word_plugin_nyumaya'],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mycroft plugin wake word',
    entry_points={'mycroft.plugin.wake_word': PLUGIN_ENTRY_POINT}
)
