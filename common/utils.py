import os
from uuid import uuid4
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image

def optimize_image_for_web(image_path, delete_original: bool, new_name=None, height=None, width=None, quality=85):
    """
    Optimize image for web use, change its height or width if supplied, overwrite the original image,
    and return the path of the optimized image in webp format.
    
    :param image_path: The path to the original image.
    :param new_name: New name of the original image as supplied.   
    :param height: Optional. New height for the image.
    :param width: Optional. New width for the image.
    :return: The django path to the optimized webp image.
    
    example use: optimized_webp = optimize_image_for_web(image_field.path)
    """
    # Open the image
    with default_storage.open(image_path, 'rb') as image_file:
        image = Image.open(image_file)

        # If height or width is provided, resize the image
        if height or width:
            # Calculate new size maintaining the aspect ratio
            original_width, original_height = image.size
            if height and not width:
                width = int((height / original_height) * original_width)
            elif width and not height:
                height = int((width / original_width) * original_height)
            new_size = (width, height)
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        # Convert image to webp
        image = image.convert("RGB")
        webp_image = ContentFile(b'')
        image.save(webp_image, 'webp', quality=quality)
        webp_image.seek(0)

        # Overwrite the original image with the optimized one
        optimized_image_path = image_path.split('.')[0] + '.webp'  
        saved_image = default_storage.save(optimized_image_path, webp_image)
        
        
    if new_name is not None:        
        directory, filename = os.path.split(optimized_image_path)  
        ext = filename.split('.')[-1]
        new_filename = f"{new_name}.{ext}" 
        new_path = os.path.join(directory, new_filename)   
        if os.path.exists(new_path):              
            new_filename = f"{new_name}_{uuid4().hex[:8]}.{ext}"
            new_path = os.path.join(directory, new_filename)  
            
        # Make sure the file is closed before renaming
        
        os.rename(optimized_image_path, new_path)  # Rename the file
        # saved_image = new_path
 
        # os.rename(optimized_image_path, new_path)            
        saved_directory, _ = os.path.split(saved_image)            
        saved_image = (os.path.join(saved_directory, new_filename)).replace("\\", "/")  
        
    if delete_original:      
        default_storage.delete(image_path)


    return saved_image

