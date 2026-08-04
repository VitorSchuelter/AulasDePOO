import arcade
import random

ALTURA = 600
LARGURA = 1000
TITULO = "Spider Game"

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("AranhaDireita.png", scale=0.17)
        self.textura_direita = arcade.load_texture("AranhaDireita.png")
        self.textura_esquerda = arcade.load_texture("AranhaEsqueda.png")
        
    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        if (self.change_x > 0):
            self.texture = self.textura_direita
        elif (self.change_x < 0):
            self.texture = self.textura_esquerda

        if (self.right > LARGURA):
            self.change_x = 0
            self.right = LARGURA
        if (self.left < 0):
            self.change_x = 0
            self.left = 0
        if (self.top > ALTURA):
            self.change_y = 0
            self.top = ALTURA
        if (self.bottom < 0):
            self.change_y = 0
            self.bottom = 0

class Moeda(arcade.Sprite):
    valor_moeda = 1
    def __init__ (self):
        super().__init__("TeiaPonto.png", scale=0.2)

class MoedaEspecial(arcade.Sprite):
    valor_moeda = 5
    def __init__(self):
        super().__init__("AranhaPonto.png", scale=0.07)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0 or self.right > LARGURA:
            self.change_x *= -1
        if self.bottom < 0 or self.top > ALTURA:
            self.change_y *= -1

class Inimigo(arcade.Sprite):
    def __init__(self):
        super().__init__("Venom.png", scale=0.082)
    
    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0 or self.right > LARGURA:
            self.change_x *= -1
        if self.bottom < 0 or self.top > ALTURA:
            self.change_y *= -1

class InimigoEspecial(arcade.Sprite):
    def __init__(self, jogador):
        super().__init__("VenomEspecial.png", scale=0.15)
        self.jogador = jogador
        self.movimento = 1.65

    def update(self, delta_time):
        if self.center_x < self.jogador.center_x: self.center_x += self.movimento
        elif self.center_x > self.jogador.center_x: self.center_x -= self.movimento
        
        if self.center_y < self.jogador.center_y: self.center_y += self.movimento
        elif self.center_y > self.jogador.center_y: self.center_y -= self.movimento

