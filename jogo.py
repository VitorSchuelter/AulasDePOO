import arcade
import random


class Jogador(arcade.Sprite):
    def __init__(self):
        super().__init__("personagem-direita.png", scale=0.2)

        self.textura_direita = arcade.load_texture("personagem-direita.png")
        self.textura_esquerda = arcade.load_texture("personagem-esquerda.png")

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        if self.right > 800:
            self.change_x = 0
            self.right = 800

        if self.top > 600:
            self.change_y = 0
            self.top = 600

        if self.left < 0:
            self.change_x = 0
            self.left = 0

        if self.bottom < 0:
            self.change_y = 0
            self.bottom = 0


class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale=0.2)

    def update(self, delta_time):
        if self.center_x > 800 or self.center_x < 0:
            self.change_x *= -1

        if self.center_y > 600 or self.center_y < 0:
            self.change_y *= -1

        self.center_x += self.change_x
        self.center_y += self.change_y


class MoedaEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale=0.4)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0 or self.right > 800:
            self.change_x *= -1

        if self.bottom < 0 or self.top > 600:
            self.change_y *= -1


class Inimigo(arcade.Sprite):
    def __init__(self):
        super().__init__("donquixote.png", scale=0.2)

        self.change_x = random.choice([-2, 2])
        self.change_y = random.choice([-2, 2])

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0 or self.right > 800:
            self.change_x *= -1

        if self.bottom < 0 or self.top > 600:
            self.change_y *= -1


class InimigoEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("donquixote.png", scale=0.3)

        self.change_x = random.choice([-3, 3])
        self.change_y = random.choice([-3, 3])

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0 or self.right > 800:
            self.change_x *= -1

        if self.bottom < 0 or self.top > 600:
            self.change_y *= -1


class JanelaJogo(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Jogo com Inimigos")
        self.fundo = arcade.load_texture("fundo.png")
        self.movimento = 3
        self.pontuacao = 0

        self.personagem = Jogador()
        self.personagem.center_x = 400
        self.personagem.center_y = 300

        self.sprite_jogador = arcade.SpriteList()
        self.sprite_jogador.append(self.personagem)

        self.lista_moeda = arcade.SpriteList()

        for i in range(random.randint(20, 50)):
            moeda = Moeda()

            moeda.center_x = random.randint(50, 750)
            moeda.center_y = random.randint(50, 550)

            moeda.change_x = random.choice([-2, -1, 1, 2])
            moeda.change_y = random.choice([-2, -1, 1, 2])

            self.lista_moeda.append(moeda)

        self.moeda_especial = MoedaEspecial()
        self.moeda_especial.center_x = 650
        self.moeda_especial.center_y = 500
        self.moeda_especial.change_x = self.movimento
        self.moeda_especial.change_y = self.movimento - 1

        self.lista_moeda.append(self.moeda_especial)

        # Lista de inimigos
        self.lista_inimigos = arcade.SpriteList()

        for i in range(5):
            inimigo = Inimigo()

            inimigo.center_x = random.randint(50, 750)
            inimigo.center_y = random.randint(50, 550)

            self.lista_inimigos.append(inimigo)

        self.inimigo_especial = InimigoEspecial()

        self.inimigo_especial.center_x = random.randint(50, 750)
        self.inimigo_especial.center_y = random.randint(50, 550)

        self.lista_inimigos.append(self.inimigo_especial)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            texture=self.fundo,
            rect=arcade.XYWH(
                x=800 / 2,
                y= 600 / 2,
                width=800,
                height=600
            )
        )

        self.sprite_jogador.draw()
        self.lista_moeda.draw()
        self.lista_inimigos.draw()

        arcade.draw_text(
            f"Moedas Coletadas: {self.pontuacao}",
            10,
            570,
            arcade.color.WHITE,
            14
        )


    def on_update(self, delta_time):
        self.sprite_jogador.update()
        self.lista_moeda.update()
        self.lista_inimigos.update()

        moedas_colididas = arcade.check_for_collision_with_list(
            self.personagem,
            self.lista_moeda
        )

        for moeda in moedas_colididas:
            if moeda == self.moeda_especial:
                self.pontuacao += 5
            else:
                self.pontuacao += 1

            moeda.remove_from_sprite_lists()

        inimigos_colididos = arcade.check_for_collision_with_list(
            self.personagem,
            self.lista_inimigos
        )

        for inimigo in inimigos_colididos:

            if inimigo == self.inimigo_especial:

                inimigo.remove_from_sprite_lists()

                self.inimigo_especial = InimigoEspecial()

                self.inimigo_especial.center_x = random.randint(50, 750)
                self.inimigo_especial.center_y = random.randint(50, 550)

                self.lista_inimigos.append(self.inimigo_especial)

            else:
                print("Você colidiu com um inimigo!")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.personagem.change_x -= self.movimento

        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.personagem.change_x += self.movimento

        if key == arcade.key.W or key == arcade.key.UP:
            self.personagem.change_y += self.movimento

        if key == arcade.key.S or key == arcade.key.DOWN:
            self.personagem.change_y -= self.movimento

        if key == arcade.key.ESCAPE:
            self.close()

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.A, arcade.key.LEFT,
                   arcade.key.D, arcade.key.RIGHT]:
            self.personagem.change_x = 0

        if key in [arcade.key.W, arcade.key.UP,
                   arcade.key.S, arcade.key.DOWN]:
            self.personagem.change_y = 0


def main():
    tela = JanelaJogo()
    arcade.run()


if __name__ == "__main__":
    main()