# assets.py
import pygame
import os

# Fatores de escala
ESCALA_SOLDADO = 3.5
ESCALA_INIMIGOS = 4
ESCALA_BOSS = 4

def carregar_imagem(caminho, escala=1, flip=False):
    try:
        img = pygame.image.load(caminho).convert_alpha()
        largura = int(img.get_width() * escala)
        altura = int(img.get_height() * escala)
        img = pygame.transform.scale(img, (largura, altura))
        return pygame.transform.flip(img, flip, False) if flip else img
    except Exception as e:
        print(f"Erro ao carregar {caminho}: {e}")
        return pygame.Surface((50, 50), pygame.SRCALPHA)

def carregar_frames(pasta, prefixo, qtd, escala, flip=False, zeros=1):
    frames = []
    for i in range(1, qtd + 1):
        num = str(i).zfill(zeros)
        caminho = os.path.join(pasta, f"{prefixo}{num}.png")
        frames.append(carregar_imagem(caminho, escala, flip))
    return frames
    
def carregar_animacoes():
    animacoes = {
        # Soldado
        'soldado': {
            'parado': [],
            'andando': [],
            'ataque_leve': [],
            'ataque_pesado': [],
            'ataque_arco': [],
            'dano': [],
            'morrer': [],
        },
        
        # Inimigos
        'orc_normal': {
            'parado': [],
            'andando': [],
            'ataque1': [],
            'ataque2': [],
            'dano': [],
            'morrendo': [],
        },
        
        'esqueleto': {
            'parado': [],
            'andando': [],
            'ataque1': [],
            'ataque2': [],
            'dano': [],
            'morrendo': [],
        },
        
        'boss1': {
            'parado': [],
            'andando': [],
            'ataque_fraco': [],
            'ataque_pesado': [],
            'ataque_especial': [],
            'dano': [],
            'morrendo': [],
        }
    }

    try:
        # ===== Soldado =====
        base_path = 'assets'
        animacoes['soldado']['parado'] = carregar_frames(
            os.path.join(base_path, 'soldado_parado'), 'soldado_parado', 5, ESCALA_SOLDADO)
        
        animacoes['soldado']['andando'] = carregar_frames(
            os.path.join(base_path, 'soldado_andando'), 'soldado_andando', 7, ESCALA_SOLDADO)
        
        animacoes['soldado']['ataque_leve'] = carregar_frames(
            os.path.join(base_path, 'ataque_leve'), 'ataque_leve', 5, ESCALA_SOLDADO)
        
        animacoes['soldado']['ataque_pesado'] = carregar_frames(
            os.path.join(base_path, 'ataque_pesado'), 'ataque_pesado', 5, ESCALA_SOLDADO)
        
        animacoes['soldado']['ataque_arco'] = carregar_frames(
            os.path.join(base_path, 'ataque_arco'), 'ataque_arco', 8, ESCALA_SOLDADO)
        
        animacoes['soldado']['dano'] = carregar_frames(
            os.path.join(base_path, 'dano_soldado'), 'dano', 3, ESCALA_SOLDADO)
        
        animacoes['soldado']['morrer'] = carregar_frames(
            os.path.join(base_path, 'morrer_soldado'), 'morrer', 3, ESCALA_SOLDADO)

        # ===== Orc Normal =====
        base_path = 'assets/inimigos/orc_normal'
        animacoes['orc_normal']['parado'] = carregar_frames(
            os.path.join(base_path, 'orc_parado'), 'Idle_', 6, ESCALA_INIMIGOS)
        
        animacoes['orc_normal']['andando'] = carregar_frames(
            os.path.join(base_path, 'orc_andando'), 'Andar_', 6, ESCALA_INIMIGOS)
        
        animacoes['orc_normal']['ataque1'] = carregar_frames(
            os.path.join(base_path, 'orc_ataque1'), 'Ataque1_', 6, ESCALA_INIMIGOS)
        
        animacoes['orc_normal']['ataque2'] = carregar_frames(
            os.path.join(base_path, 'orc_ataque_2'), 'Ataque2_', 6, ESCALA_INIMIGOS)
        
        animacoes['orc_normal']['dano'] = carregar_frames(
            os.path.join(base_path, 'orc_dano'), 'Machucar_', 4, ESCALA_INIMIGOS)
        
        animacoes['orc_normal']['morrendo'] = carregar_frames(
            os.path.join(base_path, 'orc_morrendo'), 'Morte_', 4, ESCALA_INIMIGOS)

        # ===== Esqueleto =====
        base_path = 'assets/inimigos/esqueleto'
        animacoes['esqueleto']['parado'] = carregar_frames(
            os.path.join(base_path, 'esqueleto_parado'), 'Idle_', 4, ESCALA_INIMIGOS)
        
        animacoes['esqueleto']['andando'] = carregar_frames(
            os.path.join(base_path, 'andando'), 'Andar_', 8, ESCALA_INIMIGOS)
        
        animacoes['esqueleto']['ataque1'] = carregar_frames(
            os.path.join(base_path, 'ataque1'), 'Ataque1_', 6, ESCALA_INIMIGOS)
        
        animacoes['esqueleto']['ataque2'] = carregar_frames(
            os.path.join(base_path, 'ataque2'), 'Ataque2_', 7, ESCALA_INIMIGOS)
        
        animacoes['esqueleto']['dano'] = carregar_frames(
            os.path.join(base_path, 'esqueleto_dano'), 'Machucar_', 4, ESCALA_INIMIGOS)
        
        animacoes['esqueleto']['morrendo'] = carregar_frames(
            os.path.join(base_path, 'esqueleto_morte'), 'Morte_', 4, ESCALA_INIMIGOS)

        # ===== Boss 1 =====
        base_path = 'assets/inimigos/boss1'
        animacoes['boss1']['parado'] = carregar_frames(
            os.path.join(base_path, 'parado'), 'Idle - ', 4, ESCALA_BOSS, False, 2)
        
        animacoes['boss1']['andando'] = carregar_frames(
            os.path.join(base_path, 'andando'), 'Walk - ', 8, ESCALA_BOSS, False, 2)
        
        animacoes['boss1']['ataque_fraco'] = carregar_frames(
            os.path.join(base_path, 'ataque_fraco'), 'ataque1 - ', 7, ESCALA_BOSS, False, 2)
        
        animacoes['boss1']['ataque_pesado'] = carregar_frames(
            os.path.join(base_path, 'ataque_pesado'), 'ataque2 - ', 11, ESCALA_BOSS, False, 2)
        
        animacoes['boss1']['ataque_especial'] = carregar_frames(
            os.path.join(base_path, 'ataque_especial'), 'ataque3 - ', 9, ESCALA_BOSS, False, 2)
        
        animacoes['boss1']['dano'] = carregar_frames(
            os.path.join(base_path, 'dano'), 'Hurt - ', 4, ESCALA_BOSS, False, 2)
        
        animacoes['boss1']['morrendo'] = carregar_frames(
            os.path.join(base_path, 'morte'), 'death - ', 4, ESCALA_BOSS, False, 2)

    except Exception as e:
        print(f"Erro crítico ao carregar assets: {e}")
        raise
    
    return animacoes