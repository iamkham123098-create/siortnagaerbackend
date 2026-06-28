from django.core.exceptions import ValidationError


def validate_file_size(file):
    """
    Validate that uploaded file is not larger than 3MB.
    """
    max_size = 3 * 1024 * 1024  # 3MB in bytes
    
    if hasattr(file, 'size') and file.size > max_size:
        raise ValidationError(
            f"File size must be no more than 3MB. Your file is {file.size / (1024 * 1024):.2f}MB."
        )
