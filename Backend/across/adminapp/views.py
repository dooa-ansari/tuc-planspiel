from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage

@csrf_exempt
@require_POST
def upload_file(request):
    try:
            uploaded_files = request.FILES.getlist('files')

            # Specify the directory where you want to save the files
            upload_directory = 'uploads/'

            # Create a FileSystemStorage instance with the upload directory
            fs = FileSystemStorage(location=upload_directory)

            # Process and save the uploaded files
            saved_files = []
            for file in uploaded_files:
                saved_file = fs.save(file.name, file)
                saved_files.append(saved_file)

            return JsonResponse({'message': 'Files uploaded and saved successfully', 'saved_files': saved_files}, status=200)
    except Exception as e:
            return JsonResponse({'message': f'Error uploading and saving files: {str(e)}'}, status=500)
