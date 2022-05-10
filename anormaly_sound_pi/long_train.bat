@echo off

set KMP_DUPLICATE_LIB_OK=TRUE
python train.py --debug True --epochs 5000 --tensor_board True --train 20220426_car_noise\nearest_sound\nearest_360.wav --model epochs5000\models\nearest_360.h5
python train.py --debug True --epochs 5000 --tensor_board True --train 20220426_car_noise\nearest_sound\nearest_60.wav --model epochs5000\models\nearest_60.h5
python train.py --debug True --epochs 5000 --tensor_board True --train 20220426_car_noise\nearest_sound\nearest_10.wav --model epochs5000\models\nearest_10.h5

python train.py --debug True --epochs 5000 --tensor_board True --train 20220426_car_noise\longest_sound\longest_360.wav --model epochs5000\models\longest_360.h5
python train.py --debug True --epochs 5000 --tensor_board True --train 20220426_car_noise\longest_sound\longest_60.wav --model epochs5000\models\longest_60.h5
python train.py --debug True --epochs 5000 --tensor_board True --train 20220426_car_noise\longest_sound\longest_10.wav --model epochs5000\models\longest_10.h5

python train.py --debug True --epochs 5000 --tensor_board True --train 20220426_car_noise\no_sound\none_360.wav --model epochs5000\models\none_360.h5
python train.py --debug True --epochs 5000 --tensor_board True --train 20220426_car_noise\no_sound\none_60.wav --model epochs5000\models\none_60.h5
python train.py --debug True --epochs 5000 --tensor_board True --train 20220426_car_noise\no_sound\none_10.wav --model epochs5000\models\none_10.h5
