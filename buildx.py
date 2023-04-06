import subprocess
from pathlib import Path

BUILDER_NAME = "buildx_builder"
subprocess.run(["docker", "buildx", "create", "--use", f"--name={BUILDER_NAME}"])

PLATFORM = ["linux/amd64", "linux/arm64"]
PLATFORM = ",".join(PLATFORM)

IMAGES = {
    # directory: tag
    "pygo": "nondescriptspoon/pygo:latest"
}

for directory, tag in IMAGES.items():
    print(f"Building image in {directory} with tag {tag}")
    dockerfile = Path(f"{directory}/Dockerfile").read_bytes()

    # This will read a Dockerfile from STDIN without context. Due to the lack of a context, no contents of any local
    # directory will be sent to the Docker daemon. See https://stackoverflow.com/a/54666214/8010877
    read_dockerfile_from_stdin = "-"

    subprocess.run(
        [
            "docker",
            "buildx",
            "build",
            "--platform",
            PLATFORM,
            "--push",
            "-t",
            tag,
            read_dockerfile_from_stdin,
        ],
        input=dockerfile,  # This pipes the Dockerfile into stdin.
    )

subprocess.run(["docker", "buildx", "rm", "--keep-state", BUILDER_NAME])
