import cv2
import numpy as np
import matplotlib.pyplot as plt
from ChainCode import ChainCode







class ActiveContour:
    def __init__(self, image_path, main_window):
        self.image_path = image_path
        self.ui = main_window
        self.gray_image, self.edge_image = self.load_and_process_image()
        self.contour_r, self.contour_c = [], []
        self.contour_points = []
        self.all_img = []

        
        
    def load_and_process_image(self):
        image = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        if image is None:
            print(f"Failed to load image from {self.image_path}")
            return None, None
        image = cv2.resize(image,(360,360))
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("\nSUCCESS - Image is converted to GreyScale")
        padding_img =np.pad(gray_image, pad_width=30, mode='constant',constant_values=255)
        edge_image = cv2.Canny(padding_img, 30, 150)
        print("SUCCESS - Image is converted to Canny Edges\n\n")
        return  np.array(padding_img) , np.array(edge_image)
       

    def get_contour(self):
        return self.contour_points 
    
    def get_gray_image_data(self):
        return self.gray_image

    def get_edge_image_data(self):
        return self.edge_image
    


    def Init_contour(self):     
        self.contour_r, self.contour_c = [], []
        self.contour_points =[]
        self.all_img = []
        points = int(self.ui.Points_Slider.value())
        print(f"points:{points}")
        s = np.linspace(0, 2*np.pi,points)
        contour_r =((np.abs(400- 380*np.sin(s))) // 2).astype(int)
        contour_c =((np.abs(400 + 380*np.cos(s))) // 2).astype(int)
        self.contour_r = np.array(contour_r)
        self.contour_c = np.array(contour_c)    
        for r,c in zip(self.contour_r,self.contour_c):
            self.contour_points.append((r,c))
        self.contour_points = np.array(self.contour_points)  
        self.all_img, self.area_list , self.perimeter_list = self.active_contour()
        return self.all_img, self.area_list , self.perimeter_list
            


    def norm_0_1(self, arr):
        maximum = np.amax(arr)
        if maximum == 0:
            return arr
        return arr/np.amax(arr)
    


    def draw_point(self,lap, row, col, val=0, w1=6, w2=4):
        '''Draws a cross on image at point in image'''
        lap[row - w1 // 2:row + w1 // 2 + 1, col - w2 // 2:col + w2 // 2 + 1] = val
        lap[row - w2 // 2:row + w2 // 2 + 1, col - w1 // 2:col + w1 // 2 + 1] = val
        return lap
    


    def draw_contour(self,lap,contour_points, val=255):
        for i in range(len(contour_points)):
            lap=self.draw_point(lap,contour_points[i][0], contour_points[i][1])
            cv2.line(lap,
                    (contour_points[i][1], contour_points[i][0]),  # (x, y) format
                    (contour_points[(i+1) % len(contour_points)][1], contour_points[(i+1) % len(contour_points)][0]),  # (x, y) format
                    val,
                    1)
        return lap



    def calc_elastic_energy(self, alpha,row,col,next_point):
        elastic_energy = np.zeros((7,7),np.float32)
        for i in range(-3,4):
            for j in range(-3,4):
                elastic_energy[i+3,j+3] =alpha * (np.square(next_point[0]-(row+i)) + np.square(next_point[1]-(col+j)))
        return self.norm_0_1(elastic_energy)
    


    def calc_smooth_energy(self,beta,row,col,next_point,prior_point):
        smooth_energy = np.zeros((7,7),np.float32)
        for i in range(-3,4):
            for j in range(-3,4):
                smooth_energy[i+3,j+3] =  beta* (np.square(next_point[0]-(2*(row+i))+prior_point[0]) + np.square(next_point[1]-(2*(col+j))+prior_point[1]))       
        return self.norm_0_1(smooth_energy)



    def calc_external_energy(self,gamma,row,col,img):
        external_energy = np.zeros((7,7),np.float32)
        for i in range(-3,4):
            for j in range(-3,4):
                external_energy[i+3,j+3] = gamma*np.square(img[row+i,col+j])
        return 1-self.norm_0_1(external_energy)
    

    
    def sum_energies(self,e1,e2,e3,row,col):
        new_row =row
        new_col = col
        total_energies = []  
        total_energies.append(e1)
        total_energies.append(e2)
        total_energies.append(e3)
        total_energies =np.array(total_energies)
        total_energies = np.sum(total_energies,axis=0)
        min_energy = np.argmin(total_energies)
        new_row += min_energy//7 - 3
        new_col += min_energy%7 - 3
        return new_row,new_col
    


    def update_points(self,x,y):
        self.contour_points =[]
        for r,c in zip(x,y):
            self.contour_points.append((r,c))
        return self.contour_points    
    


    def calculate_area(self,contour_data):
        area =0
        for idx in range(len(contour_data)):
            x = contour_data[idx][0]
            y = contour_data[idx][1]
            new_x = contour_data[(idx+1)%(len(contour_data))][0]
            new_y = contour_data[(idx+1)%(len(contour_data))][1]
            dx = new_x - x
            dy = new_y - y
            area += 0.5*(y*dx-x*dy)
        return np.abs(area)
    


    def calculate_perimeter(self,contour_data):
        perimeter = 0
        for idx in range(len(contour_data)):
            x = contour_data[idx][0]
            y = contour_data[idx][1]
            new_x = contour_data[(idx+1)%(len(contour_data))][0]
            new_y = contour_data[(idx+1)%(len(contour_data))][1]
            distance = np.sqrt(((x-new_x)**2)+((y-new_y)**2))      
            perimeter += distance
        return perimeter
            
            

    def active_contour(self):
        iterations = int(self.ui.iterations_Slider.value())
        area_list, perimeter_list = [], []
        for __ in range(iterations):
            lapcopy = np.copy(self.gray_image)
            new_contour_r, new_contour_c = [], []
            for idx in range(len(self.contour_points)):
                row = self.contour_points[idx][0]
                col = self.contour_points[idx][1]
                next_point = (self.contour_points[(idx+1) % len(self.contour_points)][0],self.contour_points[(idx+1) % len(self.contour_points)][1])
                if idx :
                    prior_point = (self.contour_points[idx-1][0],self.contour_points[idx-1][1])
                else:
                    prior_point = (self.contour_points[-1][0],self.contour_points[-1][1])
                e1 = self.calc_elastic_energy(1,row,col,next_point)
                e2 = self.calc_smooth_energy(1,row,col,next_point,prior_point)
                e3 = self.calc_external_energy(1,row,col,self.get_edge_image_data())
                new_row,new_col = self.sum_energies(e1,e2,e3,row,col)
                new_contour_r.append(new_row)
                new_contour_c.append(new_col)
            self.contour_c = new_contour_c
            self.contour_r = new_contour_r
            self.contour_points= self.update_points(new_contour_r,new_contour_c)
            area_list.append(self.calculate_area(self.contour_points))
            perimeter_list.append(self.calculate_perimeter(self.contour_points))
            lapcopy = self.draw_contour(lapcopy,self.contour_points)
            self.all_img.append(lapcopy)
        return self.all_img, area_list, perimeter_list    