import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot_plugin_maze",
    version="0.2.3",
    author="T_EtherLeaF",
    author_email="thetapilla@gmail.com",
    keywords=["pip", "nonebot2", "nonebot", "nonebot_plugin"],
    description="""NoneBot2交互式走迷宫插件""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EtherLeaF/nonebot_plugin_maze",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    platforms="any",
    install_requires=['nonebot-adapter-onebot>=2.1.0',
                      'nonebot2>=2.0.0-beta.2',
                      'pillow>=9.0.0',
                      'asyncer>=0.0.1'
                      ],
    python_requires=">=3.8"
)
