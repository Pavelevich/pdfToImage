import io

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from pdf2image import convert_from_bytes

app = FastAPI(title="PDF to Image API")

SUPPORTED_FORMATS = ["PNG", "JPEG", "TIFF", "BMP"]


@app.post("/convert")
async def convert_pdf(
        file: UploadFile = File(...),
        image_format: str = Form(...),
        quality: int = Form(100)
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
