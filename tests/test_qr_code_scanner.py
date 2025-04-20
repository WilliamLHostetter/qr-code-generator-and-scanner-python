from qr_code_scanner import scan_qr_code
import pytest

test_data_folder = "./tests/data/"


def test_scan_qr_code():
    '''
    Testing scan_qr_code(image_filepath)
    '''
    image_filepath = test_data_folder + "QR_Code_Scanner.png"
    expected = "QR Code Scanner"
    assert scan_qr_code(image_filepath) == expected


def test_small_image_size():
    '''
    Testing scan_qr_code(image_filepath) with QR Code generated 
    with small image size (120x120)
    '''
    image_filepath = test_data_folder + "image_size_small.png"
    expected = "Unit test for small image size"
    assert scan_qr_code(image_filepath) == expected


def test_medium_image_size():
    '''
    Testing scan_qr_code(image_filepath) with QR Code generated 
    with medium image size (230x230)
    '''
    image_filepath = test_data_folder + "image_size_medium.png"
    expected = "Unit test for medium image size"
    assert scan_qr_code(image_filepath) == expected


def test_large_image_size():
    '''
    Testing scan_qr_code(image_filepath) with QR Code generated 
    with large image size (350x350)
    '''
    image_filepath = test_data_folder + "image_size_large.png"
    expected = "Unit test for large image size"
    assert scan_qr_code(image_filepath) == expected


def test_error_correction_L():
    '''
    Testing scan_qr_code(image_filepath) with QR Code generated 
    with the error correction L option
    '''
    image_filepath = test_data_folder + "error_correction_L.png"
    expected = "Unit test for error correction L option"
    assert scan_qr_code(image_filepath) == expected


def test_error_correction_M():
    '''
    Testing scan_qr_code(image_filepath) with QR Code generated 
    with the error correction M option
    '''
    image_filepath = test_data_folder + "error_correction_M.png"
    expected = "Unit test for error correction M option"
    assert scan_qr_code(image_filepath) == expected


def test_error_correction_Q():
    '''
    Testing scan_qr_code(image_filepath) with QR Code generated 
    with the error correction Q option
    '''
    image_filepath = test_data_folder + "error_correction_Q.png"
    expected = "Unit test for error correction Q option"
    assert scan_qr_code(image_filepath) == expected


def test_error_correction_H():
    '''
    Testing scan_qr_code(image_filepath) with QR Code generated 
    with the error correction H option
    '''
    image_filepath = test_data_folder + "error_correction_H.png"
    expected = "Unit test for error correction H option"
    assert scan_qr_code(image_filepath) == expected
