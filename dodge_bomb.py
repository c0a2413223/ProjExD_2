import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DEITA={#いどうじしょ
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.rect)-> tuple[bool,bool]:
    yoko,tate=True,True
    if rct.left<0 or WIDTH<rct.right:
        yoko=False
    if rct.top<0 or HEIGHT <rct.bottom:
        tate=False
    return yoko,tate


def gameover(screen:pg.Surface)-> None:
    #ぶらっくあうと
    black=pg.Surface(screen.get_size())
    black.set_alpha(150)
    screen.blit(black,(0,0))
    pg.draw.rect(black,(0,0,0),black.get_rect())

    #こうかとんしょうかん
    kiharu_sad=pg.image.load("fig/8.png")#8.png
    kiharu_rct=kiharu_sad.get_rect(center=(740,330))
    
    koukaon_sad=pg.image.load("fig/8.png")
    koukaon_rct=koukaon_sad.get_rect(center=(370,330))
    screen.blit(kiharu_sad,kiharu_rct)
    screen.blit(koukaon_sad,koukaon_rct)
    
    #げーむおーばーもじ
    font=pg.font.Font(None,80)
    text=font.render("Game Over",True,(255,255,255))
    text_rect=text.get_rect(center=(550,330))
    screen.blit(text,text_rect)

    pg.display.update()
    time.sleep(5)

    #2,時間とともに
def init_bb_imgs()->tuple[list[pg.Surface],list[int]]:
    bb_imgs=[]
    bb_accs=[a for a in range(1,11)]#加速リスト
    for r in range(1,11):
        bb_img=pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    return bb_imgs,bb_accs


# if kk_rct.colliderect(bb_rct):
#     gameover(screen)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img=pg.Surface((20,20))    #からのsurfaceをつくる（ばくだんよう）
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)  #あかいえんをえがく
    bb_img.set_colorkey((0,0,0))
    bb_rct=bb_img.get_rect()#ばくだんrectしゅとく
    bb_rct.centerx=random.randint(0,WIDTH)#よこざひょうのらんすう
    bb_rct.centery=random.randint(0,HEIGHT)#たてざひょうのらんすう
    vx,vy=+5,+5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DEITA.items():
            if key_lst[key]:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) !=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_imgs,bb_accs=init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]


        bb_rct.move_ip(avx,avy)
        yoko,tate=check_bound(bb_rct)
        if not yoko:
            vx*=-1
        if not tate:
            vy*=-1
        screen.blit(bb_img,bb_rct)
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

df