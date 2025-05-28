import os
import pygame
from tilemap import TileMap
from config import FUNDO_BRANCO

def checklist_debug():
    print("==== CHECKLIST DEBUG ====")

    # 1 - Checar fundo
    print(f"FUNDO_BRANCO: {FUNDO_BRANCO}")
    if FUNDO_BRANCO == (0, 0, 0):
        print("[ALERTA] Fundo branco está como preto! Quer isso mesmo?")

    # 2 - Checar arquivo do mapa
    mapa_path = 'Mapas/Mapa1/mapa1.tmx'
    if os.path.exists(mapa_path):
        print(f"[OK] Mapa encontrado: {mapa_path}")
    else:
        print(f"[ERRO] Mapa NÃO encontrado: {mapa_path}")

    # 3 - Testar carregamento do TileMap
    try:
        mapa = TileMap(mapa_path, zoom=3)
        largura, altura = mapa.map_size
        print(f"[OK] TileMap carregado: {largura}x{altura}")
        print(f"[OK] Colisões carregadas: {len(mapa.collision_rects)}")
        print(f"[OK] Spawn points: {len(mapa.spawn_points)}")
    except Exception as e:
        print(f"[ERRO] Falha ao carregar TileMap: {e}")

    # 4 - Checar render
    try:
        pygame.init()
        tela = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        mapa = TileMap(mapa_path, zoom=3)
        from camera import Camera
        camera = Camera(800, 600)
        camera.configurar_limites(*mapa.map_size)
        print("[OK] Renderizando TileMap em janela de teste...")

        for _ in range(30):
            tela.fill(FUNDO_BRANCO)
            mapa.render(tela, camera)
            pygame.display.flip()
            clock.tick(10)
        print("[OK] Renderização do TileMap testada com sucesso.")
        pygame.quit()
    except Exception as e:
        print(f"[ERRO] Falha ao renderizar TileMap: {e}")
        pygame.quit()

    print("==== FIM DO CHECKLIST ====")

if __name__ == "__main__":
    checklist_debug()
