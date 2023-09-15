import os
import cv2
import gtuner
from pubg import *

Weapon_information = {"1":2,   "2":2,    "3":2,    "4":4,    "5":4,     "6":6     ,"7":9,    "8":7 , "9":3, "10":8}

Weapon_accessories_num = {
"5":[   [["1_0","1_1","1_2",],[],["10_1","10_2","10_3","10_4","10_5","10_6"],[],[akm]],#akm
        [["1_0","1_1","1_2"],["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6"],[],[m762]],#m762
        [[],[],[],[],[groza]],#groza
        [["1_0","1_1","1_2"],["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6"],["9_2"],[ace32]]#ace32
    ],

"6":[
        [["1_0","1_1","1_2"],["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6"],[],[G36c]],#G36c
        [["1_0","1_1","1_2"],["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6"],["9_2"],[m416]],#m416
        [["1_0","1_1","1_2"],["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6"],[],[scar_l]],#scar_l
        [["1_0","1_1","1_2"],["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6"],[],[qbz]],#qbz
        [["1_0","1_1","1_2"],["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6"],[],[aug]],#aug
        [["1_0","1_1","1_2"],[],["10_1","10_2","10_3","10_4","10_5","10_6"],[],[k2]]#k2
    ],
"7":[   [["1_0","1_1","1_2","2_0","2_1","2_2"],   [],                       ["10_1","10_2","10_3","10_4","10_5","10_6","10_7","10_8"],["9_1"],[sli]],#sli
        [["1_0","1_1","1_2","2_0","2_1","2_2"],   [],                       ["10_1","10_2","10_3","10_4","10_5","10_6","10_7","10_8"],[],[mini14]],#mini14
        [["1_0","1_1","1_2","2_0","2_1","2_2"],   ["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6","10_7","10_8"],["9_1"],[sks]],#sks
        [[],[],["10_1"],["9_1"],[vss]],#vss
        [["1_0","1_1","1_2","2_0","2_1","2_2"],   [],                       ["10_1","10_2","10_3","10_4","10_5","10_6","10_7","10_8"],[],[qbu]],#qbu
        [["1_0","1_1","1_2","2_0","2_1","2_2"],   [],                       ["10_1","10_2","10_3","10_4","10_5","10_6","10_7","10_8"],["9_1"],[mk14]],#mk14
        [["1_0","1_1","1_2","2_0","2_1","2_2"],   ["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6","10_7","10_8"],[],[mk12]],#mk12
        [["1_0","1_1","1_2"],                     ["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6"],              ["9_2"],[mk47]],#mk47
        [["1_0","1_1","1_2"],                     [],  ["10_1","10_2","10_3","10_4","10_5","10_6"],                                   ["9_2"],[m16]]#m16
    ],
"8":[
        [["3_0","3_1","3_2"],[],["10_1","10_2","10_3","10_4","10_5","10_6"],[],[pp_19]],#pp-19
        [["3_0"],["4_3"],["10_1","10_2"],[],[thomson_submachine]],#thomson submachine gun
        [["3_0","3_1","3_2"],["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6"],[],[akm]],#ump45
        [["3_0","3_1","3_2"],[],["10_1","10_2"],["9_3"],[uzi]],#uzi
        [["3_0","3_1","3_2"],["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6"],["9_2"],[vector]],#vector
        [["3_0","3_1","3_2"],["4_1","4_2","4_3","4_4"],["10_1","10_2","10_3","10_4","10_5","10_6"],["9_2"],[mpk5]],#mpk5
        [[],[],[],[],[p90]],#p90
        
    ]
}

