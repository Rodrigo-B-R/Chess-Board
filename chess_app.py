import tkinter as tk
import os
from PIL import Image, ImageTk

        
class Pieces:

    pieces= {
            "black-pawn" : os.path.join("pieces","black-pawn.png") ,
            "black-king": os.path.join("pieces","black-king.png"),
            "black-knight": os.path.join("pieces","black-knight.png"), 
            "black-queen": os.path.join("pieces","black-queen.png"),
            "black-bishop": os.path.join("pieces", "black-bishop.png"),
            "white-pawn": os.path.join("pieces","white-pawn.png"),
            "white-king": os.path.join("pieces", "white-king.png"),
            "white-queen": os.path.join("pieces", "white-queen.png"),
            "white-bishop": os.path.join("pieces","white-bishop.png"),
            "white-knight": os.path.join("pieces","white-knight.png"),
            "black-rook": os.path.join("pieces","black-rook.png"),
            "white-rook": os.path.join("pieces","white-rook.png")
    }
    
    @classmethod
    def get_image(cls,piece_name):
        return cls.pieces.get(piece_name)

    def is_blocked(self,start_row,start_col,end_row,end_col,pieces):

        row_diff= end_row-start_row
        col_diff= end_col-start_col

        row_step=1 if row_diff >0 else -1 if row_diff<0 else 0
        col_step=1 if col_diff>0 else -1 if col_diff<0 else 0
        

        current_col= start_col
        current_row= start_row

        while True :

            current_row= current_row + row_step
            current_col = current_col+ col_step

            if current_col==end_col and current_row==end_row:
                break

        
            for piece in pieces:
                if piece.row == current_row and piece.column ==current_col:
                    return True
            
            

        return False

        
    
    def target_piece(self,end_row,end_col,pieces):
        for piece in pieces:
            if piece.row ==end_row and piece.column == end_col :
                return piece 
        return None

    



class Pawn(Pieces):

    def __init__(self, color, row, column):
        self.row=row
        self.column=column
        self.color=color
        self.piece_name= f"{color}-pawn"
        self.image = self.get_image(self.piece_name)
        self.move_count=0
        self.Tk_Image()
        
        


    
    def Tk_Image(self):
        self.piece_image=Image.open(self.image)
        self.piece_image=self.piece_image.convert("RGBA")
        self.tk_image= ImageTk.PhotoImage(self.piece_image)

    def is_valid_move(self,start_row, start_col,end_row,end_col,pieces):

        #direction es la direccion de la pieza para que no se pueda mover hacia atras
        #positiva significa que es negra osea que baja en la interfaz y negativa que es blanca

       

        direction = 1 if self.color == "black" else -1

        row_diff = end_row - start_row
        col_diff = abs(end_col - start_col)

                
        if row_diff == direction and col_diff == 0:
            
            if not self.is_blocked(start_row, start_col, end_row, end_col, pieces):
                
                self.move_count += 1
                return True, None

        
        if self.move_count == 0 and row_diff == 2 * direction and col_diff == 0:
            
            if not self.is_blocked(start_row, start_col, end_row, end_col, pieces):
               
                self.move_count += 1
                return True, None

       
        if row_diff == direction and col_diff == 1:
            target_piece = self.target_piece(end_row, end_col, pieces)

            
            if target_piece is not None and target_piece.color != self.color:
               
                self.move_count += 1
                return True, target_piece

        return False, None

    # def en_passant(self,end_row,end_col,pieces,direction):

    #     for piece in pieces:
    #         if "pawn" in piece.piece_name:
    #             if piece.row == end_row - direction and piece.column == end_col and piece.move_count == 0:
    #                 return True, piece 
    #     return False, None





class Rook(Pieces):

    def __init__(self, color, row, column):
        self.row=row
        self.column=column
        self.color=color
        self.piece_name= f"{color}-rook"
        self.image = self.get_image(self.piece_name)
        self.Tk_Image()
        self.move_count=0

    def Tk_Image(self):
        self.piece_image=Image.open(self.image)
        self.piece_image=self.piece_image.convert("RGBA")
        self.tk_image= ImageTk.PhotoImage(self.piece_image)

    def is_valid_move(self,start_row, start_col,end_row,end_col,pieces):

        row_diff= abs(start_row-end_row)
        col_diff= abs(start_col-end_col)

        if  self.is_blocked(start_row,start_col,end_row,end_col,pieces):
            return False,None
        
        target_piece=self.target_piece(end_row,end_col,pieces)

        if row_diff==0 or col_diff==0:
            if target_piece:
                if target_piece.color==self.color:
                    return False, None
                else:
                    
                    self.move_count+=1
                    return True, target_piece
       
            else:
               
                self.move_count +=1
                return True,None
            
        else: return False,None