class TelaInicial(arcade.View):
    def __init__(self):
        super().__init__()
        self.fundo = arcade.load_texture("TelaInicio.png")

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            texture = self.fundo,
            rect = arcade.XYWH(
                x = LARGURA / 2,
                y = ALTURA / 2,
                width=LARGURA,
                height=ALTURA
            )
        )

        # Alterado de 750 para LARGURA / 2 para centralizar na tela
        arcade.draw_text("Pressione [F] para Jogar", LARGURA / 2, 160, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Pressione [T] para ver o Tutorial", LARGURA / 2, 130, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Pressione [S] para Saber Mais", LARGURA / 2, 100, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Pressione [ESC] para Sair", LARGURA / 2, 70, arcade.color.WHITE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            tela_jogo = TelaJogo()
            self.window.show_view(tela_jogo)
        elif key == arcade.key.T:
            tela_tutorial = TelaTutorial()
            self.window.show_view(tela_tutorial)
        elif key == arcade.key.S:
            tela_sobre = TelaSobre()
            self.window.show_view(tela_sobre)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()
        self.fundo = arcade.load_texture("TelaJogo.png")

        self.jogo_finalizado = False
        self.dano = False
        self.alerta_timer = 0
        self.movimento = 4

        self.qtd_moedas = 50
        self.qtd_moedas_especiais = 5

        self.pontuacao_maxima = (self.qtd_moedas * Moeda.valor_moeda) + (self.qtd_moedas_especiais * MoedaEspecial.valor_moeda)

        self.pontuacao = 0
        self.tempo = 0.0
        
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_moedas = arcade.SpriteList()
        self.sprite_inimigoEspecial = arcade.SpriteList()
        self.sprite_inimigos = arcade.SpriteList()

        self.jogador = Player()
        self.jogador.center_x = 0
        self.jogador.center_y = 0
        self.sprite_jogador.append(self.jogador)

        for i in range (self.qtd_moedas_especiais):
            self.especial = MoedaEspecial()
            self.especial.center_x = random.randint(0, LARGURA - 50)
            self.especial.center_y = random.randint(50, ALTURA - 50)
            self.especial.change_x = self.movimento
            self.especial.change_y = self.movimento
            self.sprite_moedas.append(self.especial)

        for i in range(self.qtd_moedas):
            self.moeda_simples = Moeda()
            self.moeda_simples.center_x = random.randint(50, LARGURA - 50)
            self.moeda_simples.center_y = random.randint(50, ALTURA - 50)
            self.sprite_moedas.append(self.moeda_simples)

        self.inimigoEspecial = InimigoEspecial(self.jogador)
        self.inimigoEspecial.center_x = 850
        self.inimigoEspecial.center_y = 200
        self.sprite_inimigoEspecial.append(self.inimigoEspecial)
        
        self.inimigo = Inimigo()
        self.inimigo.center_x = random.randint(0, LARGURA - 50)
        self.inimigo.center_y = random.randint(50, ALTURA - 50)
        self.inimigo.change_x = self.movimento
        self.inimigo.change_y = self.movimento
        self.sprite_inimigos.append(self.inimigo)

    def respawn (self, inimigo):
        distancia_min = 500
        while True:
            colisao = False
            inimigo.center_x = random.randint(50, LARGURA - 50)
            inimigo.center_y = random.randint(50, ALTURA - 50)
            for jogador in self.sprite_jogador:
                distancia = arcade.get_distance_between_sprites(inimigo, jogador)
                if distancia < distancia_min:
                    colisao = True
                    break

            if not colisao:
                break
    
    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            texture = self.fundo,
            rect = arcade.XYWH(
                x = LARGURA / 2,
                y = ALTURA / 2,
                width=LARGURA,
                height=ALTURA
            )
        )

        self.sprite_jogador.draw()
        self.sprite_moedas.draw()
        self.sprite_inimigoEspecial.draw()
        self.sprite_inimigos.draw()
        arcade.draw_text(f"Pontos: {self.pontuacao}", 10, 570, arcade.color.AZURE_MIST, 14)
        arcade.draw_text(f"Tempo: {self.tempo:.2f}s", 10, 550, arcade.color.AZURE_MIST, 14)

        if self.dano:
            arcade.draw_text("DANO RECEBIDO!", LARGURA/2, ALTURA/2, arcade.color.RED, 30, anchor_x="center")

    def on_update(self, delta_time):
        if self.jogo_finalizado:
            return

        self.tempo += delta_time
        self.sprite_jogador.update(delta_time)
        self.sprite_moedas.update(delta_time)
        self.sprite_inimigoEspecial.update(delta_time)
        self.sprite_inimigos.update(delta_time)

        moedas_colididas = arcade.check_for_collision_with_list(self.jogador, self.sprite_moedas)
        for moeda in moedas_colididas:
            moeda.remove_from_sprite_lists()
            self.pontuacao += moeda.valor_moeda

        if (arcade.check_for_collision_with_list(self.jogador, self.sprite_inimigoEspecial)):
            self.pontuacao -= 1
            self.alertaDano()
            self.respawn(self.inimigoEspecial)

        if (arcade.check_for_collision_with_list(self.jogador, self.sprite_inimigos)):
            self.pontuacao -= 1
            self.alertaDano()

        if self.dano:
            self.alerta_timer -= delta_time
            if self.alerta_timer <= 0:
                self.dano = False

        if len(self.sprite_moedas) == 0:
            self.jogo_finalizado = True
            tela_final = TelaFinal(self.pontuacao, self.tempo, self.pontuacao_maxima)
            self.window.show_view(tela_final)

    def alertaDano(self):
        self.dano = True
        self.alerta_timer = 0.5

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.jogador.change_x = -self.movimento
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.jogador.change_y = -self.movimento
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.jogador.change_x = self.movimento
        elif key == arcade.key.W or key == arcade.key.UP:
            self.jogador.change_y = self.movimento

        elif key == arcade.key.BACKSPACE:
            self.jogo_finalizado = True
            tela_final = TelaFinal(self.pontuacao, self.tempo, self.pontuacao_maxima)
            self.window.show_view(tela_final)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.LEFT or key == arcade.key.D or key == arcade.key.RIGHT:
            self.jogador.change_x = 0
        if key == arcade.key.S or key == arcade.key.DOWN or key == arcade.key.W or key == arcade.key.UP:
            self.jogador.change_y = 0

