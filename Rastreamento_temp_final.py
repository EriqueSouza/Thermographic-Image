import cv2
import numpy as np
import matplotlib.pyplot as plt

#Função para gerar os histogramas
def get_histograma(src):

    bgr_planes = cv2.split(src)  # Divide uma imagem de 3 canais em 3 imagens de um canal
    histSize = 1024
    histRange = (0, histSize) # the upper boundary is exclusive

    #Calculo histograma
    b_hist = cv2.calcHist(bgr_planes, [0], None, [histSize], histRange)  # Calcula Histograma do canal Blue
    g_hist = cv2.calcHist(bgr_planes, [1], None, [histSize], histRange)  # Calcula Histograma do canal Green
    r_hist = cv2.calcHist(bgr_planes, [2], None, [histSize], histRange)  # Calcula Histograma do canal Red

    #Normalização devido a distancia da foto na imagem. Exemplo; O calculo do histograma da cabeça para o corpo pode mudar devido a distancia da foto tirada
    b = b_hist / sum(b_hist)  # Normaliza canal Blue
    r = r_hist / sum(r_hist)  # Normaliza canal Red
    g = g_hist / sum(g_hist)  # Normaliza canal Green

    #Histograma
    histograma = np.array([b,g,r]).reshape(-1,1)  # Concatena as 3 arrays em uma única array

    return histograma, b,g,r


#Histograma das imagens dos times originais
mhot = cv2.imread('mhot.jpg')  # Carrega Imagem
hmh,b1,g1,r1 = get_histograma(mhot)
#ax[0][0].set_title("More Hot")
#ax[0][0].plot(hmh)  # faz a plotagem do histograma

hot = cv2.imread('hot.jpg')  # Carrega Imagem
hho,b1,g1,r1 = get_histograma(hot)
#ax[0][1].set_title("Hot")
#ax[0][1].plot(ht)  # faz a plotagem do histograma

mid = cv2.imread('mid.jpg')  # Carrega Imagem
hmd,b1,g1,r1 = get_histograma(mid)
#ax[0][2].set_title("Mid")
#ax[0][2].plot(hmd)  # faz a plotagem do histograma

mlower = cv2.imread('mlower.jpg')  # Carrega Imagem
hml,b1,g1,r1 = get_histograma(mlower)
#ax[1][3].set_title("Lower")
#ax[1][3].plot(hml)  # faz a plotagem do histograma


def get_tracker():

  tracker = cv2.TrackerCSRT_create()


  return tracker

cap = cv2.VideoCapture("teste1.mp4") # Criamos o objeto de leitura de vídeo

fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Cria o objeto para gravar vídeo


_, frame = cap.read()  # Capturamos o primeiro frame
bb = []  # Criamos uma lista vazia que receberá as coordenadas dos boxes

out = cv2.VideoWriter('teste_out.mp4', fourcc, 30.0, (frame.shape[1], frame.shape[0]))  # Determina o nome do arquivo de saída, sua taxa de FPS e sua resolução.

while True:

  roi = cv2.selectROI('Frame', frame)  # Função para seleção de ROI
  #print(roi)
  bb.append(roi)  #  Coordenadas do box da ROI adicionadas à lista

  k = cv2.waitKey(0)
  if k == ord('q'):
    break

multiTracker = cv2.MultiTracker_create()  # Cria o objeto Tracker

for bbox in bb:
  multiTracker.add(get_tracker(), frame, bbox)  # Inicializa o objeto Tracker para cada ROI selecionada

while True:

    old_frame = frame

    ret, frame = cap.read()  #  Captura um frame
    if not ret:  # Verifica status do vídeo
        exit()

    _, bxs = multiTracker.update(frame) # Atualiza o objeto Tracker para a nova posição de cada ROI selecionada

    for ID, box in enumerate(bxs):

        p1 = (int(box[0]), int(box[1]))  # coordenadas do box das detecções
        p2 = (int(box[0] + box[2]), int(box[1] + box[3]))

        x=int(box[1])
        y=int(box[0])
        a=int(box[2])
        b=int(box[3])
        cortada = frame[x:x+b,y:y+a]

        cv2.rectangle(frame, p1, p2, (0,255,0), 2, cv2.LINE_AA)  # Retângulo nas áreas detectadas

        ho,bo,go,ro = get_histograma(cortada)  # recebe o histograma da imagem velha
        mh = cv2.compareHist(ho,hmh,0)
        ht = cv2.compareHist(ho,hho,0)
        md = cv2.compareHist(ho,hmd,0)
        ml = cv2.compareHist(ho,hml,0)

        if mh > ht and mh > md and mh > ml:
            #print ("Very Hot")
            cv2.putText(frame, "Very Hot", (int(box[0]-8),int(box[1]-8)), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0,0,255),2,cv2.LINE_AA)  # Texto com o ID de cada objetos
        elif ht > mh and ht > md and ht > ml:
            #print("Hot")
            cv2.putText(frame, "Hot", (int(box[0]-8),int(box[1]-8)), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0,255,255),2,cv2.LINE_AA)  # Texto com o ID de cada objeto
        elif md > mh and md > ht and md > ml:
            #print("Cold")
            cv2.putText(frame, "Cold", (int(box[0]-5),int(box[1]-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(255,255,0),2,cv2.LINE_AA)  # Texto com o ID de cada objeto
        elif ml > mh and ml > ht and ml > md:
            #print("Very Cold")
            cv2.putText(frame, "Very Cold", (int(box[0]-5),int(box[1]-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(255,0,0),2,cv2.LINE_AA)  # Texto com o ID de cada objeto

    cv2.imshow('Frame', frame)
    out.write(frame)

    k = cv2.waitKey(15)
    if  k == ord('q'):
        out.release() # sem isso não funciona o vídeo
        exit()

out.release()
cv2.destroyAllWindows()