class Queen(Pieces):

    def __init__(self, color, row, column):
        self.row=row
        self.column=column
        self.color=color
        self.piece_name= f"{color}-queen"
        self.image = self.get_image(self.piece_name)
        self.Tk_Image()


    
    def Tk_Image(self):
        self.piece_image=Image.open(self.image)
        self.piece_image=self.piece_image.convert("RGBA")
        self.tk_image= ImageTk.PhotoImage(self.piece_image)

    def is_valid_move(self,start_row, start_col,end_row,end_col,pieces):

        col_diff=abs(end_col-start_col)
        row_diff= abs(end_row-start_row)

        if self.is_blocked(start_row,start_col,end_row,end_col,pieces):
            return False,None

        target_piece=self.target_piece(end_row,end_col,pieces)

        if (col_diff==row_diff) or (col_diff == 0 or row_diff==0):
            if target_piece: #Verifica si hay un pieza a capturar

                if target_piece.color == self.color: #Verifica si es del mismo color
                    return False,None

                else:
                    return True, target_piece 


            else:#Mueve la pieza si no hay pieza que capturar
            
                self.row= end_row
                self.column= end_col 
                return True, target_piece
        else: return False,None

        


    

class   Bishop(Pieces):

    def __init__(self, color, row, column):
        self.row=row
        self.column=column
        self.color=color
        self.piece_name= f"{color}-bishop"
        self.image = self.get_image(self.piece_name)
        self.Tk_Image()


    
    def Tk_Image(self):
        self.piece_image=Image.open(self.image)
        self.piece_image=self.piece_image.convert("RGBA")
        self.tk_image= ImageTk.PhotoImage(self.piece_image)

    def is_valid_move(self,start_row, start_col,end_row,end_col,pieces):

        row_diff= abs(start_row-end_row)
        col_diff=abs(start_col-end_col)

        if   row_diff != col_diff :
            return False,None

        if self.is_blocked(start_row,start_col,end_row,end_col,pieces):
            return False,None

        target_piece=self.target_piece(end_row,end_col,pieces)

        
        if target_piece: #Verifica si hay un pieza a capturar

            if target_piece.color ==self.color: #Verifica si es del mismo color
                return False,None

            else:
              
                return True, target_piece 


        else:#Mueve la pieza si no hay pieza que capturar
            
          
            return True, target_piece


class Knight(Pieces):

    def __init__(self, color, row, column):
        self.row=row
        self.column=column
        self.color=color
        self.piece_name= f"{color}-knight"
        self.image = self.get_image(self.piece_name)
        self.Tk_Image()

    def Tk_Image(self):
        self.piece_image=Image.open(self.image)
        self.piece_image=self.piece_image.convert("RGBA")
        self.tk_image= ImageTk.PhotoImage(self.piece_image)

    def is_valid_move(self,start_row, start_col,end_row,end_col,pieces):

        row_diff=abs(end_row-start_row)
        col_diff=abs(end_col-start_col)

        target_piece= self.target_piece(end_row,end_col,pieces)

        
        if (row_diff==2 and col_diff==1) or (row_diff==1 and col_diff==2):

            if target_piece:
                if target_piece.color == self.color:
                    return False,None
                else:
                    return True,target_piece

            else: 
                
                return True,None
                
        else:
            return False,None

        

