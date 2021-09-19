import pygame
import os
import random
import time
import pickle
bodies=[]

class Environment(object):
    def build_object(self,surface, loaded_image,position,position_prev):
        self.position=position
        self.position_prev=position_prev
        self.image=pygame.image.load(loaded_image)
        surface.blit(self.image,self.position)

    def start_screen(self, surface,sc):
        self.font_title=pygame.font.Font(None,60)
        self.font_play = pygame.font.Font(None, 30)
        self.font_score=pygame.font.Font(None, 30)
        self.font_author = pygame.font.Font(None, 20)
        text=self.font_title.render('Snake',True,(60,50,150))
        text2 = self.font_title.render('Snake', True, (0, 0, 0))
        text3 = self.font_play.render('[ESC - exit]   [SPACE - play]', True, (0, 0, 0))
        best_score_text=self.font_score.render(("Best score: "+sc),True,(0,250,10))
        author = self.font_author.render('Copyright by Adrian Ginalski', True, (255, 255, 255))
        while True:
            self.build_object(surface, "background.png",(0,0),(0,0))
            surface.blit(text2, (328, 198))
            surface.blit(text,(330,200))
            surface.blit(text3, (250, 250))
            surface.blit(best_score_text, (315, 280))
            surface.blit(author, (600, 580))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.system(exit(0))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        os.system(exit(0))
                    if event.key == pygame.K_SPACE:
                        return

    def pause(self,surface):
        self.font_title = pygame.font.Font(None, 60)
        self.font_play = pygame.font.Font(None, 30)
        text = self.font_title.render('PAUSE', True, (60, 50, 150))
        text2 = self.font_title.render('PAUSE', True, (0, 0, 0))
        text3 = self.font_play.render('[ESC - exit]   [SPACE - continue]', True, (0, 0, 0))
        while True:
            self.build_object(surface, "background.png", (0, 0), (0, 0))
            surface.blit(text2, (328, 198))
            surface.blit(text, (330, 200))
            surface.blit(text3, (230, 250))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.system(exit(0))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        os.system(exit(0))
                    if event.key == pygame.K_SPACE:
                        return

    def game_over(self, surface,score,best_score):
        self.font_title = pygame.font.Font(None, 60)
        self.font_title2 = pygame.font.Font(None, 70)
        self.font_score=pygame.font.Font(None, 30)
        game_over_text=self.font_title.render('GAME OVER!', True, (255, 10, 10))
        game_over_text2 = self.font_title.render('GAME OVER!', True, (0, 0, 0))
        score_text=self.font_score.render(('Your score: '+score),True,(0,0,0))
        best_score_text = self.font_score.render(('Best score: ' + best_score), True, (0, 240, 10))
        self.build_object(surface, "background.png", (0, 0), (0, 0))
        surface.blit(game_over_text2, (247, 177))
        surface.blit(game_over_text, (250, 180))
        surface.blit(score_text,(220, 230))
        surface.blit(best_score_text, (400, 230))
        pygame.display.flip()
        time.sleep(3)

    def show_points(self, surface):
        self.show_info=pygame.font.Font(None, 20)
        self.points=pygame.font.Font(None, 30)
        calculate_points=str((len(bodies)-3)*10)
        set_points=self.points.render(("POINTS: "+calculate_points),True,(150,150,20))
        show_info=self.show_info.render("ESC - quit     P - PAUSE", True, (255,255,255))
        surface.blit(set_points, (650,30))
        surface.blit(show_info,(10,580))

class Create_head(Environment):
    def clear_flag(self):
        self.flag_down = False
        self.flag_up = False
        self.flag_left = False
        self.flag_right = False
        self.changed_direction=False

    def check_flag(self):
        if self.flag_up == True:
            self.position[1]=self.position[1]-25
        if self.flag_down == True:
            self.position[1]=self.position[1]+25
        if self.flag_left == True:
            self.position[0]=self.position[0]-25
        if self.flag_right == True:
            self.position[0]=self.position[0]+25

    def calculating_prev_position(self):
        self.position_prev[0] = self.position[0]
        self.position_prev[1] = self.position[1]
        head_position_prev = [self.position_prev[0], self.position_prev[1]]
        return head_position_prev

    def calculating_actual_position(self):
        head_position = [self.position[0], self.position[1]]
        return head_position

    def check_wall_collision(self):
        width,height=pygame.display.get_surface().get_size()
        if (self.position[0]<0 or self.position[0]>width-20 or self.position[1]<0 or self.position[1]>height-20):
            return True
        else:
            return False

