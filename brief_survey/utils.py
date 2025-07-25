import importlib.util
import os
import inspect
from typing import Optional, Callable

from brief_survey.core.exceptions.validators import ValidatorNotFountError


def find_function_in_folder(func_name: str,folder_path: str=".validators" ) -> Optional[Callable]:
    """
    Сканирует все .py файлы в заданной папке, импортирует модули и ищет функцию с заданным именем.
    Возвращает функцию или None, если не найдена.
    """
    if isinstance(func_name, str):
        if not func_name:
            raise ValidatorNotFountError("Validator name is empty")
    for filename in os.listdir(folder_path):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_path = os.path.join(folder_path, filename)
            module_name = filename[:-3]

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for name, obj in inspect.getmembers(module, inspect.isfunction):
                    print(name)
                    if name == func_name:
                        return obj
    return None

# Пример
if __name__ == '__main__':
    folder = '../../validators'
    function_name = 'phone_international'

    found_func = find_function_in_folder( function_name,folder)
    if found_func:
        print(f"Функция '{function_name}' найдена: {found_func}")
    else:
        print(f"Функция '{function_name}' не найдена в папке {folder}")
