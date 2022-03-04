# Create project (sh project.sh)

DIR="$1"

if [ -d "$DIR" ]; then # directory already exists
    echo "Project directory already exists."
else
    echo "Creating project directory."
    mkdir ${DIR}
fi

cd ${DIR}
pio project init --board esp32dev --project-option="monitor_speed=115200" --project-option "framework=espidf"

