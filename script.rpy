label start:

    "ewfyg" "start"


    init python:

        class View():
            def __init__(self, position, displayable, min_size=(0, 0), **kwargs):
                if "box_view" in kwargs:
                    kwargs["box_view"].addView(self)
                self._x = position[0]
                self._y = position[1]
                self._displayable = displayable
                self._min_size = (min_size[0], min_size[1])
                self._size = self._min_size


            def render(self, r, width, height, st, at):
                render_view = renpy.render(self._displayable, width, height, st, at)
                size = render_view.get_size()
                self._size = (max(size[0], self._min_size[0]), max(size[1], self._min_size[1]))
                r.blit(render_view, (self._x, self._y))


            def event(self, position, **kwargs):
                return False

            def get_displayable(self):
                return self._displayable

            def set_position(self, position):
                self._x, self._y = position[0], position[1]

            def get_position(self):
                return (self._x, self._y)

            def get_size(self):
                return self._size

            def exit(self):
                pass


        class ButtonView(View):

            def __init__(self, view, **kwargs):
                if "box_view" in kwargs:
                    kwargs["box_view"].addView(self)
                self._root_view = view

            def event(self, position, **kwargs):
                if "recursive_event" in kwargs:
                    self._root_view.event(position, kwargs=kwargs)
                x, y = self.get_position()
                size = self.get_size()
                return (x + size[0]) > position[0] > x and (y + size[1]) > position[1] > y

            def render(self, r, width, height, st, at):
                self._root_view.render(r, width, height, st, at)

            def get_position(self):
                return self._root_view.get_position()

            def get_view(self):
                return self._root_view

            def set_position(self, position):
                self._root_view.set_position(position)

            def get_size(self):
                return self._root_view.get_size()

            def exit(self):
                self._root_view.exit()




        class EditText(View):



            def __init__(self, start_text, position, max_symbol=float("inf"), **kwargs):
                if "box_view" in kwargs:
                    kwargs["box_view"].addView(self)
                self._start_text = start_text
                self._text = self._start_text
                self._cursor = "|"
                self._max_symbol = max_symbol
                self._text_view = Text("".join(self._text))
                self._position = position
                super(EditText, self).__init__(self._position, self._text_view, (max_symbol * 19.4, 0))
                self._text_button = ButtonView(self)
                self._update_cursor = EditText.UpdateCursor(1, self._render_add_function, self._render_remove_function, self)
                self._update_cursor.setDaemon(True)
                self._update_cursor.start()
                self._is_active = False


            def _render_add_function(self, parent):
                self._text_view.set_text(self._text + self._cursor)

            def _render_remove_function(self, parent):
                self._text_view.set_text(self._text)

            def set_position(self, position):
                super(EditText, self).set_position(position)
                self._position = position

            def get_position(self):
                return self._position


            def on_active(self):
                self._is_active = True
                self._update_cursor.resume()

            def off_active(self):
                self._is_active = False
                self._update_cursor.pause()

            def get_text(self):
                return self._text

            def event(self, position, symbol=None, backspace=False, **kwargs):
                if "position" in kwargs:
                    position = kwargs["position"]
                if "symbol" in kwargs:
                    symbol = kwargs["symbol"]
                if "backspace" in kwargs:
                    backspace = kwargs["backspace"]
                if symbol != None:
                    if self._is_active:
                        self._update_cursor.pause()
                        if backspace:
                            if len(self._text) > len(self._start_text):
                                self._text = self._text[:-1]
                                self._text_view.set_text(self._text)
                        elif len(self._text) < self._max_symbol:
                            self._text += symbol
                            self._text_view.set_text(self._text)
                        self._update_cursor.resume()
                elif self._text_button.event(position):
                    self._update_cursor.resume()
                    self.on_active()
                else:
                    self._update_cursor.pause()
                    self.off_active()


            def exit(self):
                self._update_cursor.exit()




            import threading

            class UpdateCursor(threading.Thread):

                import time

                def __init__(self, update_time, render_add_function, render_remove_function, parent):
                    import pygame, threading

                    super(EditText.UpdateCursor, self).__init__(self)
                    self._render_add_function = render_add_function
                    self._render_remove_function = render_remove_function
                    self._update_time = update_time
                    self._is_add_function = 0
                    self._is_work = True
                    self._parent = parent
                    self._clock = pygame.time.Clock()
                    self._event = threading.Event()

                def run(self):
                    while self._is_work:
                        if self._is_add_function:
                            self._event.wait()
                            self._render_add_function(self._parent)
                        else:
                            self._render_remove_function(self._parent)
                            self._event.wait()
                        self._is_add_function = not self._is_add_function
                        self._clock.tick(2)



                def exit(self):
                    self.resume()
                    self._is_work = False
                    super(UpdateCursor, self).exit()


                def pause(self):
                    self._event.clear()

                def resume(self):
                    self._event.set()


        class FieldView(View):
            def __init__(self, position, root_view, *views, **kwargs):
                if "box_view" in kwargs:
                    kwargs["box_view"].addView(self)
                self._child_view = []
                self._child_start_position = []
                self._view = root_view
                self._position = position
                super(FieldView, self).__init__(self._position, self._view)
                for value in views:
                    self._child_start_position.append(value.get_position())
                    self._child_view.append(value)
                self._set_child_position()

            def _set_child_position(self):
                for i in range(len(self._child_view)):
                    self._child_view[i].set_position((self._child_start_position[i][0] + self._position[0], self._child_start_position[i][1] + self._position[1]))

            def render(self, r, width, height, st, at):
                super(FieldView, self).render(r, width, height, st, at)
                for value in self._child_view:
                    value.render(r, width, height, st, at)

            def exit(self):
                super(FieldView, self).exit()
                for value in self._child_view:
                    value.exit()

            def event(self, position, **kwargs):
                answer = []
                for value in self._child_view:
                    answer.append(value.event(position, kwargs=kwargs))
                return answer

            def get_views(self):
                return self._child_view


            def set_position(self, position):
                self._position = position
                super(FieldView, self).set_position(position)
                self._set_child_position()

            def get_position(self):
                return self._position

            def get_size(self):
                return self._size



        class FlyView(View):

            def __init__(self, view, speed=5, **kwargs):
                if "box_view" in kwargs:
                    kwargs["box_view"].addView(self)
                self._root_view = view
                self._start_x, self._start_y = self._root_view.get_position()
                self._current_x = float(self._start_x)
                self._current_y = float(self._start_y)
                self._k_x = 1.0
                self._k_y = 1.0
                self._size = (0, 0)
                self._speed = speed
                self._stop = True
                self._last_coordinates = None
                self._end_position = None


            def render(self, r, width, height, st, at):
                if (not self._stop):
                    self._move()
                self._root_view.render(r, width, height, st, at)


            def get_end_position(self):
                return self._end_position

            def is_in_start(self):
                return abs(self._current_y - self._start_y) < self._speed

            def is_in_end(self):
                return self._stop and not self.is_in_start()

            def get_view(self):
                return self._root_view



            def _move(self):
                if abs(self._current_y - self._last_coordinates[1]) < self._speed and abs(self._current_x - self._last_coordinates[0]) < self._speed:
                    self._stop = True
                else:
                    self._current_x += self._k_x
                    self._current_y += self._k_y
                self._root_view.set_position((self._current_x, self._current_y))


            def event(self, position, **kwargs):
                return self._root_view.event(position, kwargs=kwargs)

            def get_position(self):
                return self._root_view.get_position()

            def set_position(self, position):
                self._current_x, self._current_y = position
                self._stop = True
                self._root_view.set_position(position)

            def get_size(self):
                return self._root_view.get_size()

            def get_view(self):
                return self._root_view

            def exit(self):
                self._root_view.exit()


            def fly(self, last_coordinates):
                if last_coordinates != None:
                    self._end_position = last_coordinates
                if (self._stop):
                    if last_coordinates == None:
                        last_coordinates = (self._start_x, self._start_y)
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



        class BoxView:

            def __init__(self):
                self._views = []

            def addView(self, view):
                self._views.append(view)

            def render(self, r, width, height, st, at):
                for value in self._views:
                    value.render(r, width, height, st, at)

            def exit(self):
                for value in self._views:
                    value.exit()



        class GameDisplayable(renpy.Displayable):

            def __init__(self):

                import pygame

                renpy.Displayable.__init__(self)

                self._target_position = [(520, 95), (715, 145), (635, 195), (520, 245), (670, 295), (430, 345), (0, 0)]
                self._target_position_available = [True, True, True, True, True, True, True, True]

                self._box_view = BoxView()

                self._prepare_game_over = False
                self._game_result = 0
                self._FPS = 60
                self._clock = pygame.time.Clock()

                self._correct_answer = ["солнце", "прелестный", "проснись", "сомкнуты", "Авроры", "Звездою"]
                self._text_color = "#000080"

                self._image = View((0, 500), Image("tree.png"), box_view=self._box_view)

                self._text_image = View((180, 0), Image("light_tree.png"), box_view=self._box_view)

                self._exit_button = ButtonView(View((1050, 630), Text("Закончить")))

                self._surf_text = [View((420, 100), Text("Мороз и _____________; день чудесный!", color=self._text_color), box_view=self._box_view),
                             View((420, 150), Text("Еще ты дремлешь, друг _____________ —", color=self._text_color), box_view=self._box_view),
                             View((420, 200), Text("Пора, красавица, ______________:", color=self._text_color), box_view=self._box_view),
                             View((420, 250), Text("Открой _____________ негой взоры", color=self._text_color), box_view=self._box_view),
                             View((420, 300), Text("Навстречу северной ______________,", color=self._text_color), box_view=self._box_view),
                             View((420, 350), Text("_____________ севера явись!", color=self._text_color), box_view=self._box_view)]

                self._example_add_text = [FlyView(ButtonView(View((100, 630), Text("солнце"))), speed=5, box_view=self._box_view),
                                          FlyView(ButtonView(View((200, 630), Text("сомкнуты"))), speed=5, box_view=self._box_view),
                                          FlyView(ButtonView(View((332, 630), Text("Авроры"))), speed=5, box_view=self._box_view),
                                          FlyView(ButtonView(View((437, 630), Text("прелестный"))), speed=5, box_view=self._box_view),
                                          FlyView(ButtonView(View((595, 630), Text("Звездою"))), speed=5, box_view=self._box_view),
                                          FlyView(ButtonView(View((712, 630), Text("проснись"))), speed=5, box_view=self._box_view)]
                self.winner = None


            def render(self, width, height, st, at):
                r = renpy.Render(width, height)

                self._box_view.render(r, width, height, st, at)

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
                            if value.event((x, y)):
                                value.fly(position)
                                if "".join(value.get_view().get_view().get_displayable().text) == self._correct_answer[position_available]:
                                    self._game_result += 1
                                is_used = True
                                break
                        elif value.is_in_end():
                            result = value.event((x, y))
                            if result:
                                value.fly(None)
                                if not is_used:
                                    self._put_end_position(position)
                                    is_used = True
                                if self._correct_answer[self._put_end_position(value.get_end_position())] == "".join(value.get_view().get_view().get_displayable().text):
                                    self._game_result -= 1
                                break
                    if not is_used:
                        self._put_end_position(position)
                    self._prepare_game_over = self._target_position[self._get_position_available()] == (0, 0)
                    if self._prepare_game_over:
                        if self._exit_button.event((x, y)):
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

