## Technical stack
![Codelabs](https://img.shields.io/badge/Codelabs-violet?style=for-the-badge)
![GCP provider](https://img.shields.io/badge/GCP-orange?style=for-the-badge&logo=google-cloud&color=orange)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)

## Link to the Live Applications
* [Streamlit] ()
* [Codelabs](https://codelabs-preview.appspot.com/?file_id=1E2Z6QsyAEtmAuYTbtrClYIojHb8P_ISyPxjJWQZxXi8#0)


# SoundJot
The cutting-edge audio journaling application designed to preserve your thoughts, 
emotions, and cherished moments through seamless voice recording. 
With intuitive features and secure cloud storage, SoundJot offers a private and immersive journaling experience, 
enabling you to relive your memories anytime, anywhere.

Explore the comprehensive documentation for our application, SoundJot, and unlock a wealth of knowledge and guidance to enhance your audio journaling experience. [Click here](https://codelabs-preview.appspot.com/?file_id=1E2Z6QsyAEtmAuYTbtrClYIojHb8P_ISyPxjJWQZxXi8#0) to access a wealth of resources and start journaling with ease and creativity.

## Running the application
### Pre-requisites
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker compose](https://docs.docker.com/compose/install/)

### Steps to run application locally
1. Clone the repository
    ```bash
        git clone https://github.com/BigDataIA-Summer2023-Team2/Assignment3.git
    ```
2. Create a gcs_key.json{} file in airflow and streamlit folder with following variables defined
{
    "type": "service_account",
    "project_id": "projectid",
    "private_key_id": "xxx",
    "private_key": "\n---- PRIVATE KEY-----\n",
    "client_email": "clientname@projectid.iam.gserviceaccount.com",
    "client_id": "000",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/client_email",
    "universe_domain": "googleapis.com"
  }
  
3. 3. Create a kaggle.json{} file in airflow folder with following variables defined
    {"username":"xxx","key":"000"}

4. Run the make command to build and deploy the application
    ```bash
        make build-up
    ```
5. Applciation would be accessible on localhost at following URLs \
    **Streamlit:** http://localhost:8090/ \
6. Destroying the deployed environment
    ```bash
        make down
    ```
## Project Tree


## References
-[Kaggle] https://www.kaggle.com/ejlok1/surrey-audiovisual-expressed-emotion-savee
-[Kaggle] https://www.kaggle.com/uwrfkaggler/ravdess-emotional-speech-audio
-[Kaggle] https://www.kaggle.com/ejlok1/toronto-emotional-speech-set-tess
-[Kaggle] https://www.kaggle.com/ejlok1/cremad
-[Kaggle] https://www.kaggle.com/code/ejlok1/audio-emotion-part-3-baseline-model/notebook
-[Pinecone] https://docs.pinecone.io/docs/audio-search
-[OpenAI]https://medium.com/muthoni-wanyoike/implementing-text-summarization-using-openais-gpt-3-api-dcd6be4f6933

