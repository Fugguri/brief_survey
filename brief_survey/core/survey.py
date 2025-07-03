from typing import List, Optional, Callable, Any, Dict, Union, Literal, Tuple, Set

from aiogram.enums import ContentType
from pydantic import BaseModel, ValidationError, Field
from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram_dialog import Dialog, DialogManager, Window, StartMode, setup_dialogs
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State

from .builders.questions import QuestionBuilder
from .exceptions.questions import NoQuestionsEnteredError,MessageNotEnteredError
from .models.buttons import InfoButtons
from .models.messages import InfoMessages
from .models.question import Question, QuestionType

from typing import Dict, Tuple, Any, List
from pydantic import BaseModel, create_model, Field

class BriefSurvey:
    """

    """
    def __init__(
        self,
        *,
        save_handler: Callable[[int, Any], Any],
        result_model: BaseModel = None,
        questions: Optional[List[Question]]=[],
        messages: Optional[Dict[str, str]] = None,
        states_prefix: str = "SurveyStates",
        start_command:str = "start_survey",
    ):
        self.questions = questions
        self.save_handler = save_handler
        self.result_model = result_model
        self.command_start= start_command
        self.info_messages = InfoMessages()
        self.buttons = InfoButtons()
        self.states_prefix = states_prefix
        self._dialog = None

    @staticmethod
    def _create_states_group(class_name: str, state_names: List[str]):
        attrs = {name: State() for name in state_names}
        group = type(class_name, (StatesGroup,), attrs)
        mapping = {name: getattr(group, name) for name in state_names}
        return group, mapping

    def get_dialog(self) -> Dialog:
        return self._dialog

    async def _process_text_input(self, message: types.Message, dialog: Dialog, manager: DialogManager):
        text = message.text.strip()
        state_name = manager.current_context().state.state.split(":")[1]
        question = self._get_question(state_name)
        if not question:
            await message.answer("Ошибка: вопрос не найден.")
            return

        if question.validator and not question.validator(text):
            await message.answer(self.info_messages.invalid_input)
            return

        if question.name == "weight":
            text = text.replace(",", ".")

        manager.current_context().dialog_data[question.name] = text
        await manager.next()

    async def _process_choice_selected(self, c: types.CallbackQuery, widget: Button, manager: DialogManager):
        # selected = widget.widget_id
        selected = widget.text.text  # Получаем текст кнопки, а не id (callback_data)
        state_name = manager.current_context().state.state.split(":")[1]

        question = self._get_question(state_name)
        if not question:
            await c.answer("Ошибка: вопрос не найден.")
            return

        manager.current_context().dialog_data[question.name] = selected
        await manager.next()
        await c.answer()

    async def _process_multi_choice_selected(self, c: types.CallbackQuery, widget: Button, manager: DialogManager):
        selected_text = widget.text.text
        state_name = manager.current_context().state.state.split(":")[1]
        question = self._get_question(state_name)
        if not question:
            await c.answer("Ошибка: вопрос не найден.")
            return

        ctx_data = manager.current_context().dialog_data
        multi_selected = ctx_data.get(f"multi_selected_{state_name}", set())
        if not isinstance(multi_selected, set):
            multi_selected = set(multi_selected)

        if selected_text in multi_selected:
            multi_selected.remove(selected_text)
        else:
            multi_selected.add(selected_text)
        ctx_data[f"multi_selected_{state_name}"] = multi_selected

        ctx_data[question.name] = ", ".join(multi_selected)

        await c.answer(f"Выбрано: {', '.join(multi_selected) if multi_selected else 'ничего'}")
        await manager.show()

    async def _process_media_input(self, message: types.Message, dialog: Dialog, manager: DialogManager):
        state_name = manager.current_context().state.state.split(":")[1]
        question = self._get_question(state_name)
        if not question:
            await message.answer("Ошибка: вопрос не найден.")
            return

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.video:
            file_id = message.video.file_id
        else:
            await message.answer(self.info_messages.invalid_input)
            return
        print(message.photo)
        ctx_data = manager.current_context().dialog_data
        media_list = ctx_data.get(question.name, None)
        # if not isinstance(media_list, list):
        #     media_list = [media_list]
        # media_list.append(file_id)

        ctx_data[question.name] = file_id

        await manager.next()
        return

    async def _process_media_list_input(self, message: types.Message, dialog: Dialog, manager: DialogManager):
        state_name = manager.current_context().state.state.split(":")[1]
        question = self._get_question(state_name)
        if not question:
            await message.answer("Ошибка: вопрос не найден.")
            return

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.video:
            file_id = message.video.file_id
        else:
            await message.answer(self.info_messages.invalid_input)
            return

        ctx_data = manager.current_context().dialog_data
        media_list = ctx_data.get(question.name, None)
        # if not isinstance(media_list, list):
        #     media_list = [media_list]
        media_list.append(file_id)
        ctx_data[question.name] = media_list

        await manager.next()
        return

    async def _confirm_multi_choice(self, c: types.CallbackQuery, widget: Button, manager: DialogManager):
        ctx_data = manager.current_context().dialog_data

        state_name = manager.current_context().state.state.split(":")[1]
        multi_selected = ctx_data.get(f"multi_selected_{state_name}", set())
        question = self._get_question(state_name)
        ctx_data[question.name] = ", ".join(multi_selected)
        await manager.next()
        await c.answer()

    def _get_question(self, name: str) -> Optional[Question]:
        for q in self.questions:
            if q.name == name:
                return q
        return None

    def _make_window_for_question(self, question: Question) -> Window:
        state = self.state_map[question.name]
        qtext = question.text

        if question.type in ["text", "number"]:
            window = Window(
                Const(qtext),
                MessageInput(self._process_text_input),
                state=state,
            )
        elif question.type == "choice":
            buttons = [
                Button(text=Const(label), id=key, on_click=self._process_choice_selected)
                for key, label in question.choices  # type: ignore
            ]
            window = Window(Const(qtext), *buttons, state=state)
        elif question.type == "multi_choice":
            buttons = [
                Button(text=Const(label), id=str(i), on_click=self._process_multi_choice_selected)
                for i, (_, label) in enumerate(question.choices)  # type: ignore
            ]
            confirm_btn = Button(Const("Подтвердить выбор"), id="confirm", on_click=self._confirm_multi_choice)
            window = Window(Const(qtext), *buttons, confirm_btn, state=state)
        elif question.type in ["photo", "video", "media"]:
            # Ожидаем медиа (фото или видео)
            allowed_types = []
            if question.type == "photo":
                allowed_types = [ContentType.PHOTO]
            elif question.type == "video":
                allowed_types = [ContentType.VIDEO]
            else:
                allowed_types = [ContentType.PHOTO, ContentType.VIDEO]

            window = Window(
                Const(qtext),
                MessageInput(self._process_media_input, content_types=allowed_types),
                state=state,
            )
        else:
            raise NotImplementedError(f"Тип вопроса {question.type} не поддерживается")

        return window

    async def _on_finish(self, c: types.CallbackQuery, button, manager: DialogManager):
        data = manager.current_context().dialog_data
        user_id = c.from_user.id
        try:
            result_obj = self.result_model.parse_obj(data)
        except ValidationError as e:
            await c.message.answer(f"Некорректные данные:\n" + "\n".join(
                [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            ))
            return

        try:
            await self.save_handler(user_id, result_obj)
        except Exception as e:
            print("Save handler error:", e)
            await c.message.answer(self.info_messages.save_fail)
        else:
            await c.message.answer(self.info_messages.save_success)
        finally:
            await c.message.delete()
            await manager.done()

    async def start(self, message: types.Message, dialog_manager: DialogManager, state: FSMContext):
        first_state_name = self.questions[0].name if self.questions else None
        if first_state_name:
            await state.set_state(self.state_map[first_state_name])
            await dialog_manager.start(self.state_map[first_state_name], mode=StartMode.RESET_STACK)
        else:
            await message.answer("Нет вопросов для опроса.")

    async def cmd_start_survey_handler(
            self,
            message: types.Message,
            dialog_manager: DialogManager,
            state: FSMContext,
    ):
        await self.start(message, dialog_manager, state)


    def register_handlers(self, dp: Dispatcher,
                          command_start: str = None,
                          callback_data:str=None,

                          text:str=None,
                          ):
        if not self.questions:
            raise NoQuestionsEnteredError
        else:
            self.create_result_model_from_questions()
        if command_start:
            dp.message.register(self.cmd_start_survey_handler, Command(command_start))
        else:
            dp.message.register(self.cmd_start_survey_handler, Command(self.command_start))
        if callback_data:
            dp.callback_query.register(self.cmd_start_survey_handler, F.data == callback_data)
        if text:
            dp.message.register(self.cmd_start_survey_handler, F.text == text)
        self.States, self.state_map = self._create_states_group(
            class_name=self.states_prefix,
            state_names=[q.name for q in self.questions] + ["finish"],
        )

        self.windows = [self._make_window_for_question(q) for q in self.questions]
        self.windows.append(
            Window(
                Const(self.info_messages.finish_text),
                Button(Const(self.buttons.finish_text), id="finish", on_click=self._on_finish),
                state=self.state_map["finish"],
            )
        )

        self._dialog = Dialog(*self.windows)
        dp.include_router(self.get_dialog())
        setup_dialogs(dp)

    def add_question(
            self,
            text: str,
            question_type: QuestionType="text",
            name: str = None,
            choices: Optional[List[str]|Tuple[str]|Set[str]] = None,
            *args,
            **kwargs
    ):
        """
            Добавляет новый вопрос в конец опроса.

            Args:
                text (str): Текст вопроса. Не может быть пустым.
                question_type (Literal["text", "number", "choice", "multi_choice","photo", "video", "media"]): Тип вопроса.
                    - "text" — текстовый вопрос,
                    - "number" — числовой вопрос,
                    - "choice" — выбор одного варианта,
                    - "multi_choice" — выбор нескольких вариантов.
                name (Optional[str], optional): Уникальное имя вопроса. Если не указано, генерируется автоматически.
                choices (Optional[List[str]], optional): Список вариантов ответа для вопросов типа "choice" и "multi_choice".
                *args: Дополнительные позиционные аргументы, передаваемые в билдер вопроса.
                **kwargs: Дополнительные именованные аргументы, передаваемые в билдер вопроса.

            Raises:
                MessageNotEnteredError: Если текст вопроса пустой.

            """

        if not text:
            raise MessageNotEnteredError("Текст вопроса не может быть пустым.")
        if choices:
            choices = [(str(i[0]), i[1]) for i in enumerate(choices)]
        if choices and question_type=="text":
            question_type = 'choice'
        if not name:
            name = f"q{len(self.questions) + 1}"

        question_model = QuestionBuilder.create(
                                                text=text,
                                                question_type=question_type,
                                                name=name,
                                                choices=choices,
                                                *args,
                                                **kwargs
                                                )
        self.questions.append(question_model)

    @staticmethod
    def get_field_type_and_default(question_type: str) -> Tuple[Any, Any]:
        if question_type in ("text", "choice", "multi_choice"):
            return (str, Field(default=None))
        elif question_type == "number":
            return (float, Field(default=None))
        elif question_type in ("photo", "video"):
            return (Optional[str], Field(default_factory=None))
        elif question_type in ("media"):
            return (Optional[List[str]], Field(default_factory=list))
        else:
            return (str, Field(default=None))

    def create_result_model_from_questions(self) -> BaseModel:
        """
        Создаёт динамическую Pydantic-модель результата на основе списка вопросов.

        Args:
            questions (List): Список объектов вопросов, у каждого должен быть атрибут name и type.

        Returns:
            BaseModel: Класс модели результата.
        """
        fields: Dict[str, Tuple[Any, Any]] = {}

        for q in self.questions:
            field_type, default = self.get_field_type_and_default(q.type)
            fields[q.name] = (field_type, default)
        if not self.result_model:
            self.result_model = create_model('DynamicResultModel', **fields)
            return self.result_model
        else:
            DynamicResultModel = create_model('DynamicResultModel', **fields)
            return DynamicResultModel