label start:

    "ewfyg" "start"


    init python:

        RANDOM_COLOR = (234, 165, 43)
        target_position = [(550, 95), (745, 145), (665, 195), (550, 245), (700, 295), (460, 345), (0, 0)]
        target_position_available = [True, True, True, True, True, True, True, True]



        class Button():

            def __init__(self, text, position, size):

                self._text = text
                self._root_text = Text(text, color="#9cee90")
                self._x = position[0]
                self._y = position[1]
                self._size = size


            def render(self, r, width, height, st, at):
                button = renpy.render(self._root_text, width, height, st, at)
                r.blit(button, (self._x, self._y))


            def _is_hit_by_coordinates(self, x, y):
                if (self._x + self._size[0]) > x > self._x and (self._y + self._size[1]) > y > self._y:
                    return True
                return False

            def event(self, x, y):
                return self._is_hit_by_coordinates(x, y)





        class FlyTextButton():

            def __init__(self, text, position, size):

                self._text = text
                self._example_add_text = Text(text, color="#000080")
                self._x = position[0]
                self._y = position[1]
                self._current_x = float(self._x)
                self._current_y = float(self._y)
                self._k_x = 1.0
                self._k_y = 1.0
                self._size = size
                self._speed = 5
                self._stop = True
                self._last_coordinates = None
                self._end_position = None


            def render(self, r, width, height, st, at):
                if (not self._stop):
                    self._move()
                text = renpy.render(self._example_add_text, width, height, st, at)
                r.blit(text, (self._current_x, self._current_y))

            def get_text(self):
                return self._text

            def get_end_position(self):
                return self._end_position

            def is_in_start(self):
                return abs(self._current_y - self._y) < self._speed

            def is_in_end(self):
                return self._stop and not self.is_in_start()

            def _is_hit_by_coordinates(self, x, y):
                if (self._current_x + self._size[0]) > x > self._current_x and (self._current_y + self._size[1]) > y > self._current_y:
                    return True
                return False



            def event(self, x, y, last_coordinates):
                if last_coordinates != None:
                    self._end_position = last_coordinates
                if (self._stop):
                    if last_coordinates == None:
                        last_coordinates = (self._x, self._y)
                    if self._is_hit_by_coordinates(x, y):
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
                    #self._example_add_text = Text("Гав", (50, 500))


                        # Needed to ensure that event is called, noticing
                        # the winner.
                    #renpy.timeout(0)
                return False

            def _move(self):
                #self._example_add_text = Text(self.get_text())
                self._current_x += self._k_x
                self._current_y += self._k_y
                if abs(self._current_y - self._last_coordinates[1]) < self._speed:
                    self._stop = True




            def event(self, x, y, last_coordinates):
                if last_coordinates != None:
                    self._end_position = last_coordinates
                if (self._stop):
                    if last_coordinates == None:
                        last_coordinates = (self._x, self._y)
                    if self._is_hit_by_coordinates(x, y):
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
                    #self._example_add_text = Text("Гав", (50, 500))


                        # Needed to ensure that event is called, noticing
                        # the winner.
                    #renpy.timeout(0)
                return False







        class GameDisplayable(renpy.Displayable):

            def __init__(self):

                import pygame

                renpy.Displayable.__init__(self)


                self._prepare_game_over = False
                self._game_result = 0
                self._FPS = 60
                self._clock = pygame.time.Clock()
                self._exit_button = Button("Закончить", (1050, 630), (120, 30))
                self._correct_answer = ["солнце", "прелестный", "проснись", "сомкнуты", "Авроры", "Звездою"]
                self._text_color = "ff0000"


                self._image = Image("tree.png")

                self._surf_text = [(Text("Мороз и _____________; день чудесный!", color=self._text_color), 100),
                             (Text("Еще ты дремлешь, друг _____________ —", color=self._text_color), 150),
                             (Text("Пора, красавица, ______________:", color=self._text_color), 200),
                             (Text("Открой _____________ негой взоры", color=self._text_color), 250),
                             (Text("Навстречу северной ______________,", color=self._text_color), 300),
                             (Text("_____________ севера явись!", color=self._text_color), 350)]

                self._example_add_text = [FlyTextButton("солнце", (100, 630), (80, 25)),
                                          FlyTextButton("сомкнуты", (200, 630), (112, 25)),
                                          FlyTextButton("Авроры", (332, 630), (85, 25)),
                                          FlyTextButton("прелестный", (437, 630), (138, 25)),
                                          FlyTextButton("Звездою", (595, 630), (97, 25)),
                                          FlyTextButton("проснись", (712, 630), (110, 25))]

                # If the ball is stuck to the paddle.

                self.winner = None


            # Recomputes the position of the ball, handles bounces, and
            # draws the screen.
            def render(self, width, height, st, at):


                # The Render object we'll be drawing into.
                r = renpy.Render(width, height)


                for value in self._surf_text:
                    text = renpy.render(value[0], width, height, st, at)
                    r.blit(text, (450, value[1]))



                image = renpy.render(self._image, width, height, st, at)
                r.blit(image, (0, 500))

                for value in self._example_add_text:
                    value.render(r, width, height, st, at)

                if self._prepare_game_over:
                    self._exit_button.render(r, width, height, st, at)



                self._clock.tick(self._FPS)

                #example_add_text = renpy.render(self._example_add_text, width, height, st, at)
                #r.blit(example_add_text, (50, 500))



                renpy.redraw(self, 0)



                return r


            def _put_end_position(self, end_position):
                for i in range(len(target_position)):
                    if target_position[i] == end_position:
                        target_position_available[i] = True
                        return i





            def _get_position_available(self):
                for i in range(len(target_position_available)):
                    if target_position_available[i]:
                        return i

            # Handles events.
            def event(self, ev, x, y, st):

                import pygame

                # Mousebutton down == start the game by setting stuck to
                # false.
                exit_game = False
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    position_available = self._get_position_available()
                    position = target_position[position_available]
                    target_position_available[position_available] = False
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
                    # Ensure the pong screen updates.
                    self._prepare_game_over = target_position[self._get_position_available()] == (0, 0)
                    if self._prepare_game_over:
                        if self._exit_button.event(x, y):
                            exit_game = True
                    renpy.restart_interaction()


                if exit_game:
                    return self._game_result
                else:
                    raise renpy.IgnoreEvent()

    screen pong():

        default pong = GameDisplayable()

        add "game_photo1"

        add pong




    label play_pong:

        window hide  # Hide the window and  quick menu while in pong
        $ quick_menu = False

        call screen pong

        $ quick_menu = True
        window show

    show eileen vhappy


    if _return == 6:

        "we4ftihu" "верно 6"

    elif _return == 5:

        "ouewGF" "верно 5"
    elif _return == 4:

        "ouewGF" "верно 4"

    elif _return == 3:

        "ouewGF" "верно 3"

    elif _return == 2:

        "ouewGF" "верно 2"
    elif _return == 1:

        "ouewGF" "верно 1"

    elif _return == 0:

        "ouewGF" "верно 0"
    else:
        "weiygfg" "верно > 6"

