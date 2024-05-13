import streamlit as st

import pickle
import numpy as np

# Charger le modèle depuis le fichier
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


def predict_species(sep_len, sep_width, petal_len, petal_width):
    input = np.array([[sep_len, sep_width, petal_len, petal_width]]).astype(np.float64)
    pred = model.predict(input)
    return int(pred)


def main():
    html_temp = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">Application ML de prédiction des espèces de fleurs d'iris </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    # sep_len = st.text_input("Sepal Length","Type Here")
    sep_len = st.slider('Entrer Sepal Length', 0.0, 10.0)
    # sep_width = st.text_input("Sepal Width","Type Here")
    sep_width = st.slider('Entrer Sepal Width', 0.0, 10.0)
    # petal_len = st.text_input("Petal Length","Type Here")
    petal_len = st.slider('Entrer Petal Length', 0.0, 10.0)
    # petal_width = st.text_input("Petal Width","Type Here")
    petal_width = st.slider('Entrer Petal Width', 0.0, 10.0)

    setosa_html = """  
      <div style="background-color:#33FF39;padding:10px >
       <h2 style="color:white;text-align:center;"> L'espece de fleur detectée est SETOSA</h2>
       </div>
    """
    versicolor_html = """  
      <div style="background-color:#DD33FF;padding:10px >
       <h2 style="color:white;text-align:center;"> L'espece de fleur detectée est  VERSICOLOR</h2>
       </div>
    """
    virginica_html = """  
      <div style="background-color:#336BFF;padding:10px >
       <h2 style="color:white;text-align:center;"> L'espece de fleur detectée est  VIRGINICA</h2>
       </div>
    """

    if st.button("Prediction"):
        output = predict_species(sep_len, sep_width, petal_len, petal_width)
        # st.success('The probability of this species is {}'.format(output))

        if output == 0:
            st.markdown(setosa_html, unsafe_allow_html=True)
        elif output == 1:
            st.markdown(versicolor_html, unsafe_allow_html=True)
        else:
            st.markdown(virginica_html, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
