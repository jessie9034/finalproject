#good
import pygame
import sys
import math

# 初始化 Pygame
pygame.init()

# 設定視窗大小
win_width, win_height = 640, 480
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Pikachu Ball Game")

# 設定顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 設定初始速度
GRAVITY = 1500.0
MOVING_SPEED = 15
PIKACHU_JUMP_FORCE = -600

# 載入 Pikachu 圖片
pikachu_a = pygame.image.load("pikachu_left.png")
pikachu_a = pygame.transform.scale(pikachu_a, (90, 150))  # 調整大小

pikachu_b = pygame.image.load("pikachu_right.png")
pikachu_b = pygame.transform.scale(pikachu_b, (90, 150))  # 調整大小

# 載入 volleyball 圖片
volleyball = pygame.image.load("volleyball.png")
volleyball = pygame.transform.scale(volleyball, (60, 60))

# 載入背景圖片
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (win_width, win_height))  # 調整背景圖片大小

# Pikachu 屬性
left_pikachu_pos = [40, win_height - 150]
left_pikachu_vector = [0.0, 0.0]
left_pikachu_jumping = False

right_pikachu_pos = [500, win_height - 150]
right_pikachu_vector = [0.0, 0.0]
right_pikachu_jumping = False

pikachu_width = 85
pikachu_height = 73
# Ball 屬性
ball_pos = [200, 100]
ball_vector = [500, -1000]
volleyball_size = (60, 60)  # 調整球的大小

# 設定分數
point1 = 0
point2 = 0

# 設定字型
font = pygame.font.Font(None, 36)

# 圍欄屬性
fence_height = 200

# 初始化聲音模組
pygame.mixer.init()

# 載入背景音樂
pygame.mixer.music.load("background_music.mp3")

# 設定音量（選擇性）
pygame.mixer.music.set_volume(0.5)

# 載入殺球音效
kill_sound = pygame.mixer.Sound("kill_sound.wav")
button_sound = pygame.mixer.Sound("button_sound.wav")
jump_sound = pygame.mixer.Sound("jump_sound.wav")
land_sound = pygame.mixer.Sound("landing_sound.wav")

# 播放背景音樂（循環播放）
pygame.mixer.music.play(-1)

debug = pygame.image.load("debug_icon.png")
debug = pygame.transform.scale(debug, (100, 100))  # 調整大小
debug_mode = 0

