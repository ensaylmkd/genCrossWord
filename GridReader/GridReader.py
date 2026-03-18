import cv2
import numpy as np
import random
import math
import os

IMG_PATH = "image.png"
DIR_RES_PATH = "res6"
# ================= Outil ====================
def projection_ligne(thresh_img):
    vertical_projection = np.sum(thresh_img, axis=0) // 255
    
    # Somme des pixels lignes par lignes (axis=1)
    horizontal_projection = np.sum(thresh_img, axis=1) // 255
    
    return vertical_projection, horizontal_projection

def moyenne_ensemble_ligne(proj,x,r,maxlenght):
    """
    Renvoie la moyenne dela somme des pixes de la ligne x-r à x+r 
    proj : projection,
    x: indice,
    r: rayon,
    maxlenght: taille max de l'image
    """
    acc = proj[x]
    for i in range(1,r+1):
        if x+i < maxlenght:
            acc+= proj[x+i] 
        if x-i >= 0:
            acc+= proj[x-i]
    return acc // (1+r*2)

def projection_entre_p1_P2(img,p1,p2):
    x1, y1 = p1
    x2, y2 = p2

    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)

    zone = img[y_min:y_max+1, x_min:x_max+1]

    acc = np.sum(zone) // 255
    return acc

def nb_pixel_entre(p1,p2):
    return (p2[0]-p1[0]) * (p2[1]-p1[1])


