from setuptools import setup, find_packages

setup(
    name="Serializer-Lasevich",
    version="0.0.1",
    description="library for python serialization as lab",
    url="https://github.com/Eugene-Lasevich/4semLabsIGI/tree/lab3/lab3",
    author="Eugene Lasevich",
    author_email="lasevich009@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["serializers/json", "serializers/dict_serilizer", "serializers/xml", "serializers"],
    include_package_data=True
)
