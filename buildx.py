import subprocess
from pathlib import Path

BUILDER_NAME = "nondescriptspoon_buildx_builder"
subprocess.run(["docker", "buildx", "create", "--use", f"--name={BUILDER_NAME}"])

PLATFORM = ["linux/amd64", "linux/arm64"]
PLATFORM = ",".join(PLATFORM)

DOCKER_HUB_USERNAME = "nondescriptspoon"
IMAGE_DIRS = ["pygo"]


images = {
    # path: tag
}
for image_dir in IMAGE_DIRS:
    for dockerfile in Path(image_dir).glob("*.Dockerfile"):
        version_tag = dockerfile.stem
        tag = f"{DOCKER_HUB_USERNAME}/{image_dir}:{version_tag}"
        images[dockerfile] = tag

for path, tag in images.items():
    print(f"Building {tag}...")
    dockerfile = path.read_bytes()

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