# ========= traitement Image =============
def preprocess_image(image_originale):
    ## //// met en niveau de gris 
    gray = cv2.cvtColor(image_originale, cv2.COLOR_BGR2GRAY)

    ## //// flou gaussien 
    n=5
    blur = cv2.GaussianBlur(gray, (n, n), 10)

    edges = cv2.Canny(blur, 30, 80, 3)
    edges = cv2.adaptiveThreshold(edges, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    edges_proc = edges.copy()
    edges_proc = cv2.dilate(edges_proc, (3,3), iterations=1)
    # edges_proc = cv2.erode(edges_proc, (3,3), iterations=1)
    
    
    edges_proc= cv2.erode(edges_proc,(50,50),iterations=10)
    edges_proc = cv2.morphologyEx(edges_proc, cv2.MORPH_CLOSE, (10,10),iterations=10)

    hori_proj,vert_proj = projection_ligne(edges)

    # img = image_originale.copy()
    # maxvert, maxhori = max(vert_proj),max(hori_proj)
    # seuil = (maxvert+maxhori)*0.6
    # avg_vert,avg_hori= np.mean(vert_proj) , np.mean(hori_proj)
    # for y in range(len(hori_proj)//5):
    #     for x in range(len(vert_proj)//5):
    #         if vert_proj[x*5] + hori_proj[y*5] > seuil:
    #             cv2.circle(img, (y*5, x*5), 3, (255,0,0), 1)

    # cv2.imshow("gray", gray)
    # cv2.imshow("blur", blur)
    # cv2.imshow("edges", edges)
    Fname= IMG_PATH.split('.')[0]
    # cv2.imwrite(f"{DIR_RES_PATH}/{Fname}_gray.jpg",gray)
    # cv2.imwrite(f"{DIR_RES_PATH}/{Fname}_blur.jpg",blur)
    cv2.imwrite(f"{DIR_RES_PATH}/{Fname}_edges.jpg",edges)
    cv2.imwrite(f"{DIR_RES_PATH}/{Fname}_edges_proc.jpg",edges_proc)
    cv2.imwrite(f"{DIR_RES_PATH}/{Fname}_sicamarchecfou.jpg",img)
    
    return edges

def FoundRawAndCol(tresh):
    hori_proj,vert_proj = projection_ligne(tresh)
    h, w = img.shape[:2]
    rawIndex=[]
    colIndex=[]

    seuil_h = np.max(hori_proj) * 0.5
    seuil_v = np.max(vert_proj) * 0.5
    print(seuil_h)
    print(seuil_v)

    diametre = 5 # doit etre impaire

    for i in range(w//diametre):
        x= i * diametre
        if moyenne_ensemble_ligne(hori_proj,x,diametre//2,h) > seuil_h:
            rawIndex.append(x)
    print(f"[Foundraw] : {rawIndex}")

    for i in range(h//diametre):
        y = i * diametre # La vraie coordonnée Y
        if moyenne_ensemble_ligne(vert_proj,y,diametre//2,w) > seuil_v:
            colIndex.append(y)
    print(f"[Colindex] : {colIndex}")
    return rawIndex,colIndex

def mergeIndex(L, maxLen):
    if not L:
        return []
    
    seuil = int(maxLen * 0.05)
    
    newT = []
    if len(L) > 0:
        accL = [L[0]]
        for i in range(1, len(L)):
            if L[i] - L[i-1] < seuil:
                accL.append(L[i])
            else:
                newT.append(int(np.mean(accL)))
                accL = [L[i]]
        newT.append(int(np.mean(accL)))
        
    return newT




    # seuil = (maxvert+maxhori)*0.6

    # avg_vert,avg_hori= np.mean(vert_proj) , np.mean(hori_proj)
    # for y in range(len(hori_proj)//5):
    #     for x in range(len(vert_proj)//5):
    #         if vert_proj[x*5] + hori_proj[y*5] > seuil:
    #             cv2.circle(img, (y*5, x*5), 3, (255,0,0), 1)

def Drawintersec(image,pointss):
    img = image.copy()
    for points in pointss:
        for p in points:
                cv2.circle(img, p, 10, (0,0,255), -1)
    return img 

def DrawLine(img,preproc_img):
    lines = cv2.HoughLines(preproc_img, 2, np.pi / 180, 300)
    if (lines is not None):
        lines = lines[:, 0]
        lines = sorted(lines, key=lambda line:line[0])

        h, w = img.shape[:2]
        diag = int(math.sqrt(w**2 + h**2)) 

        pos_hori = 0
        pos_vert = 0
        dist_min = diag * 0.03 # nom var à changer
        for rho,theta in lines:
            # ================ Calcule point de la droite Polaire =====================
            # =============== 
            # transformation de Hough : rho = x*cos(theta)+ y*sin(theta)
            # (x0,y0) point le plus proche de l'origine:
            # x0 = rho*cos(theta)
            # y0 = rho*sin(theta)
            # =============== 
            a = np.cos(theta) 
            b = np.sin(theta)

            x0 = a*rho
            y0 = b*rho

            #============ Toute l'image (+ en vrai)
            x1 = int(x0 + diag*(-b))
            y1 = int(y0 + diag*(a))
            x2 = int(x0 - diag*(-b))
            y2 = int(y0 - diag*(a))
            #============
            # ======================================================
            
            
            if (b>0.5): # rapelle: sin(theta) = 1 verticale parfait ; sin(theta) = 0 horizontale parfait
                # eviter de placer des droites similaire
                if(abs(rho-pos_hori)>dist_min):
                    pos_hori=rho
                    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),10)
            else:
                # eviter de placer des droites similaire
                if(abs(rho-pos_vert)>dist_min):
                    pos_vert=rho
                    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),10)
        Fname= IMG_PATH.split('.')[0]
        cv2.imwrite(f"{DIR_RES_PATH}/{Fname}_LineDraw.jpg",img)

def DrawLine2(img,preproc_img):
    
    lines = cv2.HoughLinesP(preproc_img, 1, np.pi / 180, threshold=500, 
                            minLineLength=100, maxLineGap=100)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
    Fname= IMG_PATH.split('.')[0]
    cv2.imwrite(f"{DIR_RES_PATH}/{Fname}_LineDraw2.jpg",img)

os.makedirs(DIR_RES_PATH, exist_ok=True)
img = cv2.imread(IMG_PATH)
h, w = img.shape[:2]
print("[MAIN]taille image :",h,w)

prepoc_img = preprocess_image(img)

R,C = FoundRawAndCol(prepoc_img)
R = mergeIndex(R,h)
C = mergeIndex(C,w)
nbC = len(R)-1
nbR= len(C)-1
print(f"[MAIN] grille détecté: {nbR}x{nbC}")
res=[[0 for _ in range(nbC)]for _ in range(nbR)]

intersec = [[(x, y) for x in R] for y in C]
newimg= Drawintersec(img,intersec)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

for i in range(len(intersec)-1):
    for j in range(len(intersec[0])-1):
        p1 = intersec[i][j]
        p2 = intersec[i+1][j+1]
        proj = projection_entre_p1_P2(thresh,p1,p2)
        if proj <= nb_pixel_entre(p1,p2)*0.5:
            res[i][j]=1

Fname= IMG_PATH.split('.')[0]
cv2.imwrite(f"{DIR_RES_PATH}/{Fname}_intersec.jpg",newimg)
for l in res:
    print(l)


# DrawLine(img,prepoc_img)
# DrawLine2(img,prepoc_img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
