import os
import logging
from pypdf import PdfReader, PdfWriter

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("PDFService")

class PDFService:
    """
    A service class for handling PDF manipulation operations including
    merging, splitting, and rotating PDF documents.
    """

    def merge_pdfs(self, file_paths: list[str], output_path: str) -> None:
        """
        Merges multiple PDF files into a single output PDF file.

        Args:
            file_paths (list[str]): List of absolute file paths to input PDFs.
            output_path (str): Absolute file path for the output merged PDF.

        Raises:
            ValueError: If fewer than 2 files are provided, or file path list is empty.
            FileNotFoundError: If any of the input files do not exist.
            Exception: For any processing errors.
        """
        if not file_paths or len(file_paths) < 2:
            logger.error("Merge operation requires at least two PDF files.")
            raise ValueError("You must select at least two PDF files to merge.")

        writer = PdfWriter()

        try:
            for path in file_paths:
                if not os.path.exists(path):
                    logger.error(f"File not found: {path}")
                    raise FileNotFoundError(f"Input PDF file not found: {path}")

                logger.info(f"Adding file to merge queue: {path}")
                reader = PdfReader(path)
                writer.append(reader)

            # Ensure the output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            logger.info(f"Successfully merged PDFs into: {output_path}")

        except Exception as e:
            logger.error(f"Error occurred during PDF merge: {str(e)}")
            raise e
        finally:
            writer.close()

    def parse_page_ranges(self, page_ranges_str: str, total_pages: int) -> list[int]:
        """
        Parses a custom page range string (e.g. '1-3, 5, 8-10') and returns a list
        of 0-based page indices.

        Args:
            page_ranges_str (str): The page range input from user (1-indexed).
            total_pages (int): The total pages of the PDF being processed.

        Returns:
            list[int]: Unique sorted list of 0-based page indices.

        Raises:
            ValueError: If the page range format is invalid or references out-of-bound pages.
        """
        if not page_ranges_str or not page_ranges_str.strip():
            raise ValueError("Page range string cannot be empty.")

        page_indices = set()
        parts = page_ranges_str.split(",")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            if "-" in part:
                range_parts = part.split("-")
                if len(range_parts) != 2:
                    raise ValueError(f"Invalid range format: '{part}'")
                
                try:
                    start = int(range_parts[0].strip())
                    end = int(range_parts[1].strip())
                except ValueError:
                    raise ValueError(f"Range values must be integers: '{part}'")

                if start <= 0 or end <= 0:
                    raise ValueError(f"Page numbers must be positive integers: '{part}'")
                if start > end:
                    raise ValueError(f"Start page cannot be greater than end page: '{part}'")
                if end > total_pages:
                    raise ValueError(f"Page range '{part}' exceeds total pages ({total_pages})")

                # Convert to 0-based index and include end page
                for p in range(start - 1, end):
                    page_indices.add(p)
            else:
                try:
                    page_num = int(part)
                except ValueError:
                    raise ValueError(f"Invalid page number: '{part}'")

                if page_num <= 0:
                    raise ValueError(f"Page number must be a positive integer: '{part}'")
                if page_num > total_pages:
                    raise ValueError(f"Page number {page_num} exceeds total pages ({total_pages})")

                page_indices.add(page_num - 1)

        return sorted(list(page_indices))

    def split_pdf(self, file_path: str, page_ranges: str, output_path: str) -> None:
        """
        Extracts specific page ranges from a PDF and saves them to a new PDF.

        Args:
            file_path (str): Path to the input PDF file.
            page_ranges (str): 1-indexed page range list (e.g. '1-3, 5').
            output_path (str): Path for the output PDF containing extracted pages.

        Raises:
            FileNotFoundError: If input file is missing.
            ValueError: If page range is invalid.
            Exception: For other write/read failures.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            logger.info(f"Loaded source PDF with {total_pages} pages: {file_path}")

            target_indices = self.parse_page_ranges(page_ranges, total_pages)
            writer = PdfWriter()

            for idx in target_indices:
                writer.add_page(reader.pages[idx])

            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            logger.info(f"Successfully extracted pages ({page_ranges}) to: {output_path}")

        except Exception as e:
            logger.error(f"Error during PDF splitting: {str(e)}")
            raise e
        finally:
            writer.close()

    def split_all_pages(self, file_path: str, output_dir: str) -> list[str]:
        """
        Splits a single PDF file into individual page files.

        Args:
            file_path (str): Path to the input PDF file.
            output_dir (str): Directory where split page PDFs should be written.

        Returns:
            list[str]: Paths to the generated individual PDF page files.

        Raises:
            FileNotFoundError: If the input file is missing.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        generated_files = []
        base_name = os.path.splitext(os.path.basename(file_path))[0]

        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)

            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                out_file_name = f"{base_name}_page_{i + 1}.pdf"
                out_path = os.path.join(output_dir, out_file_name)

                with open(out_path, "wb") as out_file:
                    writer.write(out_file)

                writer.close()
                generated_files.append(out_path)
                logger.info(f"Extracted single page file: {out_path}")

            return generated_files

        except Exception as e:
            logger.error(f"Error during split all pages: {str(e)}")
            raise e

    def rotate_pdf(self, file_path: str, output_path: str, rotation_angle: int) -> None:
        """
        Rotates all pages of a PDF by a specific angle.

        Args:
            file_path (str): Path to the input PDF file.
            output_path (str): Path for the output rotated PDF.
            rotation_angle (int): Angle of rotation in degrees clockwise (90, 180, 270).

        Raises:
            FileNotFoundError: If the input file is missing.
            ValueError: If the angle is invalid.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

        if rotation_angle not in [90, 180, 270]:
            raise ValueError("Rotation angle must be 90, 180, or 270 degrees.")

        try:
            reader = PdfReader(file_path)
            writer = PdfWriter()

            for page in reader.pages:
                page.rotate(rotation_angle)
                writer.add_page(page)

            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            logger.info(f"Successfully rotated PDF by {rotation_angle} degrees: {output_path}")

        except Exception as e:
            logger.error(f"Error during PDF rotation: {str(e)}")
            raise e
        finally:
            writer.close()
