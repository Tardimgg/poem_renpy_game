label start:

    "ewfyg" "start"


    init python:


        class View():
            def __init__(self, position, displayable):
                self._x = position[0]
                self._y = position[1]
                self._displayable = displayable
                self._size = (0, 0)


            def render(self, r, width, height, st, at):
                render_view = renpy.render(self._displayable, width, height, st, at)
                self._size = render_view.get_size()
                r.blit(render_view, (self._x, self._y))


            def event(self, x, y):
                return (self._x + self._size[0]) > x > self._x and (self._y + self._size[1]) > y > self._y

            def set_position(self, position):
                self._x, self._y = position[0], position[1]



        class Button(View):

            def __init__(self, text, position):
                self._root_text = Text(text, color="#9cee90")
                super(Button, self).__init__(position, self._root_text)
                self._x = position[0]
                self._y = position[1]
                self._size = (0, 0)




        class FlyTextButton(View):

            def __init__(self, text, position):

                self._text = text
                self._example_add_text = Text(text, color="#ffffff")
                self._start_x = float(position[0])
                self._start_y = float(position[1])
                self._current_x = float(self._start_x)
                self._current_y = float(self._start_y)
                super(FlyTextButton, self).__init__((self._current_x, self._current_y), self._example_add_text)
                self._k_x = 1.0
                self._k_y = 1.0
                self._size = (0, 0)
                self._speed = 5
                self._stop = True
                self._last_coordinates = None
                self._end_position = None


            def render(self, r, width, height, st, at):
                if (not self._stop):
                    self._move()
                super(FlyTextButton, self).render(r, width, height, st, at)


            def get_text(self):
                return self._text

            def get_end_position(self):
                return self._end_position

            def is_in_start(self):
                return abs(self._current_y - self._start_y) < self._speed

            def is_in_end(self):
                return self._stop and not self.is_in_start()


            def _move(self):
                self._current_x += self._k_x
                self._current_y += self._k_y
                super(FlyTextButton, self).set_position((self._current_x, self._current_y))
                if abs(self._current_y - self._last_coordinates[1]) < self._speed and abs(self._current_x - self._last_coordinates[0]) < self._speed:
                    self._stop = True



            def event(self, x, y, last_coordinates):
                if last_coordinates != None:
                    self._end_position = last_coordinates
                if (self._stop):
                    if last_coordinates == None:
                        last_coordinates = (self._start_x, self._start_y)
                    if super(FlyTextButton, self).event(x, y):
                        self._last_coordinates = last_coordinates
                        delta_x = abs(self._current_x - self._last_coordinates[0])
                        delta_y = abs(self._current_y - self._last_coordinates[1])
                        if delta_x > delta_y:
                            self._k_x = 1
                            self._k_y = float(abs(self._current_y - self._last_coordinates[1])) / abs(self._current_x - self._last_coordinates[0])
                        elif delta_x < delta_y:
                            self._k_x = float(abs(self._current_x - self._last_coordinates[0])) / abs(self._current_y - self._last_coordinates[1])
                            self._k_y = 1
                        else:
                            self._k_x = 1
                            self._k_y = 1
                        self._k_x *= 1 if self._current_x < self._last_coordinates[0] else -1
                        self._k_y *= 1 if self._current_y < self._last_coordinates[1] else -1
                        self._k_x *= self._speed
                        self._k_y *= self._speed
                        self._stop = False
                        self._move()
                        return True

                return False



        class GameDisplayable(renpy.Displayable):

            def __init__(self):

                import pygame

                renpy.Displayable.__init__(self)

                self._target_position = [(520, 95), (715, 145), (635, 195), (520, 245), (670, 295), (430, 345), (0, 0)]
                self._target_position_available = [True, True, True, True, True, True, True, True]

                self._prepare_game_over = False
                self._game_result = 0
                self._FPS = 60
                self._clock = pygame.time.Clock()
                self._exit_button = Button("Закончить", (1050, 630))
                self._correct_answer = ["солнце", "прелестный", "проснись", "сомкнуты", "Авроры", "Звездою"]
                self._text_color = "#000080"

                self._image = Image("tree.png")


                self._text_image = Image("light_tree.png")

                self._surf_text = [(Text("Мороз и _____________; день чудесный!", color=self._text_color), 100),
                             (Text("Еще ты дремлешь, друг _____________ —", color=self._text_color), 150),
                             (Text("Пора, красавица, ______________:", color=self._text_color), 200),
                             (Text("Открой _____________ негой взоры", color=self._text_color), 250),
                             (Text("Навстречу северной ______________,", color=self._text_color), 300),
                             (Text("_____________ севера явись!", color=self._text_color), 350)]

                self._example_add_text = [FlyTextButton("солнце", (100, 630)),
                                          FlyTextButton("сомкнуты", (200, 630)),
                                          FlyTextButton("Авроры", (332, 630)),
                                          FlyTextButton("прелестный", (437, 630)),
                                          FlyTextButton("Звездою", (595, 630)),
                                          FlyTextButton("проснись", (712, 630))]
                self.winner = None


            def render(self, width, height, st, at):
                r = renpy.Render(width, height)

                image = renpy.render(self._image, width, height, st, at)
                r.blit(image, (0, 500))

                image = renpy.render(self._text_image, width, height, st, at)
                r.blit(image, (180, 0))

                for value in self._surf_text:
                    text = renpy.render(value[0], width, height, st, at)
                    r.blit(text, (420, value[1]))

                for value in self._example_add_text:
                    value.render(r, width, height, st, at)

                if self._prepare_game_over:
                    self._exit_button.render(r, width, height, st, at)

                self._clock.tick(self._FPS)
                renpy.redraw(self, 0)

                return r


            def _put_end_position(self, end_position):
                for i in range(len(self._target_position)):
                    if self._target_position[i] == end_position:
                        self._target_position_available[i] = True
                        return i


            def _get_position_available(self):
                for i in range(len(self._target_position_available)):
                    if self._target_position_available[i]:
                        return i

            # Handles events.
            def event(self, ev, x, y, st):

                import pygame

                exit_game = False
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    position_available = self._get_position_available()
                    position = self._target_position[position_available]
                    self._target_position_available[position_available] = False
                    is_used = False
                    for value in self._example_add_text:
                        if value.is_in_start():
                            if value.event(x, y, position):
                                if value.get_text() == self._correct_answer[position_available]:
                                    self._game_result += 1
                                is_used = True
                                break
                        elif value.is_in_end():
                            result = value.event(x, y, None)
                            if result:
                                if not is_used:
                                    self._put_end_position(position)
                                    is_used = True
                                if self._correct_answer[self._put_end_position(value.get_end_position())] == value.get_text():
                                    self._game_result -= 1
                                break
                    if not is_used:
                        self._put_end_position(position)
                    self._prepare_game_over = self._target_position[self._get_position_available()] == (0, 0)
                    if self._prepare_game_over:
                        if self._exit_button.event(x, y):
                            exit_game = True
                    renpy.restart_interaction()


                if exit_game:
                    return self._game_result
                else:
                    raise renpy.IgnoreEvent()

    screen game():

        default word_game = GameDisplayable()

        add "background"

        add word_game




    label play_game:

        window hide
        $ quick_menu = False

        call screen game

        $ quick_menu = True
        window show

    show eileen vhappy


    "we4ftihu" "верно [_return]"