class  King(Pieces):

    def __init__(self, color, row, column):
        self.row=row
        self.column=column
        self.color=color
        self.piece_name= f"{color}-king"
        self.image = self.get_image(self.piece_name)
        self.Tk_Image()
        self.move_count=0


    
    def Tk_Image(self):
        self.piece_image=Image.open(self.image)
        self.piece_image=self.piece_image.convert("RGBA")
        self.tk_image= ImageTk.PhotoImage(self.piece_image)

    def is_valid_move(self,start_row, start_col,end_row,end_col,pieces):

        row_diff=abs(end_row-start_row)
        col_diff=abs(end_col-start_col)

        
        target_piece= self.target_piece(end_row,end_col,pieces)
        
            
        if (end_col == start_col+2 or end_col==start_col-2 ) and end_row==start_row :

            can_castle, rook= self.can_castle(start_row,start_col,end_col,pieces)

            
            if can_castle:
                if end_col == start_col+2: #enroque corto
                   
                    self.move_count +=1

                    rook.column= end_col-1
                    rook.move_count +=1

                    return True, None, rook

                if end_col == start_col-2: #enroque largo
                    
                    self.move_count +=1

                    rook.column= end_col+1
                    rook.move_count+=1
                    return True, None, rook

        if row_diff<2 and col_diff<2:

            

            if target_piece: #Verifica si hay un pieza a capturar

                if target_piece.color ==self.color or "king" in target_piece.piece_name: #Verifica si es del mismo color
                    return False, None, None

                else:
                 
                    self.move_count+=1
                    return True,target_piece,None


            else:#Mueve la pieza si no hay pieza que capturar
            
                self.move_count+=1
                return True, target_piece,None
        else: 
            return False,None,None

        

    def can_castle(self,start_row,start_col,end_col,pieces):


        if end_col == start_col+2: #enroque corto
            rook_col=start_col+3
                
        elif end_col == start_col-2: #enroque largo
            rook_col=start_col-4

        else: return False, None
            
        rook=None
        for p in pieces:
                    if "rook" in p.piece_name and p.color ==self.color and p.move_count==0 and p.column==rook_col and p.row == start_row:
                        rook=p
                        break
        if rook==None:
            return False,None
        
        if self.is_blocked(start_row, start_col, rook.row, rook.column, pieces):
            return False, None
        
        if self.move_count==0:
            return True, rook
    


