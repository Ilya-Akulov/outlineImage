from PIL import Image, ImageDraw #Подключим необходимые библиотеки.
import numpy as np
import math


def main():
	print("Выбирете оператор:")
	print("Оператор Лапласа - 1")
	print("Оператор Робертса - 2")
	print("Оператор Собеля - 3")
	mode = int(input('mode:')) #Считываем номер преобразования.

	image = Image.open("Gran.jpg")#Открываем изображение.
	width = image.size[0] #Определяем ширину.
	height = image.size[1] #Определяем высоту.
	mask = []#Маска со значениями яркости пикселя
	picture = []#Массив для записи градиентов точек

	# Маска 3х3
	for j in range(3):
		mask2 = []
		for i in range(3):
			mask2.append(0)
		mask.append(mask2)

	# Вспомогательный массив, который хранит яркости пикселей для нового изображения
	for j in range(width):
		picture2 = []
		for i in range(height):
			picture2.append(0)
		picture.append(picture2)

	# Подгонка изображения для матрицы 3х3
	if (width%3 != 0 and height%3 != 0):
		imag = image.crop((0,0,width - width%3,height - height%3))
	elif (width%3 != 0):
		imag = image.crop((0, 0, width - width%3, height))
	elif (height%3 != 0):
		imag = image.crop((0, 0, width, height - height % 3))
	else:
		imag = image

	draw = ImageDraw.Draw(imag)#Создаем инструмент для рисования.
	width = imag.size[0] #Определяем ширину.
	height = imag.size[1] #Определяем высоту.
	pix = imag.load() #Выгружаем значения пикселей.

	#Функция нахождения яркости пикселя
	def brightness(x, y):
		R,G,B = pix[x, y]
		return sum([R,G,B]) // 3 #0 is dark (black) and 255 is bright (white)

	# Функция изменения цвета
	def changeColor(alpha, maska, x, y):
		for i in [x - 2, x - 1, x]:
			for j in [y - 3, y - 2, y-1]:
				picture[i][j] =  alpha

	#**************************************
	#Оператор Робертса
	def operRoberts(matrix, x, y):
		Gx = matrix[x+1][y+1] - matrix[x][y]
		Gy = matrix[x+1][y] - matrix[x][y+1]
		#G = np.sqrt(sum([Gx ** 2, Gy ** 2]))
		G = np.abs(Gx) + np.abs(Gy)
		return G
	#**************************************

	#**************************************
	#Оператор Собеля
	def operSobel(matrix, x, y):
		Gx = (matrix[x+1][y-1] + 2 * matrix[x+1][y] + matrix[x+1][y+1]) - (matrix[x-1][y-1]+ 2*matrix[x-1][y] + matrix[x-1][y+1])
		Gy = (matrix[x-1][y+1] + 2 * matrix[x][y + 1] + matrix[x+1][y+1]) - (matrix[x-1][y-1]+ 2*matrix[x][y - 1] + matrix[x+1][y-1])
		G = np.sqrt(sum([Gx ** 2, Gy ** 2]))
		return G
	#**************************************

	#**************************************
	#Оператор Лапласа
	def operLaplas(matrix, x, y):
		Gx = 4*matrix[x][y] - matrix[x - 1][y] - matrix[x][y-1] - matrix[x][y+1] - matrix[x+1][y]
		Gy = 8*matrix[x][y] - matrix[x - 1][y-1] - matrix[x - 1][y] - matrix[x - 1][y+1] - matrix[x][y-1] - matrix[x][y+1] - matrix[x+1][y-1] - matrix[x+1][y] - matrix[x+1][y+1]
		G = np.sqrt(sum([Gx ** 2, Gy ** 2]))
		return G
	#**************************************

	# Функция выбора оператора
	def choiceOper():
		if(mode == 1):
			changeColor(operLaplas(mask, 1, 1), mask, _wid, _hei)
		elif(mode == 2):
			changeColor(operRoberts(mask, 1, 1), mask, _wid, _hei)
		else:
			changeColor(operSobel(mask, 1, 1), mask, _wid, _hei)


	print(imag.size)# Размер изображения
	_hei = 0 # Индекс для прохода по длине
	_wid = 0 # Индекс для прохода по ширине
	_i_wid = 0 # Индекс для прохода по ширине по маске (3x3)

 	#Обход изображения применяя к нему маску выбранного оператора
	while _wid < width:
		_j_hei = 0# Индекс для прохода по длне по маске (3x3)
		while _hei < height and _j_hei < 3:
			mask[_i_wid][_j_hei] = brightness(_wid, _hei)# записываем значение яркости пикселя в маску
			_j_hei += 1
			_hei += 1
		if (_i_wid == 2):
			if (_hei == height):
			#alph = math.atan(operRoberts(mask, 1, 1)) - угол
				choiceOper()
				_hei = 0;
				_i_wid = 0
				_wid += 1
			else:
				choiceOper()
				#alph = math.atan(operRoberts(mask, 1, 1)) - угол
				_i_wid = 0
				_wid -= 2
		else:
			_hei -= 3
			_i_wid += 1
			_wid += 1

		if (_hei == height):
			_hei = 0

	#Перерисовывание изображения новыми пикселями
	for i in range(width):
			for j in range(height):
				draw.point((i, j), (int(picture[i][j]), int(picture[i][j]), int(picture[i][j])))#(a, b, c))

	#Сохранение нового изображения
	if (mode == 1):
		imag.save("Laplas.jpg", "JPEG")
		del draw
	elif (mode == 2):
		imag.save("Roberts.jpg", "JPEG")
		del draw
	else:
		imag.save("Sobel.jpg", "JPEG")
		del draw

	print("Хотите попробовать другой оператор? 1-да, 2-нет: ")
	restart = int(input('Restart: '))

	if(restart == 1):
		main()
	else:
		return 0

main()