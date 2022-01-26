from re import search
from subprocess import check_output
from os import path
from pathlib import Path
from csv import writer

# generates results for all testsets in the "testsets" folder, each subfolder
# should contain a set of songs from the "datasets" folder with the same
# names and processed with a different parameter combination, and the subfolder
# should have a name of the form:
# "[segment_length]_[segment_start]_[noise_level]_[noise_type]"

with open("results.csv", "w", newline='') as results_file:
    csv_writer = writer(results_file)
    csv_writer.writerow(["Segment Length (s)", "Segment Start (s)",
                         "Noise Level", "Noise Type", "Compression Type",
                         "Accuracy"])

for parameter_set_dir in Path("testsets").iterdir():

    test_parameters = path.basename(parameter_set_dir).split("_")

    segment_length = test_parameters[0]
    segment_start = test_parameters[1]
    noise_level = test_parameters[2]
    noise_type = test_parameters[3]

    for compression_type in ["gzip", "bzip2", "lzma"]:

        accuracy_count, total_count = 0, 0
        for target_file in Path(parameter_set_dir).rglob("*.wav"):

            target_name = path.basename(target_file).split('.')[0]

            output = check_output(["python", "./src/main.py",
                                   "--dataset", "datasets",
                                   "--target", target_file,
                                   "--compression", compression_type])

            predicted_name = path.basename(
                search("\('(.*)\.wav", str(output)).group(1))

            accuracy_count += predicted_name == target_name
            total_count += 1

        accuracy = accuracy_count / total_count

        with open("results.csv", "a", newline='') as results_file:
            csv_writer = writer(results_file)
            csv_writer.writerow([segment_length, segment_start, noise_level,
                                 noise_type, compression_type,
                                 f"{accuracy:.2%}"])
