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
        print(f'image_path: {image_path}')
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
        webp_image_full_path = image_path.split('.')[0] + '.webp'  
        
        # get image str to save in database
        saved_webp_image_database_path = default_storage.save(webp_image_full_path, webp_image)        
        
        # extracting image file name and dir name
        image_dir, image_name = os.path.split(webp_image_full_path)
        
        # building full path of new genarated optimized image.
        # we need to avoid twing of upload path in model   
        # it is needed to rename 
        optimized_full_path =  os.path.normpath(os.path.join(image_dir, os.path.split(saved_webp_image_database_path)[-1]))   
    
    # genarally new new name comes from thumbnail image   
    if new_name is not None:            
        ext = image_name.split('.')[-1]
        new_image_name = f"{new_name}.{ext}" 
        new_full_path = os.path.join(image_dir, new_image_name)   
        if os.path.exists(new_full_path):              
            new_image_name = f"{new_name}_{uuid4().hex[:8]}.{ext}"
            new_full_path = os.path.join(image_dir, new_image_name)                       
        os.rename(optimized_full_path, new_full_path)   
        saved_webp_image = os.path.normpath(os.path.join(os.path.split(saved_webp_image_database_path)[0], new_image_name))       
     
     
    # after optimizing thumbnail then main image we would delete original image we uploaded   
    if delete_original:     
        default_storage.delete(image_path)


    return saved_webp_image