class GCVWorker:
    def __init__(self, width, height):
        os.chdir(os.path.dirname(__file__))
        
        self.gcvdata = bytearray([0x00])
        self.dic_muzzle={}
        self.dic_grip={}
        self.dic_Weapon_name={}
        self.dic_gunstock = {}
        self.dic_muzzle = self.read(1,3)#加载所有图片
        self.dic_grip = self.read(4,4)
        self.dic_Weapon_name = self.read(5,8)
        self.dic_gunstock = self.read(9,9)
        self.dic_Holographic_SIGHT =  self.read(10,10)

        self.ret_1_muzzle = []#武器枪口信息
        self.ret_2_muzzle = []
        self.ret_1_grip = []#武器握把信息
        self.ret_2_grip = []
        self.ret_1_Weapon = []#武器名称信息
        self.ret_2_Weapon = []
        self.ret_1_gunstock = []#武器枪托信息
        self.ret_2_gunstock = []
        self.ret_1_dicHolographic_SIGHT = []#武器倍镜信息
        self.ret_2_dicHolographic_SIGHT = []
        self.weapon_name = cv2.imread(str(os.path.dirname(os.path.realpath('__file__')))+'\\picture\\'+"weapon.png")
        self.Weapon_list_1 = []#武器配件1
        self.Weapon_list_2 = []#武器配件2
        self.moban = cv2.imread(str(os.path.dirname(os.path.realpath('__file__')))+'\\picture\\'+'3.png')
    def __del__(self):
        del self.gcvdata
    def tu_pian_mo_ban(self,frame,template,mode):   #图片对比
        res = cv2.matchTemplate(frame,template,mode)
        min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
        return min_val

    def detection(self,frame,x1,y1,x2,y2,dic):#配件比对
        ret = []
        for i in dic:
            for j in range(0,Weapon_information[str(i)]):
   
                sim = self.tu_pian_mo_ban(frame[y1:y2,x1:x2],dic[i][j],cv2.TM_SQDIFF_NORMED)
                ret.append([sim,i,j+1])
        ret.sort(key=lambda x: x[0])
        return ret
    def read(self,p1_start,p1_end):#读取图片
        dic = {}
        
        path = str(os.path.dirname(os.path.realpath('__file__')))+'\\picture\\'
        for i in range(p1_start,p1_end+1):
            list = []
            for j in range(1,Weapon_information[str(i)]+1):
                list.append(cv2.imread(path + str(i)+"_"+str(j)+".png")) 
            dic[str(i)] = list
        return dic

    def _1_or_2(self,frame):#枪位判断
        img1= frame[934:934+56,1460:1460+164 ]
        img2= frame[991:991+56,1460:1460+164 ]

        img1=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        ret1,th1 = cv2.threshold(img1,220,255,cv2.THRESH_BINARY)
        ret1,th2 = cv2.threshold(img2,220,255,cv2.THRESH_BINARY)
        num1 = len(th1[th1==255])
        num2 = len(th1[th2==255])
        return 3 if abs(num1-num2)<=400 else 2 if num1>num2 else 1
    def Weapon_validity_check(self,list_1,ret_Weapon,ret_parts,sim,position,Optical_sight = 0):#武器配件合法性
        if len(ret_parts)>1 and ret_parts[0][0]<sim and Weapon_accessories_num[str(ret_Weapon[0][1])][ret_Weapon[0][2]-1][position].count(str(ret_parts[0][1])+"_"+str(ret_parts[0][2])):
            
            list_1.append([ret_parts[0][1],ret_parts[0][2]])
        elif Optical_sight:
            list_1.append(["10",1])
        else:
            list_1.append([])
        
        return list_1
    def cv_ui(self,frame,weapon_list,sum,mode,fire_mode):
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame = cv2.putText(frame,'weapon',(5,30), font, 1,(255,255,255),2,cv2.LINE_AA)

        
        frame = cv2.putText(frame,'muzzle:',(5,30+60), font, 1,(255,255,255),2,cv2.LINE_AA)
        frame = cv2.putText(frame,'grip:',(5,30+60*2), font, 1,(255,255,255),2,cv2.LINE_AA)
        frame = cv2.putText(frame,'optical sight:',(5,30+60*3), font, 1,(255,255,255),2,cv2.LINE_AA)
        frame = cv2.putText(frame,'gunstock:',(5,30+60*4), font, 1,(255,255,255),2,cv2.LINE_AA)
        frame = cv2.putText(frame,'weapon coefficient:'+str(sum),(5,30+60*5), font, 1,(255,255,255),2,cv2.LINE_AA)
        frame = cv2.putText(frame,'shooting mode:'+mode[1],(5,30+60*6), font, 1,(255,255,255),2,cv2.LINE_AA)
        frame = cv2.putText(frame,'fire mode:'+str(fire_mode),(5,30+60*7), font, 1,(0,255,0),2,cv2.LINE_AA)
        frame = cv2.putText(frame,'QQ:762278834:',(5,30+60*8), font, 1,(0,255,0),2,cv2.LINE_AA)
        frame = cv2.putText(frame,'Game:PUBG',(960-150,30), font, 1,(0,0,255),2,cv2.LINE_AA)
        if len(weapon_list)>0:
            x = 5+230
            y = 0
            frame[y:y+42,x:x+154] = self.dic_Weapon_name[weapon_list[0][0]][weapon_list[0][1]-1]
            x = 5+230
            y = 0
            if len(weapon_list[1])>0:
                frame[y+60:y+60+59,x:x+58] = self.dic_muzzle[weapon_list[1][0]][weapon_list[1][1]-1]
            if len(weapon_list[2])>0:
                frame[y+60*2:y+60*2+59,x:x+58] = self.dic_grip[weapon_list[2][0]][weapon_list[2][1]-1]
            if len(weapon_list[3])>0:
                frame[y+60*3:y+60*3+59,x:x+58] = self.dic_Holographic_SIGHT[weapon_list[3][0]][weapon_list[3][1]-1]
            if len(weapon_list[4])>0:
                frame[y+60*4:y+60*4+59,x:x+58] = self.dic_gunstock[weapon_list[4][0]][weapon_list[4][1]-1]

        return frame
    def Recognition(self,frame):
        sim = self.tu_pian_mo_ban(frame[1024:1024+26,1716:1716+13],self.weapon_name,cv2.TM_SQDIFF_NORMED)
        if sim<0.15:
            self.ret_1_muzzle = self.detection(frame,1447,278,1447+58,278+59,self.dic_muzzle)#读取背包所有武器信息
            self.ret_2_muzzle = self.detection(frame,1447,278+212,1447+58,278+212+59,self.dic_muzzle)  
            self.ret_1_grip = self.detection(frame,1447+66,278,    1447+66+58,278+59,self.dic_grip)
            self.ret_2_grip = self.detection(frame,1447+66,278+212,1447+66+58,278+212+59,self.dic_grip) 
            
            self.ret_1_Weapon = self.detection(frame,1318,149,    1318+154,149+42,self.dic_Weapon_name)
            self.ret_2_Weapon = self.detection(frame,1318,149+212,1318+154,149+212+42,self.dic_Weapon_name) 

            self.ret_1_gunstock= self.detection(frame,1447+66+66+66+66,  278,       1447+66+66+66+66+58,278+59 ,self.dic_gunstock)
            self.ret_2_gunstock= self.detection(frame,1447+66+66+66+66,  278+212,   1447+66+66+66+66+58,278+59+212 ,self.dic_gunstock)

            self.ret_1_dicHolographic_SIGHT= self.detection(frame,1447+66+66+66,  278,       1447+66+66+66+58,278+59 ,self.dic_Holographic_SIGHT)
            self.ret_2_dicHolographic_SIGHT= self.detection(frame,1447+66+66+66,  278+212,   1447+66+66+66+58,278+59+212 ,self.dic_Holographic_SIGHT) 
            self.Weapon_list_1 = []
            self.Weapon_list_2 = []
        
            if len(self.ret_1_Weapon)>0 and self.ret_1_Weapon[0][0]<0.03 and self.ret_1_Weapon[0][1] != '7' :#判断武器配件信息合法性
                self.Weapon_list_1.append([self.ret_1_Weapon[0][1],self.ret_1_Weapon[0][2]])
                self.Weapon_validity_check(self.Weapon_list_1,self.ret_1_Weapon,self.ret_1_muzzle,0.03,0)
                self.Weapon_validity_check(self.Weapon_list_1,self.ret_1_Weapon,self.ret_1_grip,0.03,1)
                self.Weapon_validity_check(self.Weapon_list_1,self.ret_1_Weapon,self.ret_1_dicHolographic_SIGHT,0.03,2,Optical_sight = 1)
                self.Weapon_validity_check(self.Weapon_list_1,self.ret_1_Weapon,self.ret_1_gunstock,0.03,3)

            if len(self.ret_2_Weapon)>1 and self.ret_2_Weapon[0][0]<0.03 and self.ret_2_Weapon[0][1] != '7':
                self.Weapon_list_2.append([self.ret_2_Weapon[0][1],self.ret_2_Weapon[0][2]])
                self.Weapon_validity_check(self.Weapon_list_2,self.ret_2_Weapon,self.ret_2_muzzle,0.03,0)
                self.Weapon_validity_check(self.Weapon_list_2,self.ret_2_Weapon,self.ret_2_grip,0.03,1)
                self.Weapon_validity_check(self.Weapon_list_2,self.ret_2_Weapon,self.ret_2_dicHolographic_SIGHT,0.03,2,Optical_sight = 1)
                self.Weapon_validity_check(self.Weapon_list_2,self.ret_2_Weapon,self.ret_2_gunstock,0.03,3)

        num = self._1_or_2(frame)   
        
        return []if num==3 else  self.Weapon_list_1 if num==1 else self.Weapon_list_2

    def calculate(self,list_information):
        dic = {}
        ret = 1.0
        Firing_patterns = [1,"Repeating"] 
        if len(list_information)>0:
            dic = Weapon_accessories_num[list_information[0][0]][list_information[0][1]-1][len(Weapon_accessories_num[list_information[0][0]][list_information[0][1]-1])-1][0]
            
            if int(list_information[0][0]) == 7:
                Firing_patterns = [1,"Single"] 
            if len(list_information[1]):
                ret = ret * dic[list_information[1][0]+"_"+str(list_information[1][1])]
            
            if len(list_information[2]):
                ret = ret *dic[list_information[2][0]+"_"+str(list_information[2][1])]
            
            if len(list_information[3]):
                ret = ret *dic[list_information[3][0]+"_"+str(list_information[3][1])]
            
            if len(list_information[4]):
                ret = ret *dic[list_information[4][0]+"_"+str(list_information[4][1])]
            ret = ret * dic["all"]
    
        return ret,Firing_patterns
    def fire_mode(self,list_information):
        '''sim = self.tu_pian_mo_ban(fream[1000:1000+21,909:909+17],self.moban,cv2.TM_SQDIFF_NORMED)
        if sim <=0.08:
            return 0
        else:
            return 1'''
        if len(list_information)>=1:
            if int(list_information[0][0])==7:
                return 1
        return 0
    def dispose(self,mode,sum,list_information):
        
        if len(list_information)>=1:
            self.gcvdata = bytearray()
            name1 = int(list_information[0][0])
            name2 = list_information[0][1]
            name1 = int(name1).to_bytes(4, byteorder='big', signed=True)
            name2 = int(name2).to_bytes(4, byteorder='big', signed=True)
            mode = int(mode).to_bytes(4, byteorder='big', signed=True)
            sum   = int(sum*0x10000).to_bytes(4, byteorder='big', signed=True)
            self.gcvdata.extend(name1)
            self.gcvdata.extend(name2)
            self.gcvdata.extend(mode)
            self.gcvdata.extend(sum)
        else:
            self.gcvdata = bytearray()
            name1 = int(0).to_bytes(4, byteorder='big', signed=True)
            name2 = int(0).to_bytes(4, byteorder='big', signed=True)
            mode = int(0).to_bytes(4, byteorder='big', signed=True)
            sum   = int(0.0*0x10000).to_bytes(4, byteorder='big', signed=True)
            self.gcvdata.extend(name1)
            self.gcvdata.extend(name2)
            self.gcvdata.extend(mode)
            self.gcvdata.extend(sum)
    def process(self, frame):

        list_information = self.Recognition(frame)
        mode = self.fire_mode(list_information)
        sum,a = self.calculate(list_information)
        frame = self.cv_ui(frame,list_information,sum,a,mode)
        self.dispose(mode,sum,list_information)

        return (frame, self.gcvdata)
