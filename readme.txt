사용법 : 먼저 linesetting에 아무값도 넣지 않고, traingulation이 잘 시각화 되는지 확인한다. main.py참조
이후 linesetting.txt에 1:2,4,5,6 과 같은 형태로 넣어 주면 point1과 point2,4,5,6이 연결된 형태로 시각화를 수행해준다.

TODO : 
1. 현재 3d visualization에서 기준이 되는 plane이 없으므로, 실험 할때마다 기준 plane이 다르게 설정되어, 3d를 어떤 view에서 보여줄지가 다르게 설정된다. 
-> 기준이 되는 plane또한 카메라로 찍고, 3차원에서 point로 보여주고, 그 3개의 point를 하나의 plane으로 만들어서 그 plane을 기준으로 축을 회전변환 시킨다. 
(in experiment, 땅바닥에다가 marker 3개를 붙여놓고 걔를 기준으로 사용하면 될듯) 

2. calibrate의 정확도 향상이 이루어져야 실제 point사이의 거리를 정확하게 측정할 수 있음.

3. 