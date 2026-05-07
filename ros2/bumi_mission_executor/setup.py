import os

from setuptools import find_packages, setup

package_name = "boomy_mission_executor"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            os.path.join("share", package_name, "launch"),
            [os.path.join("launch", "mission_executor.launch.py")],
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Yahboom MCP",
    maintainer_email="dev@local",
    description="Executor for /boomy/mission JSON plans from yahboom-mcp",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "mission_executor = boomy_mission_executor.mission_executor_node:main",
        ],
    },
)
