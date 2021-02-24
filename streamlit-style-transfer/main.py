import streamlit as st
from PIL import Image

import style


st.title("Pytorch Style Transfer")

img=st.sidebar.selectbox('Select Image',('amber.jpg','cat.png'))

style_name=st.sidebar.selectbox('Select Style',('candy','mosaic','rain_princess','udnie'))

model_name="saved_models/"+style_name+".pth"

input_image_name="images/content-images/"+img

output_image_name="images/output-images/"+style_name+"-"+img

style_image_name="images/style-images/"+("rain-princess" if style_name=="rain_princess" else style_name)+".jpg"
# print(style_image_name)


image=Image.open(input_image_name)
style_image=Image.open(style_image_name)

col1, col2 = st.beta_columns(2)

col1.header("Source Image:")
col1.image(image, use_column_width=True)

col2.header("Style Image:")
col2.image(style_image, use_column_width=True)



clicked=st.button("Stylize")




if clicked:
    model=style.load_model(model_name)
    style.stylize(model,input_image_name,output_image_name)

    st.write("### Output Image:")
    image=Image.open(output_image_name)
    st.image(image,width=400)


