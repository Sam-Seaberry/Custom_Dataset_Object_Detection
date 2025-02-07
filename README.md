# Custom-Object-Detection-GUI
Custom training of object detection models using TensorFlow.

## .EXE Application Install Instructions 
 - Go to [samseaberry.com](https://www.samseaberry.com/objectdetectiongui)
 - Download the application using the Download button
 - Extract the folder to a desired location
 - Once extracted open the folder and run MainGUI.exe
 - Click on the top Help bar for instructions on how to train your first model

## Training Instructions
1. Gather all images to be used for training.
 1.1 Make sure all images are the same size (width and height in pix)
2. Go to [VGG Annotation Tool](https://annotate.officialstatistics.org/) ![alt text](https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/1.png)
3. Add your images

<img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/3.png" alt="placeholder" width="150" height="300"><img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/2.png" alt="placeholder" width="150" height="300">

4. Add your first attribute (name of the thing you want to detect). Here we are detecting red and black pens so the first attribute will be "Red Pen"

<img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/4.png" alt="placeholder" width="150" height="300"><img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/5.png" alt="placeholder" width="200" height="200">

5. Draw boxes around each instance of the object.

<img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/6.png" alt="placeholder" width="400" height="300"><img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/7.png" alt="placeholder" width="400" height="300">

6.Once all objects of this type have been labeled across all images delete the attirbute.

<img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/8.png" alt="placeholder" width="300" height="300"><img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/9.png" alt="placeholder" width="300" height="200">

7.If there are other object types, repeat from step 4.

<img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/10.png" alt="placeholder" width="300" height="300"><img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/11.png" alt="placeholder" width="250" height="200"><img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/12.png" alt="placeholder" width="250" height="200">

8.Once all object have been labeled, export the annotations as a .csv file.

<img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/13.png" alt="placeholder" width="400" height="300"><img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/14.png" alt="placeholder" width="400" height="300">

9. Run MainGUI.exe and select "Create New Project" from the top toolbar.

<img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/15.png" alt="placeholder" width="400" height="300"><img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/16.png" alt="placeholder" width="400" height="300">

10.Chose a project name and location. If you are training from scratch check the "Download" checkbox and select a model type. Descriptions of model types can be found online. Generally, FRCNN is the most accurate but largest and slowest wheras SSD is less accurate but fast and small. Select an image size to train the model with. Keeping all images the same dimensions aid the models accuracy. It is suggested to select an image size of 640 unless using a desktop computer with and appropriate GPU and Cuda/CuDNN installed.  

<img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/17.png" alt="placeholder" width="400" height="300">

11. Add all the images used in step 3 by clicking on the "Add" button. Once all images are added type the image size selected in the last step into the box below the image list and click "Resize" (If your images have already been resized this part may be skipped). Add the annotations file downloaded in step 8. If training and testing datasets are to be kept static and separate add them to their respective boxes. Otherwise, a random split will occur.

<img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/18.png" alt="placeholder" width="400" height="300"> 

12.Write the names of all annotations used from step 4, seperated by a comma. NOTE: These names must match exactly to the names used using step 4 if they do not unexpected results will occur. 

<img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/19.png" alt="placeholder" width="400" height="300"><img src="https://github.com/Sam-Seaberry/Custom_Dataset_Object_Detection/blob/main/res/images/20.png" alt="placeholder" width="400" height="300">

13.Wait for the model to finish downloading. The downloading screen will automatically disappear once the download is completed.


## Source Code Install Instructions

1. **Create a Python virtual environment**:
 - Open a PowerShell window in admin mode.
 - Locate the install location of the virtual environment and activate it.
 - Follow the next steps with the environment activated.

2. **Install TensorFlow**:
 - Use instructions from [ReadTheDocs](https://www.tensorflow.org/install).
 - Optional: Install Cuda and CUDNN (8.6 - 11.2).

3. While still in the PowerShell window with the virtual environment activated, run:

   ```bash
   python -m pip install -r requirements_gui.txt `

1.  **Try to Run `MainGui.py`**:

    -   If you get the error: `Module import Error TensorFlow.keras not found`, follow these steps:

        -   Modify the file `site-packages/tensorflow/__init__.py` near line 387.

        -   **Before**:

            ```
            _keras_module = "keras.api._v2.keras"
            keras = _LazyLoader("keras", globals(), _keras_module)
            _module_dir = _module_util.get_parent_dir_for_name(_keras_module)
            if _module_dir:
                _current_module.__path__ = [_module_dir] + _current_module.__path__
            setattr(_current_module, "keras", keras)
            ```

        -   **After**:

           ```
           import typing as _typing
            if _typing.TYPE_CHECKING:
                from keras.api._v2 import keras
            else:
                _keras_module = "keras.api._v2.keras"
                keras = _LazyLoader("keras", globals(), _keras_module)
                _module_dir = _module_util.get_parent_dir_for_name(_keras_module)
                if _module_dir:
                    _current_module.__path__ = [_module_dir] + _current_module.__path__
                setattr(_current_module, "keras", keras)
           ```

        Source: [TensorFlow Issue #53144](https://github.com/tensorflow/tensorflow/issues/53144#issuecomment-985179600)

2.  Try running `MainGUI.py` again. If you encounter the error:

    `ImportError: cannot import name 'eval_pb2' from 'object_detection.protos'`

    -   Copy all files from the installed `tensorflow/models/research/protos` folder into your Python environment's `site-packages/object_detection/protos` folder.
3.  **If you get this error**:

    `AttributeError: module 'tensorflow' has no attribute 'contrib'`

    This is due to changes made to the TensorFlow package that have not been updated. To fix errors about `tf.contrib.slim`, follow these steps:

    -   Delete the line defining `slim` as `tf.contrib.slim` and change it to:

        `import tf_slim as slim`

        This will need to be done in multiple files.

4.  **Next error**: Due to changes in TensorFlow, fix this by modifying:

    -   Change `bipartite_matcher.py` line 20 from:

        `from tensorflow.contrib.image.python.ops import image_ops`

        to:

        `from tensorflow.python.ops import image_ops`

5.  **Next error**: "No module named 'nets'". Fix this by changing the line:

    `from net import inception_v2`

    to:

    `from tf_slim.nets import inception_v2`

6.  **If you get the error `ModuleNotFoundError: No module named 'keras.layers.preprocessing'`**, solve this by changing the line to:

    `from tensorflow.keras.preprocessing import image as image_ops`

Once `MainGUI.py` opens the GUI, you can start training a model.

## Watch the output from the GUI carefully
there may still be some missing imports. When running TensorFlow, it may not know to use the virtual environment. Solve these errors by simply installing the missing packages using `pip`. **Note**: These must be installed on the Python system (not in the virtual environment)!
- Open command prompt
` python -m pip install <package_name>`
### Common missing packages (Add these outside of Virtual Environment):

-   `protobuf == 3.20.3`
-   `tf-models-official`
-   `tensorflow_io`
-   `scipy`
-   `lvis` (make sure `pip` is updated here)
-   `pycocotools`
-   `tf_slim`
-   `tensorflow==2.13.0`
-   `absl-py==1.4.0`

GPU Support
-----------

This project uses TensorFlow 2.10.0. To use GPU support, download CUDNN 8.1 and CUDA 11.2.

Other releases of TensorFlow use later versions of CUDNN and CUDA. See the compatibility list here: [TensorFlow Installation (GPU)](https://www.tensorflow.org/install/source#gpu)
