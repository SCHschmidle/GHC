from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()
result, elapse = ocr('image.png')

# Extract text
text = ' '.join([line[1] for line in result])
print(text)