class TelaFinal(arcade.View):
    def __init__(self, pontos, tempo, pontuacao_maxima):
        super().__init__()
        self.fundo = arcade.load_texture("TelaFinal.png")
        self.pontos = pontos
        self.tempo = tempo
        self.pontuacao_maxima = pontuacao_maxima

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            texture = self.fundo,
            rect = arcade.XYWH(
                x = LARGURA / 2,
                y = ALTURA / 2,
                width=LARGURA,
                height=ALTURA
            )
        )
        if self.pontos >= self.pontuacao_maxima:
            arcade.draw_text("PARABÉNS! O JOGO FOI PERFEITO!", 750, 270, arcade.color.AZURE_MIST, 22, anchor_x="center")
        else:
            arcade.draw_text("PARABÉNS! O JOGO FOI CONCLUÍDO", 750, 270, arcade.color.AZURE_MIST, 22, anchor_x="center")
        arcade.draw_text(f"Pontuação: {self.pontos}  |  Tempo: {self.tempo:.1f}s", 750, 210, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Pressione [R] para Jogar Novamente", 750, 160, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Pressione [ESC] para Sair", 750, 100, arcade.color.WHITE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            tela_jogo = TelaJogo()
            self.window.show_view(tela_jogo)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class TelaTutorial(arcade.View):
    def __init__(self):
        super().__init__()
        self.fundo = arcade.load_texture("TelaTutorial.png")

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            texture = self.fundo,
            rect = arcade.XYWH(
                x = LARGURA / 2,
                y = ALTURA / 2,
                width=LARGURA,
                height=ALTURA
            )
        )

        arcade.draw_text("COMO JOGAR", LARGURA/2, 450, arcade.color.WHITE, 30, anchor_x="center")

        arcade.draw_text("Use W A S D ou ⬅ ⮕ ⬆ ⬇ para se mover", LARGURA/2, 330, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("A Moeda Especial vale (+3 Pontos)", LARGURA/2, 300, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("As Moedas valem (+1 Ponto)", LARGURA/2, 270, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("Os Inimigos fazem você perder (-1 Ponto)", LARGURA/2, 240, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("O Inimigo Especial te persegue e faz você perder (-1 Ponto)", LARGURA/2, 210, arcade.color.WHITE, 18, anchor_x="center")

        arcade.draw_text("Pressione [T] ou [ESC] para voltar ao início", LARGURA/2, 110, arcade.color.WHITE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.T or key == arcade.key.ESCAPE: self.window.show_view(TelaInicial())

class TelaSobre(arcade.View):
    def __init__(self):
        super().__init__()

        self.sprite_maria = arcade.SpriteList()

        self.maria = arcade.Sprite("TelaFinal.png", scale = 1)
        self.maria.center_x = LARGURA/2
        self.maria.center_y = 280
        self.sprite_maria.append(self.maria)

    def on_draw(self):
        self.clear()
        self.sprite_maria.draw()

        arcade.draw_text("Feito por Vitor Schuelter", LARGURA/2, 550, arcade.color.WHITE, 22.5, anchor_x="center")
        arcade.draw_text("Trabalho de Programação Orientada à Objetos", LARGURA/2, 450, arcade.color.WHITE, 22.5, anchor_x="center")
        arcade.draw_text("Desenvolvido com Python Arcade", LARGURA/2, 420, arcade.color.WHITE, 22.5, anchor_x="center")
        arcade.draw_text("Pressione [S] ou [ESC] para Voltar", LARGURA/2, 50, arcade.color.WHITE, 18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.S:
            tela_inicial = TelaInicial()
            self.window.show_view(tela_inicial)

def main():
    janela = arcade.Window(LARGURA, ALTURA, TITULO)
    tela_inicial = TelaInicial()
    janela.show_view(tela_inicial)
    arcade.run()

if __name__ == "__main__":
    main()