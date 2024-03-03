import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
cap=cv2.VideoCapture(0)
detector=FaceMeshDetector(maxFaces=1)  ## Yüz izleme detektörünün oluşturulması
plotY=LivePlot(960,720,[0,40],invert=True) ## Canlı grafik çizim için LivePlot oluşturulması
idList=[22,23,24,26,110,157,158,159,160,161,130,243] ## İzlenecek yüz noktalarının belirlenmesi:
ratioList=[] ## Kırpma sayma için değişkenlerin başlatılması
blinkCounter=0
counter=0


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == (cv2.CAP_PROP_FRAME_COUNT): 
        ##cap.get(cv2.CAP_PROP_POS_FRAMES) ifadesi, video kaynağından okunan mevcut çerçevenin pozisyonunu (sırasını) döndürür.

##cv2.CAP_PROP_FRAME_COUNT ifadesi, video kaynağının toplam çerçeve sayısını döndürür.
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)    ## burada aslında hem sağ göz hem sağ göz için algoritma çalışması için kodlanma yapıldı

    success,img=cap.read()
    img,faces=detector.findFaceMesh(img,draw=False) ##Yüzün tespit edilmesi
    if faces: ## Yüz noktalarının çizdirilmesi:
        face=faces[0]
        for id in idList:
            cv2.circle(img,face[id],5,(255,0,0),cv2.FILLED) ##çizim için circle kullanılır

        solUst=face[159]  ## üst nokta,alt nokta,sağdan ve soldan sınırlar buluunyor
        solAlt=face[23]
        solEnsol=face[130]
        solEnsag=face[243]

        lengtVer,a=detector.findDistance(solUst,solAlt)
        lengtHor,a=detector.findDistance(solEnsol,solEnsag) ## bu sınırlar hatlar halinde çizdirilerek göz kısımlarının tespiti sağlanıyor
        cv2.line(img,solUst,solAlt,(0,255,0),3)
        cv2.line(img,solEnsol,solEnsag,(0,255,255),3)
        ratio=int((lengtVer/lengtHor)*100) ##burada dikey / yata oranı bulunarak saklanıyor 
        ratioList.append(ratio)

        if len(ratioList) > 3:   ## Eğer ratioList listesindeki veri miktarı 3'ten fazlaysa, yani daha önce 3 oran saklandıysa, ratioList.pop(0) ifadesi kullanılır. Bu, listedeki en eski veriyi (ilk elemanı) çıkarır.
            ratioList.pop(0)
        ratioAvg=sum(ratioList) / len(ratioList)
        if ratioAvg < 35 and counter == 0:
            blinkCounter +=1
            counter=1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter=0
##Bilgi metni ve canlı grafik oluşturulması
        cvzone.putTextRect(img,f'Blink Counter{blinkCounter}',(100,100))  
        imgPlot=plotY.update(ratioAvg)
        imgStack=cvzone.stackImages([img,imgPlot],2,1)
        
    else:
        img=cv2.resize(img,(960,720))
        imgStack=cvzone.stackImages([img,img],2,1)

## Görüntünün gösterilmesi:
    img=cv2.resize(img,(960,720))
    cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    

    cv2.imshow("image",imgStack)


    if cv2.waitKey(25) & 0xFF==ord("q"):break

cap.release()
cv2.destroyAllWindows()