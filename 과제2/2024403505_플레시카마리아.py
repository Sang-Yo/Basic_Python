import os
import time
import pyautogui as pag

#앱을 열기
os.startfile('calc.exe')
time.sleep(1)

#앱 창 크기에 대한 정보 얻기
calc = pag.getWindowsWithTitle('계산기')[0]
w = calc.width
h = calc.height

#원하는 창 크기
new_width = 500
new_height = 800

#원하는 크기의 창을 얻기 위한 움직임을 정의하는 변수
drag_x = new_width - w
drag_y = new_height - h

#앱 창의 위치 및 크기 변경
for win in pag.getAllWindows():
  if win.title == '계산기':
    win.moveTo(0, 0)
    pag.moveTo(w-11, h-9, duration=0.5)
    pag.dragTo(w+drag_x, h+drag_y, duration=0.5)
    win.activate()

#이 프로젝트에 필요한 모든 버튼
buttons = {'other': (32,77), 'graph': (32, 267), 'formula mod': (460, 70), 'graph mod':(420, 70), '1': (155, 699), '2': (250, 699), '3': (345, 699), '+':(450, 699), '-':(450, 642), '=':(355, 520), '/':(450, 522), '(':(155, 520), ')':(255, 520), 'x':(353, 462), 'y':(445, 460), '^2':(50, 460), '2nd':(50, 400), 'cbrt': (50, 515)}

#주요 부분! 그래프를 위한 함수 작성 및 표시하기
pag.click(buttons['other'], duration=0.3)
pag.click(buttons['graph'], duration=0.3)
pag.click(buttons['formula mod'], duration=0.3)
pag.typewrite('[x^2+(3y/2-cbrt(x^2))^2=1', interval=0.1)
pag.click(buttons['graph mod'], duration=0.3)
