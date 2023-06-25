import os
from PyQt5.QtWidgets import*


#2.hafta
from PyQt5.QtCore import Qt # En boy oranını koruyarak yeniden boyutlandırma için Qt.KeepAspectRatio sabitine ihtiyaç vardır..
from PyQt5.QtGui import QPixmap # ekranda görüntülenecek şekilde optimize edilmiş resim
from PIL import Image
#--


#3.hafta
from PIL.ImageQt import ImageQt#grafikleri pillowdan Qt çevir.
from PIL.ImageFilter import*
#--


app=QApplication([])
win = QWidget()
win.resize(700,500)
win.setWindowTitle('Easy Editor')
lb_image=QLabel("Tablo")
btn_dir=QPushButton("Dosya")
lw_files = QListWidget()


btn_left=QPushButton("Sol")
btn_right=QPushButton("Sağ")
btn_flip=QPushButton("Ayna")
btn_sharp=QPushButton("Keskinlik")
btn_bw=QPushButton("S/B")


row=QHBoxLayout() #ana satır
col1=QVBoxLayout()#dikey
col2=QVBoxLayout()#dikey
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image,95)
row_tools=QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)


row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)


win.show()


def filter(files,extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


#2.hafta


def chooseWorkdir():
    global workdir
    workdir=QFileDialog.getExistingDirectory()


def showFilenamesList():
    extensions=['.jpg','.jpeg','.png','gif','.bmp']
    chooseWorkdir()
    filenames=filter(os.listdir(workdir),extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)


class ImageProcessor():
    def __init__(self):
        self.image = None #mevcut resim
        self.dir =None #geçerli dosya yeri
        self.filename = None #dosya adı
        self.save_dir = "Modified/"#değiştirilen dosyaların kaydedilecği yer


    def loadImage(self, dir, filename):
        self.dir=dir
        self.filename=filename
        image_path = os.path.join(dir,filename)
        self.image =Image.open(image_path)#resmi aç


    def do_bw(self):
        self.image =self.image.convert("L")#siyah-beyaz yap
        self.saveImage()#resmimizi kaydet
        image_path = os.path.join(self.dir, self.save_dir, self.filename)#yola ulaş
        self.showImage(image_path)#göster


    def saveImage(self):
        '''dosyanın bir kopyasını alt klasöre kaydeder'''
        path=os.path.join(self.dir, self.save_dir)
                #dosya yolu varmı, dosya bir dizin halinde mi?
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)#yeni bir dizin oluştur
        image_path = os.path.join(path, self.filename)#dosyaya gidiyoruz.
        self.image.save(image_path)#kaydet


    #3.hafta
    def showImage(self,path):
        lb_image.hide()
        pixmapimage=QPixmap(path)
        w, h =lb_image.width(),lb_image.height()
        pixmapimage =pixmapimage.scaled(w, h,Qt.KeepAspectRatio)#jırpma olmadan resmi boyutlandır.
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    
    def do_left(self):
        self.image =self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path=os.path.join(workdir,self.save_dir,self.filename)#alt klasör olan modified a kaydetme
        self.showImage(image_path)


    def do_right(self):
        self.image=self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path=os.path.join(workdir,self.save_dir,self.filename)#alt klasör olan modified a kaydetme
        self.showImage(image_path)
    
    def do_flip(self):
        self.image=self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path=os.path.join(workdir,self.save_dir,self.filename)#alt klasör olan modified a kaydetme
        self.showImage(image_path)
    
    def do_sharpen(self):
        self.image=self.image.filter(SHARPEN)
        self.saveImage()
        image_path=os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)


#resimler için bir tuşlama işlemi yapıyoruz...
def showChoosenImage():
    if lw_files.currentRow() >=0: #liste öğesi boş değilse
        #dosya isimlerinden herhangi birine tıkladığımda dosyanın adını al.
        filename=lw_files.currentItem().text()
        workimage.loadImage(workdir,filename)#seçilen resmin yüklenmesi.
        #resmin dosya yolundan ve isminden resme ulaştık.
        image_path=os.path.join(workimage.dir,workimage.filename)
        workimage.showImage(image_path)


workimage = ImageProcessor()#iş için yeni resim nesnesi oluştur.
lw_files.currentRowChanged.connect(showChoosenImage)#dosyalardan bir öğe seçilirse fonk çağır
btn_bw.clicked.connect(workimage.do_bw)
btn_dir.clicked.connect(showFilenamesList)


#3.hafta
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)


app.exec()
