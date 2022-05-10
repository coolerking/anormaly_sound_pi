@echo off
set EVALLOG="epochs5000\long_eval.log"
echo "long_eval.bat result" >%EVALLOG%
echo "**********" >> %EVALLOG%


set MODELPATH="epochs5000\models\nearest_360.h5"
echo "model: %MODELPATH%  result" >> %EVALLOG%
echo "model: %MODELPATH%, eval: nearest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_360.wav 1>> %EVALLOG% 2>>&1
echo "**********" >> %EVALLOG%

set MODELPATH="epochs5000\models\nearest_60.h5"
echo "model: %MODELPATH%  result" >> %EVALLOG%
echo "model: %MODELPATH%, eval: nearest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_360.wav 1>> %EVALLOG% 2>>&1
echo "**********" >> %EVALLOG%

set MODELPATH="epochs5000\models\nearest_10.h5"
echo "model: %MODELPATH%  result" >> %EVALLOG%
echo "model: %MODELPATH%, eval: nearest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_360.wav 1>> %EVALLOG% 2>>&1
echo "**********" >> %EVALLOG%



set MODELPATH="epochs5000\models\longest_360.h5"
echo "model: %MODELPATH%  result" >> %EVALLOG%
echo "model: %MODELPATH%, eval: nearest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_360.wav 1>> %EVALLOG% 2>>&1
echo "**********" >> %EVALLOG%

set MODELPATH="epochs5000\models\longest_60.h5"
echo "model: %MODELPATH%  result" >> %EVALLOG%
echo "model: %MODELPATH%, eval: nearest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_360.wav 1>> %EVALLOG% 2>>&1
echo "**********" >> %EVALLOG%

set MODELPATH="epochs5000\models\longest_10.h5"
echo "model: %MODELPATH%  result" >> %EVALLOG%
echo "model: %MODELPATH%, eval: nearest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_360.wav 1>> %EVALLOG% 2>>&1
echo "**********" >> %EVALLOG%


set MODELPATH="epochs5000\models\none_360.h5"
echo "model: %MODELPATH%  result" >> %EVALLOG%
echo "model: %MODELPATH%, eval: nearest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_360.wav 1>> %EVALLOG% 2>>&1
echo "**********" >> %EVALLOG%

set MODELPATH="epochs5000\models\none_60.h5"
echo "model: %MODELPATH%  result" >> %EVALLOG%
echo "model: %MODELPATH%, eval: nearest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_360.wav 1>> %EVALLOG% 2>>&1
echo "**********" >> %EVALLOG%

set MODELPATH="epochs5000\models\none_10.h5"
echo "model: %MODELPATH%  result" >> %EVALLOG%
echo "model: %MODELPATH%, eval: nearest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: nearest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\nearest_sound\nearest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: longest_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\longest_sound\longest_360.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_10" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_10.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_60" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_60.wav 1>> %EVALLOG% 2>>&1
echo "model: %MODELPATH%, eval: none_360" >> %EVALLOG%
python eval.py --model %MODELPATH% --eval_path 20220426_car_noise\no_sound\none_360.wav 1>> %EVALLOG% 2>>&1
echo "**********" >> %EVALLOG%
