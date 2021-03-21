# 3dImagemodel
This app takes 3 2D images and returns a 3D model of the 3 images

Running the app locally

Prerequisites
1. Ensure you have python3 installed
2. Recommended(use virtualenv)

Setting up via virtualenv
1. Install virtualenv (https://pypi.org/project/virtualenv/)
2. clone the repo into a local directory
3. open the terminal and navigate to the root of the project (cd 3dImagemodel)
4. create virtual env
    - virtualenv --python=python3 venv
5. Activate by running:
    - . venv/bin/activate
    
6. intall requirements: Run
    - pip install -r requirements.txt

7. Run migrations:
    - python manage.py migrate
    
8. Run app:
    - python manage.py runserver
    
10. open the app on your browser:
    - http://localhost:8000
    
    
    
Generate 3D models:
1. Click the button to generate the models
2. Attach 3 images by clicking in the input area and selecting 3 images at ones
3. click on save
4. Wait for the model to generate
5. Once complete, the added model will display on the table
6. Click on the download link to download the .stl file
7. view the downloaded .stl file using a 3d model viewer such as (https://www.creators3d.com/online-viewer)