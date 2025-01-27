# PDF to Image API
![image](https://github.com/user-attachments/assets/dfcc1efa-4cf8-4719-bf91-0b89f8f60f69)


This FastAPI application converts the first page of a given PDF file to an image and returns it directly to the client for download. It supports multiple image formats (e.g., PNG, JPEG, TIFF, BMP) and allows adjusting the quality for JPEG outputs.

## Features

- Converts the **first page** of a PDF to an image.
- Supports output image formats:
  - PNG
  - JPEG
  - TIFF
  - BMP
- Allows configuring the JPEG quality (1–100).
- Streams the resulting image directly to the client without saving it to the server's file system.

## Requirements

To run this application, make sure you have the following installed:

- Python 3.8 or higher
- The following Python libraries:
  - `fastapi`
  - `uvicorn`
  - `pdf2image`
  - `Pillow`

You can install the required packages with:

```bash
pip install fastapi uvicorn pdf2image pillow
```

Additionally, you must install **poppler-utils**, which is required by `pdf2image` to process PDF files. Use the following commands depending on your platform:

- **Ubuntu/Linux**:
  ```bash
  sudo apt-get install -y poppler-utils
  ```

- **Windows**:
  1. Download the latest Poppler binary for Windows from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/).
  2. Extract the archive and add the `bin` folder to your system's PATH.

---

## How to Run

1. Save the app code into a file, for example, `app.py`.

2. Start the server using the following command:
   ```bash
   uvicorn app:app --reload
   ```

   After starting, the server will be live at `http://127.0.0.1:8000`.

---

## API Endpoints

### 1. `POST /convert`

This endpoint converts a PDF file into an image.


#### Request Parameters:
| Field Name     | Type        | Required | Description                                                                 |
| -------------- | ----------- | -------- | --------------------------------------------------------------------------- |
| `file`         | `File`      | Yes      | The PDF file to convert.                                                   |
| `image_format` | `str`       | Yes      | The output image format. Must be one of: `PNG`, `JPEG`, `TIFF`, `BMP`.      |
| `quality`      | `int` (1-100)| No       | (Optional) Sets the quality of the image if the format is `JPEG`. Default is `100`. |

#### Example cURL Request:
```bash
curl --location 'http://127.0.0.1:8000/convert' \
--form 'file=@/path/to/your/file.pdf' \
--form 'image_format=JPEG' \
--form 'quality=100' \
--output converted_image.jpeg
```

#### Response:
The API returns the generated image file directly as a downloadable response.

---

## Examples

### Example 1: Convert PDF to PNG
```bash
curl --location 'http://127.0.0.1:8000/convert' \
--form 'file=@/path/to/sample.pdf' \
--form 'image_format=PNG' \
--output output_image.png
```

### Example 2: Convert PDF to JPEG with Quality Adjustment
```bash
curl --location 'http://127.0.0.1:8000/convert' \
--form 'file=@/path/to/sample.pdf' \
--form 'image_format=JPEG' \
--form 'quality=80' \
--output output_image.jpeg
```

---

## Notes

- The API only converts the **first page** of the input PDF.
- **JPEG Quality Configuration:** The `quality` parameter only applies if the output format is `JPEG`. Default is `100` (highest quality).

---

## License
PAVEL CHMIRENKO
This project is open-source and available under the MIT License.
