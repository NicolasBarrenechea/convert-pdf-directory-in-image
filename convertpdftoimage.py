import os
import argparse
from pdf2image import convert_from_path


def is_pdf(filename):
    return filename.lower().endswith('.pdf')

def convert_pdf_to_images(pdf_path, output_dir, format='PNG', dpi=200):
    try:
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        # Convertir PDF a imágenes
        images = convert_from_path(pdf_path, dpi=dpi)
        num_pages = len(images)
        
        if num_pages == 1:
            # Si solo tiene una página, guardar directamente en output_dir
            image_path = os.path.join(output_dir, f"{pdf_name}.{format.lower()}")
            images[0].save(image_path, format)
            print(f"Convertido: {pdf_path} (1 página)")
        else:
            # Si tiene múltiples páginas, crear una carpeta para el PDF
            pdf_output_dir = os.path.join(output_dir, pdf_name)
            if not os.path.exists(pdf_output_dir):
                os.makedirs(pdf_output_dir)
            
            # Guardar cada página como una imagen separada
            for i, image in enumerate(images):
                image_path = os.path.join(pdf_output_dir, f"{pdf_name}_page_{i+1}.{format.lower()}")
                image.save(image_path, format)
            
            print(f"Convertido: {pdf_path} ({num_pages} páginas)")
    except Exception as e:
        print(f"Error al convertir el PDF {pdf_path}: {e}")

def process_directory(base_dir, output_dir, format='PNG', dpi=200):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Recorrer todos los archivos y directorios
    for root, dirs, files in os.walk(base_dir):
        # Evitar procesar el directorio de salida
        if os.path.abspath(root).startswith(os.path.abspath(output_dir)):
            continue
        
        # Procesar archivos PDF
        pdf_files = [f for f in files if is_pdf(f)]
        for pdf_file in pdf_files:
            pdf_path = os.path.join(root, pdf_file)
            convert_pdf_to_images(pdf_path, output_dir, format, dpi)

def main():
    parser = argparse.ArgumentParser(description="Convertir PDFs a imágenes")
    parser.add_argument("directory", help="Ruta del directorio con PDFs")
    parser.add_argument("-o", "--output", help="Directorio de salida para las imágenes", default=None)
    parser.add_argument("-f", "--format", help="Formato de imagen (PNG, JPEG, etc.)", default="PNG")
    parser.add_argument("-d", "--dpi", help="Resolución en DPI", type=int, default=200)
    args = parser.parse_args()
    
    # Si no se proporciona un directorio de salida, usar uno dentro del directorio actual
    if args.output is None:
        args.output = os.path.join(args.directory, "converted_images")
    
    process_directory(args.directory, args.output, args.format, args.dpi)
    print(f"Conversión completada. Las imágenes se guardaron en {args.output}")

if __name__ == "__main__":
    main()