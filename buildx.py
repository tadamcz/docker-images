import subprocess
from pathlib import Path

BUILDER_NAME = "buildx_builder"
PROJECT_ROOT = Path(__file__).parent

subprocess.run(["docker", "buildx", "create", "--use", f"--name={BUILDER_NAME}"])

PLATFORM = ["linux/amd64", "linux/arm64"]

PLATFORM = ",".join(PLATFORM)

IMAGES = {
    # directory: tag
    "pygo": "nondescriptspoon/pygo:latest"
}

for directory, tag in IMAGES.items():
    print(f"Building image in {directory} with tag {tag}")
    dockerfile = Path(f"{directory}/Dockerfile").absolute()
    dockerfile = dockerfile.read_bytes()
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
        input=dockerfile,
    )

subprocess.run(["docker", "buildx", "rm", "--keep-state", BUILDER_NAME])
