import tarfile

# Set the path to the .tar file
tar_file_path = "../yelp_dataset.tar"

# Open the .tar file for reading
with tarfile.open(tar_file_path, "r") as tar_file:

    # Extract all files in the .tar file to a subdirectory named "extracted_files"
    tar_file.extractall("extracted_files")
