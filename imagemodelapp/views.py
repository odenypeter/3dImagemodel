from django.conf import settings
from django.shortcuts import render
from .models import (Image, GeneratedFile)

from .utils.uncalibrated_rec import (construct_3d_model,)
from os.path import join


def index(request):
    """
    Renders the index.html
    :param request:
    :return:
    """
    # Handle for posting
    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        file_name = data.get('file_name', None)
        if file_name:
            # save the information about the model to be created
            generated_model = GeneratedFile.objects.create(file_name=file_name)

            # save the individual images
            if generated_model:
                images = files.getlist('images')
                # save the individual images
                if images:
                    for image in images:
                        saved_image = Image(generated_file=generated_model, image=image)
                        saved_image.save()

                    # Construct the 3D model
                    construct_3d_model(generated_model)

    # render available 3D models for listing on the table
    return render(request, 'index.html', {
        'generated_files': GeneratedFile.objects.prefetch_related('model_images').all()
    })
