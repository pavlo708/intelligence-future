import pygame as pg
from settings import *
from window_settings import *
from game import *
from shop import draw_shop
from button import Button
from player import Player
# Инициализация Pygame
pg.init()
# Зациклить фоновую музыку
class MenuState:                                                                                                                                                         
    def __init__(self):
        self.buttons = []
        self.create_buttons()
        self.temp_player = Player(0, 0, 100, 0, 0, "basic")
        self.temp_coins = 25
        self.scroll_offset = 0
        self.items_per_page = 3
        self.show_controls = False
        self.next_state = None
        
        # Настройки звука
        self.music_volume = 0.5  # текущая громкость музыки (0.0-1.0)
        self.sfx_volume = 0.5    # текущая громкость звуков (0.0-1.0)
        
    def create_buttons(self):
        button_width, button_height = 200, 50
        start_y = SCREEN_HEIGHT // 2 - 100
        
        self.buttons = [
            Button(SCREEN_WIDTH//2 - button_width//2, start_y, button_width, button_height, "Играть", 
                  lambda: self.set_state("game")),
            Button(SCREEN_WIDTH//2 - button_width//2, start_y + 70, button_width, button_height, "Магазин", 
                  lambda: self.set_state("shop")),
            Button(SCREEN_WIDTH//2 - button_width//2, start_y + 140, button_width, button_height, "Настройки", 
                  lambda: self.set_state("settings")),
            Button(SCREEN_WIDTH//2 - button_width//2, start_y + 210, button_width, button_height, "Управление", 
                  lambda: self.toggle_controls()),
            Button(SCREEN_WIDTH//2 - button_width//2, start_y + 280, button_width, button_height, "Выход", 
                  lambda: self.set_state("quit"))
        ]
        
        # Кнопки для настроек звука
        self.sound_buttons = [
            Button(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 - 60, 100, 40, "Музыка +", 
                  lambda: self.adjust_volume("music", 0.1)),
            Button(SCREEN_WIDTH//2 + 150, SCREEN_HEIGHT//2 - 60, 100, 40, "Музыка -", 
                  lambda: self.adjust_volume("music", -0.1)),
            Button(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 + 10, 100, 40, "Звуки +", 
                  lambda: self.adjust_volume("sfx", 0.1)),
            Button(SCREEN_WIDTH//2 + 150, SCREEN_HEIGHT//2 + 10, 100, 40, "Звуки -", 
                  lambda: self.adjust_volume("sfx", -0.1)),
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 40, "Назад (TAB)", 
                  lambda: self.set_state("menu"))
        ]
    
    def adjust_volume(self, volume_type, change):
        """Изменяет громкость с ограничением диапазона"""
        if volume_type == "music":
            self.music_volume = max(0.0, min(1.0, self.music_volume + change))
            pg.mixer.music.set_volume(self.music_volume)
        elif volume_type == "sfx":
            self.sfx_volume = max(0.0, min(1.0, self.sfx_volume + change))
            # Здесь нужно обновить громкость звуковых эффектов
    
    def toggle_controls(self):
        self.show_controls = not self.show_controls
        
    def set_state(self, new_state):
        self.next_state = new_state

    def update(self, mouse_pos, events):
        # Обновляем состояние кнопок в зависимости от текущего экрана
        if self.next_state == "settings":
            buttons = self.sound_buttons
        else:
            buttons = self.buttons
            
        for button in buttons:
            button.check_hover(mouse_pos)     

    def draw(self, surface):
        bg = pg.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(bg, (0, 0))
        
        title = font.render("Future Game", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        warning = small_font.render("Внимание: при выходе в меню во время игры деньги не сохранятся!", True, (255, 0, 0))
        surface.blit(warning, (SCREEN_WIDTH//2 - warning.get_width()//2, 120))
        
        # Рисуем кнопки в зависимости от текущего состояния
        if self.next_state == "settings":
            self.draw_settings(surface)
        else:
            for button in self.buttons:
                button.draw(surface)
            
        if self.show_controls:
            self.draw_controls(surface)
    
    def draw_settings(self, surface):
        """Отрисовка экрана настроек звука"""
        # Фон
        settings_bg = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        settings_bg.fill((30, 30, 30))
        surface.blit(settings_bg, (0, 0))
        
        # Заголовок
        title = font.render("Настройки звука", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        # Кнопки регулировки громкости
        for button in self.sound_buttons:
            button.draw(surface)
        
        # Текущие значения громкости
        music_text = font.render(f"Музыка: {int(self.music_volume * 100)}%", True, WHITE)
        sfx_text = font.render(f"Звуки: {int(self.sfx_volume * 100)}%", True, WHITE)
        
        surface.blit(music_text, (SCREEN_WIDTH//2 - music_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
        surface.blit(sfx_text, (SCREEN_WIDTH//2 - sfx_text.get_width()//2, SCREEN_HEIGHT//2 + 10))
        
        # Подсказка
        hint = small_font.render("Используйте кнопки +/- для регулировки громкости", True, (200, 200, 200))
        surface.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT//2 + 80))
    
    def draw_controls(self, surface):
        """Отрисовка окна управления"""
        controls_bg = pg.Surface((500, 300))
        controls_bg.fill((50, 50, 50))
        surface.blit(controls_bg, (SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//3))
        
        controls_title = font.render("Управление", True, WHITE)
        surface.blit(controls_title, (SCREEN_WIDTH//2 - controls_title.get_width()//2, SCREEN_HEIGHT//2 - 130))
        
        controls = [
            "Движение: W, A, S, D",
            "Стрельба: ЛКМ",
            "Поставить барьер: X",
            "Граната: ПКМ",
            "Пауза: ESC",
            "Выход в меню: TAB"
        ]
        
        for i, control in enumerate(controls):
            text = small_font.render(control, True, WHITE)
            surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 80 + i * 30))
            
        close_hint = small_font.render("Нажмите любую кнопку чтобы закрыть", True, WHITE)
        surface.blit(close_hint, (SCREEN_WIDTH//2 - close_hint.get_width()//2, SCREEN_HEIGHT//2 + 100))

def main_menu():
    load_player_stats()
    
    temp_player = Player(0, 0, 100, 0, 10, player_stats["equipment"])
    temp_player.grenades = player_stats["grenades"]
    temp_player.has_pistol = player_stats.get("has_pistol", False)
    temp_player.has_rifle = player_stats.get("has_rifle", False)
    temp_player.has_shotgun = player_stats.get("has_shotgun", False)
    
    menu_state = MenuState()
    current_state = "menu"
    running = True
    
    while running:
        mouse_pos = pg.mouse.get_pos()
        events = pg.event.get()
        # Обновляем состояние кнопок для текущего экрана
        if current_state == "menu":
            menu_state.update(mouse_pos, events)
        elif current_state == "settings":
            # Обновляем кнопки настроек звука
            for button in menu_state.sound_buttons:
                button.check_hover(mouse_pos)
        
        for event in events:
            if event.type == pg.QUIT:
                running = False
                
            if current_state == "menu":
                if menu_state.show_controls and event.type in (pg.MOUSEBUTTONDOWN, pg.KEYDOWN):
                    menu_state.show_controls = False
                else:
                    for button in menu_state.buttons:
                        if button.handle_event(event):
                            button.action()
                            if menu_state.next_state:
                                current_state = menu_state.next_state
                                menu_state.next_state = None
                            break
            
            # Обработка событий для экрана настроек
            elif current_state == "settings":
                for button in menu_state.sound_buttons:
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        if button.rect.collidepoint(mouse_pos):
                            button.action()
                
                # Выход по TAB
                if event.type == pg.KEYDOWN and event.key == pg.K_TAB:
                    current_state = "menu"
        
        screen.blit(menu_background_scaled, (0, 0))
        
        if current_state == "menu":
            menu_state.draw(screen)
            
        elif current_state == "game":
            game_loop()
            current_state = "menu"
            load_player_stats()
            
        elif current_state == "shop":
            coins = draw_shop(screen, temp_player, player_stats["coins"], player_stats)
            player_stats["coins"] = coins
            save_player_stats()
            
            if pg.key.get_pressed()[pg.K_TAB]:
                current_state = "menu"
                
        elif current_state == "settings":
            menu_state.draw_settings(screen)
    
        elif current_state == "quit":
            running = False
        
        pg.display.flip()
        clock.tick(FPS)