# 開始按鈕相關設定
start_button_font = pygame.font.Font(None, 48)
start_button_text = start_button_font.render("Start", True, WHITE)
start_button_rect = start_button_text.get_rect(center=(win_width // 2, win_height // 2))
start_button_active = False

# 重新開始按鈕相關設定
restart_button_font = pygame.font.Font(None, 48)
restart_button_text = restart_button_font.render("Restart", True, WHITE)
restart_button_rect = restart_button_text.get_rect(center=(win_width // 4, win_height // 2))

# 退出按鈕相關設定
exit_button_font = pygame.font.Font(None, 48)
exit_button_text = exit_button_font.render("Exit", True, WHITE)
exit_button_rect = exit_button_text.get_rect(center=(3 * win_width // 4, win_height // 2))

# 遊戲迴圈
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 點擊 (0, 0) 到 (100, 100) 區域時切換 debug_mode
            if 0 <= event.pos[0] <= 100 and 0 <= event.pos[1] <= 100:
                debug_mode = 1 - debug_mode  # 切換 0 和 1
            elif start_button_rect.collidepoint(event.pos):
                # 按下開始按鈕
                button_sound.play()
                start_button_active = False
            elif restart_button_rect.collidepoint(event.pos):
                # 按下重新開始按鈕
                button_sound.play()
                point1 = 0
                point2 = 0
                start_button_active = False
                ball_pos = [200, 100]
                ball_vector = [500, -1000]
                left_pikachu_pos = [40, win_height - 150]
                right_pikachu_pos = [500, win_height - 150]
                left_pikachu_vector = [0.0, 0.0]
                right_pikachu_vector = [0.0, 0.0]
                left_pikachu_jumping = False
                right_pikachu_jumping = False
                pygame.time.delay(500)  # 等待 0.5 秒
            elif exit_button_rect.collidepoint(event.pos):
                # 按下退出按鈕
                pygame.quit()
                sys.exit()
            elif not start_button_active:
                # 若遊戲未開始，設定按下時的殺球動作
                x, y = event.pos
                x -= ball_pos[0]
                y -= ball_pos[1]
                distance = math.sqrt(x ** 2 + y ** 2)
                angle = math.atan2(y, x)
                speed = math.sqrt(ball_vector[0] ** 2 + ball_vector[1] ** 2)
                ball_vector[0] = speed * math.cos(angle)
                ball_vector[1] = speed * math.sin(angle)
                kill_sound.play()

    # 在遊戲迴圈的主要更新部分
    keys = pygame.key.get_pressed()
    mods = pygame.key.get_mods()    
    # 判斷是否開始遊戲
    if not start_button_active:
        
        # 重置球的位置和速度
        if point1 == 12 or point2 == 12:
            ball_pos = [200, 100]
            ball_vector = [500, -1000]
            land_sound.play()
            
        # 左 Pikachu 控制
        if keys[pygame.K_a] and left_pikachu_pos[0] > 0:
            left_pikachu_pos[0] -= MOVING_SPEED

        if keys[pygame.K_d] and left_pikachu_pos[0] < fence_rect.left - pikachu_width - 5:
            left_pikachu_pos[0] += MOVING_SPEED

        if keys[pygame.K_w] and not left_pikachu_jumping:
            left_pikachu_vector[1] = PIKACHU_JUMP_FORCE
            left_pikachu_jumping = True
            jump_sound.play()

        # 右 Pikachu 控制
        if keys[pygame.K_LEFT] and right_pikachu_pos[0] > fence_rect.right:
            right_pikachu_pos[0] -= MOVING_SPEED

        if keys[pygame.K_RIGHT] and right_pikachu_pos[0] < win_width - pikachu_width - 5:
            right_pikachu_pos[0] += MOVING_SPEED

        if keys[pygame.K_UP] and not right_pikachu_jumping:
            right_pikachu_vector[1] = PIKACHU_JUMP_FORCE
            right_pikachu_jumping = True
            jump_sound.play()

        # 判斷按下的修飾鍵是哪一邊的 SHIFT 鍵
        if mods & pygame.KMOD_LSHIFT:  # 左 SHIFT
            if keys[pygame.K_LSHIFT] and ball_rect.colliderect(left_pikachu_rect):
                # 左 SHIFT 被按下時的殺球動作
                ball_vector = [1000, -2000]  # 設定殺球速度
                kill_sound.play()  # 播放殺球音效

        if mods & pygame.KMOD_RSHIFT:  # 右 SHIFT
            if keys[pygame.K_RSHIFT] and ball_rect.colliderect(right_pikachu_rect):
                # 右 SHIFT 被按下時的殺球動作
                ball_vector = [-1000, -2000]  # 設定殺球速度
                kill_sound.play()  # 播放殺球音效


        # Ball 物理
        ball_vector[1] += GRAVITY / 120.0  # 減緩球的垂直速度
        ball_pos[0] += ball_vector[0] / 120.0
        ball_pos[1] += ball_vector[1] / 120.0

        # Pikachu 跳躍物理
        if left_pikachu_jumping:
            left_pikachu_vector[1] += GRAVITY / 60.0
            left_pikachu_pos[1] += left_pikachu_vector[1] / 60.0 * 2

            if left_pikachu_pos[1] > (win_height - 150):
                left_pikachu_pos[1] = (win_height - 150)
                left_pikachu_jumping = False

        if left_pikachu_pos[1] > (win_height - 150):
            left_pikachu_pos[1] = (win_height - 150)

        if right_pikachu_jumping:
            right_pikachu_vector[1] += GRAVITY / 60.0
            right_pikachu_pos[1] += right_pikachu_vector[1] / 60.0 * 2

            if right_pikachu_pos[1] > (win_height - 150):
                right_pikachu_pos[1] = (win_height - 150)
                right_pikachu_jumping = False

        # Ball 邊界檢查
        if ball_pos[0] <= 0:
            ball_vector[0] *= -1  # 反轉水平方向
            ball_pos[0] = 1

        if ball_pos[0] + 60 >= win_width:
            ball_vector[0] *= -1  # 反轉水平方向
            ball_pos[0] = 579

        if ball_pos[1] <= 0:
            ball_vector[1] *= -1
            ball_pos[1] = 1

        if ball_pos[1] >= win_height - 40:  # 假設球的半徑是20
            # 確定哪個玩家得分
            if ball_pos[0] < win_width // 2:
                point2 += 1
                next_serving_player = "left"  # 下一次球權給左邊的玩家
            else:
                point1 += 1
                next_serving_player = "right"  # 下一次球權給右邊的玩家

            # 重置球的位置、速度，確保速度為初始速度
            ball_pos = [400, 100] if next_serving_player == "left" else [200, 100]
            ball_vector = [500, -1000]


            # 檢查任一玩家是否達到12分
            if point1 == 12 or point2 == 12:
                win.blit(background, (0, 0))
                font_size = 72
                win.blit(font.render(f"Player 1 Wins!", True, RED), (win_width // 4, win_height // 3))
                win.blit(font.render(f"Player 2 Loss", True, RED), (win_width // 4, win_height // 3 + font_size))

                # 顯示重新開始按鈕
                pygame.draw.rect(win, RED, restart_button_rect)
                win.blit(restart_button_text, restart_button_rect)

                # 顯示退出按鈕
                pygame.draw.rect(win, RED, exit_button_rect)
                win.blit(exit_button_text, exit_button_rect)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if restart_button_rect.collidepoint(event.pos):
                            # 重新開始按鈕被點擊
                            button_sound.play()
                            point1 = 0
                            point2 = 0
                            start_button_active = False
                        elif exit_button_rect.collidepoint(event.pos):
                            # 退出按鈕被點擊
                            pygame.quit()
                            sys.exit()

                pygame.time.delay(2000)  # 暫停 2 秒

            # 播放碰到地面的音效
            land_sound.play()

        # Ball 和 Pikachu 碰撞
        ball_rect = pygame.Rect(ball_pos[0], ball_pos[1], 60, 60) 
        # 假設球的半徑是30
        left_pikachu_rect = pygame.Rect(left_pikachu_pos[0] + 3, left_pikachu_pos[1] + 38, pikachu_width, pikachu_height)
        right_pikachu_rect = pygame.Rect(right_pikachu_pos[0] + 3, right_pikachu_pos[1] + 38, pikachu_width, pikachu_height)
        
         # 修改 left_pikachu_rect 的碰撞檢測
        if ball_rect.colliderect(left_pikachu_rect):
            x = ball_pos[0] - (left_pikachu_pos[0])  # 調整為 Pikachu 寬度
            y = ball_pos[1] - (left_pikachu_pos[1])  # 調整為 Pikachu 高度
            distance = math.sqrt(x ** 2 + y ** 2)

            angle = math.atan2(y, x)
            speed = math.sqrt(ball_vector[0] ** 2 + ball_vector[1] ** 2)
            ball_vector[0] = speed * math.cos(angle)
            ball_vector[1] = speed * math.sin(angle)

            # 立即移動球以避免持續碰撞
            ball_pos[0] += ball_vector[0] / 60.0
            ball_pos[1] += ball_vector[1] / 60.0

        # 修改 right_pikachu_rect 的碰撞檢測
        if ball_rect.colliderect(right_pikachu_rect):
            x = ball_pos[0] - (right_pikachu_pos[0])  # 調整為 Pikachu 寬度
            y = ball_pos[1] - (right_pikachu_pos[1])  # 調整為 Pikachu 高度
            distance = math.sqrt(x ** 2 + y ** 2)

            angle = math.atan2(y, x)
            speed = math.sqrt(ball_vector[0] ** 2 + ball_vector[1] ** 2)
            ball_vector[0] = speed * math.cos(angle)
            ball_vector[1] = speed * math.sin(angle)

            # 立即移動球以避免持續碰撞
            ball_pos[0] += ball_vector[0] / 60.0
            ball_pos[1] += ball_vector[1] / 60.0

        # Ball 和 Fence 碰撞
        fence_rect = pygame.Rect(315, win_height - fence_height, 15, fence_height - 40)
        if ball_rect.colliderect(fence_rect):
            # 調整水平位置，讓球不會持續碰撞
            if ball_vector[0] > 0:  # 如果球正在向右移動
                ball_pos[0] = min(ball_pos[0], fence_rect.left - ball_rect.width - 1)
            else:  # 如果球正在向左移動
                ball_pos[0] = max(ball_pos[0], fence_rect.right + 1)

            # 設定反彈後的速度，這裡只反彈水平方向
            ball_vector[0] *= -1

            # 顯示背景
        win.blit(background, (0, 0))

        # 顯示 Pikachu 和 Ball
        win.blit(pikachu_a, left_pikachu_pos)
        win.blit(pikachu_b, right_pikachu_pos)
        win.blit(debug, (0, 0))

        # 顯示旋轉的 volleyball 圖片
        win.blit(volleyball, (int(ball_pos[0]), int(ball_pos[1])))

        # 顯示圍欄
        if debug_mode:
            pygame.draw.rect(win, BLACK, fence_rect)  # 使用黑色繪製圍欄
            pygame.draw.rect(win, BLACK, ball_rect)
            pygame.draw.rect(win, BLACK, left_pikachu_rect)
            pygame.draw.rect(win, BLACK, right_pikachu_rect)

        # 顯示分數
        score_text = font.render(f"{point1} - {point2}", True, RED)
        win.blit(score_text, (win_width // 2 - 40, 10))

        pygame.display.flip()

    else:
        # 顯示開始按鈕
        win.fill(BLACK)
        pygame.draw.rect(win, RED, start_button_rect)
        win.blit(start_button_text, start_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    # 開始按鈕被點擊
                    button_sound.play()
                    start_button_active = False

        pygame.display.flip()

    pygame.time.Clock().tick(60)