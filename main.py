import io
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from pdf2image import convert_from_bytes
from PIL import Image

app = FastAPI(title="PDF to Image API")

SUPPORTED_FORMATS = ["PNG", "JPEG", "TIFF", "BMP"]


@app.post("/convert")
async def convert_pdf(
        file: UploadFile = File(...),
        image_format: str = Form(...),
        quality: int = Form(100),
        width: int = Form(None),  # Optional width parameter
        height: int = Form(None)  # Optional height parameter
):
    image_format = image_format.upper()
    if image_format not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format. Supported formats: {SUPPORTED_FORMATS}"
        )

    try:
        pdf_bytes = await file.read()
        pages = convert_from_bytes(pdf_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing the PDF: {str(e)}"
        )

    if not pages:
        raise HTTPException(
            status_code=400,
            detail="The PDF does not contain any pages."
        )

    first_page = pages[0]

    if width or height:
        try:
            original_width, original_height = first_page.size
            if width and not height:
                # Calculate height based on the aspect ratio
                height = int((width / original_width) * original_height)
            elif height and not width:
                # Calculate width based on the aspect ratio
                width = int((height / original_height) * original_width)

            first_page = first_page.resize(
                (width, height), Image.Resampling.LANCZOS  # Use LANCZOS for high-quality resizing
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error resizing the image: {str(e)}"
            )

    save_kwargs = {}
    if image_format == "JPEG":
        save_kwargs["quality"] = quality
        save_kwargs["optimize"] = True

    image_buffer = io.BytesIO()
    try:
        first_page.save(image_buffer, format=image_format, **save_kwargs)
        image_buffer.seek(0)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving the image: {str(e)}"
        )

    return StreamingResponse(
        image_buffer,
        media_type=f"image/{image_format.lower()}",
        headers={
            "Content-Disposition": f"attachment; filename=converted_image.{image_format.lower()}"
        }
    )


@app.post("/pdf-info")
async def pdf_info(file: UploadFile = File(...)):
    """
    Endpoint to extract information about the uploaded PDF.
    Returns details such as:
    - Number of pages
    - Dimensions (width, height) of the first page
    - DPI of the first page
    - Format of the pages
    """
    try:
        pdf_bytes = await file.read()

        pages = convert_from_bytes(pdf_bytes)

        if not pages:
            raise HTTPException(
                status_code=400,
                detail="The PDF does not contain any pages."
            )

        first_page = pages[0]
        width, height = first_page.size
        dpi = first_page.info.get('dpi', (72, 72))
        format = first_page.format or "Unknown"

        pdf_info = {
            "pages": len(pages),
            "width": width,
            "height": height,
            "dpi": dpi,
            "format": format
        }

        return JSONResponse(content=pdf_info)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing the PDF: {str(e)}"
        )