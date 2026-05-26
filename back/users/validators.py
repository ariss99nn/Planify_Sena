from PIL import Image
from django.core.exceptions import ValidationError


# Formatos de imagen permitidos en el sistema
_ALLOWED_FORMATS = {'jpeg', 'png', 'webp'}
_ALLOWED_LABEL = 'JPG, PNG o WEBP'


def _validate_image_base(image, max_mb: int) -> None:
    """Validación compartida de tamaño y formato real para imágenes."""

    # 1. Tamaño
    if image.size > max_mb * 1024 * 1024:
        raise ValidationError(f'La imagen no puede superar {max_mb} MB.')

    # 2. Formato real via Pillow (no confiar en la extensión ni en el Content-Type)
    try:
        img = Image.open(image)
        fmt = (img.format or '').lower()
        if fmt not in _ALLOWED_FORMATS:
            raise ValidationError(
                f'Formato no permitido. Solo se aceptan imágenes {_ALLOWED_LABEL}.'
            )
    except ValidationError:
        raise
    except Exception:
        raise ValidationError('El archivo no es una imagen válida.')
    finally:
        image.seek(0)  # Resetear cursor para que Django pueda guardar el archivo


def validate_imagen(image) -> None:
    """Validador para fotos de perfil de usuario (máx. 2 MB)."""
    _validate_image_base(image, max_mb=2)


def validate_imagen_5mb(image) -> None:
    """
    Validador para imágenes de aulas y bloques (máx. 5 MB).
    Se permite mayor resolución para uso en pantallas grandes.
    """
    _validate_image_base(image, max_mb=5)