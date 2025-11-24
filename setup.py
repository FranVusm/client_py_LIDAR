from setuptools import setup, find_packages

setup(
    name="si3-opcua-client",
    version="0.1.0",
    description="Clean architecture OPC UA client for SI3 monitoring and history with Bokeh visualization",
    python_requires=">=3.8",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "asyncua",
        "bokeh",
        "tornado",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "si3-client = si3_opcua_client.cli:main",
        ]
    },
    include_package_data=True,
)