class Create_body(Create_head):
    pass

class Item(object):
    def calculate_position(self):
            X = random.randint(0, 31)
            Y = random.randint(0, 23)
            self.X = X * 25
            self.Y = Y * 25
            self.position = [self.X, self.Y]
            self.check_collision_with_body()

    def check_collision_with_body(self):
        for element in bodies:
            if self.position == element.position:
                self.calculate_position()
    def clear_counter(self):
        self.counter=3

    def draw_item(self,surface,image):
        self.image = pygame.image.load(image)
        surface.blit(self.image, self.position)

    def check_touch(self,surface,head_position):
        item_position=[self.X, self.Y]
        if head_position==item_position:
            bodies_last_element=bodies[len(bodies)-1]
            body = Create_body()
            body.build_object(surface, "body.png", bodies_last_element.position_prev, (0,0))
            bodies.append(body)
            self.calculate_position()
            self.counter=self.counter+1

    def check_counter(self):
        return self.counter

class Start_game(object):
    def start_game(self):
        try:
            with open("score.sc",'rb') as file:
                sc=pickle.load(file)
        except:
            with open("score.sc",'wb') as file:
                pickle.dump("0",file)
            with open("score.sc",'rb') as file:
                sc=pickle.load(file)

        ###### Preparing variables ######
        Y_pos = 100 #Start X position
        X_pos = 100 #Start Y position
        speed=5 #Snake speed
        counter=0 #Bodies counting
        status_flag=False
        esc_flag=False
        ###### End variables ######

        if pygame.init()[1] != 0:
            print("LIB. INSTALLED WRONGLY")
            return
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 45)
        clock = pygame.time.Clock()
        size = (800, 600)
        surface = pygame.display.set_mode(size, 0, 0)
        background=Environment()
        pygame.display.set_caption("Snake")
        background.start_screen(surface,str(sc))
        head = Create_head()
        head.build_object(surface, "head.png", (X_pos,Y_pos),(X_pos,Y_pos))
        head.clear_flag()
        bodies.append(head)
        item = Item()
        item.calculate_position()
        item.clear_counter()

        ########Creating start body##############
        for i in range(1,3):
            body = Create_body()
            body.build_object(surface, "body.png", (X_pos,Y_pos),(X_pos,Y_pos))##############3
            bodies.append(body)
        ########################################
        head_position_prev = [head.position_prev[0], head.position_prev[1]]
        while True:
            clock.tick(speed)
            head.check_flag()
            status_flag=head.check_wall_collision()
            background.build_object(surface, "background.png", (0, 0), (0, 0))
            item.draw_item(surface, "item.png")
            item.check_touch(surface,head.position)
            counter=item.check_counter()
            if counter%13==0:
                speed=speed+3
                item.clear_counter()
            head_position = head.calculating_actual_position()
            head.build_object(surface, "head.png", head_position, head_position_prev)
            for i in range(0,len(bodies)-1):
                body_position = [bodies[i].position_prev[0], bodies[i].position_prev[1]]
                body_position_prev=[bodies[i+1].position_prev[0], bodies[i+1].position_prev[1]]
                bodies[i+1].build_object(surface, "body.png", body_position, body_position_prev)
                if counter>3:
                    if head_position==body_position:
                         status_flag=True
            head_position_prev = head.calculating_prev_position()
            for i in range(1,len(bodies)):
                bodies[i].position_prev[0] = bodies[i].position[0]
                bodies[i].position_prev[1] = bodies[i].position[1]

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    os.system(exit(0))
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        status_flag=True
                        esc_flag=True
                    if event.key==pygame.K_p:
                        background.pause(surface)
                    if event.key==pygame.K_DOWN:
                        head.clear_flag()
                        head.flag_down=True
                    if event.key==pygame.K_UP:
                        head.clear_flag()
                        head.flag_up = True
                    if event.key==pygame.K_LEFT:
                        head.clear_flag()
                        head.flag_left = True
                    if event.key==pygame.K_RIGHT:
                        head.clear_flag()
                        head.flag_right = True
            if status_flag==True:
                if esc_flag==True:
                    break
                if ((len(bodies)-3)*10)>int(sc):
                    sc=(len(bodies)-3)*10
                with open("score.sc", 'wb') as file:
                    pickle.dump(str(sc), file)
                background.game_over(surface,str((len(bodies)-3)*10),str(sc))
                break
            background.show_points(surface)
            pygame.display.flip()

new_game=Start_game()
while True:
    bodies = []
    new_game.start_game()