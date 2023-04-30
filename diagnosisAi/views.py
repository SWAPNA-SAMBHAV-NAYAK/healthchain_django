from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.http import JsonResponse

import pickle
import pandas as pd

# Create your views here.
liver_filepath=str(settings.BASE_DIR)+"/liver_votesClass.sav"
liver_scaler_filepath=str(settings.BASE_DIR)+"/liver_robust.sav"
liver_encoder_filepath=str(settings.BASE_DIR)+"/liver_label.sav"
heart_filepath=str(settings.BASE_DIR)+"/heart.sav"
heart_scaler_filepath=str(settings.BASE_DIR)+"/heart_scaler.sav"


class LiverAnalysis(APIView):
    def post(self,request):
        result=django_Lrun(request)
        print(result)
        return Response(result.tolist()[0],status=status.HTTP_200_OK)

def django_Lrun(request):
    print("Hello inside django_Lrun")
    age=0
    gender=""
    totalbilirubin=0
    alkalinephosphatase=0
    alamineamino=0
    albuminandglobulin=0
    if request.POST["gender"]== 'Male':
        gender = 1
    else:
        gender = 0
    age = int(request.POST["age"])
    totalbilirubin = float(request.POST["totalbilirubin"])
    alkalinephosphatase = int(request.POST["alkalinephosphatase"])
    alamineamino = int(request.POST["alamineamino"])
    albuminandglobulin = float(request.POST["albuminandglobulin"])

    df_data_dict = {
        'gender':gender,
        'total_bilirubin': totalbilirubin,
        'alkaline_phosphotase':alkalinephosphatase,
        'alamine_aminotransferase':alamineamino,
        'albumin_and_globulin_ratio': albuminandglobulin,
        'age':age,
    }

    cols =['age', 'gender', 'total_bilirubin', 'alkaline_phosphotase',
       'alamine_aminotransferase', 'albumin_and_globulin_ratio']
    
    new_df=pd.DataFrame(data = df_data_dict,index=[0], columns=cols)
    loaded_label_encoder = pickle.load(open(liver_encoder_filepath,"rb"))
    loaded_scaler = pickle.load(open(liver_scaler_filepath,"rb"))
    loaded_model= pickle.load(open(liver_filepath,"rb"))
    new_df['gender'] = loaded_label_encoder.fit_transform(new_df['gender'])
    for i in new_df[['age', 'gender', 'total_bilirubin', 'alkaline_phosphotase', 
                    'alamine_aminotransferase', 'albumin_and_globulin_ratio']].columns:
        new_df[i] = loaded_scaler.fit_transform(new_df[i].values.reshape(-1, 1))
    result = loaded_model.predict(new_df)
    return result

    # ------------------------------------------------------------------------------------------
class HeartAnalysis(APIView):
    def post(self,request):
        result=django_run(request)
        print(result)
        return Response(result.tolist()[0],status=status.HTTP_200_OK)



def django_run(request):
    
    
    age=0
    cholesterol=0
    restingbp=0
    fastingbs=0
    maxhr=0
    exerciseangina=""
    stslope_up=""
    stslope_flat=""
    restingecg_normal=""
    restingecg_st=""
    sex=""
    chestpaintype_ata=""
    chestpaintype_nap=""
    chestpaintype_ta=""
    oldpeak=0
    
    if request.POST["chestpaintype"] == 'ATA':
        chestpaintype_ata=1
        chestpaintype_nap=0
        chestpaintype_ta=0
    elif request.POST["chestpaintype"] == 'NAP':
        chestpaintype_ata=0
        chestpaintype_nap=1
        chestpaintype_ta=0
    else:
        chestpaintype_ata=0
        chestpaintype_nap=0
        chestpaintype_ta=1
        
    if request.POST["sex"]== 'M':
        sex = 1
    else:
        sex = 0
        
    if request.POST["restingecg"] == 'Normal':
        restingecg_normal=1
        restingecg_st=0
    else:
       restingecg_normal=0
       restingecg_st=1
       
    if request.POST["stslope"]=='Up':
       stslope_flat=0
       stslope_up=1
    else:
        stslope_flat=1
        stslope_up=0
        
    if request.POST["exerciseangina"]=='Y':
        exerciseangina=1
    else:
        exerciseangina=0

    cholesterol = int(request.POST["cholesterol"])
    age = int(request.POST["age"])
    restingbp = int(request.POST["restingbp"])
    fastingbs = int(request.POST["fastingbs"])
    maxhr = int(request.POST["maxhr"])
    oldpeak = float(request.POST["oldpeak"])
    
    df_data_dict = {
        'ChestPainType_ATA': chestpaintype_ata,
        'ChestPainType_NAP': chestpaintype_nap,
        'ChestPainType_TA': chestpaintype_ta,
        'Sex_M':sex,
        'RestingECG_Normal': restingecg_normal,
        'RestingECG_ST':restingecg_st,
        'ST_Slope_Flat':stslope_flat,
        'ST_Slope_Up': stslope_up,
        'ExerciseAngina_Y':exerciseangina,
        'Cholesterol':cholesterol,
        'Age':age,
        'Oldpeak':oldpeak,
        'RestingBP':restingbp,
        'FastingBS':fastingbs,
        'MaxHR':maxhr,
    }
    
    
    cols=['Age', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Oldpeak', 'Sex_M', 'ChestPainType_ATA', 'ChestPainType_NAP',
       'ChestPainType_TA', 'RestingECG_Normal', 'RestingECG_ST',
       'ExerciseAngina_Y', 'ST_Slope_Flat', 'ST_Slope_Up']
    
    
    new_df=pd.DataFrame(data = df_data_dict,index=[0], columns=cols)
    
    numericalCols = [
    'Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak'
    ]
    
    
    loaded_model = pickle.load(open(heart_filepath,"rb"))
    loaded_scaler = pickle.load(open(heart_scaler_filepath,"rb"))
    features = loaded_scaler.transform(new_df[numericalCols].values)
    new_df[numericalCols] = features
    result = loaded_model.predict(new_df)
    return result


