import email
import os
import os.path

from email.policy import default


def extract_mhtml(file_path: str, output_dir: str="."):
    """Extracts resources from an MHTML file and saves them to a directory.

    Args:
        file_path (str): Path to the MHTML file.
        output_dir (str): Directory where extracted files will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(file_path, "rb") as fp:
        msg = email.message_from_binary_file(fp, policy=default)

    boundary = msg.get_boundary()
    if not boundary:
        raise ValueError("MHTML file is missing the boundary string.")
    
    for part in msg.iter_parts():
        content_type = part.get_content_type()
        content_id = part.get("Content-ID")
        content_location = part.get("Content-Location")

        if content_location:
            filename = os.path.basename(content_location)
        else:
            ext = os.path.basename(content_type)
            filename = os.path.basename(content_id) + "." + ext

        with open(os.path.join(output_dir, filename), "wb") as out_file:
            out_file.write(part.get_payload(decode=True))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Extract resources from an MHTML file.")
    parser.add_argument("file_path", help="Path to the MHTML file.")
    parser.add_argument("-o", "--output-dir", default=".", help="Directory to save extracted files.")
    args = parser.parse_args()

    extract_mhtml(args.file_path, args.output_dir)
