import os
import pytest
from pypdf import PdfWriter, PdfReader
from services.pdf_service import PDFService

def create_dummy_pdf(path: str, page_count: int = 1):
    """Utility helper to create a dummy PDF file with a set page count."""
    writer = PdfWriter()
    for _ in range(page_count):
        # Add a blank page
        writer.add_blank_page(width=72 * 8.5, height=72 * 11)
    with open(path, "wb") as f:
        writer.write(f)
    writer.close()

@pytest.fixture
def pdf_service():
    return PDFService()

@pytest.fixture
def sample_pdfs(tmp_path):
    """Fixture to generate two sample PDFs for testing merging and splitting."""
    pdf1_path = os.path.join(tmp_path, "sample1.pdf")
    pdf2_path = os.path.join(tmp_path, "sample2.pdf")
    
    create_dummy_pdf(pdf1_path, page_count=3)  # 3-page PDF
    create_dummy_pdf(pdf2_path, page_count=2)  # 2-page PDF
    
    return pdf1_path, pdf2_path

def test_merge_pdfs_success(pdf_service, sample_pdfs, tmp_path):
    pdf1, pdf2 = sample_pdfs
    output_pdf = os.path.join(tmp_path, "merged.pdf")
    
    pdf_service.merge_pdfs([pdf1, pdf2], output_pdf)
    
    assert os.path.exists(output_pdf)
    reader = PdfReader(output_pdf)
    assert len(reader.pages) == 5  # 3 + 2 = 5 pages

def test_merge_pdfs_insufficient_files(pdf_service, sample_pdfs, tmp_path):
    pdf1, _ = sample_pdfs
    output_pdf = os.path.join(tmp_path, "merged.pdf")
    
    with pytest.raises(ValueError, match="You must select at least two PDF files to merge."):
        pdf_service.merge_pdfs([pdf1], output_pdf)

def test_merge_pdfs_file_not_found(pdf_service, tmp_path):
    non_existent = os.path.join(tmp_path, "does_not_exist.pdf")
    output_pdf = os.path.join(tmp_path, "merged.pdf")
    
    with pytest.raises(FileNotFoundError):
        pdf_service.merge_pdfs([non_existent, non_existent], output_pdf)

def test_parse_page_ranges_valid(pdf_service):
    # Test valid standard formats
    assert pdf_service.parse_page_ranges("1-3", 5) == [0, 1, 2]
    assert pdf_service.parse_page_ranges("1, 3, 5", 5) == [0, 2, 4]
    assert pdf_service.parse_page_ranges("1-2, 4-5, 3", 5) == [0, 1, 2, 3, 4]
    assert pdf_service.parse_page_ranges(" 2-4, 1 ", 5) == [0, 1, 2, 3]

def test_parse_page_ranges_invalid(pdf_service):
    with pytest.raises(ValueError):
        pdf_service.parse_page_ranges("1-6", 5)  # Out of range
    with pytest.raises(ValueError):
        pdf_service.parse_page_ranges("0", 5)  # Invalid 1-based index
    with pytest.raises(ValueError):
        pdf_service.parse_page_ranges("3-1", 5)  # Start > End
    with pytest.raises(ValueError):
        pdf_service.parse_page_ranges("abc", 5)  # Non-integer

def test_split_pdf_success(pdf_service, sample_pdfs, tmp_path):
    pdf1, _ = sample_pdfs  # pdf1 has 3 pages
    output_pdf = os.path.join(tmp_path, "extracted.pdf")
    
    pdf_service.split_pdf(pdf1, "1, 3", output_pdf)
    
    assert os.path.exists(output_pdf)
    reader = PdfReader(output_pdf)
    assert len(reader.pages) == 2

def test_split_all_pages_success(pdf_service, sample_pdfs, tmp_path):
    pdf1, _ = sample_pdfs  # pdf1 has 3 pages
    out_dir = os.path.join(tmp_path, "split_pages")
    
    generated = pdf_service.split_all_pages(pdf1, out_dir)
    
    assert len(generated) == 3
    for file_path in generated:
        assert os.path.exists(file_path)
        reader = PdfReader(file_path)
        assert len(reader.pages) == 1

def test_rotate_pdf_success(pdf_service, sample_pdfs, tmp_path):
    pdf1, _ = sample_pdfs
    output_pdf = os.path.join(tmp_path, "rotated.pdf")
    
    pdf_service.rotate_pdf(pdf1, output_pdf, 90)
    
    assert os.path.exists(output_pdf)
    reader = PdfReader(output_pdf)
    assert len(reader.pages) == 3
    # First page should be rotated 90 degrees
    assert reader.pages[0].rotation == 90

def test_rotate_pdf_invalid_angle(pdf_service, sample_pdfs, tmp_path):
    pdf1, _ = sample_pdfs
    output_pdf = os.path.join(tmp_path, "rotated.pdf")
    
    with pytest.raises(ValueError, match="Rotation angle must be 90, 180, or 270 degrees."):
        pdf_service.rotate_pdf(pdf1, output_pdf, 45)