class Board():

    def __init__(self,root,rows=8,columns=8,square_size=100):

        self.rows = rows
        self.columns = columns
        self.square_size = square_size
        self.root = root
                                                                                                                           
        
        self.board = tk.Canvas(root, width= columns * square_size, height= rows*square_size)
        self.board.pack(fill='both',expand=True)

        
        self.image_references=[]
        self.piece_list=[]

        self.black_pieces=[]
        self.white_pieces=[]

        self.selected_piece=None
        self.move_count=0

        self.create_board()

        self.board.bind("<Button-1>", self.select_piece)
        self.board.bind("<B1-Motion>",self.drag_piece)
        self.board.bind("<ButtonRelease-1>",self.drop_piece)

        
    def create_board(self):

        for row in range(self.rows):

            for column in range(self.columns):

                if (row+column)%2 ==0 : 
                    color='white' 

                else: 
                    color='green'

                x1= column * self.square_size 
                x2= x1 + self.square_size  
                y1=row*self.square_size 
                y2=y1+ self.square_size

                self.board.create_rectangle(x1,y1,x2,y2, fill= color, outline='red')


    def place_piece(self,piece): 

        self.piece_list.append(piece)

        if piece.color =="black": self.black_pieces.append(piece)
        if piece.color=="white": self.white_pieces.append(piece)

        x= piece.column*self.square_size +(self.square_size//2) #Donde esta la pieza, mas la mitad del tamaño del cuadrado en x y y
        y= piece.row*self.square_size + (self.square_size//2)
        piece_id= self.board.create_image(x,y,image=piece.tk_image,anchor="center")


        self.image_references.append(piece.tk_image)
        piece.graphic=piece_id
        

        
    def turns(self):
        

        if self.move_count %2 ==0:
            return "white"
        else:
            return "black"
    
    def select_piece(self,event):
        
       x,y=  event.x, event.y 
       col, row= x//self.square_size, y//self.square_size
       turn=self.turns()

       for piece in self.piece_list:
        if piece.column == col and piece.row == row and piece.color ==turn :
            
            self.selected_piece= piece
            

            break


    def drag_piece(self,event):

        if self.selected_piece:
            self.board.coords(self.selected_piece.graphic,event.x,event.y)

    # def square_is_attacked(self,row,column,color):
         
    #     enemy_color= "black" if color =="white" else "white"

    #     for p in self.piece_list:
    #         if p.color == enemy_color:  
    #             start_row,start_col=p.row,p.column
    #             is_valid,*_= p.is_valid_move(start_row,start_col,row,column,self.piece_list,check_for_check=False)
    #             if is_valid:
    #                 return True
    #     return False


    # def is_king_checked(self,color):
    #     king= self.find_king(color)

    #     return self.square_is_attacked(king.row,king.column,king.color)
        
    # def check_for_check(self):
    #     turn=self.turns()
    #     if self.is_king_checked(turn):
    #         print("El rey esta en jaque")
            


    # def check(self):

    #     #check=False

    #     for p in self.piece_list:
    #         if p.color == self.turns() and "king" in p.piece_name:
    #             king = p

        

    #     enemy_color = "white" if king.color == "black" else "black"

    #     return king

        #por cada pieza del color opuesto al del rey checamos si ataca la casilla del rey 
        # for p in self.piece_list:
        #     if "king" not in p.piece_name:
        #         is_valid, target_piece = p.is_valid_move(start_row,start_col,king_row,king_col,self.piece_list)

        #         if p.color == enemy_color and is_valid == True:
        #             check =True

        # if check==True:
        #     print("Jaque")


    def is_valid_move(self,start_row,start_col,end_row,end_col):

        

        for p in self.piece_list:
            if p.row==self.selected_piece.row and p.column == self.selected_piece.column :
                piece=p
                break
        
        
        
        return piece.is_valid_move(start_row,start_col,end_row,end_col,self.piece_list)
        
        #Mando a checar si el movimiento es valido a la clase de la pieza, tambien se updatea el valor de la pieza (row y column) en ese objeto

                

    def drop_piece(self,event):

        if self.selected_piece:

            original_col=self.selected_piece.column
            original_row=self.selected_piece.row

            eliminated_pieces=[]

            x,y =event.x,event.y
            col_target,row_target= x//self.square_size, y//self.square_size

            new_x= col_target * self.square_size +(self.square_size//2)
            new_y= row_target *self.square_size +(self.square_size//2)

            

            #nuevas reglas
            #taken_piece=self.selected_piece.target_piece(row_target,col_target)


            # king=check()self.
            # king_row,king_col = king.row,king.column
            # enemy_color = "white" if king.color == "black" else "black"

            

            

            extra_piece= None
            if "king" in self.selected_piece.piece_name:
                is_valid, taken_piece,extra_piece = self.is_valid_move(original_row, original_col, row_target, col_target)
                
            else: 
                is_valid, taken_piece = self.is_valid_move(original_row, original_col, row_target, col_target) #llamo a funcion is_valid_move que me da la pieza capturada y si el movimiento es legal
                # check, taken_piece = self.is_valid_move(original_row, original_col, king_row , king_col)

                # if check==True  :
                #     print("Check")

            if is_valid == True: #Si el movimiento es legal updateo el tablero, la lista de piezas y piezas eliminadas
                self.selected_piece.column = col_target
                self.selected_piece.row = row_target


                self.board.coords(self.selected_piece.graphic, new_x,new_y)
                self.move_count +=1
                


                if taken_piece is not None:
                    self.board.delete(taken_piece.graphic)
                    eliminated_pieces.append(taken_piece)

                    self.piece_list.remove(taken_piece)

                    
                    #self.selected_piece=None
                if extra_piece is not None:
                    self.board.coords(
                        extra_piece.graphic, 
                        extra_piece.column*self.square_size+(self.square_size//2), 
                        extra_piece.row*self.square_size+(self.square_size//2))
                    
                

                

            else: 
                self.board.coords(
                        self.selected_piece.graphic, 
                        original_col*self.square_size+(self.square_size//2), 
                        original_row*self.square_size+(self.square_size//2))

        self.selected_piece=None


def main():


    root=tk.Tk()
    root.title('Chess Board')

 
    tablero= Board(root)
  
   

    black_pawns= {}
    white_pawns={}


    for i in range(8):


        black_pawn=Pawn(color="black",row=1,column=i)

        black_pawns[f"black_pawn{i+1}"]=black_pawn
        tablero.place_piece(black_pawn)

        white_pawn=Pawn(color="white",row=6,column=i)
        white_pawns[f"white_pawn{i+1}"]=white_pawn
        tablero.place_piece(white_pawn)

 

    back_rank_pieces={
    "rook_a1":Rook(color="white",row=7,column=0),
    "rook_h1":Rook(color="white",row=7,column=7),

    "rook_a8":Rook(color="black",row=0,column=0),
    "rook_h8":Rook(color="black",row=0,column=7),

    "black_queen":Queen(color="black",row=0,column=3),
    "white_queen":Queen(color="white",row=7,column=3),

    "white_king": King(color="white", row=7,column=4),
    "black_king": King(color="black",row=0,column=4),

    "knight_b1":Knight(color="white",row=7,column=1),
    "knight_g1":Knight(color="white",row=7,column=6),

    "knight_b8":Knight(color="black",row=0,column=1),
    "knight_g8":Knight(color="black",row=0,column=6),

    "bishop_c1":Bishop(color="white",row=7,column=2),
    "bishop_f1":Bishop(color="white",row=7,column=5),

    "bishop_c8":Bishop(color="black",row=0,column=2),
    "bishop_f8":Bishop(color="black",row=0,column=5)
    }


    for value in back_rank_pieces.values():
        tablero.place_piece(value)
        
    root.mainloop()
    
    
if __name__ == '__main__':
    main()


