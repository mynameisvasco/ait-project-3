from os import mkdir
from pathlib import Path, PurePath
import subprocess
from shutil import rmtree

if not Path("testsets").exists():
    mkdir("testsets")
else:
    for existing_file in Path("testsets").iterdir():
        if existing_file.is_dir():
            rmtree(existing_file)

for segment_length in [5, 30]:
    for segment_start in [30, 120]:
        for noise_level in [0.2, 0.9]:
            for noise_type in ["whitenoise", "brownnoise", "pinknoise"]:

                testset_dir = f"testsets/{segment_length}_{segment_start}_{noise_level}_{noise_type}"

                if not Path(testset_dir).exists():
                    mkdir(testset_dir)

                for target_file in Path("datasets").rglob("*.wav"):

                    processed_file_path = PurePath(testset_dir).joinpath(target_file.name)

                    sox_piped_cmd = f"sox {target_file} -p synth {noise_type} vol {noise_level}"
                    proc1 = subprocess.Popen(sox_piped_cmd.split(" "),
                                             stdout=subprocess.PIPE)

                    sox_final_cmd = f"sox -m {target_file} - {processed_file_path} trim {segment_start} {segment_length}"
                    proc2 = subprocess.run(sox_final_cmd.split(" "),
                                           stdin=proc1.stdout)
