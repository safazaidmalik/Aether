AETHER: Desktop Application for the generation of realistic 3D outdoor virtual scenes using Natural Language Processing
Final Year Project

This is a Java based program which provides the implementation for Mesh Join to be used in a near realtime data warehouse. 
  Submitted to: FYP Committee FAST Islamabad
  Submitted by: Aamna Kamran, Momin Tariq and Safa Zaid Malik
  Roll Number: 19I-0454, 19I-0437 and 19I-0555
  Project Type: Development
  Group Number: F22-062
  Submission Date: Sunday, 9th January, 2023

Installation Requirements:
Before starting the application, make sure that the following installations have been made:

  pip install rdflib
  pip install SPARQLWrapper
  pip install owlready2
  pip install -U sentence-transformers
  pip install SpeechRecognition
  pip install spacy
  python -m spacy download en
  pip install SceneGraphParser
  pip install networkx
  pip install matplotlib
  
Hardware Requirements:
  1. GPU (at least)
  2. Microphone
  3. Keyboard

 
For using Unreal Engine 5 on Linux:
  1. Create an account on EpicGames.
  2. Clone Unreal Engine repository from https://github.com/EpicGames to install Unreal Engine.
  3. Download and install JetBrains Rider.
  4. (Connecting Unreal and Rider)
  
  
Running the Application
  1. Place Populated_Assets_KG.ttl in <>
  2. Place complete_py_pipeline.py in <>
  3. Launch the Unreal Engine project (Project1) from Rider.
  4. Run complete_py_pipeline.py with the terminal command: python complete_py_pipeline.py
  5. Speak into your microphone to give an input.
  6. After complete_py_pipeline.py has terminated, Run the project from Unreal Editor to spawn the assets.
  
  

Please Note
  For execution of the program, pip and Python must be installed and version should be up to date.
