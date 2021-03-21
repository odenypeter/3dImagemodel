from django.conf import settings
from django.shortcuts import render
from .models import (Image, GeneratedFile)

from .utils.uncalibrated_rec import (construct_3d_model,)
from os.path import join


def index(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        file_name = data.get('file_name', None)
        if file_name:
            generated_model = GeneratedFile.objects.create(file_name=file_name)

            if generated_model:
                images = files.getlist('images')
                # save the individual images
                if images:
                    for image in images:
                        saved_image = Image(generated_file=generated_model, image=image)
                        saved_image.save()
                    # save generated model
                    path = join(settings.MEDIA_ROOT, 'features', 'features_poster.txt')
                    construct_3d_model(generated_model)

    return render(request, 'index.html', {
        'generated_files': GeneratedFile.objects.prefetch_related('model_images').all()
    })
